import unittest
import json
import os

import mock

import api


class ConfigTestCase(unittest.TestCase):
    def test_should_be_a_conf_for_public_host(self):
        self.assertIn("PUBLIC_HOST", api.app.config)

    def test_public_host_conf_should_be_defined_by_environ(self):
        public_host = api.app.config["PUBLIC_HOST"]
        os.environ["PUBLIC_HOST"] = "ble"
        reload(api)
        self.assertEqual("ble", api.app.config["PUBLIC_HOST"])
        api.app.config["PUBLIC_HOST"] = public_host

    def test_public_host_default_value_should_be_defined_by_memcached_conf_value(self):
        self.assertEqual(api.app.config["MEMCACHED"], api.app.config["PUBLIC_HOST"])

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

    def test_bind_should_return_public_host_on_body(self):
        api.app.config["PUBLIC_HOST"] = "10.10.10.10:11212"
        response = self.app.post("/resources/app")
        data = json.loads(response.data)
        expected = {"MEMCACHED": "10.10.10.10:11212"}
        self.assertEqual(expected, data)
        api.app.config["PUBLIC_HOST"] = api.app.config["MEMCACHED"]

    def test_unbind(self):
        response = self.app.delete("/resources/app")
        self.assertEqual(200, response.status_code)

    def test_remove_instance_should_returns_200(self):
        response = self.app.delete("/resources/app/host/foo")
        self.assertEqual(200, response.status_code)

    def test_status_should_returns_204_when_memcached_is_connected(self):
        with mock.patch('memcache.Client') as MockClass:
            instance = MockClass.return_value
            instance.servers[0].connect.return_value = 1
            response = self.app.get("/resources/app/status")
        self.assertEqual(204, response.status_code)

    def test_status_should_returns_500_when_memcached_is_not_connected(self):
        with mock.patch('memcache.Client') as MockClass:
            instance = MockClass.return_value
            instance.servers[0].connect.return_value = 0
            response = self.app.get("/resources/app/status")
        self.assertEqual(500, response.status_code)


if __name__ == "__main__":
    unittest.main()
