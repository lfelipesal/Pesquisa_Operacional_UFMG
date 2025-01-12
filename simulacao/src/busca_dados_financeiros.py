from typing import List
from src.ativo import Ativo
import yfinance as yf

ACOES_BRASILEIRAS = ["PETR3.SA", "PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBAS3.SA"]

def busca_dados_financeiros(nome_ativos: List[str] = ACOES_BRASILEIRAS) -> List[Ativo]:
    ativos = []
    for nome_ativo in nome_ativos:
        acao = yf.Ticker(nome_ativo)
        ultimo_dividendo = acao.dividends.iloc[0] if len(acao.dividends) > 0 else 0
        ultimo_valor_ativo = acao.history(period="1d")['Close'].iloc[0]
        ativos.append(Ativo(ultimo_valor_ativo, ultimo_dividendo))
    
    return ativos
