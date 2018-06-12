Systers Slackbot - Sysbot Project
==================================
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

Mentors: Ramit Sawhney, Akshita Aggarwal
Project Manager: Prachi Manchanda

Systers being a vibrant open source community, participates in a lot of major open source programs throughout the year,
like - Outreachy,RGSoC, GCI, GSoC etc. These programs go on round the year and often even overlap. To maintain the quality,
the mentors, admins and students try to clean the repositories and also at the same time aid the newcomers to get started,
and get comfortable with the work flow. This becomes really hectic specially when transitioning fom one program to another.
Hence came the idea of Sysbot, which is a Slack-bot integrated with Github to streamline open source workflow.

**This project is under active development.**

This project is currently hosted here - sombuddha2016.pythonanywhere.com and will be shifted to paid servers soon.  

####Technological Stack

This project is made with Python and using the Flask framework.
Some of the other technologies used include Slack Event API, web-hooks and Github API, NLTK.

#####Reading Resources :-
The following are some links to read about the technologies used.
The contributors can get used to these before contributing.

1. [Flask](http://flask.pocoo.org/)
2. [Slack Events API](https://api.slack.com/events-api)
3. [Slack Bot Users](https://api.slack.com/bot-users)
4. [Slash Commands](https://api.slack.com/slash-commands)
5. [Github API](https://developer.github.com/v3/?)
6. [Stemmer](https://pypi.org/project/stemming/1.0/)
7. [Lemmatizer](https://pythonprogramming.net/lemmatizing-nltk-tutorial/)

Functionalities
-----

####On Github:
1. Each newly opened issue is labelled to be Not Approved by the bot.
2. Any member of the organization can claim issues by using leaving a comment of '@sys-bot claim' on the issue.
3. Similarly, maintainers and collaborators can assign an issue to a member by the comment '@sys-bot assign <assignee_github_username>'
4. Any issue can be approved by maintainers and collaborators via a comment '@sys-bot approve' or via normal comments which have variants of the word approval and issue(E.g - I am approving this issue, Approve this issue, etc). Also, a check has been kept so that the author of an issue cannot approve it.
5. A check has been kept for multiple claims( same issue can't be claimed by or assigned to multiple members) on the same issue and also any unapproved issue cannot be claimed or assigned.
6. Any new PR that's opened get's labelled as 'Under Review'.  

####On Slack:
1. Any newcomer who joins Systers slack workspace gets a DM from the bot with a welcome message, providing help on how to start and how to use the bot.
2. A slash command /sysbot_invite can be used to get invited to the newcomers team and hence become a member of the org. However it checks if the
newcomer member level is completed as mentioned [here](http://systers.io/member-levels)
3. A slash command /sysbot_approve_issue <repo_name> <issue_number> can be used to approve an issue on Github directly from Slack.
However this command can only be used by members of @maintainers team on Slack. E.g. of usage - /sysbot_approve_issue sysbot 23 .
4. A slash command /sysbot_assign_issue <repo_name> <issue_number> <assignee_github_username> can be used to assign any issue from Github directly via Slack.
However this command can only be used by members of @maintainers team on Slack. E.g. of usage - /sysbot_assign_issue sysbot 23 sammy1997.
5. A slash command /sysbot_claim <repo_name> <issue_number> <assignee_github_username> can be used to claim any issue from Github directly via Slack.
E.g. of usage - /sysbot_claim sysbot 23.
[NOTE: To claim or assign an issue, it must first be approved]
6. A slash command /sysbot_open_issue <repo_name> <author_username> *Title of issue(in between star symbols)* Issue Body  

Function Descriptions
---------
####Slack Functions:

1. `dm_new_users():` This sends a direct message to any user.
2. `is_maintainer_comment():` Checks if a certain commenter is a member of the Slack maintainers team.
3. `approve_issue_label_slack():` Handles approval of issue from Slack. Extracts info from the event data and send the required data to github function for approval.
4. `check_newcomer_requirements():` Checks if a newcomer has met the reqirements as mentioned in the membership levels guidelines.
5. `assign_issue_slack():` Handles assigning of issues from Slack. Extracts info from the event data and send the required data to github function for assigning.
6. `claim_issue_slack():` Handles claiming of issues from Slack. Extracts info from the event data and send the required data to github function for claiming.
7. `send_message_to_channels():` Sends a message to a channel(public, private or DM channel).
8. `send_message_ephimeral():` Sends message to channels, but is only visible to the person who caused the message from the bot.
9. `get_detailed_profile():` Gets the detailed profile of a user( this includes custom fields like date of birth, and Github profile).
10. `get_github_username_profile():` Extracts the github username from github field value.

####Github Functions:
1. `label_opened_issue():` Handles the labelling(not approved) of new issues.
2. `send_github_invite():` Sends invite to Systers newcomer team.
3. `issue_comment_approve_github():` Approves issues via approve comments on Github and via Slack.
4. `github_pull_request_label():` Labels newly opened PRs with under review label.
5. `issue_assign():` Assign issues from github and slack.
6. `check_assignee_validity():` Checks if an assignee is valid( if the assignee is a member).
7. `github_comment():` Add comments on github with the author as sys-bot
8. `issue_claim_github():` Assigns a user to an issue,i.e., handles both assign and claim commands.
9. `check_multiple_issue_claim():` Check if same issue is being claimed multiple times.
10. `get_issue_author():` Gets the author of an issue.

Installation
----------
This project uses Python version 2.7( has been developed on 2.7.12). The setup fo this project requires
pip and virtualenv. So first you need to install pip followed by virtualenv.

First fork the project and clone the project using command :
```
git clone https://github.com/<your username>/sysbot.git
```

####Installing Pip

#####On Windows
1. After installing Python, first download [get-pip.py](https://bootstrap.pypa.io/get-pip.py) to a directory.
2. Open cmd, and navigate to the folder where get-py was downloaded.
3. Then run `python get-pip.py`.
4. Verify a successful installation by opening a command prompt window and navigating to your Python installation's script directory (default is `C:\Python27\Scripts`).
Type `pip freeze` from this location to launch the Python interpreter.  
[NOTE: `pip freeze` displays the version number of all modules installed in your Python non-standard library; On a fresh install, `pip freeze` probably won't have much info to show but we're more interested in any errors that might pop up here than the actual content]

#####On Linux
1. Update your System Software: Run the following command to update the package list and upgrade all of your system software to the latest version available:-  

```
sudo apt-get update && sudo apt-get -y upgrade
```

2. Install Pip on Ubuntu: Once the upgrade is completed, you can move on and install Pip. The only thing you need to do is to run the following command:-  
```
sudo apt-get install python-pip
```

3. Verify the Pip Installation: The apt package manager will install Pip and all the dependencies required for the software to work optimally. Once the installation is completed, you can verify that it was successful by using the following command:-  

```
pip -V
```

####Installing virtualenv

##### Both Windows and Linux

1. After pip has been installed, type the following command to install virtualenv:-  
```
pip install virtualenv
```
2. After installing virtualenv, to create an environment,first change directory and get to the project folder, and then type the command:-  
```
virtualenv venv
```
3. Once done, activate the virtual environment using the command **on Windows**:
```
venv/bin/activate
```
And **on Linux** use this command:
```
source venv/bin/activate
```

After virtual environment is active, use this command to install all required packages:

```
pip install -r requirements.txt
```

Once Flask and other requirements have been installed, **on Windows** start the server using:

```
python main_server.py
```
And **on Linux**, use:

```
FLASK_APP=main_server.py flask run
```

To test that the server is running, go to url: [127.0.0.1:5000](127.0.0.1:5000)  
If the server is running properly, you will get a page showing `Response to test hosting`.
And you are good to go!!

Contribute
----------

- Issue Tracker: [sysbot/issues](http://github.com/systers/sysbot/issues)
- Source Code: [sysbot](http://github.com/systers/sysbot/)
- Linking pull request to an issue

  When you create a pull request, use closes #id_of_issue or fixes #id_of_issue. It will link the issue with your pull request. It also
  automatically closes the issue if your pull request gets merged.


Documentation
-------------

User and developer documentation for Systers Sysbot project is generated
using [Markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet).


Support
-------

If you are having issues, please let us know.
We have a mailing list located at: systers-dev@systers.org

Communicate
-----------

The best way to connect with the maintainers is through GitHub comments.
Feel free to discuss more about an issue by commenting on it or asking questions. We also have Systers Slack channel, you can request an invite [here](http://systers.io/slack-systers-opensource/).
If there is something you want to discuss privately with the maintainer and you are being hesitant to discuss it on above mediums, then drop an email.
For Systers Sysbot join #sysbot on Slack.


License
-------

The project is licensed under the [GNU GENERAL PUBLIC LICENSE](https://github.com/systers/sysbot/blob/develop/LICENSE).



A heartfelt thank you to all wonderful contributors of software, guidance, and
encouragement.
