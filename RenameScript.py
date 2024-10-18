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

                print("Auto Renaming!")

            elif opt1 == option_list1[4]:

                # Exit the script
                logging.info("Exiting RenameScript!")
                print("Exiting RenameScript!")

            else:

                print("!------INVALID OPTION------!")


if __name__ == "__main__":
    rename_script()
