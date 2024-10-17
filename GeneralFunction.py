import logging
import os

# Configure logging
log_filename = "file_management.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


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


# Used to create a Option Dialog with multiple options
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
def check_work_path(path):
    if not os.path.exists(path):
        return "Invalid"

    if os.path.isabs(path):
        return path

    abs_path = os.path.abspath(path)
    return abs_path
