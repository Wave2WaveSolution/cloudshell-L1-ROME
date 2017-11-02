# importing functions
from common.driver_handler_base import DriverHandlerBase
from common.configuration_parser import ConfigurationParser
from common.resource_info import ResourceInfo
from cloudshell.core.logger.qs_logger import get_qs_logger

# importing telnet library python
import telnetlib
import time


class RomeDriverHandler(DriverHandlerBase):
    def __init__(self):
        DriverHandlerBase.__init__(self)
        self._switch_model = "Rome"
        self._blade_model = "Rome Patch Panel"
        self._port_model = "Rome Port"
        self._driver_name = ConfigurationParser.get("common_variable", "driver_name")
        self._command_timeout = ConfigurationParser.get("driver_variable", "command_timeout")
        if self._command_timeout is None:
            self._command_timeout = 121
        self._logger = None
        self._connection = None
        self._device_address = ''
        self._device_user = ''
        self._device_password = ''
        self._port = ''

    def login(self, address, username, password, command_logger=None):
        # Get port
        self._port = ConfigurationParser.get("common_variable", "connection_port")

        addr = address.split(":")[0]
        if self._device_address != addr or self._device_user != username or self._device_password != password:
            self._connection = None

        self._device_address = addr
        self._device_user = username
        self._device_password = password

        # Print out device login information
        self._logger = command_logger
        self._logger.info('Attempting to Connect')
        self._logger.info('Default command timeout: ' + str(self._command_timeout))
        self._logger.info('Device address is: ' + str(addr) + ', port: ' + str(self._port))
        self._logger.info('Username: ' + str(username))
        self._logger.info('Device Prompt: ' + str(self._prompt))
        self._create_connection()

    def _create_connection(self):
        # Create Telnet session if needed
        if self._connection:
            try:
                self._connection.write("\n")
            except Exception as ex:
                self._logger.info('Connection is probably closed, starting a new one')
                self._logger.info(ex.message)
                self._connection = None

        if self._connection is None:
            self._logger.info('Creating Telnet Connection')
            self._connection = telnetlib.Telnet(self._device_address, self._port)
            self._connection.write(self._device_user + "\n")
            self._connection.write(self._device_password + "\n")
            self._logger.info('Connected')

    def get_resource_description(self, address, command_logger=None):
        """Auto-load function to retrieve all information from the device
        :param address: (str) address attribute from the CloudShell portal
        :param command_logger: logging.Logger instance
        :return: xml.etree.ElementTree.Element instance with all switch sub-resources (blades, ports)
        """
        self._logger = command_logger

        # Step 1. Create root element (switch):
        depth = 0
        # switch_Family = ConfigurationParser.get("driver_variable", "switch_family")
        switch_Model = ConfigurationParser.get("driver_variable", "switch_model")

        # blade_Family = ConfigurationParser.get("driver_variable", "blade_family")
        blade_Model = "Unit"

        # port_Family = ConfigurationParser.get("driver_variable", "port_family")
        port_Model = ConfigurationParser.get("driver_variable", "port_model")

        self._logger.info('switch: %s' % (str(switch_Model)))
        self._logger.info('Patch Panel: %s' % (str(blade_Model)))
        self._logger.info('port: %s' % (str(port_Model)))

        resource_info = ResourceInfo()
        resource_info.set_depth(depth)
        resource_info.set_address(address)
        resource_info.set_index("Rome")
        resource_info.add_attribute("Software Version", "1.0.0")
        resource_info.set_model_name(switch_Model)

        letter = ""

        if 'A' in address:
            letter = "A"
        elif 'B' in address:
            letter = "B"
        else:
            self._logger.error('Resource address should specify MatrixA or MatrixB. Current address: ' + address)
            raise Exception('Resource address should specify MatrixA or MatrixB')

        # Step 2. Create child resources for the root element (blades):
        for blade_no in range(1, 2):
            blade_resource = ResourceInfo()
            blade_resource.set_depth(depth + 1)
            blade_resource.set_index(str(blade_no))
            blade_resource.set_model_name(blade_Model)
            blade_resource.set_address(address + ":" + ("Matrix%s" % letter))
            resource_info.add_child(blade_no, blade_resource)

            # Step 3. Create child resources for each root sub-resource (ports in blades)
            if letter is "A":
                for port_no in range(1, 129):
                    port_resource = ResourceInfo()
                    port_resource.set_depth(depth + 2)
                    port_resource.set_index(str(port_no).zfill(3))
                    port_resource.set_model_name(port_Model)
                    blade_resource.add_child(port_no, port_resource)
            elif letter is "B":
                for port_no in range(129, 257):
                    port_resource = ResourceInfo()
                    port_resource.set_depth(depth + 2)
                    port_resource.set_index(str(port_no).zfill(3))
                    port_resource.set_model_name(port_Model)
                    blade_resource.add_child(port_no, port_resource)

        return resource_info.convert_to_xml()

    def map_bidi(self, src_port, dst_port, command_logger):
        """Create a bidirectional connection between source and destination ports
        :param src_port: (list) source port in format ["<address>", "<blade>", "<port>"]
        :param dst_port: (list) destination port in format ["<address>", "<blade>", "<port>"]
        :param command_logger: logging.Logger instance
        :return: None
        """
        # Collect port info
        self._logger = command_logger
        self._create_connection()

        port1 = src_port[2].lstrip("0")
        port2 = dst_port[2].lstrip("0")
        self._logger.info('Creating Duplex e%s to w%s' % (port1, port2))

        # Attempt to create a duplex connection
        try:
            command1 = "con cr e%s t w%s" % (port1, port2)
            command2 = "con cr e%s t w%s" % (port2, port1)
            self._logger.info("First Connection Create Initiated")
            self._connection.write(command1 + " \n")
            message = self._connection.expect(['CONNECTION OPERATION SUCCEEDED',
                                               'CONNECTION OPERATION SKIPPED(already done)',
                                               ' FAILED'], self._command_timeout)
            if message[0] == 0 or message[0] == 1:
                self._logger.info("Second Connection Create Initiated")
                self._connection.write(command2 + " \n")
                message = self._connection.expect(['CONNECTION OPERATION SUCCEEDED',
                                                   'CONNECTION OPERATION SKIPPED(already done)',
                                                   ' FAILED'], self._command_timeout)
                if message[0] == 0 or message[0] == 1:
                    self._logger.info("Connection Create Ended")
                else:
                    self._logger.info("Unable to Create Second Connection")
                    self._logger.info("Disconnecting the First Connection")
                    command = "con di e%s from w%s" % (port1, port2)
                    self._connection.write(command + "\n")
                    message1 = self._connection.expect(['CONNECTION OPERATION SUCCEEDED',
                                                       'CONNECTION OPERATION SKIPPED(already done)',
                                                       ' FAILED'], self._command_timeout)
                    if message1[0] == 0 or message1[0] == 1:
                        self._logger.info("First Connection Disconnection Successful")
                        raise Exception('Failed during the second connection creation:' + message[2])
                    else:
                        raise Exception('Failed during the first disconnect:' + message[2])
            else:
                raise Exception('Failed during the first connection creation:' + message[2])

        except Exception as ex:
            self._logger.error('Connection error: ' + ex.message)
            raise Exception('Unable to create connection, please contact the admin')

    def map_uni(self, src_port, dst_port, command_logger):
        """Create a unidirectional connection between source and destination ports
        :param src_port: (list) source port in format ["<address>", "<blade>", "<port>"]
        :param dst_port: (list) destination port in format ["<address>", "<blade>", "<port>"]
        :param command_logger: logging.Logger instance
        :return: None
        """
        self._logger = command_logger
        self._create_connection()

        # Collect information for a simplex disconnection command
        # Collect port information
        port1 = src_port[2].lstrip("0")
        port2 = dst_port[2].lstrip("0")
        self._logger.info('Creating Simplex e%s to w%s' % (port1, port2))

        # Create a simplex connection
        try:
            self._logger.info("Connection Create Initiated")
            command = "con cr e%s t w%s" % (port1, port2)
            self._connection.write(command + "\n")
            # self._logger.info(self._connection.read_until('CONNECTION OPERATION SUCCEEDED ',30))
            message = self._connection.expect(['CONNECTION OPERATION SUCCEEDED',
                                               'CONNECTION OPERATION SKIPPED(already done)',
                                               ' FAILED'], self._command_timeout)
            if message[0] == 0 or message[0] == 1:
                self._logger.info("Connection Creation Successful")
                self._logger.info("Connection Create Ended")
            else:
                raise Exception('Failed to cross-connect.')
            # validate connection success (via the cli), until then, sleep to have more-real-life feedback to the user
        except Exception as ex:
            self._logger.error('Connection error: ' + ex.message)
            raise Exception('Unable to create connection, please contact the admin')

    def map_clear_to(self, src_port, dst_port, command_logger):
        """Remove simplex connection ending on the destination port
        :param src_port: (list) source port in format ["<address>", "<blade>", "<port>"]
        :param dst_port: (list) destination port in format ["<address>", "<blade>", "<port>"]
        :param command_logger: logging.Logger instance
        :return: None
        """
        self._logger = command_logger
        self._create_connection()

        # Collect Port range information
        port1 = src_port[2].lstrip("0")
        port2 = dst_port[2].lstrip("0")

        # Initiate a disconnect range command
        try:
            self._logger.info("Connection Disconnection Initiated")
            self._logger.info("Disconnecting e%s from w%s" % (port1, port2))
            command = "con di e%s from w%s" % (port1, port2)
            self._connection.write(command + "\n")
            message = self._connection.expect(['CONNECTION OPERATION SUCCEEDED',
                                               'CONNECTION OPERATION SKIPPED(already done)',
                                               ' FAILED'], self._command_timeout)
            if message[0] == 0 or message[0] == 1:
                self._logger.info("Connection Disconnection Successful")
            else:
                raise Exception('Failed to Disconnect.')
            #self._logger.info("Disconnect Command Sent: %s" % command)
            # validate connection success (via the cli), until then, sleep to have more-real-life feedback to the user


        except Exception as ex:
            self._logger.error('Connection error: ' + ex.message)
            raise Exception('Unable to clear connection ')

    def map_clear(self, src_port, dst_port, command_logger):
        """Remove simplex/multi-cast/duplex connection ending on the destination port
        :param src_port: (list) source port in format ["<address>", "<blade>", "<port>"]
        :param dst_port: (list) destination port in format ["<address>", "<blade>", "<port>"]
        :param command_logger: logging.Logger instance
        :return: None
        """
        self._logger = command_logger
        self._create_connection()

        # Collect information for a simplex disconnection command
        port1 = src_port[2].lstrip("0")
        port2 = dst_port[2].lstrip("0")

        # Initiate Disconnection Command
        try:
            command1 = "con di e%s f w%s" % (port1, port2)
            command2 = "con di e%s f w%s" % (port2, port1)
            self._logger.info("Connection Disconnection Initiated")
            self._logger.info("Disconnecting e%s from w%s" % (port1, port2))
            self._connection.write(command1 + " \n")
            self._logger.info("Disconnecting e%s from w%s" % (port2, port1))
            self._connection.write(command2 + " \n")
            # validate connection success (via the cli), until then, sleep to have more-real-life feedback to the user
            time.sleep(40)
            self._logger.info("Connection Disconnection Ended")

        except Exception as ex:
            self._logger.error('Connection error: ' + ex.message)
            raise Exception('Unable to clear connection ')

    # Unused Method
    def set_speed_manual(self, command_logger):
        """Set speed manual - skipped command
        :param command_logger: logging.Logger instance
        :return: None
        """
        pass
