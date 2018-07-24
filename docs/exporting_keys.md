Exporting Keys
---

In the auth_credentials.py file in code folder, you can
see all the keys which are required by the bot to function.
They are configured to accept values from the environment.

***Firstly for Github:***

Create your own sample organization. Add a sample team to it.
Use [this](https://developer.github.com/v3/teams/#list-teams) to get 
the team ID.

```
export org_repo_owner='<your org name>' newcomers_team_id='<the team id>' USERNAME='<your github username>' PASSWORD='<your password>'
```

***For LUIS API:***

Sign up for a free account [http://luis.ai/](http://luis.ai/).
Create a new app and train it (read more on how to do that 
[here](nlp_explainations.md)). Then publish it and get 
the path uid(a - separated unique id) and subscription key.
Once done use:
```
export api_key='<subscription key>' path_secret='<path uid>'
```

***For Slack:***

We are working on event mocking. But you can still test out 
the API functions. First join the sample workspace 
[here](https://join.slack.com/t/sysbotsample/shared_invite/enQtNDAzMTU2MTkwNTYyLTIwYzQ2ZTk0YzQ4MzM1MGRjMjI0ZjkxOTdlYjRlNTg5OTU4ZDM5YzFmMWYxNjAwYzg2OWY1MzA1Y2FiOGQxZjI)
This workspace has been set to mock the main Systers workspace.
All the project channels have been created with same name as that 
on Systers.

Here are the sample tokens:
```
legacy_token='xoxp-327879632387-327879632547-329042880807-656e3aa59b5abd1ea7d59056e55a7fc9'
BOT_TOKEN='xoxb-327993096738-Kg5v6qqsFlyZkngQcTRQ7R4N'
```
Export these into the environment as well.
Export announcement_channel_id='C9MCGNSQH'
Export maintainer_usergroup_id='SAQDWBCE7'

 