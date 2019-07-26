import os

def get_absolute_file_path(cur_script_file, rel_file_path):
    script_dir = os.path.dirname(cur_script_file)
    return os.path.join(script_dir, rel_file_path)

def get_travian_command_files():
    return [
        'files/travian/login.json',
        'files/travian/open_village.json',
        'files/travian/open_map.json',
        'files/travian/open_resources.json'
    ]