import pytest
from app import app  # Import the Flask app from the app.py file

# Define a pytest fixture to set up the test client
@pytest.fixture
def client():
    # Set the Flask app to testing mode
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret'
    # Create a test client
    with app.test_client() as client:
        # Set up the application context
        with app.app_context():
            yield client  # Yield the client for use in tests

# Test the GET request to the index route
def test_index_get(client):
    # Send a GET request to the root URL
    response = client.get('/')
    # Check that the response status code is 200 (OK)
    assert response.status_code == 200
    # Check that the response data contains the expected message
    assert b'Hello, World' in response.data

# Test the POST request to the index route
def test_index_post(client):
    # Send a POST request to the root URL with form data
    response = client.post('/', data={'user_input': 'test_input'}, follow_redirects=True)
    # Check that the response status code is 200 (OK)
    assert response.status_code == 200
    # Check that the response data contains the submitted input
    assert b'test_input' in response.data

# Test to ensure no computer code is accepted in the input
def test_no_code_input(client):
    code_input = "<script>alert('test');</script>"
    # Send a POST request with potentially malicious code
    response = client.post('/', data={'user_input': code_input}, follow_redirects=True)
    # Check that the response status code is 200 (OK)
    assert response.status_code == 200
    # Ensure the code is not present in the response data
    assert b'<script>' not in response.data

# Test the submitted form route
def test_submitted_form(client):
    # Use the session transaction to set the session variable
    with client.session_transaction() as sess:
        sess['user_input'] = 'test_input'
    # Send a GET request to the /submitted URL
    response = client.get('/submitted')
    # Check that the response status code is 200 (OK)
    assert response.status_code == 200
    # Check that the response data contains the session input
    assert b'test_input' in response.data
