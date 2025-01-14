class Ativo:

    PATH_FILE_CACHE = 'simulacao/cache/ativo_cache.json'

    def __init__(self, ticker: str, valor: float, retorno: float, volume_medio: float, desvio_padrao: float):
        self.ticker = ticker
        self.valor = valor
        self.retorno = retorno
        self.volume_medio = volume_medio
        self.desvio_padrao = desvio_padrao


    def __eq__(self, outro):
        return outro.ticker == self.nome

    def __str__(self):
        return f"""
            ticker={self.ticker},
            valor={self.valor},
            retorno={self.retorno},
            volume_medio={self.volume_medio},
            desvio_padrao={self.desvio_padrao}
        """
    
    def to_json(self):
        return {
            "ticker": self.ticker,
            "valor": self.valor,
            "retorno": self.retorno,
            "volume_medio": self.volume_medio,
            "desvio_padrao": self.desvio_padrao
        }
