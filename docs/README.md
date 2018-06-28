Systers Slackbot - Sysbot Project
==================================
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
![coverage](https://img.shields.io/sonar/http/sonar.petalslink.com/org.ow2.petals%3Apetals-se-ase/coverage.svg)


**This project is under active development.**

This project is currently hosted [here](sombuddha2016.pythonanywhere.com) and will be shifted to paid servers soon.  

About
-----

This is a project to develop a Slack bot to streamline Open Source workflow. Some functionalities include:
labeling, approving issues and PRs, claiming and assigning issues, both on Github and Slack,
and replying to newcomer comments with beginner resources, and many more.

Functionalities
-----

#### On Github:
1. Each newly opened issue is labelled to be Not Approved by the bot.
2. Any member of the organization can claim issues by using leaving a comment of '@sys-bot claim' on the issue.
3. Similarly, maintainers and collaborators can assign an issue to a member by the comment '@sys-bot assign <assignee_github_username>'
4. Any issue can be approved by maintainers and collaborators via a comment '@sys-bot approve' or via normal comments which have variants of the word approval and issue(E.g - I am approving this issue, Approve this issue, etc). Also, a check has been kept so that the author of an issue cannot approve it.
5. A check has been kept for multiple claims( same issue can't be claimed by or assigned to multiple members) on the same issue and also any unapproved issue cannot be claimed or assigned.
6. Any new PR that's opened get's labelled as 'not reviewed'.
7. If a PR is sent to un-approved issue, it will get closed.  

#### On Slack:
1. Any newcomer who joins Systers slack workspace gets a DM from the bot with a welcome message, providing help on how to start and how to use the bot.
2. A slash command /sysbot_invite can be used to get invited to the newcomers team and hence become a member of the org. However it checks if the
newcomer member level is completed as mentioned [here](http://systers.io/member-levels)
3. A slash command /sysbot_approve_issue <repo_name> <issue_number> can be used to approve an issue on Github directly from Slack.
However this command can only be used by members of @maintainers team on Slack. E.g. of usage - /sysbot_approve_issue sysbot 23 .
4. A slash command /sysbot_assign_issue <repo_name> <issue_number> <assignee_github_username> can be used to assign any issue from Github directly via Slack.
However this command can only be used by members of @maintainers team on Slack. E.g. of usage - /sysbot_assign_issue sysbot 23 sammy1997.
5. A slash command /sysbot_claim <repo_name> <issue_number> <assignee_github_username> or /sysbot_claim <repo_name> <issue_number> ( the latter option will work if your github URL is provided on Slack) can be used to claim any issue from Github directly via Slack.
E.g. of usage - /sysbot_claim sysbot 23.
[NOTE: To claim or assign an issue, it must first be approved]
6. A slash command /sysbot_open_issue <repo_name> <author_username> * Title of issue * Issue Description * Issue Requirement Item * Estimation
7. A slash command /sysbot_help provides a list of all the commands and functionalities of the bot.  
8. Each week prs which have been opened that week but have not been reviewed yet are collected and sent to respective Slack channels.


Installation
----------
This project uses Python version 2.7( has been developed on 2.7.12). The setup fo this project requires
pip and virtualenv. So first you need to install pip followed by virtualenv.

First fork the project and clone the project using command :
```
git clone https://github.com/<your username>/sysbot.git
```

#### Installing virtualenv

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

To test that the server is running, go to url: [127.0.0.1:5000](http://127.0.0.1:5000)  
If the server is running properly, you will get a page showing `Response to test hosting`.
And you are good to go!!

#### Technological Stack

This project is made with Python and using the Flask framework.
Some of the other technologies used include Slack Event API, web-hooks and Github API, NLTK.

##### Reading Resources :-
The following are some links to read about the technologies used.
The contributors can get used to these before contributing.

1. [Flask](http://flask.pocoo.org/)
2. [Slack Events API](https://api.slack.com/events-api)
3. [Slack Bot Users](https://api.slack.com/bot-users)
4. [Slash Commands](https://api.slack.com/slash-commands)
5. [Github API](https://developer.github.com/v3/?)
6. [Stemmer](https://pypi.org/project/stemming/1.0/)
7. [Lemmatizer](https://pythonprogramming.net/lemmatizing-nltk-tutorial/)


Contribute
----------

- Before starting with contributions, go through [contribution guidelines](https://github.com/systers/sysbot/blob/develop/docs/CONTRIBUTING.md) , [code of conduct](https://github.com/systers/sysbot/blob/develop/docs/code_of_conduct.md) and [reporting guidelines](https://github.com/systers/sysbot/blob/develop/docs/reporting_guidelines.md).  
- Linking pull request to an issue

  When you create a pull request, use closes #id_of_issue or fixes #id_of_issue. It will link the issue with your pull request. It also
  automatically closes the issue if your pull request gets merged.



Communicate
-----------

Feel free to discuss more about an issue by commenting on it or asking questions. We also have Systers Slack channel, you can request an invite [here](http://systers.io/slack-systers-opensource/).

If there is something you want to discuss privately with the maintainer and you are being hesitant to discuss it on above mediums, then drop an email.

For Systers Sysbot join #sysbot on Slack.

If you are having issues, please let us know.
We have a mailing list located at: [systers-dev@systers.org](mailto:systers-dev@systers.org)


License
-------

The project is licensed under the [GNU GENERAL PUBLIC LICENSE](https://github.com/systers/sysbot/blob/develop/LICENSE).


A heartfelt thank you to all wonderful contributors of software, guidance, and
encouragement.
