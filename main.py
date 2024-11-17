import argparse
import sys
from pacu_az.main import Main as az
import pacu



class Main():

    def __init__(self):
        self.cloud_provider = None
        
    
    def set_cloud_provider(self):
        provider = input("Select cloud provider (azure/aws): ").lower()
        if provider in ['azure', 'aws']:
            self.cloud_provider = provider
            if self.cloud_provider == 'azure':
                az().run()
            elif self.cloud_provider == 'aws':
                pacu.Main().run()
        else:
            print("Invalid provider. Please select from azure and aws.")
            self.set_cloud_provider()

    def get_pacu_version(self):
        with open('readme.md', 'r') as file:
            content = file.readline().strip()
            return content

    def run_gui(self) -> None:
        self.set_cloud_provider()
    
    
    def run(self) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument('--version', action='store_true', help='Show the version number')
        args = parser.parse_args()

        if args.version:
            print(f"Version: {self.get_pacu_version()}")  # Print the version in the desired format
            sys.exit()  # Exit after printing the version

        self.run_gui()  # Proceed to run the GUI
    

    

if __name__ == "__main__":
    Main().run()