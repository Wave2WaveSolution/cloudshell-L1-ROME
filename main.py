import sys

from common.configuration_parser import ConfigurationParser
from common.helper.system_helper import get_file_folder
from common.server_connection import ServerConnection
from common.request_manager import RequestManager
from common.request_handler import RequestHandler


SERVER_HOST = '0.0.0.0'
SERVER_PORT = 1024


if __name__ == '__main__':
    print 'Argument List: ', str(sys.argv)

    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = SERVER_PORT

    exe_folder_str = get_file_folder(sys.argv[0])
    ConfigurationParser.set_root_folder(exe_folder_str)

    request_handler = RequestHandler()
    request_manager = RequestManager()

    request_manager.bind_command('login', (RequestHandler.login, request_handler))
    request_manager.bind_command('getresourcedescription', (RequestHandler.get_resource_description, request_handler))
    request_manager.bind_command('setstateid', (RequestHandler.set_state_id, request_handler))
    request_manager.bind_command('getstateid', (RequestHandler.get_state_id, request_handler))
    request_manager.bind_command('mapbidi', (RequestHandler.map_bidi, request_handler))
    request_manager.bind_command('mapuni', (RequestHandler.map_uni, request_handler))
    request_manager.bind_command('mapclearto', (RequestHandler.map_clear_to, request_handler))
    request_manager.bind_command('mapclear', (RequestHandler.map_clear, request_handler))
    request_manager.bind_command('setspeedmanual', (RequestHandler.set_speed_manual, request_handler))

    server_connection = ServerConnection(SERVER_HOST, port, request_manager, exe_folder_str)
    server_connection.start_listeninig()
