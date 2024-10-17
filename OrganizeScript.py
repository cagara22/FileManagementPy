import os
import shutil
import re
import logging
import GeneralFunction

# Configure logging
log_filename = "file_management.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Dictionary of the file to be organized
file_type_ext = {
    "Documents": [".txt", ".pdf", ".docx", ".doc", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg"],
    "Videos": [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Code": [".py", ".java", ".cpp", ".c", ".js", ".html", ".css", ".php"],
    "Executables": [".exe", ".bat", ".sh", ".bin"]
}


# It counts the number of files in the source directory
def count_total_file(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    no_of_files = len(files)
    logging.info("Total number of files: {}".format(no_of_files))
    return no_of_files


# It counts the different file types on the source directory based on the dictionary
def count_file_type(directory):
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
def print_summary(directory):
    border_line = "|-------------------------------------------|"
    total_no_files = count_total_file(directory)
    print(border_line)
    print("Total number of files: {}".format(total_no_files))
    for category, count in count_file_type(directory).items():
        print("{:>15}: {}".format(category, count))
    print(border_line)


# Creates the folder where the files will be organized
def create_dir(directory):
    print("!---Creating Folders for each category at {}---!".format(directory))
    folder_list = list(file_type_ext.keys())  # Generate a list of folder names based on the filetype dictionary keys
    folder_list.append("Others")

    # Creates the folder based on the list
    for folder in folder_list:
        folder_path = os.path.join(directory, folder)

        # Checks if the folder already exists, if not then make it
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
            print("Created folder: {}".format(folder))
            logging.info("Created folder: {}".format(folder))
        else:
            print("Folder already exists: {}".format(folder))
            logging.info("Folder already exists: {}".format(folder))


# Checks the free space of the destination directory
def get_free_space(directory):
    usage = shutil.disk_usage(directory)
    return usage.free


# Sanitize the filename from invalid characters
def make_valid_file_name(file_name):
    invalid_chars = '<>:"/\\|?*'

    # Replace all invalid characters with '_'
    for char in invalid_chars:
        file_name = file_name.replace(char, '_')

    # Removes trailing whitespace and '.'
    if file_name.endswith(' ') or file_name.endswith('.'):
        file_name = file_name[:-1]

    # Removes the file extension
    file_name = re.sub(r"\.\w+$", "", file_name)

    return file_name


# Rename a file
def rename_file(dest_folder, extn):
    while True:
        new_file_name = input("Input new file name (exclude file extension):")
        new_file_name = "{}{}".format(make_valid_file_name(new_file_name), extn)

        # Checks if the filename already exists
        if not os.path.exists(os.path.join(dest_folder, new_file_name)):
            return new_file_name
        print("Filename already exist!")


# Moves the files to its respective folders
def move_files(source_dir, destination_dir):
    print("!---Moving Files from {} to {}---!".format(source_dir, destination_dir))
    logging.info("Moving Files from {} to {}".format(source_dir, destination_dir))
    files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]  # File list
    destination_folder = ""  # The folder where the file will be moved to

    # Moving the files
    for file in files:
        source_file = os.path.join(source_dir, file)  # File's filepath
        found = False
        pattern = r"\.\w+$"
        ext = re.search(pattern, file)  # File extension

        # Determine what category it belongs
        for category, extensions in file_type_ext.items():
            if ext[0] in extensions:
                destination_folder = os.path.join(destination_dir, category)  # Determine the folder
                found = True
                break

        # If no category match then it is on others
        if not found:
            destination_folder = os.path.join(destination_dir, "Others")

        file_size = os.path.getsize(source_file)  # Gets the file size
        free_space = get_free_space(destination_dir)  # Gets the free space of the destination directory

        # If the file size is less than the free space then move it
        if file_size < free_space:
            skip_file = False

            # Checks if the file already exists in the folder
            if os.path.exists(os.path.join(destination_folder, file)):

                # Options on what to do
                print("{} already exists on {}".format(file, destination_folder))
                logging.warning("{} already exists on {}".format(file, destination_folder))
                options_list2 = [1, 2, 3]
                dialog3 = "Options: [1-Replace destination file | 2-Rename file | 3-Skip file]"

                opt2 = GeneralFunction.option_dialog(dialog3, options_list2)
                if opt2 == options_list2[0]:
                    # Just replace the destination file
                    print("Replacing {} on {}".format(file, destination_folder))
                    logging.info("Replacing {} on {}".format(file, destination_folder))
                    pass
                elif opt2 == options_list2[1]:
                    # Rename the incoming file
                    prev_file = file
                    file = rename_file(destination_folder, ext[0])
                    print("{} has be renamed to {}".format(prev_file, file))
                    logging.info("{} has be renamed to {}".format(prev_file, file))
                elif opt2 == options_list2[2]:
                    # Skip the file
                    skip_file = True

            if skip_file:
                print("Skipping {}".format(file))
                logging.info("Skipping {}".format(file))
                continue

            destination_file = os.path.join(destination_folder, file)
            shutil.move(source_file, destination_file)
            print("Moving {} to {}".format(file, destination_folder))
            logging.info("Moving {} to {}".format(file, destination_folder))

    print("!---------------------------DONE---------------------------!")


def organize_script():
    print("This is a script for organizing files. It automatically organize all files in a chosen directory.")
    dialog1 = "Do you want to proceed?"
    if GeneralFunction.confirm_dialog(dialog1):

        source_directory = os.path.dirname(os.getcwd())  # Default source directory
        logging.info("Current source directory: {}".format(source_directory))
        destination_directory = os.path.dirname(os.getcwd())  # Default destination directory
        logging.info("Current destination directory: {}".format(destination_directory))
        os.chdir(source_directory)  # Set source as working directory

        opt1 = 1
        option_list1 = [1, 2, 3, 4, 5]
        while opt1 != option_list1[4]:
            print("!--------------------------------------------------------------------------!")
            print("Your source directory: {}".format(source_directory))
            print("Your destination directory: {}".format(destination_directory))
            dialog2 = "Options: [1-Change source dir | 2-Change destination dir | 3-Directory summary | 4-ORGANIZE | 5-Exit]"
            opt1 = GeneralFunction.option_dialog(dialog2, option_list1)
            print("!--------------------------------------------------------------------------!")

            if opt1 == option_list1[0]:

                # Changes the source directory
                new_dir = input("Input source directory (absolute or relative): ")
                new_working_directory = GeneralFunction.check_work_path(new_dir)
                if new_working_directory != "Invalid":
                    source_directory = new_working_directory
                    logging.info("Current source directory: {}".format(source_directory))
                    os.chdir(source_directory)
                    continue
                print("!------PATH DOES NOT EXIST------!")
                logging.warning("PATH DOES NOT EXIST")

            elif opt1 == option_list1[1]:

                # Changes the destination directory
                new_dir = input("Input destination directory (absolute or relative): ")
                new_working_directory = GeneralFunction.check_work_path(new_dir)
                if new_working_directory != "Invalid":
                    destination_directory = new_working_directory
                    logging.info("Current destination directory: {}".format(destination_directory))
                    continue
                print("!------PATH DOES NOT EXIST------!")
                logging.warning("PATH DOES NOT EXIST")

            elif opt1 == option_list1[2]:

                # Prints the directory summary
                print_summary(source_directory)

            elif opt1 == option_list1[3]:

                # Check if user wants to proceed with the operation
                dialog3 = "Do you want to proceed with the operation?"
                if GeneralFunction.confirm_dialog(dialog3):
                    # Creates the folders
                    create_dir(destination_directory)
                    # Move the files to destination directory
                    move_files(source_directory, destination_directory)

            elif opt1 == option_list1[4]:

                # Exit the script
                logging.info("Exiting OrganizeScript!")
                print("Exiting OrganizeScript!")

            else:

                print("!------INVALID OPTION------!")


organize_script()