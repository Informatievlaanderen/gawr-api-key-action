#!/usr/bin/python3
"""
Usage: 
    gawr.py [-h | --help] [--version]
            <command> [<args>...]

The most commonly used gawr commands are:
   add        create new api key
   remove     remove api key
   update     update update api key
"""

import sys
from docopt import docopt
from gawr_types import AddActionArgs, UpdateActionArgs, RemoveActionArgs
from gawr_services import GawrService

if __name__ == '__main__':
    args = docopt(doc=__doc__, version='gawr version 2.0.0',
                  options_first=True)

    print('command arguments:')
    argv = [args['<command>']] + args['<args>']
    if args['<command>'] == 'add':
            import gawr_cmd_add as py
            args = AddActionArgs(docopt(py.__doc__, argv=argv))
            sys.exit(GawrService(args).create_new_api_key())

    elif args['<command>'] == 'update':
            import gawr_cmd_update as py
            args = UpdateActionArgs(docopt(py.__doc__, argv=argv))
            sys.exit(GawrService(args).update_api_key())

    elif args['<command>'] == 'remove':
            import gawr_cmd_remove as py
            args = RemoveActionArgs(docopt(py.__doc__, argv=argv))
            sys.exit(GawrService(args).delete_api_key())

    else:
        exit("%r is not a gawr.py command. See 'gawr help'." % args['<command>'])