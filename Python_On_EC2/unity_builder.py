import subprocess
import properties


def build_project():
    print("Build in progress")
    log_path = "build.log"

    build_command = [
        properties.unityExecutablePath,
        "-quit",
        "-batchmode",
        "-projectpath", properties.projectPath,
        "-logFile", log_path,
        "buildTarget", "Android",
        "-executeMethod", properties.unity_script_and_method_name,
    ]

    result = subprocess.run(build_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        print("Build finished successfully.")
        print(result.stdout)
        return "success"
    else:
        print("Build failed.")
        print(result.stderr)
        return "fail"