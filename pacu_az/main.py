import sys
import argparse
from pacu_az.pacu_azure import PacuAzure as az
from typing import List, Any
from pacu_az.modules import *
from pathlib import Path
import os
import importlib
import json
import subprocess



class Main():

    def __init__(self):
         self.provider = 'az'
         self.az_instance = az()

    def exec_module(self, command: List[str]) -> None:
        module_name = command[1].lower()
        module = self.import_module_by_name(module_name)

        if module:
            print(f"Module path: {str(Path(__file__).parent/'modules'/module_name/'main.py')}")
            
            if hasattr(module, 'main') and callable(getattr(module, 'main')):
                module.main()  # Call the main function of the module
            else:
                print(f"Module {module_name} does not have a callable 'main' function.")
        else:
            print(f"Module {module_name} not found.")

    def import_module_by_name(self, module_name: str) -> Any:
        file_path = str(Path(__file__).parent/'modules'/module_name/'main.py')
        if os.path.exists(file_path):
            import_path = str(Path('pacu_az/modules')/module_name/'main').replace('/', '.').replace('\\', '.')
            module = __import__(import_path, globals(), locals(), ['main'], 0)
            importlib.reload(module)
            return module
        return None
    
    def list_modules(self) -> None:
        """List all available modules."""
        modules_path = Path(__file__).parent / 'modules'
        if modules_path.exists() and modules_path.is_dir():
            # List all directories in the modules folder
            module_folders = [d.name for d in modules_path.iterdir() if d.is_dir()]
            if module_folders:
                print("Available modules:")
                for module_name in module_folders:
                    print(f"- {module_name}")
            else:
                print("No modules available.")
        else:
            print("Modules directory does not exist.")
    
    def whoami(self):
        result = subprocess.run(['az', 'account', 'show'], capture_output=True, text=True)
        account_info = json.loads(result.stdout)
        print(f"User: {account_info['user']['name']}")

    def idle(self, provider) -> None:
        command = input('Pacu-'+provider+' > ')
        command_list = command.split()
        self.parse_command(command_list)

        if command_list[0].lower() != "exit" and command_list[0].lower() != "quit":
            self.idle(provider)

    def parse_command(self, command):
        if command[0].lower() == 'run':
            self.exec_module(command)
        elif command[0].lower() == 'list':
            self.list_modules()
        elif command[0].lower() in ["exit", "quit"]:
            self.exit()
        elif command[0].lower() == 'whoami':
            self.whoami()
        elif command[0].lower() in ["list", "ls"]:
            self.list_modules()
        else:
            print("Unknown command.")

    def exit(self) -> None:
        sys.exit('\nLater Nerd!')

    def run_gui(self) -> None:
        self.idle(self.provider)
    
    
    def run(self) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument('--version', action='store_true', help='Show the version number')
        args = parser.parse_args()

        if args.version:
            print(f"Version: {self.get_pacu_version()}")  # Print the version in the desired format
            sys.exit()  # Exit after printing the version

        self.run_gui()  # Proceed to run the GUI



if __name__ == '__main__':
    Main().run()