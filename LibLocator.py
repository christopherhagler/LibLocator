import os
import re
import argparse

# Function to locate requirements.txt in the codebase
def find_requirements_file(codebase_path):
    for root, dirs, files in os.walk(codebase_path):
        if 'requirements.txt' in files:
            return os.path.join(root, 'requirements.txt')
    return None

# Function to extract just the library name from a requirements.txt line for import check
def extract_library_name_for_import(line):
    for specifier in ['==', '>=', '<=', '>', '<', '~=']:
        if specifier in line:
            return line.split(specifier)[0].strip()
    return line.strip()

# Function to check if a library is used in a specific directory and log the usage
def log_library_usage(library, directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    for line in f:
                        if re.search(rf'\bimport {library}\b|\bfrom {library} import\b', line):
                            print(f"Library '{library}' imported in {file_path}")
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

    libraries = [lib.strip() for lib in libraries]

    # Using log_library_usage function with the original line
    src_libraries = set()
    test_libraries = set()
    for line in libraries:
        lib_name = extract_library_name_for_import(line)
        if log_library_usage(lib_name, src_path):
            src_libraries.add(line)
        elif log_library_usage(lib_name, test_path):
            test_libraries.add(line)

    # Handling dry run
    if dry_run:
        print("Dry run enabled. The following changes would be made:")
        print("requirements.txt:", src_libraries)
        print("test-requirements.txt:", test_libraries - src_libraries)
        print("dev-requirements.txt:", set(libraries) - src_libraries - test_libraries)
        return

    # Writing to different requirements files based on usage
    with open(requirements_path, 'w') as req_file, \
         open(os.path.join(codebase_path, 'test-requirements.txt'), 'w') as test_req_file, \
         open(os.path.join(codebase_path, 'dev-requirements.txt'), 'w') as dev_req_file:

        for line in libraries:
            if line in src_libraries:
                req_file.write(line + '\n')
            elif line in test_libraries and line not in src_libraries:
                test_req_file.write(line + '\n')
            elif line not in src_libraries and line not in test_libraries:
                dev_req_file.write(line + '\n')

    print("Updated requirements files based on usage.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Categorize dependencies based on usage in src and test directories.")
    parser.add_argument('-f', '--folder', required=True, help="Path to the codebase folder.")
    parser.add_argument('-m', '--dry-run', action='store_true', help="Perform a dry run without making actual changes.")
    args = parser.parse_args()

    main(args.folder, args.dry_run)
