import os

root_dir = "../"
data_dir = "data/"
clean_dir = "clean/"
joins_dir = "joins/"

root_dir = os.path.abspath(os.path.join(os.getcwd(), "..")) + os.sep
data_dir = data_dir
clean_dir = clean_dir

root_data_dir = os.path.join(root_dir, data_dir)
root_data_clean_dir = os.path.join(root_data_dir, clean_dir)
root_data_clean_joins_dir = os.path.join(root_data_clean_dir, joins_dir)