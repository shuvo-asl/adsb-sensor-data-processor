from tests.BaseCase import BaseCase

class RootEndPoint(BaseCase):
    def test_root_endpoint(self):
        response = self.app.get('/')
        assert response.status_code == 200
