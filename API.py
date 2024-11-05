from flask import Flask
from db_util import configure_app
from Routes.gerarConfiguracao import gerar_config_bp
from Routes.getConfiguracao import get_config_bp
from Routes.removerConfiguracao import remove_config_bp
from Routes.updateConfiguracao import update_config_bp
from models.models import db
from flask_migrate import Migrate
import os

migrate = Migrate()

def create_app(testing=False):
    app = Flask(__name__)
    configure_app(app)

    # Configura a aplicação para ambiente de teste se necessário
    if testing:
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Banco em memória para testes

    # Inicializa o banco de dados e migração
    db.init_app(app)
    migrate.init_app(app, db)

    # Registra os blueprints das rotas
    app.register_blueprint(gerar_config_bp)
    app.register_blueprint(get_config_bp)
    app.register_blueprint(remove_config_bp)
    app.register_blueprint(update_config_bp)

    # Cria as tabelas no banco de dados de teste
    with app.app_context():
        db.create_all()

    return app

# Apenas executa o servidor se este arquivo for executado diretamente
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
