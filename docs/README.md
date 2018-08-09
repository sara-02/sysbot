Systers Slackbot - Sysbot Project
==================================
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
![Jenkins](https://img.shields.io/badge/build-passing-green.svg)
![Coverage](https://img.shields.io/badge/coverage-91%25-brightgreen.svg)
![Language](https://img.shields.io/badge/tech-python-blue.svg)  
![Python Version](https://img.shields.io/badge/python-2.7-blue.svg)
![API Usage](https://img.shields.io/badge/API-Slack%2BGithub%2BLUIS-blue.svg)
![Framework](https://img.shields.io/badge/framework-Flask-blue.svg)

**This project is under active development.**

This project is currently hosted on Pythonanywhere 
[here](sombuddha2016.pythonanywhere.com) and on AWS 
[here](http://sysbot-dev.5uhcagxzd9.eu-central-1.elasticbeanstalk.com/).  

About
-----

This is a project to develop a Slack bot to streamline Open Source workflow. Some functionalities include:
labeling, approving issues and PRs, claiming and assigning issues, both on Github and Slack,
and replying to newcomer comments with beginner resources, and many more.

Functionalities
-----

Following are the functionalities the bot has.
Check out the function descriptions [here](https://github.com/systers/sysbot/wiki/Function-descriptions)
to know which function handles what.

#### On Github:
1. Each newly opened issue is labelled to be Not Approved by the bot.
2. Any member of the organization can claim issues by using leaving a comment of `@sys-bot claim` on the issue.
3. Similarly, maintainers and collaborators can assign an issue to a member by the comment `@sys-bot assign <assignee_github_username>`
4. Any issue can be approved by maintainers and collaborators via a comment `@sys-bot approve` or via normal comments which have variants of the word approval and issue(E.g - I am approving this issue, Approve this issue, etc). Also, a check has been kept so that the author of an issue cannot approve it.
5. A check has been kept for multiple claims( same issue can't be claimed by or assigned to multiple members) on the same issue and also any unapproved issue cannot be claimed or assigned.
6. Any new PR that's opened get's labelled as 'not reviewed'.
7. If a PR is sent to un-approved issue, it will get closed.
8. We can have three types of issue templates - Feature Request, 
User Story, and Bug report. The three options are currently functional [here](https://github.com/systers/mentorship-backend/issues/new/choose).
The bot checks if each issue follows at least one of these options. If not a `Template Mismatch` label is added, and PR cant be sent to it.
9. A check has been kept on the PR template as well. If the PR is not linked to an issue
using the `Fixes #<issue-number>` or if it has any of the necessary elements of the
template missing, then the PR gets closed.
10. PR is labelled under review or approved based on the reviews submitted by Collaborators/Owners.
11. A command @sys-bot label <list of comma-separated labels>, has been added to label an issue or PR with multiple labels. Eg:- **@sys-bot label** bug, enhancement, GSoC-18


#### On Slack:
1. Any newcomer who joins Systers slack workspace gets a DM from the bot with a welcome message, providing help on how to start and how to use the bot.
2. A slash command `/sysbot_invite` can be used to get invited to the newcomer's team and hence become a member of the Org. However, it checks if the
newcomer member level is completed as mentioned [here](http://systers.io/member-levels)
3. A slash command `/sysbot_approve_issue <repo_name> <issue_number>` can be used to approve an issue on Github directly from Slack.
However this command can only be used by members of @maintainers team on Slack. E.g. of usage - /sysbot_approve_issue sysbot 23 .
4. A slash command `/sysbot_assign_issue <repo_name> <issue_number> <assignee_github_username>` can be used to assign any issue from Github directly via Slack.
However this command can only be used by members of @maintainers team on Slack. E.g. of usage - /sysbot_assign_issue sysbot 23 sammy1997.
5. A slash command `/sysbot_claim <repo_name> <issue_number> <assignee_github_username>` or `/sysbot_claim <repo_name> <issue_number>` 
( the latter option will work if your github URL is provided on Slack) can be used to claim any issue from Github directly via Slack.
E.g. of usage - /sysbot_claim sysbot 23.
[NOTE: To claim or assign an issue, it must first be approved]
6. A slash command `/sysbot_open_issue <repo_name> <author_username>` * Title of issue * Issue Description * Issue Requirement Item * Estimation. 
The issues are opened in full markdown format, and the author's name is mentioned at the top.
7. A slash command `/sysbot_help` provides a list of all the commands and functionalities of the bot.  
8. Each week PRs which have been opened that week but have not been reviewed yet are collected and sent to respective Slack channels.
9. A slash command `/sysbot_help` provides a list of all functionalities that the bot provides
10. Each channel is notified about unreviewed PRs opened in that week in each respective repository.
11. The bot uses a trained agent provided by LUIS API to recognise questions about team maintainers and responds with team names for each channel.
12. On the intro, questions and newcomers channels, the bot responds with the list of projects based on the tech stack mentioned in the comments.
13. On the intro and newcomers channel, the bot responds to questions on getting started and about Systers, AnitaB, GSoC and other programs,
and replies with more information on these topics.
14. A slash command- /sysbot_label_issue <repo-name> <issue-number> [list of labels] to label an issue directly from Slack.
Access only to members of maintainers team. Eg- /sysbot_label_issue sysbot-test 180 [bug, enhancement]
15. A slash command on Slack to view issues directly on Slack has been added. 
Format: /sysbot_view_issue <repo-name> <issue-name> . Eg- /sysbot_view_issue sysbot 123

More explanations on NLP part can be found [here](nlp_explainations.md)


Installation
----------
This project uses Python version 2.7( has been developed on 2.7.12). The setup for this project requires
pip and virtualenv. So first you need to install pip followed by virtualenv.

First fork the project and clone the project using the command :
```
git clone https://github.com/<your username>/sysbot.git
```

#### Installing virtualenv

##### Both Windows and Linux

1. After pip has been installed, type the following command to install virtualenv:-  
```
pip install virtualenv
```
2. After installing virtualenv, to create an environment, first change directory and get to the project folder, and then type the command:-  
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

After the virtual environment is active, use this command to install all required packages:

```
pip install -r requirements.txt
```

Once Flask and other requirements have been installed, **on Windows** start the server using:

```
python main_server.py
```
And **on Linux**, use:

```
python main_server.py
```

To test that the server is running, go to url: [127.0.0.1:5000](http://127.0.0.1:5000)  
If the server is running properly, you will get a page showing `Response to test hosting`.
And you are good to go!!

Getting Started
--------------

Once your local server is up, download [ngrok](https://ngrok.com/),
open a terminal in the directory where you downloaded the file.
Then use this command:
```
./ngrok http 5000
```
Be sure you have internet access while trying this command. Once it
is connected, it will give you a unique http and https url(Eg- http://c777e5a5.ngrok.io).
Now any requests/data sent to this URL will be directed to your local server.

Also, for local usage change the imports from dictionaries.py 
in main_server, slack_functions, github_functions to dictionaries_test.py.
However **do not commit this change**. Rever it back before sending a PR.
This is **only for testing features** in the Sample Workspace!

##### For Github

Go to any Github repo that you own( or your organization owns),
and in the settings section, go to webhooks. Add a new webhook.
In the hook, URL enter the above HTTP URL generated by ngrok, 
and from the events select issues, issue comments and PRs. 
Once done save the webhook. If you are using your own repo
look [here](exporting_keys.md) for how to export keys.

##### For Slack

Have a look at my proposal on how I proposed to work around giving access
to Slack apps by simulating events 
[here](https://docs.google.com/document/d/1q5F3mumzjEYhoInLjdxCBaGtIxvEmy5OeZQKARcc0vk/edit?usp=sharing)

Join this workspace using [this](https://join.slack.com/t/sysbotsample/shared_invite/enQtNDAzMTU2MTkwNTYyLTIwYzQ2ZTk0YzQ4MzM1MGRjMjI0ZjkxOTdlYjRlNTg5OTU4ZDM5YzFmMWYxNjAwYzg2OWY1MzA1Y2FiOGQxZjI)
 invite link. This is the sample workspace for testing out Sysbot! 
 All the channel names have been kept same as the main workspace.   

To simulate an event first start the virtualenv, export all environment variables and run the local server. 
By default host **127.0.0.1** and port **5000** is considered.
If you want to use a separate host and port, export them as follows:

```
export HOST=<host address> PORT=<port number>
```

All the event data which is being simulated is stored in the folder
simulate/data as github_data.json and slack_data.json.

If you want to simulate the GitHub events also locally,
change the data in JSON file - replace the Github event
data with event data from your repository's hook.
 We are using **runp** to run functions from a file. 
 Once the server is running, do the following:
 
 ```
 cd simulate
 ```
 To mock all events( both Slack and Github events):
 
 ```
 runp simulate.py simulate_all
 ```
 
 To mock all Github events:

 ```
 runp simulate.py simulate_github_events
 ```

To mock all Slack events:
```
 runp simulate.py simulate_slack_events
```
You can mock each individual event using the respective function name.
Look at the simulate.py file for all the functions.
For example to mock an approve comment event:
```
runp simulate.py github_approve_comment
```
You can add your own simulations as well. Add the data to the respective json file and write a function to deliver the data using requests library!
 
If you want to see the changes on your own repo, remember to change the 
JSON data accordingly before simulating.


Testing
-----

The unit tests are written under two files - one for Github
functions, and another for Slack functions.  

Each of the functions expects some data which are basically delivered by Slack and Github Servers to our event webhooks. This data is stored 
in tests/setup_data.py . When you run the bot locally and configure the hooks on your own repos(for Github), or channels(for Slack), you need to change the data accordingly(for Github data change the repo name, 
owner name etc and for Slack change the channel IDs and user IDs).

In the setup data file, all the data used for GitHub are for the sysbot-test 
repo which is private. Replace the repo details with your repo if you want to test the data locally.

To run the tests use the command:
```
coverage run --source code -m unittest discover tests
```

To get the coverage report(coverage percentage):
```
coverage report -m
```

#### Technological Stack

This project is made with Python and using the Flask framework.
Some of the other technologies used include Slack Event API, webhooks and Github API, NLTK.

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
8. [LUIS API](https://www.luis.ai/home)
9. [NLP Explanations and decisions](https://github.com/systers/sysbot/blob/develop/docs/)


Contribute
----------

- Before starting with contributions, go through [contribution guidelines](https://github.com/systers/sysbot/blob/develop/docs/CONTRIBUTING.md) , [code of conduct](https://github.com/systers/sysbot/blob/develop/docs/code_of_conduct.md) and [reporting guidelines](https://github.com/systers/sysbot/blob/develop/docs/reporting_guidelines.md).  
- Linking pull request to an issue
- Go through the Commit message guide [here](https://github.com/systers/sysbot/wiki/Commit-Message-Style-Guide)

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
