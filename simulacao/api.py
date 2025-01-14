from flask import Flask
from flask_restx import Api, Resource, fields
from src.ativo import Ativo
from main import gera_simulacao

app = Flask(__name__)
api = Api(app, version="1.0", title="API de Simulação",
          description="API para realizar simulações financeiras com ativos.")

# Modelo de entrada para a documentação
simulacao_model = api.model('Simulacao', {
    'total_investido': fields.Float(required=True, description='Total investido'),
    'custo_fixo': fields.Float(required=True, description='Custo fixo'),
    'spread_fixo': fields.Float(required=True, description='Spread fixo'),
    'taxa_operacional': fields.Float(required=True, description='Taxa operacional'),
    'num_max_ativos': fields.Integer(required=True, description='Número máximo de ativos'),
    'num_min_ativos': fields.Integer(required=True, description='Número mínimo de ativos'),
    'B_max': fields.Float(required=True, description='Limite máximo de B'),
    'W_min': fields.Float(required=True, description='Limite mínimo de W'),
    'volat_max': fields.Float(required=True, description='Volatilidade máxima'),
    'limite_liquidez': fields.Float(required=True, description='Limite de liquidez'),
    'alocacao_min_por_ativo': fields.Float(required=True, description='Alocação mínima por ativo'),
    'alocacao_max_por_ativo': fields.Float(required=True, description='Alocação máxima por ativo')
})

@api.route('/simulacao')
class SimulacaoResource(Resource):
    @api.expect(simulacao_model)
    def post(self):
        # Obtendo os dados do corpo da requisição
        data = api.payload

        # Criando lista de ativos fictícia
        ativos = [
            Ativo(10, 5, 0.1, 0.01),
            Ativo(20, 1, 0.1, 0.01),
            Ativo(30, 2, 0.1, 0.01),
            Ativo(40, 3, 0.1, 0.01),
            Ativo(50, 4, 0.1, 0.01),
            Ativo(40, 3, 0.1, 0.01),
            Ativo(50, 4, 0.1, 0.01),
        ]

        try:
            # Chamando a função gera_simulacao
            resultado = gera_simulacao(
                ativos,
                data['total_investido'],
                data['custo_fixo'],
                data['spread_fixo'],
                data['taxa_operacional'],
                data['num_max_ativos'],
                data['num_min_ativos'],
                data['B_max'],
                data['W_min'],
                data['volat_max'],
                data['limite_liquidez'],
                data['alocacao_min_por_ativo'],
                data['alocacao_max_por_ativo']
            )
            return {'resultado': resultado}, 200
        except Exception as e:
            return {'error': str(e)}, 500


if __name__ == '__main__':
    app.run(debug=True)
