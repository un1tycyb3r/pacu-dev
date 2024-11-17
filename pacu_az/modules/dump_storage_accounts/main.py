import subprocess
import json

module_info = {
    'name': 'dump_ad_users',
    'author': 'Whit Taylor',
    'category': 'DUMP',
    'one_liner': 'Dumps all storage accounts',
    'description': 'This module will dump all storage accounts',
    'services': ['Azure Storage'],
    'prerequisite_modules': [],
    'external_dependencies': [],
}

def is_json(string):
    try:
        json.loads(string)
        return True
    except ValueError:
        return False

def main():
    print("Running dump_storage_accounts module")
    result = subprocess.run(['az', 'storage', 'account', 'list'], capture_output=True, text=True, check=True)
    if is_json(result.stdout):
        accounts = json.loads(result.stdout)
    else:
        accounts = result.stdout.split('\n')
    if len(accounts) > 0:
        print('\nStorage Accounts:')
        print('-' * 10)
        for account in accounts:
            print(account['name'])
        print('-' * 10 + '\n')
    else:
        print("No storage accounts found.")