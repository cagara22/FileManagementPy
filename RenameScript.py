import logging
import os
import re
import GeneralFunction

# Configure logging
log_filename = "file_management.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def make_valid_file_name(file_name: str):
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


def manual_renaming(directory: str):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]  # File list
    removed_files = []  # Removed files due to being overwritten
    total_files = 0
    renamed_files = 0
    skipped_files = 0
    overwritten_files = 0

    # Lopping through all the files
    for file in files:
        if file not in removed_files:
            total_files += 1
            print("!----------------------------------------!")
            print(f"Renaming {file}...")
            logging.info(f"Renaming {file}...")
            pattern = r"(\w+)(\.\w+)"
            file_group = re.search(pattern, file)
            file_ext = file_group.group(2)

            # Rename the files one by one
            while True:
                new_file_name = input("Input new file name (exclude file extension): ")

                # Skip file if empty
                if len(new_file_name) == 0:
                    skipped_files += 1
                    print(f"Skipping {file}...")
                    logging.info(f"Skipping {file}...")
                    break

                new_file = f"{make_valid_file_name(new_file_name)}{file_ext}"

                # Check if filename already exist
                if os.path.exists(os.path.join(directory, new_file)):
                    dialog2 = "Filename already exist! Do you want to overwrite the file?"

                    # Overwrite file
                    if GeneralFunction.confirm_dialog(dialog2):
                        overwritten_files += 1
                        removed_files.append(new_file)
                        os.remove(os.path.join(directory, new_file))
                        os.rename(os.path.join(directory, file), os.path.join(directory, new_file))
                        print(f"Overwriting {new_file}...")
                        logging.info(f"Overwriting {new_file}...")
                        break
                else:
                    # Rename File
                    renamed_files += 1
                    os.rename(os.path.join(directory, file), os.path.join(directory, new_file))
                    print(f"Renaming {file} to {new_file}...")
                    logging.info(f"Renaming {file} to {new_file}...")
                    break
            print("!----------------------------------------!")

    print(f"Total Files: {total_files}")
    print(f"Renamed Files: {renamed_files}")
    print(f"Skipped Files: {skipped_files}")
    print(f"Overwritten Files: {overwritten_files}")

    print("!---------------------------DONE---------------------------!")


def auto_renaming(directory: str):
    # Naming Sequence guide
    print("Create a Naming Sequence:")
    print("<ft> - Filetype")
    print("<inc> - Increment")
    print("<fn> - Filename")
    print("Example: 'sample.txt' -> [test_<ft>_<fn>_<inc>] = test_doc_sample_1.txt")
    logging.info("Creating Naming Sequence...")
    name_seq = input("Enter Naming Sequence: ")

    # Check if Increment is present, if not, add it
    if "<inc>" not in name_seq:
        logging.info("Increment not found! Adding Increment to Naming Sequence.")
        print("Increment not found! Adding Increment to Naming Sequence.")
        name_seq = f"{name_seq}_<inc>"

    logging.info(f"Naming Sequence: {name_seq}")

    file_type_count = {}
    # Creates an item pair in the dictionary for the count per filetype
    for category in GeneralFunction.file_type_ext.keys():
        file_type_count[category] = 0
    file_type_count["Others"] = 0

    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    exempted_files = []
    for file in files:
        if file not in exempted_files:
            pattern = r"(\w+)(\.\w+)"
            file_group = re.search(pattern, file)
            file_name = file_group.group(1)
            file_ext = file_group.group(2)
            file_type = ""
            file_inc = 0

            while True:
                new_file_name = name_seq
                # Determine what filetype it belongs then increment the counter for the said filetype
                found = False
                for category, extensions in GeneralFunction.file_type_ext.items():
                    if file_ext in extensions:
                        file_type_count[category] += 1
                        file_type = category[:3].lower()
                        file_inc = file_type_count[category]
                        found = True
                        break

                # If the filetype was not found in the dictionary then it belongs in Others
                if not found:
                    file_type_count["Others"] += 1
                    file_type = "oth"
                    file_inc = file_type_count["Others"]

                new_file_name = new_file_name.replace("<ft>", file_type)
                new_file_name = new_file_name.replace("<fn>", file_name)
                new_file_name = new_file_name.replace("<inc>", str(file_inc))
                new_file = f"{make_valid_file_name(new_file_name)}{file_ext}"

                print(f"Renaming {file} to {new_file}...")
                logging.info(f"Renaming {file} to {new_file}...")
                if os.path.exists(os.path.join(directory, new_file)):
                    exempted_files.append(new_file)
                    print(f"{new_file} already exist! Renaming again...")
                    logging.info(f"{new_file} already exist! Renaming again...")
                else:
                    os.rename(os.path.join(directory, file), os.path.join(directory, new_file))
                    print("Renaming Complete!")
                    logging.info("Renaming Complete!")
                    break

    print("!---------------------------DONE---------------------------!")


def rename_script():
    logging.info("Starting RenameScript!")
    print("This is a script for Renaming files. It automatically renames all files in a chosen directory.")
    dialog1 = "Do you want to proceed?"
    if GeneralFunction.confirm_dialog(dialog1):

        target_directory = os.path.dirname(os.getcwd())
        logging.info(f"Current target directory: {target_directory}")
        os.chdir(target_directory)

        opt1 = 1
        option_list1 = [1, 2, 3, 4, 5]
        while opt1 != option_list1[4]:
            print("!--------------------------------------------------------------------------!")
            print(f"Your target directory: {target_directory}")
            dialog2 = "Options: [1-Change target dir | 2-Directory summary | 3-Manual Renaming | 4-Auto Renaming | 5-Exit]"
            opt1 = GeneralFunction.option_dialog(dialog2, option_list1)
            print("!--------------------------------------------------------------------------!")

            if opt1 == option_list1[0]:

                # Changes the source directory
                new_dir = input("Input target directory (absolute or relative): ")
                new_working_directory = GeneralFunction.check_work_path(new_dir)
                if new_working_directory != "Invalid":
                    target_directory = new_working_directory
                    logging.info(f"Current target directory: {target_directory}")
                    os.chdir(target_directory)
                    continue
                print("!------PATH DOES NOT EXIST------!")
                logging.warning("PATH DOES NOT EXIST")

            elif opt1 == option_list1[1]:

                # Prints the directory summary
                GeneralFunction.print_summary(target_directory)

            elif opt1 == option_list1[2]:

                dialog2 = "Do you want to proceed Manual Renaming?"
                if GeneralFunction.confirm_dialog(dialog2):
                    print("Starting Manual Renaming!")
                    logging.info("Starting Manual Renaming!")
                    manual_renaming(target_directory)
                    logging.info("Exiting Manual Renaming!")

            elif opt1 == option_list1[3]:

                dialog3 = "Do you want to proceed Auto Renaming?"
                if GeneralFunction.confirm_dialog(dialog3):
                    print("Starting Auto Renaming!")
                    logging.info("Starting Auto Renaming!")
                    auto_renaming(target_directory)
                    logging.info("Exiting Auto Renaming!")

            elif opt1 == option_list1[4]:

                # Exit the script
                logging.info("Exiting RenameScript!")
                print("Exiting RenameScript!")

            else:

                print("!------INVALID OPTION------!")


if __name__ == "__main__":
    rename_script()
