import unittest
import telnetlib

class TestRomeDriverHandler(unittest.TestCase):
    def setUp(self):
        super(TestRomeDriverHandler, self).setUp()

    def tearDown(self):
        super(TestRomeDriverHandler, self).tearDown()

    def test_login(self):
        self.username = "SuperUser\n"
        self.password = "superuser\n"
        ip = "192.168.1.206"
        self.connection = telnetlib.Telnet(ip)
        self.connection.write(self.username)
        self.connection.write(self.password)

    def test_get_resource_description(self):
        pass

    def test_map_bidi(self):
        self.username = "SuperUser"
        self.password = "superuser"
        ip = "192.168.1.204"
        self.connection = telnetlib.Telnet(ip)

        port1 = "e60"
        port2 = "w60"

        # Create a duplex connection
        command1 = "con cr %s t %s \n" % (port1, port2)
        command2 = "con cr %s t %s \n" % (port2, port1)
        self.connection.write(self.username + "\n")
        self.connection.write(self.password + "\n")
        self.connection.write(command1)
        self.connection.write(command2)

    def test_map_uni(self):
        pass

    def test_map_clear_to(self):
        pass

    def test_map_clear(self):
        pass

    def test_set_speed_manual(self):
        pass
