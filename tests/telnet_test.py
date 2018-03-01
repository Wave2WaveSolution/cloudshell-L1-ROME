
import telnetlib
import re

class MyTestCase():
    def test_something(self):
        connection = telnetlib.Telnet('192.168.1.124', 23)
        connection.write('SuperUser' + "\n")
        connection.write('superuser' + "\n")


        #connection.write('conn cr e21 to w23\n')
        #message = connection.expect(['CONNECTION OPERATION SUCCEEDED',
        #                             '.*CONNECTION OPERATION SKIPPED\(already done\).*',
        #                             '.*FAILED.*'], 30)

        connection.write('cc' + "\n")
        connection.read_until('cc')
        message = connection.expect(['#'],1)
        lines = message[2].split('\r\n')
        mappings = {}
        if len(lines) > 4:
            for line in lines[4:-2]:
                values = re.match('^E(\d+)?.*?W(\d+)?.*', line).groups()
                mappings[values[0]] = values[1]

            print mappings



        print str(message[2])


if __name__ == '__main__':
    m = MyTestCase()
    m.test_something()
