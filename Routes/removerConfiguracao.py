from flask import Blueprint, jsonify
from models.models import db, Configuracao

remove_config_bp = Blueprint('remove_config', __name__)

@remove_config_bp.route('/api/configuracoes/<int:id>', methods=['DELETE'])
def remove_configuracao_by_id(id):
    configuracao = Configuracao.query.get(id)  
    if configuracao:
        db.session.delete(configuracao)  
        db.session.commit()  
        return jsonify({'message': 'Configuração removida com sucesso'}), 200
    else:
        return jsonify({'error': 'Configuração não encontrada'}), 404  
