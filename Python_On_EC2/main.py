import ftp_uploader
import properties
import scm
import slack_message_sender
import unity_builder
import utils
import xcode_builder


if __name__ == "__main__":
    scm.sync_scm()
    if unity_builder.build_project() == "success":
        if properties.buildTarget == "android":
            slack_message_sender.upload_file("Manual triggered build")
        else:
            if xcode_builder.build_project() == "success":
                if ftp_uploader.upload() == "success":
                    utils.delete_build_folder()
    utils.close_os()