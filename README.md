# LibLocator: Intelligent Python Dependency Organizer

## Overview

**LibLocator** is an innovative script, with its initial codebase generated with the assistance of ChatGPT, designed to streamline the management of Python project dependencies. It meticulously scans your Python project, targeting the src/ and test/ directories, to intelligently categorize dependencies into requirements.txt, test-requirements.txt, and dev-requirements.txt. This tool is perfect for developers looking to enhance code clarity and reduce unnecessary bloat in their projects.

## Key Features

- **Automated Dependency Categorization**: Automatically sorts dependencies into appropriate categories based on their usage in different parts of your code.
- **Precision Scanning**: Identifies which dependencies are actively used in your project's src/ and test/ directories.
- **Hyphen-to-Underscore Conversion**: Adapts to Python’s naming conventions for accurate identification of libraries.
- **Argparse Integration**: Allows users to specify their project directory using the -f flag for a user-friendly experience.
- **Clean and Maintainable Codebases**: Helps maintain a lean, efficient, and more maintainable codebase by sorting and removing unused libraries.

## Installation
To install LibLocator, simply clone the repository to your local machine:

```bash
Copy code
git clone https://github.com/christopherhagler/LibLocator.git
cd LibLocator
```
Ensure that you have Python installed on your system. LibLocator is compatible with Python 3.x.

Usage

Navigate to the directory containing LibLocator and run the script:

```bash
python liblocator.py -f /path/to/your/codebase
```
Replace /path/to/your/codebase with the actual path to your Python project.

## How It Works

LibLocator works by scanning the specified codebase directory, identifying the libraries used in the src and test directories. It then categorizes these libraries into requirements.txt, test-requirements.txt, or dev-requirements.txt based on their usage.

## Contributing

Contributions to LibLocator are welcome! If you have suggestions for improvements or bug fixes, feel free to:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes and commit them (git commit -am 'Add some feature').
Push to the branch (git push origin feature-branch).
Create a new Pull Request.
Acknowledgements

This code was initially generated with the assistance of ChatGPT, an AI developed by OpenAI.
License

This project is licensed under the MIT License - see the LICENSE.md file for details.
