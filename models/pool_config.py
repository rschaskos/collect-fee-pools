class PoolConfig:
    """Configuração da pool de liquidez."""

    def __init__(self, data_abertura: str, valor_inicial: float, tipo_moeda: str):
        self.data_abertura = data_abertura
        self.valor_inicial = valor_inicial
        self.tipo_moeda = tipo_moeda

    def __str__(self):
        return f'Pool ({self.tipo_moeda}, ${self.valor_inicial:.2f}, {self.data_abertura})'
    
    def __repr__(self):
        return self.__str__()
    
    def to_dict(self):
        """Converte para dicionário para salvar em CSV."""
        return {
            'data_abertura': self.data_abertura,
            'valor_inicial': self.valor_inicial,
            'tipo_moeda': self.tipo_moeda
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Cria instância a partir de dicionário."""
        return cls(
            data['data_abertura'],
            float(data['valor_inicial']),
            data['tipo_moeda']
        )