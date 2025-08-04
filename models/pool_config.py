from datetime import datetime
from typing import Dict, Any, Optional

class PoolConfig:
    """Representa a configuração de uma pool de liquidez."""
    
    def __init__(self, pool_id: str, nome: str, data_abertura: str, valor_inicial: float, tipo_moeda: str):
        self.pool_id = pool_id
        self.nome = nome
        self.data_abertura = data_abertura
        self.valor_inicial = valor_inicial
        self.tipo_moeda = tipo_moeda
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte a configuração para dicionário."""
        return {
            'pool_id': self.pool_id,
            'nome': self.nome,
            'data_abertura': self.data_abertura,
            'valor_inicial': self.valor_inicial,
            'tipo_moeda': self.tipo_moeda
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PoolConfig':
        """Cria uma instância a partir de um dicionário."""
        return cls(
            pool_id=data.get('pool_id', ''),
            nome=data.get('nome', ''),
            data_abertura=data.get('data_abertura', ''),
            valor_inicial=float(data.get('valor_inicial', 0.0)),
            tipo_moeda=data.get('tipo_moeda', '')
        )
    
    def __str__(self) -> str:
        return f"{self.nome} - {self.tipo_moeda}"
    
    def get_display_name(self) -> str:
        """Retorna o nome para exibição no dropdown."""
        return f"{self.nome} - {self.tipo_moeda}"