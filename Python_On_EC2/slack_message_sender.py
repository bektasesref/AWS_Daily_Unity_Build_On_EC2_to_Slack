import properties
from slack_sdk import WebClient

client = WebClient(token=properties.slackBotToken,timeout=1000)


def upload_file(commit_message):
    print("Uploading APK to Slack")
    client.files_upload_v2(
        channel=properties.slackChannelToSendMessage,
        title="Build.apk",
        file=properties.projectPath + "/BuildForAndroid/Build.apk",
        initial_comment="New build available: Content-> " + commit_message
    )