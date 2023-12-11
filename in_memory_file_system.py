import json
import os
import shutil

class InMemoryFileSystem:
    def __init__(self):
        self.current_directory = '/'
        self.file_system = {'/': {}}

    def create_directory(self, path):
        path = os.path.join(self.current_directory, path)
        if path not in self.file_system:
            self.file_system[path] = {}
            print(f"Directory '{path}' created.")
        else:
            print(f"Directory '{path}' already exists.")

    def change_directory(self, path):
        if path == '..':
            path = os.path.dirname(self.current_directory)
        elif path.startswith('/'):
            path = path
        else:
            path = os.path.join(self.current_directory, path)

        if path in self.file_system and isinstance(self.file_system[path], dict):
            self.current_directory = path
            print(f"Current directory changed to '{path}'.")
        else:
            print(f"Directory '{path}' not found.")

    def list_directory(self, path='.'):
        path = os.path.join(self.current_directory, path)
        if path in self.file_system and isinstance(self.file_system[path], dict):
            contents = ', '.join(self.file_system[path].keys())
            print(f"Contents of '{path}': {contents}")
        else:
            print(f"Directory '{path}' not found.")

    def create_file(self, path):
        path = os.path.join(self.current_directory, path)
        if path not in self.file_system:
            self.file_system[path] = ""
            print(f"File '{path}' created.")
        else:
            print(f"File '{path}' already exists.")

    def write_to_file(self, path, content):
        path = os.path.join(self.current_directory, path)
        if path in self.file_system and isinstance(self.file_system[path], str):
            self.file_system[path] = content
            print(f"Content written to '{path}'.")
        else:
            print(f"File '{path}' not found.")

    def display_file_content(self, path):
        path = os.path.join(self.current_directory, path)
        if path in self.file_system and isinstance(self.file_system[path], str):
            print(f"Content of '{path}': {self.file_system[path]}")
        else:
            print(f"File '{path}' not found.")

    def move_file_or_directory(self, source, destination):
        source = os.path.join(self.current_directory, source)
        destination = os.path.join(self.current_directory, destination)

        if source in self.file_system:
            shutil.move(source, destination)
            print(f"Moved '{source}' to '{destination}'.")
        else:
            print(f"Source '{source}' not found.")

    def copy_file_or_directory(self, source, destination):
        source = os.path.join(self.current_directory, source)
        destination = os.path.join(self.current_directory, destination)

        if source in self.file_system:
            if isinstance(self.file_system[source], dict):
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)
            print(f"Copied '{source}' to '{destination}'.")
        else:
            print(f"Source '{source}' not found.")

    def remove_file_or_directory(self, path):
        path = os.path.join(self.current_directory, path)

        if path in self.file_system:
            if isinstance(self.file_system[path], dict):
                shutil.rmtree(path)
            else:
                os.remove(path)
            print(f"Removed '{path}'.")
        else:
            print(f"File or directory '{path}' not found.")

    def save_state(self, path):
        with open(path, 'w') as file:
            json.dump(self.file_system, file)
        print(f"File system state saved to '{path}'.")

    def load_state(self, path):
        with open(path, 'r') as file:
            self.file_system = json.load(file)
        print(f"File system state loaded from '{path}'.")

def main():
    file_system = InMemoryFileSystem()

    while True:
        command = input(f"{file_system.current_directory} $ ")

        if command.startswith("mkdir"):
            _, path = command.split(" ", 1)
            file_system.create_directory(path)

        elif command.startswith("cd"):
            _, path = command.split(" ", 1)
            file_system.change_directory(path)

        elif command.startswith("ls"):
            _, path = command.split(" ", 1) if len(command.split()) > 1 else (None, '.')
            file_system.list_directory(path)

        elif command.startswith("touch"):
            _, path = command.split(" ", 1)
            file_system.create_file(path)

        elif command.startswith("echo"):
            _, rest = command.split(" ", 1)
            path, content = map(str.strip, rest.split('>'))
            file_system.write_to_file(path, content)

        elif command.startswith("cat"):
            _, path = command.split(" ", 1)
            file_system.display_file_content(path)

        elif command.startswith("mv"):
            _, source, destination = command.split(" ", 2)
            file_system.move_file_or_directory(source, destination)

        elif command.startswith("cp"):
            _, source, destination = command.split(" ", 2)
            file_system.copy_file_or_directory(source, destination)

        elif command.startswith("rm"):
            _, path = command.split(" ", 1)
            file_system.remove_file_or_directory(path)

        elif command.startswith("save_state"):
            _, path = command.split(" ", 1)
            file_system.save_state(path)

        elif command.startswith("load_state"):
            _, path = command.split(" ", 1)
            file_system.load_state(path)

        elif command == "exit":
            break

        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
