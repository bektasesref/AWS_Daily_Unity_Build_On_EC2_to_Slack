import scm
import unity_builder
import slack_message_sender
import os


def close_os():
    print("Closing OS")
    os.system("shutdown -s -t 15")


if __name__ == "__main__":
    scm.sync_scm()
    if unity_builder.build_project() == "success":
        slack_message_sender.upload_file("Manual triggered build")
        close_os()
    else:
        close_os()