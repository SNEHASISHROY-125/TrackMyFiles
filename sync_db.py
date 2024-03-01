'''

'''

import shutil
import os

import os
import shutil

def copy_and_rename(src_path, dst_dir, new_name):
    """
    Copy a file from the source path to the destination directory and rename it.

    Args:
        src_path (str): The path of the source file.
        dst_dir (str): The path of the destination directory.
        new_name (str): The new name for the copied file.

    Returns:
        None
    """

    # Ensure the destination directory exists
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    # Construct the destination path
    dst_path = os.path.join(dst_dir, new_name)

    # Copy and rename the file
    shutil.copy2(src_path, dst_path)

# Usage
copy_and_rename('path/to/source/file', 'path/to/destination/directory', 'new_file_name')