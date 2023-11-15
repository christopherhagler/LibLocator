import os
import re
import argparse
from tabulate import tabulate

# Function to locate requirements.txt in the codebase
def find_requirements_file(codebase_path):
    for root, dirs, files in os.walk(codebase_path):
        if 'requirements.txt' in files:
            return os.path.join(root, 'requirements.txt')
    return None

# Function to extract just the library name and version from a requirements.txt line for import check
def extract_library_name_and_version(line):
    # List of possible specifiers
    specifiers = ['==', '>=', '<=', '>', '<', '~=']
    
    # Check if line contains any of the specifiers and split accordingly
    for specifier in specifiers:
        if specifier in line:
            lib_name, version = line.split(specifier, 1)
            return lib_name.strip(), specifier + version.strip()
    
    # If no specifier is found, return the entire line as the library name and an empty string for version
    return line.strip(), ''

# Function to check if a library is used in a specific directory and log the usage
def log_library_usage(library, directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    for line in f:
                        if re.search(rf'\bimport {library}\b|\bfrom {library} import\b', line):
                            return True
    return False

def main(codebase_path, dry_run):
    requirements_path = find_requirements_file(codebase_path)
    if not requirements_path:
        print("requirements.txt not found in the provided path.")
        return

    src_path = os.path.join(codebase_path, 'src')
    test_path = os.path.join(codebase_path, 'test')

    with open(requirements_path, 'r') as file:
        libraries = file.readlines()

    libraries_status = []

    for line in libraries:
        line = line.strip()
        if not line or line.startswith('#'):  # Skip empty lines and comments
            continue

        lib_name, version = extract_library_name_and_version(line)
        used_in_src = log_library_usage(lib_name, src_path)
        used_in_test = log_library_usage(lib_name, test_path)

        if used_in_src:
            usage = 'src'
            dest_file = 'requirements.txt'
        elif used_in_test:
            usage = 'test'
            dest_file = 'test-requirements.txt'
        else:
            usage = 'dev'
            dest_file = 'dev-requirements.txt'

        libraries_status.append([lib_name, version, usage, dest_file])

    # Displaying the table
    print(tabulate(libraries_status, headers=['Library', 'Version', 'Usage', 'Requirements File']))

    # Rest of the script remains the same...
    # Handling dry run
    if dry_run:
        print("Dry run enabled. The following changes would be made:")
        print("requirements.txt:", [lib[0] for lib in libraries_status if lib[3] == 'requirements.txt'])
        print("test-requirements.txt:", [lib[0] for lib in libraries_status if lib[3] == 'test-requirements.txt'])
        print("dev-requirements.txt:", [lib[0] for lib in libraries_status if lib[3] == 'dev-requirements.txt'])
        return

    # Writing to different requirements files based on usage
    with open(requirements_path, 'w') as req_file, \
         open(os.path.join(codebase_path, 'test-requirements.txt'), 'w') as test_req_file, \
         open(os.path.join(codebase_path, 'dev-requirements.txt'), 'w') as dev_req_file:

        for line in libraries_status:
            if line[3] == 'requirements.txt':
                req_file.write(line[0] + '==' + line[1] + '\n')
            elif line[3] == 'test-requirements.txt':
                test_req_file.write(line[0] + '==' + line[1] + '\n')
            elif line[3] == 'dev-requirements.txt':
                dev_req_file.write(line[0] + '==' + line[1] + '\n')

    print("Updated requirements files based on usage.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Categorize dependencies based on usage in src and test directories.")
    parser.add_argument('-f', '--folder', required=True, help="Path to the codebase folder.")
    parser.add_argument('-m', '--dry-run', action='store_true', help="Perform a dry run without making actual changes.")
    args = parser.parse_args()

    main(args.folder, args.dry_run)
