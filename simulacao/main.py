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
mu = []
C = []
for ativo in ativos:
    mu.append(ativo.retorno)
    C.append(ativo.valor)

model = gp.Model("FuncaoObjetivo")


# Criar um modelo de otimização
model = gp.Model("Modelo_Com_Funcao_Objetivo")

# Variáveis do problema
w = model.addVars(num_ativos, vtype=GRB.CONTINUOUS, name="w")
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
model.addConstr(gp.quicksum(x[i] for i in range(num_ativos)) >= 4, name="restricao_soma_xi")

# Resolver o modelo
model.optimize()

for v in model.getVars():
    print(f"{v.VarName} {v.X:g}")

print(f"Obj: {model.ObjVal:g}")

