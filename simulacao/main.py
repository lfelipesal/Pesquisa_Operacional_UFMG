from typing import List
import gurobipy as gp
from gurobipy import GRB

from src.busca_dados_financeiros import busca_dados_financeiros
from src.ativo import Ativo


def gera_simulacao(
    ativos: List[Ativo],
    total_investido: float = 10000.0,
    custo_fixo: float = 10,
    spread_fixo: float = 0.005,
    taxa_operacional: float = 5,
    num_max_ativos: int = 10,
    B_max: int = 3,
    W_min: float = 0.02,
    volat_max: float = 0.05,
    limite_liquidez: float = 0.01
):
    num_ativos = len(ativos)
    desvio_padrao = []   # Defininado o desvio padrão individual (Volatilidade) de cada ativo
    limite_liquidez = [] # Definir um limite (1%-5% do volume médio diário)
    mu = []              # Definindo os retornos esperado de cada ativo com base nos dividendos
    C = []               # Definindo os custos das transações de cada ativo com base no seu ultimo valor sobre um spread fixo

    for ativo in ativos:
        print(ativo)
        desvio_padrao.append(ativo.desvio_padrao)
        limite_liquidez.append(0.01 * ativo.volume_medio)
        mu.append(ativo.retorno)
        C.append( custo_fixo + (spread_fixo * ativo.valor) + taxa_operacional)

    # Função objetivo: Max Zk = sum(μ[i]*w[i,k]) - sum(C[i]*x[i,k]) para todos os k
    # μ[i]: Retorno esperado do ativo i.
    # C[i]: Custo fixo associado a transacao do ativo i.
    # Criar um modelo de otimização
    model = gp.Model("Modelo_Com_Funcao_Objetivo")

    # Variáveis do problema
    w = model.addVars(num_ativos, vtype=GRB.INTEGER, name="w")
    x = model.addVars(num_ativos, vtype=GRB.BINARY, name="x")

    # Objetivo: Z = sum(mu[i] * w[i] - C[i] * x[i] for i in range(n))
    model.setObjective(
        gp.quicksum(
            mu[i] * w[i]
            for i in range(num_ativos)
        )
        - 
        gp.quicksum(
            C[i] * x[i]
            for i in range(num_ativos)
        ),
        GRB.MAXIMIZE)

    # Restrições
    model.addConstr(gp.quicksum(w[i]*ativos[i].valor for i in range(num_ativos)) <= total_investido, name="Total_Investido") # 1- Orçamento Total por Investidor
    model.addConstr(gp.quicksum(x[i] for i in range(num_ativos)) >= 4, name="restricao_soma_xi")                             # 2- Número Mínimo de Investimentos
    model.addConstr(gp.quicksum(x[i] for i in range(num_ativos)) <= num_max_ativos, name="restricao_Max_ativos")             # 3- Número Máximo de Ativos por Investidor
    # model.addConstrs((w[i] <= limite_liquidez[i]*x[i] for i in range(num_ativos)), name="limite_liquidez")                  # 4- Limites de Alocação por Ativo
    model.addConstr(gp.quicksum(C[i]*x[i] for i in range(num_ativos)) <= B_max, name="Custos_maximo")                        # 5- Custos de Transação
    # model.addConstrs((w[i] >= W_min*x[i] for i in range(num_ativos)), name="Alocacao_minima")                              # 6- Alocação Mínima por Ativo Selecionado
    model.addConstr(gp.quicksum(desvio_padrao[i]*x[i] for i in range(num_ativos)) <= volat_max, name="Volatilidade_maxima")  # 7- Volatilidade Máxima dos investidores    

    try:
        # Defina e resolva o modelo
        model.optimize()

        # Verifique se o modelo foi otimizado com sucesso
        if model.status == gp.GRB.OPTIMAL:
            for v in model.getVars():
                print(f"{v.VarName} {v.X:g}")
        else:
            print("A otimização não foi bem-sucedida.")

    except gp.GurobiError as e:
        print(f"Erro do Gurobi: {e.message}")
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")



ativos: List[Ativo] = busca_dados_financeiros()
total_investido = 100.000 # Total investido
custo_fixo = 10           # Custo fixo por transação
spread_fixo = 0.005       # Spread fixo de 0.5%
taxa_operacional = 5      # Custo diário fixo
num_max_ativos = 10       # Número máximo de ativos
B_max = 3                 # Custo maximo gasto em transação
W_min = 0.02              # Alocação mínima de 2% em cada ativo
volat_max =  0.05         # Definindo a volatilidade máxima dos ativos sendo 5%
limite_liquidez = 0.01    # Limite de liquidez aceita

gera_simulacao(
    ativos,
    total_investido,
    custo_fixo,
    spread_fixo,
    taxa_operacional,
    num_max_ativos,
    B_max,
    W_min,
    volat_max
)