import GeneralFunction
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


def deep_count_total_content(directory: str, content_count: dict):
    data_list = [f for f in os.listdir(directory)]
    for data in data_list:
        if os.path.isfile(os.path.join(directory, data)):
            found = False
            pattern = r"\.\w+$"
            ext = re.search(pattern, data)  # Gets the file extension

            # Determine what filetype it belongs then increment the counter for the said filetype
            for category, extensions in GeneralFunction.file_type_ext.items():
                if ext[0] in extensions:
                    content_count[category] += 1
                    found = True
                    break

            # If the filetype was not found in the dictionary then it belongs in Others
            if not found:
                content_count["Others"] += 1
        else:
            content_count["Folders"] += 1
            deep_count_total_content(os.path.join(directory, data), content_count)


def print_summary(content_sum: dict):
    border_line = "|-------------------------------------------|"
    total_content_sum = 0
    for count in content_sum.values():
        total_content_sum += count
    logging.info(f"Total Number of Content: {total_content_sum}")
    logging.info(content_sum)
    print(border_line)
    print(f"Total Number of Content: {total_content_sum}")
    for category, count in content_sum.items():
        print(f"{category:>15}: {count}")
    print(border_line)


def deep_list_content(directory: str, total: int = 0):
    data_list = [f for f in os.listdir(directory)]
    for data in data_list:
        total += 1
        if os.path.isfile(os.path.join(directory, data)):
            logging.info(os.path.join(directory, data))
            print(os.path.join(directory, data))
        else:
            logging.info(os.path.join(directory, data))
            print(os.path.join(directory, data))
            total = deep_list_content(os.path.join(directory, data), total)
    return total


def search_script():
    logging.info("Starting SearchScript!")
    print("This is a script for Searching files. It deep searches a directory for the file.")
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
            dialog2 = "Options: [1-Change target dir | 2-Directory summary | 3-List Files | 4-Search File | 5-Exit]"
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
                content_type_count = {"Folders": 0}  # Stores the count
                # Creates an item pair in the dictionary for the count per filetype
                for category in GeneralFunction.file_type_ext.keys():
                    content_type_count[category] = 0
                content_type_count["Others"] = 0

                deep_count_total_content(target_directory, content_type_count)
                print_summary(content_type_count)

            elif opt1 == option_list1[2]:

                logging.info("Listing all content in target directory...")
                print("Listing all content in target directory...")
                total_sum = deep_list_content(target_directory)
                logging.info(f"Total files found: {total_sum}")
                print(f"Total files found: {total_sum}")

            elif opt1 == option_list1[3]:

                print("Search File")

            elif opt1 == option_list1[4]:

                # Exit the script
                logging.info("Exiting RenameScript!")
                print("Exiting RenameScript!")

            else:

                print("!------INVALID OPTION------!")


if __name__ == "__main__":
    search_script()
