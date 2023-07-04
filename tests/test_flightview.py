from tests.BaseCase import BaseCase
import json
'''
This class is responsible to ensure that the FLightView API endpoint will successfully work.
'''
class FlightViewTest(BaseCase):

    def test_flight_view_endpoint_enable(self):
        response = self.app.get('/flight')

        # Check the Content-Type header
        content_type = response.headers.get('Content-Type', '')

        # Assert that the Content-Type is JSON
        self.assertIn('application/json', content_type)

        # Attempt to parse the response content as JSON
        try:
            json_response_data = json.loads(response.data)
        except json.JSONDecodeError:
            self.fail("API response is not valid JSON")

        # Additional assertions on the parsed JSON data if needed
        self.assertIsInstance(json_response_data, dict)
        self.assertIn('status', json_response_data)

    def test_pass_invalid_status(self):
        response = self.app.get('/flight/wrong_status')
        self.assertEquals(422, response.status_code)

    def test_status_wise_data(self):
        response = self.app.get('/flight/completed')
        json_response_data = json.loads(response.data)
        self.assertEquals(200, response.status_code)

        # Additional assertions on the parsed JSON data if needed
        self.assertIsInstance(json_response_data, dict)
        self.assertIn('status', json_response_data)
        self.assertIn('data', json_response_data)
        self.assertEquals('success', json_response_data['status'])


    def test_get_all_data(self):
        response = self.app.get('/flight')
        json_response_data = json.loads(response.data)
        self.assertEquals(200, response.status_code)

        # Additional assertions on the parsed JSON data if needed
        self.assertIsInstance(json_response_data, dict)
        self.assertIn('status', json_response_data)
        self.assertIn('data', json_response_data)
        self.assertEquals('success', json_response_data['status'])
