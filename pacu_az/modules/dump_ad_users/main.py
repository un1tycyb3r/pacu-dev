import subprocess
import json



module_info = {
    'name': 'dump_ad_users',
    'author': 'Whit Taylor',
    'category': 'DUMP',
    'one_liner': 'Dumps all users from Azure Active Directory',
    'description': 'This module will dump all users from Azure Active Directory',
    'services': ['Azure Active Directory'],
    'prerequisite_modules': [],
    'external_dependencies': [],
}


def main():
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


main()