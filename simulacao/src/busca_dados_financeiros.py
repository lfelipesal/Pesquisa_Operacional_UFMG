from typing import List
from src.ativo import Ativo
import yfinance as yf

ACOES_BRASILEIRAS = [
    "PETR4.SA",  # Petrobras PN
    "VALE3.SA",  # Vale ON
    "ITUB4.SA",  # Itaú Unibanco PN
    "BBDC4.SA",  # Bradesco PN
    "ABEV3.SA",  # Ambev ON
    "BBAS3.SA",  # Banco do Brasil ON
    "WEGE3.SA",  # WEG ON
    "RENT3.SA",  # Localiza ON
    "EQTL3.SA",  # Equatorial Energia ON
    "MGLU3.SA",  # Magazine Luiza ON
    "GGBR4.SA",  # Gerdau PN
    "CSNA3.SA",  # CSN ON
    "PRIO3.SA",  # PRIO (ex-PetroRio) ON
    "JBSS3.SA",  # JBS ON
    "RAIL3.SA",  # Rumo ON
    "YDUQ3.SA",  # YDUQS ON
    "BRKM5.SA",  # Braskem PN
    "TAEE11.SA", # Taesa Unit
    "XPML11.SA", # XP Malls (FII)
    "IVVB11.SA", # ETF que replica o S&P 500
    "CVCB3.SA",  # CVC ON
    "ENEV3.SA",  # Eneva ON
    "VIVT3.SA",  # Telefônica Brasil ON
    "HAPV3.SA",  # Hapvida ON
    "LREN3.SA",  # Lojas Renner ON
    "SUZB3.SA",  # Suzano ON
    "HYPE3.SA",  # Hypera ON
    "B3SA3.SA",  # B3 ON
    "PETZ3.SA",  # Petz ON
    "BRFS3.SA",  # BRF ON
    "POSI3.SA",  # Positivo Tecnologia ON
    "USIM5.SA",  # Usiminas PN
    "SANB11.SA", # Santander Brasil Unit
    "ENGI11.SA", # Engie Brasil Energia Unit
    "CPLE6.SA",  # Copel PN
    "AMER3.SA",  # Americanas ON
    "COGN3.SA",  # Cogna Educação ON
    "MRFG3.SA",  # Marfrig ON
    "MULT3.SA",  # Multiplan ON
    "TIMS3.SA",  # Tim ON
    "EGIE3.SA",  # Engie Brasil Energia ON
    "CYRE3.SA",  # Cyrela ON
    "CMIG4.SA",  # Cemig PN
    "CSAN3.SA",  # Cosan ON
    "CPFE3.SA",  # CPFL Energia ON
    "IRBR3.SA",  # IRB Brasil Resseguros ON
    "SEER3.SA",  # Ser Educacional ON
    "AZUL4.SA",  # Azul PN
    "BRAP4.SA",  # Bradespar PN
    "UGPA3.SA",  # Ultrapar ON
    "FLRY3.SA",  # Fleury ON
    #"BIDI11.SA", # Inter Unit
    #"LCAM3.SA",  # Unidas ON
    "BBSE3.SA",  # BB Seguridade ON
    "SLCE3.SA",  # SLC Agrícola ON
    #"ARZZ3.SA",  # Arezzo ON
    "ELET3.SA",  # Eletrobras ON
    "ELET6.SA",  # Eletrobras PN
    "CASH3.SA",  # Meliuz ON
    "ALPA4.SA",  # Alpargatas PN
    "RAIZ4.SA",  # Raízen PN
    "LOGG3.SA",  # Log Commercial Properties ON
    "CCRO3.SA",  # CCR ON
    "ECOR3.SA",  # EcoRodovias ON
    #"TRPL4.SA",  # Transmissão Paulista PN
    "BEEF3.SA",  # Minerva ON
    "MRVE3.SA",  # MRV ON
    "DIRR3.SA",  # Direcional Engenharia ON
    "MEAL3.SA",  # IMC ON
    #"ENBR3.SA",  # Energias do Brasil ON
    #"DMMO3.SA",  # Dommo Energia ON
    "CMIN3.SA",  # CSN Mineração ON
    "TOTS3.SA",  # Totvs ON
    #"SOMA3.SA",  # Grupo Soma ON
    "KLBN11.SA", # Klabin Unit
    "MOVI3.SA",  # Movida ON
    #"AESB3.SA",  # AES Brasil ON
    "NTCO3.SA",  # Natura ON
    #"SQIA3.SA",  # Sinqia ON
    "RDOR3.SA",  # Rede D'Or ON
    "BPAC11.SA", # BTG Pactual Unit
    #"BRML3.SA",  # BR Malls ON
    "GOLL4.SA",  # Gol PN
    "QUAL3.SA",  # Qualicorp ON
    "SMTO3.SA",  # São Martinho ON
    "MDIA3.SA",  # M. Dias Branco ON
    #"TIMP3.SA",  # Tim ON
    "LWSA3.SA",  # Locaweb ON
    #"SULA11.SA", # SulAmérica Unit
    "PSSA3.SA",  # Porto Seguro ON
    "GPIV33.SA", # GP Investments Unit
    "BPAN4.SA",  # Banco Pan PN
    #"CIEL3.SA",  # Cielo ON
    #"VVAR3.SA",  # Via Varejo ON
]

def busca_dados_financeiros(nome_ativos: List[str] = ACOES_BRASILEIRAS) -> List[Ativo]:
    ativos = []
    for nome_ativo in nome_ativos:
        acao = yf.Ticker(nome_ativo)
        ultimo_dividendo = acao.dividends.iloc[0] if len(acao.dividends) > 0 else 0
        ultimo_valor_ativo = acao.history(period="1d")['Close'].iloc[0]
        dados_historicos = acao.history(period="1mo")  # Busca os últimos 30 dias
        volume_normalizado = (dados_historicos['Volume'] - dados_historicos['Volume'].min())/(dados_historicos['Volume'].max() - dados_historicos['Volume'].min()) if not dados_historicos.empty else 0
        volume_medio = volume_normalizado.median() if not dados_historicos.empty else 0
        print(volume_medio)
        desvio_padrao = dados_historicos['Close'].pct_change().dropna().std() if not dados_historicos.empty else 0
        ativos.append(Ativo(nome_ativo,ultimo_valor_ativo, ultimo_dividendo, volume_medio, desvio_padrao))
    
    return ativos
