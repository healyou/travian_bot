import os

def get_absolute_file_path(cur_script_file, rel_file_path):
    script_dir = os.path.dirname(cur_script_file)
    return os.path.join(script_dir, rel_file_path)