import os
import re
import properties
import subprocess


def execute_command(command, cwd=None):
    result = subprocess.run(command, cwd=cwd, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"SCM: Error executing command: {command}\n{result.stderr}")
    else:
        return result.stdout


def extract_branch_name(selector_output):
    match = re.search(r'smartbranch "([^"]+)"', selector_output)
    if match:
        return match.group(1)
    return None


def extract_branch_name_from_commit(commit_message):
    match = re.search(r'New checkin to `([^`]+)`', commit_message)
    if match:
        return match.group(1)
    return None


def sync_scm():
    print("SCM: Starting sync")
    os.chdir(properties.projectPath)
    execute_command("cm undo . -r")
    selector = execute_command("cm showselector")
    branch_name = extract_branch_name(selector)
    print(f"SCM: Current branch: {branch_name}")
    execute_command(f"cm switch {branch_name}")
    print("SCM: Synced successfully")