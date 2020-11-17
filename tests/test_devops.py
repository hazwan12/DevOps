from devops.routes import register
import devops
import pytest
TEST_USER = "ggisburne0"
TEST_EMAIL = "jelstob0@lulu.com"
TEST_PW = "PlEOWNR1"

@pytest.fixture
def client():
    app = devops.app

    app.config["TESTING"] = True
    app.testing = True
    app.template_folder = 'C://Users//hazwa//Desktop//DevOps//devops//templates'
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///C://Users//hazwa//Desktop//DevOps//devops//site.db'
    app.config['WTF_CSRF_ENABLED'] = False

    client =  app.test_client()

    yield client

def login(client, email, password):
    return client.post('/login', data=dict(email=email, password=password), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def register(client, role):
    import datetime
    suffix = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    user = "test_{}".format(suffix)
    email = "{}_{}@email.com".format(role, suffix)
    password = "test_{}_{}".format(role, suffix)

    return client.post('/register', data=dict(role = role, username = user, email = email, password = password,
     confirm_password = password), follow_redirects=True)

def test_register_reporter(client):
    rv = register(client, "Reporter")
    assert 'Account created for' in rv.get_data(True)

"""
def test_register_triager(client):
    rv = register(client, "Triager")
    assert 'Account created for' in rv.get_data(True)

def test_register_developer(client):
    rv = register(client, "Developer")
    assert 'Account created for' in rv.get_data(True)

def test_register_reviewer(client):
    rv = register(client, "Reviewer")
    assert 'Account created for' in rv.get_data(True)
"""

def test_login(client):
    rv = login(client, TEST_EMAIL, TEST_PW)
    assert TEST_USER in rv.get_data(True)

def test_logout(client):
    login(client, TEST_EMAIL, TEST_PW)
    rv = logout(client)
    assert 'Log In' in rv.get_data(True)

def test_invalid_user(client):
    rv = login(client, TEST_EMAIL + 'x', TEST_PW)
    assert 'Login Unsuccessful. Please check email and password.' in rv.get_data(True)

def test_invalid_pw(client):
    rv = login(client, TEST_EMAIL, TEST_PW + 'x')
    assert 'Login Unsuccessful. Please check email and password.' in rv.get_data(True)

def test_create_bug(client):
    login(client, TEST_EMAIL, TEST_PW)
    rv = client.post('/newbug', 
    data=dict(summary = "test", product = "test", platform = "test", whatHappen = "test", howHappen = "test", 
    shouldHappen = "test"), follow_redirects=True)

    assert 'Your bug report has been created!' in rv.get_data(True)

def test_create_bug_no_login(client):
    rv = client.post('/newbug', 
    data=dict(summary = "test", product = "test", platform = "test", whatHappen = "test", howHappen = "test", 
    shouldHappen = "test"), follow_redirects=True)
    assert 'Please sign in' in rv.get_data(True)
 