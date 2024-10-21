import logging
import os
import re

# Configure logging
log_filename = "file_management.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Dictionary of the file types
file_type_ext = {
    "Documents": [".txt", ".pdf", ".docx", ".doc", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Pictures": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg"],
    "Videos": [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Code": [".py", ".java", ".cpp", ".c", ".js", ".html", ".css", ".php"],
    "Executables": [".exe", ".bat", ".sh", ".bin"]
}


# Used to create a Confirm Dialog with Yes or No Option
def confirm_dialog(dialog: str):
    cont = 'a'  # Init opt
    valid_opt = ['y', 'n']  # Valid options

    # It will keep asking unless it gets a valid answer
    while cont not in valid_opt:
        cont = input(f"{dialog} ([Y]es/[N]o): ")
        if cont.lower() == 'y':
            logging.info(f"{dialog} [Y]es")
            return True
        elif cont.lower() == 'n':
            logging.info(f"{dialog} [N]o")
            return False
        else:
            print(f"[{cont}] is an invalid response!")


# Used to create an Option Dialog with multiple options
def option_dialog(dialog: str, options: list):
    print(dialog)
    while True:
        input_opt = input("Select options: ")
        if input_opt.isdigit():
            if int(input_opt) in options:
                return int(input_opt)
            else:
                print(f"[{input_opt}] is an invalid option!")
        else:
            print(f"[{input_opt}] is an invalid option!")


# It checks if the path is valid, and then it turns it into an absolute path if not
def check_work_path(path: str):
    if not os.path.exists(path):
        return "Invalid"

    if os.path.isabs(path):
        return path

    abs_path = os.path.abspath(path)
    return abs_path


# It counts the number of files in the source directory
def count_total_file(directory: str):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    no_of_files = len(files)
    logging.info("Total number of files: {}".format(no_of_files))
    return no_of_files


# It counts the different file types on the source directory based on the dictionary
def count_file_type(directory: str):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]  # Gets the list of files
    file_type_count = {}  # Stores the count

    # Creates an item pair in the dictionary for the count per filetype
    for category in file_type_ext.keys():
        file_type_count[category] = 0
    file_type_count["Others"] = 0

    # Counts the filetype
    for file in files:
        found = False
        pattern = r"\.\w+$"
        ext = re.search(pattern, file)  # Gets the file extension

        # Determine what filetype it belongs then increment the counter for the said filetype
        if ext is not None:
            for category, extensions in file_type_ext.items():
                if ext[0] in extensions:
                    file_type_count[category] += 1
                    found = True
                    break

        # If the filetype was not found in the dictionary then it belongs in Others
        if not found:
            file_type_count["Others"] += 1

    logging.info(file_type_count)
    return file_type_count


# Prints the filetype count summary
def print_summary(directory: str):
    border_line = "|-------------------------------------------|"
    total_no_files = count_total_file(directory)
    print(border_line)
    print("Total number of files: {}".format(total_no_files))
    for category, count in count_file_type(directory).items():
        print("{:>15}: {}".format(category, count))
    print(border_line)
