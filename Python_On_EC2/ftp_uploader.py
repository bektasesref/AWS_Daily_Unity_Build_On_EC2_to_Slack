import os
import ftplib
import properties
from datetime import datetime
import re


def upload():
    print("FTP: Starting FTP Upload")
    try:
        with ftplib.FTP(properties.FTP_SERVER) as ftp:
            ftp.login(user=properties.FTP_USER, passwd=properties.FTP_PASSWORD)

            ftp.cwd(properties.FTP_SUB_FOLDER)
            with open(properties.FILE_PATH, 'rb') as file:
                ftp.storbinary(f'STOR {os.path.basename(properties.FILE_PATH)}', file)

            ftp.cwd("..//")

            local_file_path = properties.FTP_InternalTestHTMLFile
            with open(local_file_path, 'wb') as local_file:
                ftp.retrbinary('RETR ' + properties.FTP_InternalTestHTMLFile, local_file.write)

            if update_html_timestamp(local_file_path) == "success":
                upload_html(local_file_path, ftp)

        print("FTP: .ipa Upload Succeeded")
        return "success"

    except Exception as e:
        print(f"FTP: .ipa Upload Failed: {e}")
        return "error"


def update_html_timestamp(file_path):
    try:
        current_time = datetime.now().strftime("%d.%m.%Y - %H:%M")

        with open(file_path, 'r') as file:
            content = file.read()

        new_content = re.sub(
            r'(Latest iOS Update: )(.*?)(</h5>)',
            f'Latest iOS Update: {current_time}\\3',
            content
        )

        with open(file_path, 'w') as file:
            file.write(new_content)

        print("HTML: Timestamp updated successfully.")
        return "success"

    except Exception as e:
        print(f"HTML: Error updating timestamp: {e}")
        return "error"


def upload_html(file_path, ftp):
    print("FTP: Uploading updated HTML file")
    try:
        with open(file_path, 'rb') as file:
            ftp.storbinary('STOR ' + properties.FTP_InternalTestHTMLFile, file)

        print("FTP: HTML file upload succeeded.")
        return "success"

    except Exception as e:
        print(f"FTP: HTML file upload failed: {e}")
        return "error"
