import pytest
from flask import Flask, session
from flask.testing import FlaskClient
from app import app  # Assuming your Flask app is in a file named app.py

@pytest.fixture
def client() -> FlaskClient:
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret'
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_index_get(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello, World' in response.data

def test_index_post(client):
    response = client.post('/', data={'user_input': 'test_input'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'test_input' in response.data

def test_submitted_form(client):
    with client.session_transaction() as sess:
        sess['user_input'] = 'test_input'
    response = client.get('/submitted')
    assert response.status_code == 200
    assert b'test_input' in response.data
