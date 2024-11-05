from flask import Blueprint, request, jsonify
from db_util import load_componentes
from models.models import db, Configuracao
from AG.AG import algoritmo_genetico
from datetime import datetime
import json

gerar_config_bp = Blueprint('gerar_config', __name__)

# Route to generate and save the best configuration
@gerar_config_bp.route('/api/melhor_configuracao', methods=['POST'])
def melhor_configuracao():
    data = request.json
    componentes = load_componentes()
    limite_valor = data.get('limite_valor')
    
    if not componentes or not limite_valor:
        return jsonify({'error': 'Dados incompletos fornecidos'}), 400

    # Run the genetic algorithm
    melhor_config, custo_final, pontuacao_final = algoritmo_genetico(componentes, limite_valor)

    if melhor_config:
        # Save configuration to the database using SQLAlchemy
        configuracao = Configuracao(
            configuracao=json.dumps(melhor_config),
            custo_final=custo_final,
            pontuacao_final=pontuacao_final
        )
        db.session.add(configuracao)
        db.session.commit()

        return jsonify({
            'id': configuracao.id,
            'melhor_configuracao': melhor_config,
            'custo_final': custo_final,
            'pontuacao_final': pontuacao_final
        })
    else:
        return jsonify({'message': 'Não foi encontrada uma configuração válida dentro do limite de valor'}), 404
