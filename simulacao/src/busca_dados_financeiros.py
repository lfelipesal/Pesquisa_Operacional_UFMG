from collections import defaultdict
from typing import List
from src.ativo import Ativo
import yfinance as yf
import pandas as pd
import json

df = pd.read_csv('simulacao/acoes-listadas-b3.csv')
tickers = df['Ticker'].to_list()

SELIC = 0.1225
ACOES_BRASILEIRAS = [
    f'{ticker}.SA'
    for ticker in tickers
]

def busca_dados_financeiros(ticker_ativos: List[str] = ACOES_BRASILEIRAS, salvar_cache = True, le_cache = True) -> List[Ativo]:
    ativos = []
    if le_cache:
        try:
            with open(Ativo.PATH_FILE_CACHE) as cache_file:
                dados = json.load(cache_file)
                return [
                    Ativo(**dado)
                    for dado in dados
                ]
        except Exception as e:
            print("Não conseguiu ler/tratar o arquivo.")
            print(e)

    for ticker_ativo in ticker_ativos:
        try:
            acao = yf.Ticker(ticker_ativo)
            media_dividendo_anual = __get_media_dividendo_anual(acao.dividends)
            ultimo_valor_ativo = acao.history(period="1d")['Close'].iloc[0]
            media_dividendo_anual = SELIC * ultimo_valor_ativo if media_dividendo_anual > 0.22*ultimo_valor_ativo else media_dividendo_anual
            dados_historicos = acao.history(period="1mo")  # Busca os últimos 30 dias
            volume_medio = dados_historicos['Volume'].mean() if not dados_historicos.empty else 0
            desvio_padrao = dados_historicos['Close'].pct_change().dropna().std() if not dados_historicos.empty else 0
            ativos.append(Ativo(ticker_ativo, ultimo_valor_ativo, media_dividendo_anual, volume_medio, desvio_padrao))
        except Exception as e:
            print('Erro ao buscar dados do ativo')
            print(e)
    
    if salvar_cache:
        ativos_dict = [
            ativo.to_json()
            for ativo in ativos
        ]
        with open(Ativo.PATH_FILE_CACHE, 'w') as fout:
            json.dump(ativos_dict , fout)

    return ativos


def __get_media_dividendo_anual(dividendos):
    try:
        dividendos = dividendos.to_dict()
        total_por_ano = defaultdict(lambda : 0)
        for key, value in dividendos.items():
            total_por_ano[key.year] += value

        return sum(total_por_ano.values())/len(total_por_ano.keys())
    except ZeroDivisionError as e:
        print('Não tem dividendos')
        return 0

