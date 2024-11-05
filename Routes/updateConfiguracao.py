from flask import Blueprint, jsonify, request
from models.models import db, Configuracao

update_config_bp = Blueprint('update_config', __name__)

@update_config_bp.route('/api/configuracoes/<int:id>', methods=['PUT'])
def update_configuracao(id):
    configuracao = Configuracao.query.get(id)
    
    if not configuracao:
        return jsonify({'error': 'Configuração não encontrada'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Nenhum dado enviado para atualizar a configuração'}), 400
    
    configuracao.configuracao = data.get('configuracao', configuracao.configuracao)
    configuracao.custo_final = data.get('custo_final', configuracao.custo_final)
    configuracao.pontuacao_final = data.get('pontuacao_final', configuracao.pontuacao_final)
    
    db.session.commit()
    
    return jsonify({'message': 'Configuração alterada com sucesso'}), 200
