class Ativo:
    def __init__(self, valor: float, retorno: float, volume_medio: float, desvio_padrao: float):
        self.valor = valor
        self.retorno = retorno
        self.volume_medio = volume_medio
        self.desvio_padrao = desvio_padrao

    def __str__(self):
        return f"""
            valor={self.valor},
            retorno={self.retorno},
            volume_medio={self.volume_medio},
            desvio_padrao={self.desvio_padrao}
        """
