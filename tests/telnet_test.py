
import telnetlib

class MyTestCase():
    def test_something(self):
        connection = telnetlib.Telnet('192.168.1.124', 23)
        connection.write('SuperUser' + "\n")
        connection.write('superuser' + "\n")

        connection.write('cc' + "\n")
        message = connection.expect(['A22-A46','A20-A45'],1)
        print str(message[2])


if __name__ == '__main__':
    m = MyTestCase()
    m.test_something()
