import pytest
from API import create_app

@pytest.fixture
def client():
    app = create_app(testing=True)
    with app.test_client() as client:
        yield client

def test_gera_melhor_configuracao(client):
    response = client.post('/api/melhor_configuracao', json={'limite_valor': 4000})
    assert response.status_code == 200
    assert 'id' in response.json
    assert 'melhor_configuracao' in response.json
    assert 'custo_final' in response.json
    assert 'pontuacao_final' in response.json

def test_get_todas_configuracoes(client):
    response = client.get('/api/configuracoes')
    assert response.status_code == 200
    assert isinstance(response.json, list)  # Verifica se a resposta é uma lista

def test_get_configuracao_por_id(client):
    # Primeiro, criar uma configuração para obter um ID válido
    create_response = client.post('/api/melhor_configuracao', json={'limite_valor': 4000})
    config_id = create_response.json['id']
    
    # Depois, tenta obter a configuração pelo ID
    response = client.get(f'/api/configuracoes/{config_id}')
    assert response.status_code == 200
    assert 'id' in response.json
    assert response.json['id'] == config_id

def test_get_configuracao_por_id_nao_existente(client):
    response = client.get('/api/configuracoes/99999')  # ID que provavelmente não existe
    assert response.status_code == 404

def test_delete_configuracao(client):
    # Primeiro, criar uma configuração para obter um ID válido
    create_response = client.post('/api/melhor_configuracao', json={'limite_valor': 4000})
    config_id = create_response.json['id']
    
    # Depois, tenta deletar a configuração pelo ID
    delete_response = client.delete(f'/api/configuracoes/{config_id}')
    assert delete_response.status_code == 200

    # Verifica se a configuração foi realmente removida
    get_response = client.get(f'/api/configuracoes/{config_id}')
    assert get_response.status_code == 404

def test_delete_configuracao_nao_existente(client):
    response = client.delete('/api/configuracoes/99999')  # ID que provavelmente não existe
    assert response.status_code == 404

def test_update_configuracao(client):
    # Primeiro, criar uma configuração para obter um ID válido
    create_response = client.post('/api/melhor_configuracao', json={'limite_valor': 4000})
    config_id = create_response.json['id']
    
    # Depois, tenta atualizar a configuração pelo ID
    update_data = {
        'configuracao': {'novo_item': 'valor'},
        'custo_final': 900,
        'pontuacao_final': 150
    }
    update_response = client.put(f'/api/configuracoes/{config_id}', json=update_data)
    assert update_response.status_code == 200

    # Verifica se a configuração foi atualizada corretamente
    get_response = client.get(f'/api/configuracoes/{config_id}')
    assert get_response.status_code == 200
    assert get_response.json['custo_final'] == 900
    assert get_response.json['pontuacao_final'] == 150

def test_update_configuracao_nao_existente(client):
    update_data = {
        'configuracao': {'novo_item': 'valor'},
        'custo_final': 900,
        'pontuacao_final': 150
    }
    response = client.put('/api/configuracoes/99999', json=update_data)  # ID que provavelmente não existe
    assert response.status_code == 404
