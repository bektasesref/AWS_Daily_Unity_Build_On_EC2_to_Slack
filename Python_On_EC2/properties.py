import os

buildTarget = "ios" # "ios" or "android"
projectPath = f"C:\\Users\\{os.getlogin()}\\wkspaces\\ProjectName" # or on macos; os.path.expanduser("~/Documents/ProjectName")
buildFolder = projectPath + "/BuildForiOS" # or on macos;  projectPath + "/BuildForAndroid"
unityExecutablePath = "C:/Program Files/Unity/Hub/Editor/2022.3.26f1/Editor/Unity.exe" #or on macos; /Applications/Unity/Hub/Editor/2022.3.26f1/Unity.app/Contents/MacOS/Unity
unity_script_and_method_name = "YourGameNameSpace.BuildForAndroid"

slackBotToken = "xo[corrupted]]q2lUX6t0kcNi"
slackChannelToSendMessage = "C[corrupted]]S8998"

checkInAccount = "acc[corrupted].com"
checkInBranchName = "/dev"

developer_dir = "/Applications/Xcode.app/Contents/Developer"
project_path = buildFolder + "/Unity-iPhone.xcodeproj"
scheme_name = "Unity-iPhone"
configuration = "release"
sdk = "iphoneos"
archive_path = buildFolder+"/Unity-iPhone.xcarchive"
export_options_plist = os.path.join(os.path.dirname(__file__), "ExportOptions.plist")
export_path = buildFolder + "/ipa"

FTP_USER = "in[corrupted]on.com"
FTP_PASSWORD = "[corrupted]*_"
FTP_SERVER = "[corrupted].48"
FILE_PATH = export_path + "/[corrupted].ipa"
FTP_SUB_FOLDER = "ios"
FTP_InternalTestHTMLFile = "InternalTest.html"