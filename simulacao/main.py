from typing import List
import gurobipy as gp
from gurobipy import GRB

from src.busca_dados_financeiros import busca_dados_financeiros
from src.ativo import Ativo


# Função objetivo: Max Zk = sum(μ[i]*w[i,k]) - sum(C[i]*x[i,k]) para todos os k
# μ[i]: Retorno esperado do ativo i.
# C[i]: Custo fixo associado a transacao do ativo i.

ativos: List[Ativo] = busca_dados_financeiros()

# Parâmetros do problema
num_ativos = len(ativos)
custo_fixo = 10  # Custo fixo por transação
spread_fixo = 0.005  # Spread fixo de 0.5%
taxa_operacional = 5  # Custo diário fixo
N_maximo = 10 # Número máximo de ativos
B_max = 3 # Custo maximo gasto em transação
W_min = 0.02 # Alocação mínima de 2% em cada ativo
Volat_max =  0.05 # Definindo a volatilidade máxima dos ativos sendo 5%
desvio_padrao = [] # Defininado o desvio padrão individual (Volatilidade) de cada ativo
limite_liquidez = [] # Definir um limite (1%-5% do volume médio diário)
mu = []     # Definindo os retornos esperado de cada ativo com base nos dividendos
C = []      # Definindo os custos das transações de cada ativo com base no seu ultimo valor sobre um spread fixo

for ativo in ativos:
    desvio_padrao.append(ativo.desvio_padrao)
    limite_liquidez.append(0.01 * ativo.volume_medio)
    mu.append(ativo.retorno)
    C.append( custo_fixo +  (spread_fixo * ativo.valor) + taxa_operacional)



# Criar um modelo de otimização
model = gp.Model("Modelo_Com_Funcao_Objetivo")

# Variáveis do problema
w = model.addVars(num_ativos, vtype=GRB.CONTINUOUS, name="w") #
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
model.addConstr(gp.quicksum(w[i] for i in range(num_ativos)) <= 1, name="Total_Investido")                              # 1- Orçamento Total por Investidor
model.addConstr(gp.quicksum(x[i] for i in range(num_ativos)) >= 4, name="restricao_soma_xi")                            # 2- Número Mínimo de Investimentos
model.addConstr(gp.quicksum(x[i] for i in range(num_ativos)) <= N_maximo, name="restricao_Max_ativos")                  # 3- Número Máximo de Ativos por Investidor
model.addConstrs((w[i] <= limite_liquidez[i]*x[i] for i in range(num_ativos)), name="limite_liquidez")                   # 4- Limites de Alocação por Ativo
model.addConstr(gp.quicksum(C[i]*x[i] for i in range(num_ativos)) <= B_max, name="Custos_maximo")                       # 5- Custos de Transação
model.addConstrs((w[i] >= W_min*x[i] for i in range(num_ativos)), name="Alocacao_minima")                                # 6- Alocação Mínima por Ativo Selecionado
model.addConstr(gp.quicksum(desvio_padrao[i]*x[i] for i in range(num_ativos)) <= Volat_max, name="Volatilidade_maxima") # 7- Volatilidade Máxima dos investidores    


# Resolver o modelo
model.optimize()
if model.Status == GRB.OPTIMAL:
    for v in model.getVars():
        print(f"{v.VarName} {v.X:g}")
else:
    print("A otimização não foi bem-sucedida.")