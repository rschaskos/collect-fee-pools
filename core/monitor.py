import csv
import os
import shutil
import uuid
from typing import List, Optional, Dict
from utils.paths import get_data_file_path, get_legacy_file_path

from models.coleta import Coleta
from models.pool_config import PoolConfig
from datetime import datetime

class MonitorLiquidez:
    """Gerencia múltiplas pools e suas coletas."""

    def __init__(self):
        # Arquivos principais
        self.arquivo_pools = get_data_file_path('pools_config.csv')
        self.pools: Dict[str, PoolConfig] = {}
        self.pool_ativa_id: Optional[str] = None
        self.dados_pools: Dict[str, List[Coleta]] = {}

        # Migrar dados antigos se existirem
        self._migrar_dados_antigos()
        
        # Carregar pools existentes
        self.carregar_pools()
        
        # Definir pool ativa (primeira disponível)
        if self.pools:
            self.pool_ativa_id = list(self.pools.keys())[-1]
            # Carregar dados de TODAS as pools
            for pool_id in self.pools.keys():
                self.carregar_dados_pool(pool_id)

    def _calcular_dias_entre_datas(self, data_inicial: str, data_final: str) -> int:
        """Calcula dias entre duas datas no formato dd/MM/yyyy."""
        try:
            data_ini = datetime.strptime(data_inicial, "%d/%m/%Y")
            data_fim = datetime.strptime(data_final, "%d/%m/%Y")
            return (data_fim - data_ini).days
        except ValueError as e:
            print(f"Erro ao calcular dias entre {data_inicial} e {data_final}: {e}")
            return 0

    def _calcular_dias_coleta(self, pool_id: str, data_coleta: str) -> int:
        """Calcula quantos dias desde a última coleta ou data base da pool."""
        pool_config = self.pools.get(pool_id)
        dados_pool = self.dados_pools.get(pool_id, [])
        
        if not pool_config:
            return 0
        
        # Se é a primeira coleta, calcular desde a data de abertura da pool
        if not dados_pool:
            return self._calcular_dias_entre_datas(pool_config.data_abertura, data_coleta)
        
        # Se já existem coletas, calcular desde a última coleta
        ultima_coleta = dados_pool[-1]
        return self._calcular_dias_entre_datas(ultima_coleta.data, data_coleta)

    def _migrar_dados_antigos(self):
        """Migra dados do formato antigo (pool única) para o novo formato."""
        arquivo_antigo_config = get_legacy_file_path('pool_config.csv')
        arquivo_antigo_coletas = get_legacy_file_path('coletas.csv')
        
        # Se existir configuração antiga, migrar
        if os.path.exists(arquivo_antigo_config) and not os.path.exists(self.arquivo_pools):
            try:
                with open(arquivo_antigo_config, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    config_data = next(reader, None)
                    if config_data:
                        # Criar pool migrada
                        pool_id = str(uuid.uuid4())
                        pool_config = PoolConfig(
                            pool_id=pool_id,
                            nome="Pool Migrada",
                            data_abertura=config_data.get('data_abertura', ''),
                            valor_inicial=float(config_data.get('valor_inicial', 0.0)),
                            tipo_moeda=config_data.get('tipo_moeda', '')
                        )
                        
                        # Salvar nova estrutura
                        self.pools[pool_id] = pool_config
                        self.salvar_pools()
                        
                        # Migrar coletas se existirem
                        if os.path.exists(arquivo_antigo_coletas):
                            arquivo_coletas_novo = get_data_file_path(f'pool_{pool_id}_coletas.csv')
                            shutil.copy2(arquivo_antigo_coletas, arquivo_coletas_novo)
                        
                        print(f"Dados migrados com sucesso para o novo formato!")
                        
            except Exception as e:
                 
                print(f"Erro ao migrar dados antigos: {e}")

    def carregar_pools(self) -> None:
        """Carrega todas as pools configuradas."""
        if not os.path.exists(self.arquivo_pools):
            return
        
        try:
            with open(self.arquivo_pools, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    pool_config = PoolConfig.from_dict(row)
                    self.pools[pool_config.pool_id] = pool_config
        except Exception as e:
            print(f"Erro ao carregar pools: {e}")

    def salvar_pools(self) -> None:
        """Salva todas as configurações de pools."""
        try:
            with open(self.arquivo_pools, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['pool_id', 'nome', 'data_abertura', 'valor_inicial', 'tipo_moeda']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for pool in self.pools.values():
                    writer.writerow(pool.to_dict())
        except Exception as e:
            raise Exception(f"Erro ao salvar pools: {e}")

    def criar_nova_pool(self, nome: str, data_abertura: str, valor_inicial: float, tipo_moeda: str) -> str:
        """Cria uma nova pool e retorna seu ID."""
        pool_id = str(uuid.uuid4())
        pool_config = PoolConfig(pool_id, nome, data_abertura, valor_inicial, tipo_moeda)
        
        self.pools[pool_id] = pool_config
        self.dados_pools[pool_id] = []
        
        self.salvar_pools()
        self.salvar_dados_pool(pool_id)
        
        return pool_id

    def excluir_pool(self, pool_id: str) -> None:
        """Exclui uma pool e seus dados."""
        if pool_id in self.pools:
            # Remover arquivos
            arquivo_coletas = get_data_file_path(f'pool_{pool_id}_coletas.csv')
            if os.path.exists(arquivo_coletas):
                os.remove(arquivo_coletas)
            
            # Remover da memória
            del self.pools[pool_id]
            if pool_id in self.dados_pools:
                del self.dados_pools[pool_id]
            
            # Se era a pool ativa, selecionar outra
            if self.pool_ativa_id == pool_id:
                self.pool_ativa_id = list(self.pools.keys())[-1] if self.pools else None
                if self.pool_ativa_id:
                    self.carregar_dados_pool_ativa()
            
            self.salvar_pools()

    def atualizar_pool(self, pool_id: str, nome: str, data_abertura: str, valor_inicial: float, tipo_moeda: str) -> None:
        """Atualiza uma pool existente."""
        if pool_id in self.pools:
            self.pools[pool_id].nome = nome
            self.pools[pool_id].data_abertura = data_abertura
            self.pools[pool_id].valor_inicial = valor_inicial
            self.pools[pool_id].tipo_moeda = tipo_moeda
            
            self.salvar_pools()
            self.recalcular_taxas_pool(pool_id)

    def definir_pool_ativa(self, pool_id: str) -> None:
        """Define qual pool está ativa."""
        if pool_id in self.pools:
            self.pool_ativa_id = pool_id
            self.carregar_dados_pool_ativa()

    def get_pool_ativa(self) -> Optional[PoolConfig]:
        """Retorna a configuração da pool ativa."""
        if self.pool_ativa_id and self.pool_ativa_id in self.pools:
            return self.pools[self.pool_ativa_id]
        return None

    def get_dados_pool_ativa(self) -> List[Coleta]:
        """Retorna os dados da pool ativa."""
        if self.pool_ativa_id and self.pool_ativa_id in self.dados_pools:
            return self.dados_pools[self.pool_ativa_id]
        return []

    def carregar_dados_pool_ativa(self) -> None:
        """Carrega dados da pool ativa."""
        if not self.pool_ativa_id:
            return
        
        self.carregar_dados_pool(self.pool_ativa_id)

    def carregar_dados_pool(self, pool_id: str) -> None:
        """Carrega dados de uma pool específica."""
        arquivo_coletas = get_data_file_path(f'pool_{pool_id}_coletas.csv')
        
        if pool_id not in self.dados_pools:
            self.dados_pools[pool_id] = []
        
        if not os.path.exists(arquivo_coletas):
            return
        
        try:
            with open(arquivo_coletas, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                header = next(reader, None)
                if header is None:
                    return

                self.dados_pools[pool_id].clear()
                pool_config = self.pools.get(pool_id)
                
                for row in reader:
                    if len(row) >= 2:
                        try:
                            data = row[0]
                            coleta_usd = float(row[1])
                            
                            # Calcular taxa se temos configuração da pool
                            taxa = 0.0
                            if pool_config:
                                if len(row) >= 3:
                                    try:
                                        taxa = float(row[2])
                                    except (ValueError, IndexError):
                                        taxa = (coleta_usd / pool_config.valor_inicial) * 100
                                else:
                                    taxa = (coleta_usd / pool_config.valor_inicial) * 100
                            
                            # Calcular ou ler dias
                            dias = 0
                            if len(row) >= 5:  # Se já tem dados de dias no CSV
                                try:
                                    dias = int(float(row[4]))  # 5ª coluna seria dias
                                except (ValueError, IndexError):
                                    # Se não conseguir ler, recalcular
                                    if pool_config:
                                        # Se é a primeira coleta desta sessão de carregamento
                                        if not self.dados_pools[pool_id]:
                                            dias = self._calcular_dias_entre_datas(pool_config.data_abertura, data)
                                        else:
                                            ultima_coleta = self.dados_pools[pool_id][-1]
                                            dias = self._calcular_dias_entre_datas(ultima_coleta.data, data)
                            else:
                                # Recalcular dias para dados antigos
                                if pool_config:
                                    if not self.dados_pools[pool_id]:
                                        dias = self._calcular_dias_entre_datas(pool_config.data_abertura, data)
                                    else:
                                        ultima_coleta = self.dados_pools[pool_id][-1]
                                        dias = self._calcular_dias_entre_datas(ultima_coleta.data, data)
                            
                            self.dados_pools[pool_id].append(Coleta(data, coleta_usd, taxa, dias))
                        except (ValueError, IndexError) as e:
                            print(f'Erro ao ler a linha {row}. Erro: {e}')
                            
            # Após carregar, salvar novamente para incluir dias calculados
            self.salvar_dados_pool(pool_id)
            
        except Exception as e:
            print(f"Erro ao carregar dados da pool {pool_id}: {e}")

    def salvar_dados_pool(self, pool_id: str) -> None:
        """Salva dados de uma pool específica."""
        arquivo_coletas = get_data_file_path(f'pool_{pool_id}_coletas.csv')
        dados = self.dados_pools.get(pool_id, [])
        
        try:
            with open(arquivo_coletas, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # Header atualizado com coluna Dias
                writer.writerow(['Data', 'Coleta_USD', 'Taxa_Percentual', 'Total_Acumulado_USD', 'Dias'])
                
                total_acumulado = 0
                for coleta in dados:
                    total_acumulado += coleta.coleta_usd
                    writer.writerow([
                        coleta.data, 
                        coleta.coleta_usd, 
                        coleta.taxa_percentual, 
                        total_acumulado,
                        coleta.dias  # Nova coluna
                    ])
        except Exception as e:
            raise Exception(f"Erro ao salvar dados da pool {pool_id}: {e}")

    def registrar_nova_coleta(self, data: str, valor: float) -> Optional[Coleta]:
        """Registra uma nova coleta na pool ativa."""
        if not self.pool_ativa_id:
            return None
        
        pool_config = self.get_pool_ativa()
        if not pool_config:
            return None
        
        # Calcular taxa
        taxa = (valor / pool_config.valor_inicial) * 100
        
        # Calcular dias desde última coleta/data base
        dias = self._calcular_dias_coleta(self.pool_ativa_id, data)
        
        # Criar nova coleta com dias calculados
        nova_coleta = Coleta(data, valor, taxa, dias)
        
        if self.pool_ativa_id not in self.dados_pools:
            self.dados_pools[self.pool_ativa_id] = []
        
        self.dados_pools[self.pool_ativa_id].append(nova_coleta)
        self.salvar_dados_pool(self.pool_ativa_id)
        
        return nova_coleta

    def recalcular_taxas_pool(self, pool_id: str) -> None:
        """Recalcula todas as taxas de uma pool."""
        pool_config = self.pools.get(pool_id)
        dados = self.dados_pools.get(pool_id, [])
        
        if not pool_config or not dados:
            return
        
        for coleta in dados:
            coleta.taxa_percentual = (coleta.coleta_usd / pool_config.valor_inicial) * 100
        
        self.salvar_dados_pool(pool_id)

    def calcular_total_acumulado_pool_ativa(self) -> float:
        """Calcula o total acumulado da pool ativa."""
        dados = self.get_dados_pool_ativa()
        return sum(coleta.coleta_usd for coleta in dados)
        
    def calcular_taxa_acumulada_pool_ativa(self) -> float:
        """Calcula a taxa percentual acumulada da pool ativa."""
        dados = self.get_dados_pool_ativa()
        return sum(coleta.taxa_percentual for coleta in dados)
    
    def contar_total_coletas_todas_pools(self) -> int:
        """Conta o total de coletas de todas as pools combinadas"""
        total = 0
        for pool_id in self.dados_pools:
            total += len(self.dados_pools[pool_id])
        return total
    
    def calcular_total_acumulado_todas_pools(self) -> float:
        """Calcula o total acumulado (USD) de todas as pools combinadas"""
        total = 0.0
        for pool_id in self.dados_pools:
            for coleta in self.dados_pools[pool_id]:
                total += coleta.coleta_usd
        return total

    def exportar_dados_pool_ativa(self, nome_arquivo: str) -> None:
        """Exporta dados da pool ativa para um arquivo CSV."""
        pool_config = self.get_pool_ativa()
        dados = self.get_dados_pool_ativa()
        
        if not pool_config:
            raise Exception("Nenhuma pool ativa selecionada")
        
        try:
            with open(nome_arquivo, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # Header com informações da pool
                writer.writerow(['# Configuração da Pool'])
                writer.writerow(['Nome', pool_config.nome])
                writer.writerow(['Tipo de Moeda', pool_config.tipo_moeda])
                writer.writerow(['Data de Abertura', pool_config.data_abertura])
                writer.writerow(['Valor Inicial', pool_config.valor_inicial])
                writer.writerow([])
                
                # Header da tabela - incluindo Dias
                writer.writerow(['Data', 'Dias', 'Valor (USD)', 'Taxa (%)', 'Acumulado (USD)'])
                
                # Dados
                total_acumulado = 0
                for coleta in dados:
                    total_acumulado += coleta.coleta_usd
                    writer.writerow([
                        coleta.data,
                        coleta.dias,  # Nova coluna
                        f"{coleta.coleta_usd:.2f}",
                        f"{coleta.taxa_percentual:.4f}",
                        f"{total_acumulado:.2f}"
                    ])
        except Exception as e:
            raise Exception(f"Erro ao exportar dados: {e}")

    def limpar_dados_pool_ativa(self) -> None:
        """Remove todos os dados da pool ativa."""
        if not self.pool_ativa_id:
            return
        
        self.dados_pools[self.pool_ativa_id] = []
        arquivo_coletas = get_data_file_path(f'pool_{self.pool_ativa_id}_coletas.csv')
        if os.path.exists(arquivo_coletas):
            os.remove(arquivo_coletas)

    def get_lista_pools(self) -> List[PoolConfig]:
        """Retorna lista de todas as pools."""
        return list(self.pools.values())
    
    def excluir_coleta(self, linha_index: int) -> None:
        """Exclui uma coleta específica da pool ativa."""
        if not self.pool_ativa_id or self.pool_ativa_id not in self.dados_pools:
            raise Exception("Nenhuma pool ativa selecionada")
        
        dados = self.dados_pools[self.pool_ativa_id]
        if linha_index < 0 or linha_index >= len(dados):
            raise Exception("Índice de coleta inválido")
        
        # Remover a coleta
        dados.pop(linha_index)
        
        # Recalcular dias para as coletas seguintes
        self._recalcular_dias_pool(self.pool_ativa_id)
        
        # Salvar as mudanças
        self.salvar_dados_pool(self.pool_ativa_id)

    def atualizar_coleta(self, linha_index: int, nova_data: str, novo_valor: float) -> None:
        """Atualiza uma coleta específica da pool ativa."""
        if not self.pool_ativa_id or self.pool_ativa_id not in self.dados_pools:
            raise Exception("Nenhuma pool ativa selecionada")
        
        dados = self.dados_pools[self.pool_ativa_id]
        if linha_index < 0 or linha_index >= len(dados):
            raise Exception("Índice de coleta inválido")
        
        pool_config = self.get_pool_ativa()
        if not pool_config:
            raise Exception("Configuração da pool não encontrada")
        
        # Atualizar dados da coleta
        coleta = dados[linha_index]
        coleta.data = nova_data
        coleta.coleta_usd = novo_valor
        coleta.taxa_percentual = (novo_valor / pool_config.valor_inicial) * 100
        
        # Recalcular dias para todas as coletas (a ordem pode ter mudado)
        self._recalcular_dias_pool(self.pool_ativa_id)
        
        # Salvar as mudanças
        self.salvar_dados_pool(self.pool_ativa_id)

    def _recalcular_dias_pool(self, pool_id: str) -> None:
        """Recalcula os dias de todas as coletas de uma pool."""
        pool_config = self.pools.get(pool_id)
        dados = self.dados_pools.get(pool_id, [])
        
        if not pool_config or not dados:
            return
        
        # Ordenar coletas por data para garantir ordem correta
        try:
            dados.sort(key=lambda x: datetime.strptime(x.data, "%d/%m/%Y"))
        except ValueError:
            print("Erro ao ordenar coletas por data")
            return
        
        # Recalcular dias para cada coleta
        for i, coleta in enumerate(dados):
            if i == 0:
                # Primeira coleta: dias desde data de abertura da pool
                coleta.dias = self._calcular_dias_entre_datas(pool_config.data_abertura, coleta.data)
            else:
                # Demais coletas: dias desde a coleta anterior
                coleta_anterior = dados[i-1]
                coleta.dias = self._calcular_dias_entre_datas(coleta_anterior.data, coleta.data)
        
        # Atualizar a lista ordenada
        self.dados_pools[pool_id] = dados