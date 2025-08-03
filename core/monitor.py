import csv
import os
from typing import List, Optional

from models.coleta import Coleta
from models.pool_config import PoolConfig

class MonitorLiquidez:
    """Gerencia as coletas e a persistência de dados."""

    def __init__(self, nome_arquivo_base: str = 'coletas.csv'):
        self.nome_arquivo_base = nome_arquivo_base
        self.nome_arquivo = nome_arquivo_base
        self.arquivo_config = 'pool_config.csv'
        self.dados: List[Coleta] = []
        self.pool_config: Optional[PoolConfig] = None

        self.carregar_config_pool()
        self.carregar_dados()

    def carregar_config_pool(self) -> None:
        """Carrega a configuração da pool."""
        if not os.path.exists(self.arquivo_config):
            return
    
        try:
            with open(self.arquivo_config, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                config_data = next(reader, None)
                if config_data:
                    self.pool_config = PoolConfig.from_dict(config_data)
        except Exception as e:
            print(f"Erro ao carregar configuração: {e}")
    
    def salvar_config_pool(self, config: PoolConfig) -> None:
        """Salva a configuração da pool."""
        self.pool_config = config
        try:
            with open(self.arquivo_config, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['data_abertura', 'valor_inicial', 'tipo_moeda']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(config.to_dict())
        except Exception as e:
            raise Exception(f"Erro ao salvar configuração: {e}")
    
    def carregar_dados(self) -> None:
        """Carrega dados existentes do arquivo CSV."""
        if not os.path.exists(self.nome_arquivo):
            print(f'Arquivo "{self.nome_arquivo_base}" não encontrado. Será criado automaticamente.')
            return
        
        try:
            with open(self.nome_arquivo, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                header = next(reader, None)
                if header is None:
                    return

                for row in reader:
                    if len(row) >= 2:
                        try:
                            data = row[0]
                            coleta_usd = float(row[1])
                            
                            # Calcular taxa se temos configuração da pool
                            taxa = 0.0
                            if self.pool_config:
                                if len(row) >= 3:
                                    try:
                                        taxa = float(row[2])
                                    except (ValueError, IndexError):
                                        taxa = (coleta_usd / self.pool_config.valor_inicial) * 100
                                else:
                                    taxa = (coleta_usd / self.pool_config.valor_inicial) * 100
                            
                            self.dados.append(Coleta(data, coleta_usd, taxa))
                        except (ValueError, IndexError) as e:
                            print(f'Erro ao ler a linha {row}. Erro: {e}')
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")

    def salvar_todos_dados(self) -> None:
        """Salva todos os dados no arquivo CSV."""
        try:
            with open(self.nome_arquivo, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Data', 'Coleta_USD', 'Taxa_Percentual', 'Total_Acumulado_USD'])
                
                total_acumulado = 0
                for coleta in self.dados:
                    total_acumulado += coleta.coleta_usd
                    writer.writerow([
                        coleta.data, 
                        coleta.coleta_usd, 
                        coleta.taxa_percentual, 
                        total_acumulado
                    ])
        except Exception as e:
            raise Exception(f"Erro ao salvar dados: {e}")

    def calcular_total_acumulado(self) -> float:
        """Calcula o total acumulado de todas as coletas."""
        return sum(coleta.coleta_usd for coleta in self.dados)
    
    def calcular_taxa_acumulada(self) -> float:
        """Calcula a taxa percentual acumulada."""
        return sum(coleta.taxa_percentual for coleta in self.dados)
    
    def registrar_nova_coleta(self, data: str, valor: float) -> Coleta:
        """Registra uma nova coleta."""
        taxa = 0.0
        if self.pool_config:
            taxa = (valor / self.pool_config.valor_inicial) * 100
        
        nova_coleta = Coleta(data, valor, taxa)
        self.dados.append(nova_coleta)
        self.salvar_todos_dados()
        
        return nova_coleta
    
    def recalcular_taxas(self) -> None:
        """Recalcula todas as taxas baseado na configuração atual da pool."""
        if not self.pool_config:
            return
        
        for coleta in self.dados:
            coleta.taxa_percentual = (coleta.coleta_usd / self.pool_config.valor_inicial) * 100
        
        self.salvar_todos_dados()
    
    def exportar_dados(self, nome_arquivo: str) -> None:
        """Exporta dados para um arquivo CSV."""
        try:
            with open(nome_arquivo, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # Header com informações da pool
                if self.pool_config:
                    writer.writerow(['# Configuração da Pool'])
                    writer.writerow(['Tipo de Moeda', self.pool_config.tipo_moeda])
                    writer.writerow(['Data de Abertura', self.pool_config.data_abertura])
                    writer.writerow(['Valor Inicial', self.pool_config.valor_inicial])
                    writer.writerow([])
                
                # Header da tabela
                writer.writerow(['Data', 'Valor (USD)', 'Taxa (%)', 'Acumulado (USD)'])
                
                # Dados
                total_acumulado = 0
                for coleta in self.dados:
                    total_acumulado += coleta.coleta_usd
                    writer.writerow([
                        coleta.data,
                        f"{coleta.coleta_usd:.2f}",
                        f"{coleta.taxa_percentual:.4f}",
                        f"{total_acumulado:.2f}"
                    ])
        except Exception as e:
            raise Exception(f"Erro ao exportar dados: {e}")
    
    def limpar_dados(self) -> None:
        """Remove todos os dados de coletas."""
        self.dados.clear()
        if os.path.exists(self.nome_arquivo):
            os.remove(self.nome_arquivo)