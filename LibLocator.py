import os
import re
import argparse

# Function to locate requirements.txt in the codebase
def find_requirements_file(codebase_path):
    for root, dirs, files in os.walk(codebase_path):
        if 'requirements.txt' in files:
            return os.path.join(root, 'requirements.txt')
    return None

# Function to extract just the library name from a requirements.txt line and replace hyphens with underscores
def extract_library_name(line):
    for specifier in ['==', '>=', '<=', '>', '<', '~=']:
        if specifier in line:
            lib_name = line.split(specifier)[0].strip()
            return lib_name.replace('-', '_')
    return line.strip().replace('-', '_')

# Function to check if a library is used in a specific directory
def is_library_used(library, directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    contents = f.read()
                    if re.search(rf'\bimport {library}\b|\bfrom {library} import\b', contents):
                        return True
    return False

def main(codebase_path):
    requirements_path = find_requirements_file(codebase_path)
    if not requirements_path:
        print("requirements.txt not found in the provided path.")
        return

    src_path = os.path.join(codebase_path, 'src')
    test_path = os.path.join(codebase_path, 'test')

    with open(requirements_path, 'r') as file:
        libraries = file.readlines()

    libraries = [extract_library_name(lib) for lib in libraries]

    src_libraries = set(lib for lib in libraries if is_library_used(lib, src_path))
    test_libraries = set(lib for lib in libraries if is_library_used(lib, test_path))

    # Writing to different requirements files based on usage
    with open(requirements_path, 'w') as req_file, \
         open(os.path.join(codebase_path, 'test-requirements.txt'), 'w') as test_req_file, \
         open(os.path.join(codebase_path, 'dev-requirements.txt'), 'w') as dev_req_file:

        for line in libraries:
            lib_name = extract_library_name(line)
            if lib_name in src_libraries or lib_name in test_libraries:
                req_file.write(line + '\n')
            elif lib_name not in src_libraries and lib_name not in test_libraries:
                dev_req_file.write(line + '\n')

            if lib_name in test_libraries and lib_name not in src_libraries:
                test_req_file.write(line + '\n')

    print("Updated requirements files based on usage.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Categorize dependencies based on usage in src and test directories.")
    parser.add_argument('-f', '--folder', required=True, help="Path to the codebase folder.")
    args = parser.parse_args()

    main(args.folder)