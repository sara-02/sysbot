# -*- coding: utf-8 -*-

MESSAGE = {
    'first_timer_message': 'Hello!\nWelcome to the Systers Open Source community!\nHow to get started:'+\
        '\n• Join <#C0CAF47RQ|intro> and introduce yourself! :slightly_smiling_face:\n• Join the <#C52CRK4HJ|code-of-conduct> and read the community rules.'+\
        '\n         - Update your profile in accordance with the community rules.'+\
        '\n• Find and join the other channels relevant to you (i.e. different projects).'+\
        '\nIf you have any questions, post them in the <#C0S15BFNX|questions> channel! :slightly_smiling_face:\nTag <@U0BKKUBQU|may> if no one answers immediately.'+\
        '\nTo get more information or ask questions about the larger community, post in <#C4KLZ90SV|systers>.'+\
        '\nTo track GitHub activity of all Systers\' repos, join the <#C6TBYMBPH|github-activity> channel.'+\
        '\nTo keep up with the Systers-Dev email list, join <#C4TRT3UEQ|mailing-list>.'+\
        '\nTo give any thanks or recognition to other members, shoutout in the <#C571VAZQR|celebrate> channel.'
        '\n\nHow to operate Sysbot?'+\
        '\nType /sysbot_help',
    'newcomer_requirement_incomplete': 'Please complete the newcomers requirements! Visit http://systers.io/member-levels for more info.',
    'wrong_info': 'You have either provided wrong info or you are not eligible to be assigned this issue.',
    'success': 'Success',
    'correct_approve_format': 'The correct format is /sysbot_approve_issue <repo> <issue_no>',
    'error_slash_command': 'The slash command got a 500 error. Please check and try again.',
    'not_a_maintainer': 'You are not a maintainer. Please contact <@U0BKKUBQU|may> to get added.',
    'correct_assign_format': 'The correct format is /sysbot_assign_issue <repo_name> <issue_no> <assignee_github_username>',
    'not_an_org_member': 'You can\'t be assigned as you are not a member of the org. Join slack for more info.',
    'wrong_format_github': 'Wrong format of command.',
    'correct_claim_format': 'The correct format is /sysbot_claim <repo_name> <issue_no> <your_github_username>',
    'not_a_member': 'You are not a member of the org yet. Please use /sysbot_invite to get invited to newcomers team.',
    'already_claimed': 'This issue has already been assigned or claimed. Please try another issue.',
    'add_tests': 'Please add tests as the coverage has decreased.',
    'invite_sent': 'Invitation has been sent.',
    'wrong_params_issue_command': 'Insufficient or wrong parameters for issue command.',
    'success_issue': 'Successfully opened issue.',
    'error_issue': 'Some error occurred while opening issue. Please try again.',
    'author_cannot_approve': 'The author of the issue cannot approve the issue.',
    'error_claim_alternate': 'To use this format of the command, please complete your Slack profile with your Github account link.',
    'help_message': 'Following are the functionalities of the Sysbot:-\n'+\
        '*On Github*:\n'+\
        '1. Each newly opened issue is labelled to be *Not Approved*.\n'+\
        '2. If you are a member of the org on Github, you can claim an issue by commenting *@sys-bot claim* on the issue.\n'+\
        '3. This is for maintainers/mentors/owners: You can assign an issue to a member of the Github org using command *@sys-bot assign <assignee_github_username> *.\n'+\
        '4. Any issue can be approved by maintainers and collaborators via a comment *@sys-bot approve* or via normal comments which have variants of the word approval'+\
        ' and issue(E.g - I am approving this issue, Approve this issue, etc). Also, a check has been kept so that the author of an issue cannot approve it.\n'+\
        '5. Any newly opened PRs will be labelled *Under Review*.\n\n'+\
        '*On Slack*:\n'+\
        '1. A slash command */sysbot_invite* can be used to get invited to the newcomers team and hence become a member of the org on Github.'+\
        ' However it checks if the newcomer member level is completed as mentioned here(http://systers.io/member-levels).\n'+\
        '2. A slash command */sysbot_approve_issue <repo_name> <issue_number>* can be used to approve an issue on Github directly from Slack.'+\
        'However this command can only be used by members of *@maintainers* team on Slack.\n'+\
        '3. A slash command */sysbot_assign_issue <repo_name> <issue_number> <assignee_github_username>* can be used to assign any issue from Github directly via Slack.'+\
        'However this command can only be used by members of *@maintainers* team on Slack.\n'+\
        '4. A slash command */sysbot_claim <repo_name> <issue_number> <assignee_github_username>* or */sysbot_claim <repo_name> <issue_number>* '+\
        ' ( the latter option will work if your github URL is provided on Slack) can be used to claim any issue from Github directly via Slack.\n'+\
        '5. You can mention the bot in a channel and query it about slack team for the channel. Format: @Sysbot <Your query>. The bot will always respond to the command:'+\
        '@Sysbot maintainer team name . You can play around and try some other variants. Eg: "@Sysbot I have a doubt about this project. Who to contact?" and similar questions',
    'no_permission': 'You do not have permissions for this action.',
    'not_approved': 'This issue has not been approved yet. Please try a different issue.',
    'pr_to_unapproved_issue': 'Please send PRs only to approved issues.',
    'template_mismatch': 'Please make sure that your issue follows the provided template.',
    'list_of_unreviewed_prs': 'Following are the list of not reviewed PRs:\n %s',
    "issue_template": "Created via Slack by @%s \r\n ## Description\r\n" \
             "%s\r\n\r\n ## Acceptance Criteria\r\n" \
             "### Update [Required]\r\n - [ ] %s \r\n\r\n" \
             "## Definition of Done\r\n - [ ] All of the required " \
             "items are completed.\r\n - [ ] Approval by 1 mentor.\r\n\r\n" \
             "## Estimation\r\n %s hours.\r\n",
    'slack_team_message': 'For any doubt related to this project, mention <!subteam^%s|%s> in your queries.',
    'slack_team_DNE': 'I have no information about the team for this channel.',
    'wrong_query_format': 'Query format is wrong. Please read the docs or use /sysbot_help to know more',
    'no_answer': 'I have no answer for this query! Please type /sysbot_help to know more.'
}
