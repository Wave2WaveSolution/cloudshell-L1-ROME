from common.driver_handler_base import DriverHandlerBase
from common.configuration_parser import ConfigurationParser
from common.resource_info import ResourceInfo
from cloudshell.core.logger.qs_logger import get_qs_logger

import telnetlib

"""
Created by: Hezekiah Valdez
Date: 7/31/17
Driver for the ROME. Connection commands should be sent to the machine after these methods are called.
"""


class RomeDriverHandler(DriverHandlerBase):
    def __init__(self):
        DriverHandlerBase.__init__(self)
        self._switch_model = "Rome"
        self._blade_model = "Rome Patch Panel"
        self._port_model = "Rome Port"

        self._driver_name = ConfigurationParser.get("common_variable", "driver_name")

        self._logger = None

    def login(self, address, username="SuperUser", password="superuser", command_logger=None):
        # Get port
        self._port = ConfigurationParser.get("common_variable", "connection_port")

        # Print out device login information
        self._logger = command_logger
        self._logger.info('Attempting to Conenct')
        self._logger.info('Device address is: ' + str(address))
        self._logger.info('Username: ' + str(username))
        self._logger.info('Device Prompt: ' + str(self._prompt))

        # Create Telnet session
        """
        Attempt 2 Using _session
        Not working
        self._logger.info('Attempting to create a Telnet session')
        self._session.connect(address, username, password, port = self._port, re_string=self._prompt)
        self._logger.info('Connection Created')
        """

        # Attempt 1 using telnet
        self._logger.info('Creating Telnet Connection')
        self.connection = telnetlib.Telnet(address)
        self.connection.write(username + "\n")
        self.connection.write(password + "\n")
        self._logger.info('Connected')

    def get_resource_description(self, address, command_logger=None):
        """Auto-load function to retrieve all information from the device

        :param address: (str) address attribute from the CloudShell portal
        :param command_logger: logging.Logger instance
        :return: xml.etree.ElementTree.Element instance with all switch sub-resources (blades, ports)

        """

        self._logger = command_logger

        # Attempt 3

        # Step 1. Create root element (switch):
        depth = 0
        # switch_Family = ConfigurationParser.get("driver_variable", "switch_family")
        switch_Model = ConfigurationParser.get("driver_variable", "switch_model")

        # blade_Family = ConfigurationParser.get("driver_variable", "blade_family")
        blade_Model = "Unit"

        # port_Family = ConfigurationParser.get("driver_variable", "port_family")
        port_Model = ConfigurationParser.get("driver_variable", "port_model")

        self._logger.info('switch: %s' % (str(switch_Model)))
        self._logger.info('(Patch Panel: %s' % (str(blade_Model)))
        self._logger.info('port: %s' % (str(port_Model)))

        resource_info = ResourceInfo()
        resource_info.set_depth(depth)
        resource_info.set_address(address)
        resource_info.set_index("Rome")
        resource_info.add_attribute("Software Version", "1.0.0")
        resource_info.set_model_name(switch_Model)

        # Step 2. Create child resources for the root element (blades):
        for blade_no in range(1, 3):
            blade_resource = ResourceInfo()
            blade_resource.set_depth(depth + 1)
            blade_resource.set_index(str(blade_no))
            blade_resource.set_model_name(blade_Model)
            resource_info.add_child(blade_no, blade_resource)

            # Step 3. Create child resources for each root sub-resource (ports in blades)
            for port_no in range(1, 129):
                if blade_no == 2:
                    port_no += 128
                port_resource = ResourceInfo()
                port_resource.set_depth(depth + 2)
                port_resource.set_index(str(port_no).zfill(3))
                port_resource.set_model_name(port_Model)
                blade_resource.add_child(port_no, port_resource)

        self._logger.info('switch: %s' % (str(vars(resource_info))))

        # for num in range(1,256):
        #
        #    east_port = "e" + str(num)
        #    west_port = "w" + str(num)

        return resource_info.convert_to_xml()

    def map_bidi(self, src_port, dst_port, command_logger):
        """Create a bidirectional connection between source and destination ports

        :param src_port: (list) source port in format ["<address>", "<blade>", "<port>"]
        :param dst_port: (list) destination port in format ["<address>", "<blade>", "<port>"]
        :param command_logger: logging.Logger instance
        :return: None

        Example:
        error_map = OrderedDict([
            ("error|ERROR", "Failed to perform command"),
        ])
        """
        # Collect port info
        self._logger = command_logger
        port1 = src_port[2].lstrip("0")
        port2 = dst_port[2].lstrip("0")
        self._logger.info('Creating Duplex e%s to w%s' % (port1, port2))

        # Attempt to create a duplex connection
        try:

            command1 = "con cr e%s t w%s" % (port1, port2)
            command2 = "con cr e%s t w%s" % (port2, port1)
            self.connection.write(command1 + " \n")
            self.connection.write(command2 + " \n")
            self._logger.info("Connection Create Initiated")
            self.connection.close()
            self._logger.info("Telnet Connection Closed")

        except BaseException:
            self._logger.info('Connection error')

    def map_uni(self, src_port, dst_port, command_logger):
        """Create a unidirectional connection between source and destination ports

        :param src_port: (list) source port in format ["<address>", "<blade>", "<port>"]
        :param dst_port: (list) destination port in format ["<address>", "<blade>", "<port>"]
        :param command_logger: logging.Logger instance
        :return: None

        Example:
        error_map = OrderedDict([
            ("error|ERROR", "Failed to perform command"),
        ])
        command = "connect simplex {} to {}".format(src_port, dst_port)
        self._session.send_command(command, re_string=self._prompt, error_map=error_map)
        """
        self._logger = command_logger

        # Collect port information
        port1 = src_port[2]
        port2 = dst_port[2]
        self._logger.info('Creating Simplex e%s to w%s' % (port1, port2))

        # Create a simplex connection
        try:
            command = "con cr e%s t w%s" % (port1, port2)
            self.connection.write(command + "\n")
            self._logger.info("Connection Create Initiated")
            self.connection.close()
            self._logger.info("Telnet Connection Closed")
        except BaseException:
            self._logger.info('Connection error')


    def map_clear_to(self, src_port, dst_port, command_logger):
        """Remove simplex/multi-cast/duplex connection ending on the destination port

        :param src_port: (list) source port in format ["<address>", "<blade>", "<port>"]
        :param dst_port: (list) destination port in format ["<address>", "<blade>", "<port>"]
        :param command_logger: logging.Logger instance
        :return: None

        Example:
        error_map = OrderedDict([
            ("error|ERROR", "Failed to perform command"),
        ])
        command = "disconnect simplex {} from {}".format(src_port, dst_port)
        self._session.send_command(command, re_string=self._prompt, error_map=error_map)
        """
        self._logger = command_logger

        # Collect Port range information
        start_port = src_port[2].lstrip("0")
        end_port = dst_port[2].lstrip("0")
        self._logger.info("Disconnection Range Initiated")

        # Initiate a disconnect range command
        command = "con di range w%s t w%s" % (start_port, end_port)
        yes_command = "y \n"

        try:
            self.connection.write(command + "\n")
            self._logger.info("Disconnect Command Sent %s" % command)
            self.connection.write(yes_command)
            self._logger.info("%s Sent" % yes_command)
            self.connection.close()
            self._logger.info("Telnet Connection Closed")
        except BaseException:
            self._logger.info('Connection error')

    def map_clear(self, src_port, dst_port, command_logger):
        """Remove simplex/multi-cast/duplex connection ending on the destination port

        :param src_port: (list) source port in format ["<address>", "<blade>", "<port>"]
        :param dst_port: (list) destination port in format ["<address>", "<blade>", "<port>"]
        :param command_logger: logging.Logger instance
        :return: None

        Example:
        error_map = OrderedDict([
            ("error|ERROR", "Failed to perform command"),
        ])
        command = "disconnect duplex {} from {}".format(src_port, dst_port)
        self._session.send_command(command, re_string=self._prompt, error_map=error_map)
        """
        self._logger = command_logger

        # Collect information for a simplex disconnection command
        port1 = src_port[2].lstrip("0")
        port2 = dst_port[2].lstrip("0")
        self._logger.info("Disconnecting e%s from w%s" % (port1, port2))
        command = "con di e%s f w%s" % (port1, port2)

        # Initiate Disconnection Command
        try:
            self.connection.write(command + "\n")
            self._logger.info("Connection Disconnection Initiated")
            self.connection.close()
            self._logger.info("Telnet Connection Closed")
        except BaseException:
            self._logger.info('Connection error')

    # Unused Method
    def set_speed_manual(self, command_logger):
        """Set speed manual - skipped command

        :param command_logger: logging.Logger instance
        :return: None
        """
        pass
