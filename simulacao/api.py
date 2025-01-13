from flask import Flask, request, jsonify

app = Flask(__name__)

# Importando função de simulação
from src.ativo import Ativo
from typing import List
from main import gera_simulacao

@app.route('/simulacao', methods=['POST'])
def simulacao():
    # Pegando os dados enviados pelo cliente
    data = request.get_json()

    # Validando se todos os parâmetros necessários estão presentes
    required_params = [
        'total_investido', 'num_max_ativos', 'num_min_ativos',
        'B_max', 'volat_max', 
        'alocacao_min_por_ativo', 'alocacao_max_por_ativo'
    ]
    missing_params = [param for param in required_params if param not in data]
    if missing_params:
        return jsonify({'error': f'Missing parameters: {", ".join(missing_params)}'}), 400

    # Extraindo os parâmetros
    ativos = [
        Ativo(10, 5, 0.1, 0.01),
        Ativo(20, 1, 0.1, 0.01),
        Ativo(30, 2, 0.1, 0.01),
        Ativo(40, 3, 0.1, 0.01),
        Ativo(50, 4, 0.1, 0.01),
        Ativo(40, 3, 0.1, 0.01),
        Ativo(50, 4, 0.1, 0.01),
    ]
    total_investido = data['total_investido']
    custo_fixo = data['custo_fixo']
    spread_fixo = data['spread_fixo']
    taxa_operacional = data['taxa_operacional']
    num_max_ativos = data['num_max_ativos']
    num_min_ativos = data['num_min_ativos']
    B_max = data['B_max']
    W_min = data['W_min']
    volat_max = data['volat_max']
    limite_liquidez = data['limite_liquidez']
    alocacao_min_por_ativo = data['alocacao_min_por_ativo']
    alocacao_max_por_ativo = data['alocacao_max_por_ativo']

    # Chamando a função gera_simulacao com os parâmetros
    try:
        resultado = gera_simulacao(
            ativos, total_investido, custo_fixo, spread_fixo,
            taxa_operacional, num_max_ativos, num_min_ativos,
            B_max, W_min, volat_max, limite_liquidez,
            alocacao_min_por_ativo, alocacao_max_por_ativo
        )
        return jsonify({'resultado': resultado})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
