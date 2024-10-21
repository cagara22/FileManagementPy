import logging
import GeneralFunction
from OrganizeScript import organize_script
from RenameScript import rename_script
from SearchScript import search_script

# Configure logging
log_filename = "file_management.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logging.info("Script Started!")
print("Hi! This script is made by Vincent Felix Cagara. This is used for file management.")

opt = 1
option_list = [1, 2, 3, 4]
while opt != option_list[3]:
    dialog = "Options: [1-OrganizeScript | 2-RenameScript | 3-SearchScript | 4-EXIT]"
    opt = GeneralFunction.option_dialog(dialog, option_list)
    if opt == option_list[0]:
        logging.info("OrganizeScript is Selected.")
        organize_script()
    elif opt == option_list[1]:
        logging.info("RenamingScript is Selected.")
        rename_script()
    elif opt == option_list[2]:
        logging.info("SearchScript is Selected.")
        search_script()
    elif opt == option_list[3]:
        logging.info("Exiting Script!")
        print("Exiting Script!")
