from typing import List
import gurobipy as gp
import random
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
    num_min_ativos: int = 4,
    B_max: int = 3,
    volat_max: float = 0.05,
    alocacao_min_por_ativo: int = 5,
    alocacao_max_por_ativo: int = 200,
):
    num_ativos = len(ativos)
    desvio_padrao = []   # Defininado o desvio padrão individual (Volatilidade) de cada ativo
    limite_liquidez = [] # Definir um limite (1%-5% do volume médio diário)
    mu = []              # Definindo os retornos esperado de cada ativo com base nos dividendos
    C = []               # Definindo os custos das transações de cada ativo com base no seu ultimo valor sobre um spread fixo

    for ativo in ativos:
        desvio_padrao.append(ativo.desvio_padrao)
        limite_liquidez.append(ativo.volume_medio)
        mu.append(ativo.retorno)
        C.append(custo_fixo + (spread_fixo * ativo.valor) + taxa_operacional)

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
    model.addConstr(gp.quicksum(w[i]*ativos[i].valor + C[i]*x[i] for i in range(num_ativos)) <= total_investido, name="Total_Investido")  # 1- Orçamento Total Investido
    model.addConstrs((w[i] >= alocacao_min_por_ativo*x[i] for i in range(num_ativos)), name="Alocacao_Min_Ativo_Selecionado") # 2- Alocação minima do Ativo Se Selecionado
    model.addConstrs((w[i] <= alocacao_max_por_ativo*x[i]*limite_liquidez[i] for i in range(num_ativos)), name="Alocacao_Max_Ativo_Selecionado") # 3- Alocação máxima do Ativo Se Selecionado
    model.addConstr(gp.quicksum(x[i] for i in range(num_ativos)) >= num_min_ativos, name="Numero_Min_Ativos_Diferentes")      # 4- Número Mínimo de Investimentos
    model.addConstr(gp.quicksum(x[i] for i in range(num_ativos)) <= num_max_ativos, name="Numero_Max_Ativos_Diferentes")      # 5- Número Máximo de Ativos por Investidor
    model.addConstr(gp.quicksum(C[i]*x[i] for i in range(num_ativos)) <= B_max, name="Custos_Max_Total_Transacao")            # 6- Custos de Transação
    model.addConstr(gp.quicksum(desvio_padrao[i]*x[i] for i in range(num_ativos)) <= volat_max, name="Volatilidade_Max")      # 7- Volatilidade Máxima dos investidores
    #model.addConstrs((w[i]*ativos[i].valor <= limite_liquidez[i] for i in range(num_ativos)), name= "Limite de liquidez" )

    try:
        # Defina e resolva o modelo
        model.update()
        print(model.display())
        model.optimize()

        # Verifique se o modelo foi otimizado com sucesso
        investimento_total = 0
        if model.status == gp.GRB.OPTIMAL:
            for i in range(len(ativos)):
                if(x[i].X > 0 and w[i].X > 0):
                    print(f"Nome Ativo: {ativos[i].ticker}")
                    print(f"Quantidade Adquirido: {w[i].X}")
                    investimento_total += C[i] + ativos[i].valor*w[i].X
                    print(f"Nome Ativo: {ativos[i].ticker}  Quantidade Adquirido: {w[i].X} Valor: {ativos[i].valor:.2f}  Volatilidade: {ativos[i].desvio_padrao:.3f}")
            print(f"Total gasto investido: {investimento_total}")
            print(f"Lucro Máx Obtido: {model.ObjVal}")
            print(f'Rendimento Anual: {(model.ObjVal/total_investido)*100}%')
        else:
            print("A otimização não foi bem-sucedida.")

    except gp.GurobiError as e:
        print(f"Erro do Gurobi: {e.message}")
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")



ativos: List[Ativo] = busca_dados_financeiros()

total_investido = 100000      # Total investido
custo_fixo = 5                # Custo fixo por transação
spread_fixo = 0.05            # Spread fixo de 0.5%
taxa_operacional = 2          # Custo diário fixo
num_min_ativos = 4            # Número min de ativos
num_max_ativos = 8            # Número máximo de ativos
B_max = total_investido*0.5   # Custo maximo gasto em transação
volat_max =  0.07             # Definindo a volatilidade máxima dos ativos sendo 5%
alocacao_min_por_ativo = 20   # Alocacao minima por ativo
alocacao_max_por_ativo = 800  # Alocacao max por ativo

ativos.extend([
    Ativo('Poupança', 50, 50*0.0617, round(random.uniform(0.3, 0.8), 3), 0.0045),
    Ativo('CDB', 50, 50*0.1088, round(random.uniform(0.3, 0.8), 3), 0.0061),
    Ativo('SELIC', 50, 50*0.1212, round(random.uniform(0.3, 0.8), 3), 0.0061)    
])

gera_simulacao(
    ativos,
    total_investido,
    custo_fixo,
    spread_fixo,
    taxa_operacional,
    num_max_ativos,
    num_min_ativos,
    B_max,
    volat_max,
    alocacao_min_por_ativo,
    alocacao_max_por_ativo
)
