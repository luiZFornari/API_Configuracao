from flask import Blueprint, jsonify
from models.models import db, Configuracao
from sqlalchemy.exc import NoResultFound

get_config_bp = Blueprint('get_config', __name__)


@get_config_bp.route('/api/configuracoes', methods=['GET'])
def get_configuracoes():
    configuracoes = Configuracao.query.all()
    return jsonify([{
        'id': c.id,
        'configuracao': c.configuracao,
        'custo_final': c.custo_final,
        'pontuacao_final': c.pontuacao_final,
        'created_at': c.created_at
    } for c in configuracoes])


@get_config_bp.route('/api/configuracoes/<int:id>', methods=['GET'])
def get_configuracao_by_id(id):
    configuracao = Configuracao.query.get(id)
    if configuracao:
        return jsonify({
            'id': configuracao.id,
            'configuracao': configuracao.configuracao,
            'custo_final': configuracao.custo_final,
            'pontuacao_final': configuracao.pontuacao_final,
            'created_at': configuracao.created_at
        })
    else:
        return jsonify({'error': 'Configuração não encontrada'}), 404
