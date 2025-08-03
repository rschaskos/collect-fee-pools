class Coleta:
    """Representa uma única coleta de taxas."""

    def __init__(self, data: str, coleta_usd: float, taxa_percentual: float = 0.0):
        self.data = data
        self.coleta_usd = coleta_usd
        self.taxa_percentual = taxa_percentual

    def __str__(self):
        return f'Coleta({self.data}, ${self.coleta_usd:.2f}, {self.taxa_percentual:.4f}%)'
    
    def __repr__(self):
        return self.__str__()
