import os
import properties
import shutil


def close_os():
    print("Main: Closing OS")
    if os.name == 'nt':
        os.system("shutdown -s -t 15")
    else:
        os.system("sudo shutdown -h +0.25")


def delete_build_folder():
    build_folder = properties.buildFolder
    if os.path.exists(build_folder):
        print(f"Main: Deleting build folder: {build_folder}")
        shutil.rmtree(build_folder)
        print("Main: Build folder deleted successfully")
    else:
        print(f"Main: Build folder not found: {build_folder}")
