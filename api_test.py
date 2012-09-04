import unittest

import api


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = api.app.test_client()

    def test_add_instance_should_returns_201(self):
        response = self.app.post("/resources")
        self.assertEqual(201, response.status_code)

    def test_bind_instance_should_returns_201(self):
        response = self.app.post("/resources/app")
        self.assertEqual(201, response.status_code)

    def test_remove_instance_should_returns_200(self):
        response = self.app.delete("/resources/app/host/foo")
        self.assertEqual(200, response.status_code)

if __name__ == "__main__":
    unittest.main()
