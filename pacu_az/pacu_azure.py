import subprocess
import json
import sys

class PacuAzure():
    def __init__(self):
        self.COMMANDS = ['whoami', 'exit', 'quit', 'dump_ad_users', 'dump_storage_accounts']

    def whoami(self):
        result = subprocess.run(['az', 'account', 'show'], capture_output=True, text=True)
        account_info = json.loads(result.stdout)
        print(f"User: {account_info['user']['name']}")
    
    def dump_ad_users(self):
        try:
            result = subprocess.run(['az', 'ad', 'user', 'list'], capture_output=True, text=True, check=True)
            users = json.loads(result.stdout)
            if len(users) > 0:
                print('\nUsers:')
                print('-' * 10)
                for user in users:
                    print(user['userPrincipalName'])
                print('-' * 10 + '\n')
            else:
                print("No users found.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to retrieve users. Error: {e.stderr.strip()}")
        except json.JSONDecodeError:
            print("Failed to parse the user data. The output may not be in JSON format.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def dump_storage_accounts(self):
        result = subprocess.run(['az', 'storage', 'account', 'list'], capture_output=True, text=True, check=True)
        accounts = json.loads(result.stdout)
        if len(accounts) > 0:
            print('\nStorage Accounts:')
            print('-' * 10)
            for account in accounts:
                print(account['name'])
            print('-' * 10 + '\n')
        else:
            print("No storage accounts found.")

    def exit(self) -> None:
        sys.exit('\nLater Nerd!')


    def parse_command(self, command):
        if command == "whoami":
            self.whoami()
        elif command == "dump_ad_users":
            self.dump_ad_users()
        elif command == "dump_storage_accounts":
            self.dump_storage_accounts()
        elif command == "exit" or command == "quit":
            self.exit()
