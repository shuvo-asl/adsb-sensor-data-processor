from tests.BaseCase import BaseCase

class LiveFlight(BaseCase):
    def test_successful_live_flight_show(self):
        response = self.app.get('/live')
        self.assertEquals(200,response.status_code)