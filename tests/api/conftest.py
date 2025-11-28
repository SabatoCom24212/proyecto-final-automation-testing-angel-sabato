import pytest
import requests


@pytest.fixture(scope="session")
def base_url():
    """URL base de JSONPlaceholder"""
    return "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="function")
def api_client(base_url):
    """
    Cliente HTTP para realizar peticiones a la API.
    Incluye métodos para GET, POST, PUT, PATCH y DELETE.
    """
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Accept": "application/json"
    })
    
    class APIClient:
        def __init__(self, base_url, session):
            self.base_url = base_url
            self.session = session
        
        def get(self, endpoint, **kwargs):
            """
            Realiza una petición GET
            """
            url = f"{self.base_url}{endpoint}"
            return self.session.get(url, **kwargs)
        
        def post(self, endpoint, json=None):
            """
            Realiza una petición POST
            """
            url = f"{self.base_url}{endpoint}"
            return self.session.post(url, json=json)
        
        def put(self, endpoint, json=None):
            """
            Realiza una petición PUT (reemplazo completo del recurso)
            """
            url = f"{self.base_url}{endpoint}"
            return self.session.put(url, json=json)
        
        def patch(self, endpoint, json=None):
            """
            Realiza una petición PATCH (actualización parcial del recurso)
            """
            url = f"{self.base_url}{endpoint}"
            return self.session.patch(url, json=json)
        
        def delete(self, endpoint):
            """
            Realiza una petición DELETE
            """
            url = f"{self.base_url}{endpoint}"
            return self.session.delete(url)
        
        def get_all_todos(self):
            """Helper: Obtiene todos los TODOs"""
            return self.get("/todos")
        
        def get_all_posts(self):
            """Helper: Obtiene todos los posts"""
            return self.get("/posts")
        
        def get_all_users(self):
            """Helper: Obtiene todos los usuarios"""
            return self.get("/users")
        
        def get_user_posts(self, user_id):
            """Helper: Obtiene posts de un usuario específico"""
            return self.get(f"/users/{user_id}/posts")
        
        def get_post_comments(self, post_id):
            """Helper: Obtiene comentarios de un post"""
            return self.get(f"/posts/{post_id}/comments")
    
    return APIClient(base_url, session)