class Ativo:
    def __init__(self, nome_ativo: str, valor: float, retorno: float, volume_medio: float, desvio_padrao: float):
        self.nome_ativo = nome_ativo
        self.valor = valor
        self.retorno = retorno
        self.volume_medio = volume_medio
        self.desvio_padrao = desvio_padrao

    def __str__(self):
        return f"""
            nome_ativo={self.nome_ativo},
            valor={self.valor},
            retorno={self.retorno},
            volume_medio={self.volume_medio},
            desvio_padrao={self.desvio_padrao}
        """
