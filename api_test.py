import unittest
import json

import api


class ConfigTestCase(unittest.TestCase):
    def test_should_be_a_conf_for_memcached(self):
        self.assertIn('MEMCACHED', api.app.config)


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = api.app.test_client()

    def test_add_instance_should_returns_201(self):
        response = self.app.post("/resources")
        self.assertEqual(201, response.status_code)

    def test_bind_instance_should_returns_201(self):
        response = self.app.post("/resources/app")
        self.assertEqual(201, response.status_code)

    def test_bind_should_returns_memcached_uri_on_body(self):
        response = self.app.post("/resources/app")
        data = json.loads(response.data)
        expected = {"MEMCACHED": "127.0.0.1:11211"}
        self.assertEqual(expected, data)

    def test_unbind(self):
        response = self.app.delete("/resources/app")
        self.assertEqual(200, response.status_code)

    def test_remove_instance_should_returns_200(self):
        response = self.app.delete("/resources/app/host/foo")
        self.assertEqual(200, response.status_code)


if __name__ == "__main__":
    unittest.main()
