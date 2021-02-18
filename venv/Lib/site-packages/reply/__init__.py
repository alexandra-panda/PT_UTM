import argparse
import json
import os
from reply.config_creator import ConfigCreator
from reply.internal_server import Server
parser = argparse.ArgumentParser(description="Test your front-end's calls easily!")
parser.add_argument("--standalone", "-s", help="Outputs a standalone .py server", action="store_true")
parser.add_argument("command", help="Use 'make' to create config file. Use 'run' to run server.", choices=["make", "run"])
parser.add_argument("configfile",
                    help="Configuration file")
args = parser.parse_args()
current_dir = os.path.dirname(os.path.realpath(__file__))

if args.command == "make":
    if args.standalone:
        config = ConfigCreator.create_config_json()
        if config:
            with open(current_dir+"/server_template.py", "r") as template:
                server_template = template.read()
                server_template = server_template.replace("8081", config['port'])
                url_map = {}
                for endpoint in config['endpoints']:
                    url_map[endpoint['url']] = endpoint['response']
                server_template = server_template.replace("get_url_map = {}", "get_url_map = "+json.dumps(url_map))

                with open(args.configfile.split(".")[0]+".py", "w") as server_file:
                    server_file.write(server_template)
                    print("Created", args.configfile+".py", "standalone server")
                    print("Done!")
    else:
        config = ConfigCreator.create_config_json()
        if config:
            with open(args.configfile.split(".")[0]+".json", "w") as f:
                json.dump(config, f, indent=4)
                print("Done!")
else:
    try:
        with open(args.configfile, "r") as config_file:
            config = json.load(config_file)
        if "port" in config and "endpoints" in config:
            Server(config['port'], config['endpoints']).run()
        else:
            print("Invalid config file.")
    except json.JSONDecodeError:
        print("Invalid config file.")