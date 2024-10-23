# FileManagementPy Script - Version 1.0

**FileManagementPy** is an automation tool designed to streamline file management tasks. It categorizes and organizes files by type, enables batch renaming of multiple files, and provides fast and easy file search functionality. This solution reduces the time spent on repetitive tasks, improving productivity and simplifying complex file management processes.

## Table of Contents
- [Installation and Usage](#installation-and-usage)
- [Features](#features)
  - [MainScript](#1-mainscript)
  - [GeneralFunction](#2-generalfunction)
  - [OrganizeScript](#3-organizescript)
  - [RenameScript](#4-renamescript)
  - [SearchScript](#5-searchscript)
- [Future Updates](#future-updates)
- [Warnings](#warnings)

## Installation and Usage

1. **Download**: Download the entire project and place it in a preferred directory (e.g., Desktop).
2. **Run**: Execute the `MainScript` file to launch the tool. Alternatively, you can run individual script files if desired.
3. **Python Requirement**: Ensure that Python is installed on your system before running any scripts.

## Features

### 1. MainScript

- **Description**: Acts as the main menu for the entire script. From here, you can select which functionality to run.
- **Note**: Simply choose the desired option to execute a specific task, such as organizing, renaming, or searching files.

### 2. GeneralFunction

- **Description**: Contains common utility functions used throughout the scripts.
- **Edit with Caution**: Modifications to this file are not recommended unless you know what you're doing.
- **Customizable File Types**: You can edit the `file_type_ext` dictionary to customize how files are categorized based on their extensions.

### 3. OrganizeScript

- **Description**: Organizes files in the source directory into the destination directory based on their file types.
  
  - **Source Directory**: The folder containing the files to be organized. You can provide either a relative or absolute file path (absolute paths recommended).
  - **Destination Directory**: The folder where the files will be moved and organized. This can be the same as the source directory, if desired.
  - **Directory Summary**: Displays the total number of files and their corresponding file types.
  - **ORGANIZE**: Initiates the file organization process.

### 4. RenameScript

- **Description**: Renames files in the target directory, with both manual and automatic renaming options.

  - **Target Directory**: The folder containing the files to be renamed. Accepts relative or absolute paths.
  - **Directory Summary**: Displays a summary of all files in the target directory and their file types.
  - **Manual Renaming**: Allows you to rename each file individually. To skip a file, leave the input blank and press Enter.
  - **Auto Renaming**: Automatically renames files based on a custom naming pattern.
    - `<fn>`: Original filename
    - `<ft>`: Filetype (3-character extension)
    - `<inc>`: Incremental number
    - **Example**: `sample.txt` → `test_<ft>_<inc>_<fn>` = `test_txt_1_sample.txt`

### 5. SearchScript

- **Description**: Searches for specific files within a directory and its subdirectories.
  
  - **Target Directory**: The folder to search in, accepting both relative and absolute paths.
  - **Directory Summary**: Displays the total number of files and subdirectories.
  - **List All Files**: Lists all files in the directory, including subdirectories.
  - **Search File**: Searches for a specific file in the target directory.

## Future Updates

- **Large File Detection**: A script to identify and delete large files.
- **Additional Features**: Other enhancements planned for future versions.

## Warnings

⚠️ **WARNING: THIS SCRIPT DIRECTLY HANDLES FILES AND CAN RESULT IN DATA LOSS. USE WITH CAUTION!** Always back up important data before running the script, especially when performing batch operations.
