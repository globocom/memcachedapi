import unittest
import json
import os

import api


class ConfigTestCase(unittest.TestCase):

    def test_should_be_a_conf_for_memcached(self):
        self.assertIn("MEMCACHED", api.app.config)

    def test_memcached_conf_should_be_defined_by_environ(self):
        memcached = api.app.config["MEMCACHED"]
        os.environ["MEMCACHED"] = "ble"
        reload(api)
        self.assertEqual("ble", api.app.config["MEMCACHED"])
        api.app.config["MEMCACHED"] = memcached


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = api.app.test_client()

    def tearDown(self):
        api.app.config["PUBLIC_HOST"] = api.app.config["MEMCACHED"]

    def test_add_instance_should_return_201(self):
        response = self.app.post("/resources")
        self.assertEqual(201, response.status_code)

    def test_bind_instance_should_return_201(self):
        response = self.app.post("/resources/app")
        self.assertEqual(201, response.status_code)

    def test_bind_should_return_memcached_uri_on_body(self):
        response = self.app.post("/resources/app")
        data = json.loads(response.data)
        expected = {"MEMCACHED": "127.0.0.1:11211"}
        self.assertEqual(expected, data)

    def test_bind_should_return_public_host_on_body(self):
        api.app.config["PUBLIC_HOST"] = "10.10.10.10:11212"
        response = self.app.post("/resources/app")
        data = json.loads(response.data)
        expected = {"MEMCACHED": "10.10.10.10:11212"}
        self.assertEqual(expected, data)

    def test_unbind(self):
        response = self.app.delete("/resources/app")
        self.assertEqual(200, response.status_code)

    def test_remove_instance_should_return_200(self):
        response = self.app.delete("/resources/app/host/foo")
        self.assertEqual(200, response.status_code)


if __name__ == "__main__":
    unittest.main()
