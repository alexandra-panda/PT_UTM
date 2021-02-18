import os
import json

class ConfigCreator:

    @staticmethod
    def create_config_json():
        print("----Welcome to Reply!----")

        server_info = {}
        print("In which port do you want the server to run on?")
        port = input("> ")

        server_info['port'] = port
        server_info['endpoints'] = []

        print("\tLet's add some endpoints:\n")

        option = "y"

        while option == "y":
            while option == "y":
                print("Enter endpoint's relative url (/for/example):")
                url = input("> ")
                print("Enter example response ({status: \"connected\"}):")
                response = input("> ")
                server_info['endpoints'].append({'url': url, 'response': response})
                print("\n\nWanna add another one? (y/n)")
                option = ""
                while option not in ["y", "n"]:
                    option = input("> ").lower()

            print("Alright, so here are your endpoints: \n")
            for endpoint in server_info['endpoints']:
                print("\tUrl:", endpoint['url'])
                print("\tResponse:", endpoint['response'])
                print("\t----------------------------------\n")

            print("\n\nOn port", port)
            print("\nIs that correct? (y/n)")
            option = ""
            while option not in ["y", "n"]:
                option = input("> ").lower()
            if option == "y":
                return server_info
            else:
                return False