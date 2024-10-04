import subprocess
import os

import properties


def run_command(command):
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()

        return process.returncode, stdout, stderr
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1, None, None


def build_and_archive():
    print(f"xCode: Starting Build & Archive")
    command = f'xcodebuild -project "{properties.project_path}" -scheme "{properties.scheme_name}" clean archive -configuration "{properties.configuration}" -sdk "{properties.sdk}" -archivePath "{properties.archive_path}" -allowProvisioningUpdates'
    returncode, stdout, stderr = run_command(command)
    return returncode == 0


def export_ipa():
    print(f"xCode: Exporting .ipa")
    command = f'xcodebuild -exportArchive -archivePath "{properties.archive_path}" -exportOptionsPlist "{properties.export_options_plist}" -exportPath "{properties.export_path}" -allowProvisioningUpdates -verbose'
    returncode, stdout, stderr = run_command(command)
    return returncode == 0


def build_project():
    os.environ["DEVELOPER_DIR"] = properties.developer_dir

    if build_and_archive():
        print(f"xCode: Build & Archive Succeeded")
        if export_ipa():
            print(f"xCode: .ipa Export Succeeded")
            return "success"
        else:
            print(f"xCode: .ipa Export Failed")
            return "error"
    else:
        print(f"xCode: Build & Archive Failed")
        return "error"