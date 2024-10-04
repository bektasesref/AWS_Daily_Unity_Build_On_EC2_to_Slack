import subprocess
import properties


def build_project():
    print("Unity: Starting build")
    log_path = "build.log"

    build_command = [
        properties.unityExecutablePath,
        "-quit",
        "-batchmode",
        "-projectpath", properties.projectPath,
        "-logFile", log_path,
        "-buildTarget", properties.buildTarget,
        "-executeMethod", properties.unity_script_and_method_name,
    ]

    result = subprocess.run(build_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        print("Unity: Build finished successfully")
        return "success"
    else:
        print(f"Unity: Build failed: {result.stderr}")
        return "fail"