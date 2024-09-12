# AWS Daily Unity Build on EC2
Daily Unity Android Builder on AWS EC2 Windows Instance to distribute APK via Slack

## What is this for exactly?
It's an alternative to Unity's Cloud Build, at approximately half the price. It's used for getting daily builds on your latest commit on a pre-configured Plastic SCM account in an EC2 instance and sharing the APK to a Slack channel.

## FAQ

### Is cron-jobs needed?
No, not at all. You can invoke the URL manually to get the Android build. No scheduled event is necessary. You can skip AWS Eventbridge and similar parts.

### Is the instance always open?
No, of course not. It opens with a REST API request and is closed by Python code inside it when the job is done (or fails).

### Can I use it with another version control?
Sure thing. Plastic SCM is what I use, but it can be implemented with anything. Any kind of webhook is suitable.

### How can I manually build?
In the Plastic SCM Triggers section, you will see labeling. When I label a changeset with the keyword "BUILD," the system will give me a build. It can be triggered in any way.

### Am I crazy enough to create a custom CI/CD pipeline to distribute my app just to pay half the price of Unity's Cloud Build?
Hell yeah. Running a business means you need to cut costs as much as you can.

## Steps to install this project

### AWS Part
1. Create a Windows instance on your AWS account.
2. Install all necessary programs and log in: Unity, Plastic SCM, etc.
3. Create a Lambda function as described in the "AWS_LambdaFunction.py" file.
4. Expose with API Gateway for both POST & GET requests (see AWS_APIGateway.png). Note the invocation URLs.
5. Open IAM and create a role with "Allow Action for all lambda function invocations" as described in the AWS_IAM_Role_Permission.txt file. Choose Eventbridge during the role creation so that the Trusted Policy can be invoked by Eventbridge Scheduler.
6. Go to Eventbridge Scheduler Service. Create a schedule with the following cron-job (or any rate you want): `0 8 * * ? *` (triggers at 8 AM every morning) and select the role you just created.
7. Set the payload of the scheduler to `{"build": "BUILD"}` as shown in the AWS_Eventbridge_Target.png file.

### EC2 Part
1. Make sure you have installed (and logged in, downloaded project, etc.) Unity, Plastic SCM, and Python IDE or command line access.
2. Transfer all the files in the Python_On_EC2 folder.
3. Install the "slack_sdk" package from pip (if you want to notify/upload APK to a Slack channel, otherwise delete the corresponding code blocks).
4. Edit the Start.bat file according to your system path to run the main.py Python script.
5. Edit the properties.py file. For example, enter your Unity Editor installation folder, Slack bot token, Slack channel to send the message, Plastic SCM commit checker in a specific branch from a specific user with the `checkInAccount` and `checkInBranchName` params, etc.
6. Add Start.bat as Service that runs automatically on server login with "Task Scheduler". Open Task Scheduler, Click Action -> Create Task. On the Triggers tab, add a "At startup" option on it. Switch to "Action" tab and enter the bat file's location as a Start Program option as default.
7. Check "EC2 System Startup" -> "Task Scheduler" screenshots 

### Unity Part
1. Copy Builder.cs files from Unity folder and paste into the Unity project.
2. Edit as you want. If you are going to sign the APK, enter the keystore or delete all 3 lines. Ensure the `YourGameNameSpace.Builder` is unique and matches the `unity_script_and_method_name` parameter in properties.py. This uses Unity CLI to open the Editor and execute this method.

### Plastic SCM Part
1. To manually build by setting a label with "BUILD" on any commit you want, go to the Plastic SCM Dashboard and enter Triggers.
2. Add a Trigger with the name "after-mklabelwebhook". Set the Payload URL to your API Gateway invoke URL. Choose the trigger type as "after-mklabel". Filtering is strongly recommended to avoid triggering on every labeling action. Use a filter like `rep:[PROJECTNAME],BUILD` as shown in the SCM_Trigger.png file.

### Slack Part
1. Go to [Slack API](https://api.slack.com/apps/) and create a new App from scratch.
2. Go to the OAuth & Permissions tab. Obtain the "OAuth Tokens for Your Workspace" token and enter it in the `slackBotToken` parameter in properties.py.
3. In the "Scopes" panel, go to "Bot Token Scopes" and add the following: `chat:write`, `files:read`, and `files:write`.
4. Install the app on your workspace.
5. Ensure Bots, Permissions, and Install your app checkmarks are valid as shown in Slack_Bot_Lookup.png.
6. Obtain the Channel ID where you will upload the APK as shown in Slack_Obtain_Channel_ID.png. Go to channel details in Slack, click "About" and scroll down to the bottom. Enter this in the `slackChannelToSendMessage` parameter in properties.py.

If everything works fine, you will get the latest APK build on the Slack channel you specified every morning at 8 AM or by manually labeling a changeset with "BUILD". See Slack_Messages.png for the final result.

---