# -*- coding: utf-8 -*-

MESSAGE = {
    'first_timer_message': 'Hello!\nWelcome to the Systers Open Source community!\n\n'
                           '*GETTING STARTED:*'
                           '\n• Join <#C0CAF47RQ|intro> and introduce yourself! :slightly_smiling_face:'
                           '\n• Join the <#C52CRK4HJ|code-of-conduct> and read the community rules, then type in the '
                           'channel. *“I have read the Code of Conduct.“* (http://systers.io/code-of-conduct)'
                           '\n         - Update your profile in accordance with the community rules.'
                           '\nIf you have any questions, post them in the <#C0S15BFNX|questions> channel! :slightly_smiling_face:'
                           '\n\n*Community Meetings:*'
                           '\nGMT/UTC+00:00: https://calendar.google.com/calendar/embed?src=sh10tv3mtfve62somg9nngp9tg%40group.calendar.google.com'
                           '\nTo change the calendar’s time zone, add the following at the end of the url for: '
                           '\nPST: “&ctz=America/Los_Angeles” '
                           '\nEST: “&ctz=America/New_York” '
                           '\nGMT: Nothing! It’s currently in GMT. '
                           '\nWAT: “&ctz=Africa/Lagos” '
                           '\nIST: “&ctz=Asia/Colombo” '
                           '\nJST: “&ctz=Asia/Tokyo”'
                           '\nTo keep up with the Systers-Dev email list, join <#C4TRT3UEQ|mailing-list>.'
                           '\n*If you’re a Newcomer*, check some tutorials and various non-coding '
                           'contributions: http://systers.io/newcomers. '
                           '\n\n*About Sysbot* '
                           '\n The Systers Community has a bot of their own - Sysbot. '
                           'It is integrated on Slack and Github, and has a number of features to automate '
                           'Open Source workflow, like - claiming issues, getting invite to the organization on Github,'
                           'assigning issues etc.'
                           '\n\nHow to operate Sysbot?'
                           '\nType /sysbot_help to get detailed information on the bot. Join #sysbot channel for more info.',
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
    'help_message': 'Following are the functionalities of the Sysbot:-\n' + \
                    '*On Github*:\n' + \
                    '1. Each newly opened issue is labelled to be *Not Approved*.\n' + \
                    '2. If you are a member of the org on Github, you can claim an issue by commenting *@sys-bot claim* on the issue.\n'
                    '3. This is for maintainers/mentors/owners: You can assign an issue to a member of the Github org using command *@sys-bot assign <assignee_github_username> *.\n'
                    '4. Any issue can be approved by maintainers and collaborators via a comment *@sys-bot approve* or via normal comments which have variants of the word approval'
                    ' and issue(E.g - I am approving this issue, Approve this issue, etc). Also, a check has been kept so that the author of an issue cannot approve it.\n'
                    '5. Any newly opened PRs will be labelled *Under Review*.\n'
                    '6. If a PR is sent to *un-approved issue*, it will be closed.\n'
                    '7. A check has been kept on the PR template. If the PR is not linked to an issue using the '
                    '*Fixes #<issue-number>* or if it has any of the necessary elements of the template missing, '
                    'then the PR gets closed.\n'
                    '8. We can have three types of issue templates - Feature Request, User Story, and Bug report. '
                    'The bot checks if each issue follows at least one of these options. If not a Template Mismatch '
                    'label is added, and PR cant be sent to it.\n'
                    '9. The bot checks for multiple claims on the same issue( same issue can\'t be claimed by or assigned to '
                    'multiple members at the same time). \n'
                    '10. PR is labelled under review or approved based on the reviews submitted by Collaborators/Owners\n'
                    '11. Use command @sys-bot label <list of comma seperated labels>, to label an issue or PR with '
                    'multiple labels. Eg:- *@sys-bot label* bug, enhancement, GSoC-18\n\n'
                    '*On Slack*:\n'
                    '1. A slash command */sysbot_invite* can be used to get invited to the newcomers team and hence become a member of the org on Github.'
                    ' However it checks if the newcomer member level is completed as mentioned here(http://systers.io/member-levels).\n'
                    '2. A slash command */sysbot_approve_issue <repo_name> <issue_number>* can be used to approve an issue on Github directly from Slack.'
                    'However this command can only be used by members of *@maintainers* team on Slack.\n'
                    '3. A slash command */sysbot_assign_issue <repo_name> <issue_number> <assignee_github_username>* '
                    'can be used to assign any issue from Github directly via Slack.'
                    'However this command can only be used by members of *@maintainers* team on Slack.\n'
                    '4. A slash command */sysbot_claim <repo_name> <issue_number> <assignee_github_username>* or '
                    '*/sysbot_claim <repo_name> <issue_number>* '
                    ' ( the latter option will work if your github URL is provided on Slack) can be used to claim any'
                    ' issue from Github directly via Slack.\n'
                    '5. You can mention the bot in a channel and query it about slack team for the channel. '
                    'Format: @Sysbot <Your query>. The bot will always respond to the command:'
                    '@Sysbot maintainer team name . You can play around and try some other variants. '
                    'Eg: "@Sysbot I have a doubt about this project. Who to contact?" and similar questions. \n'
                    '6. A slash command to open issues with the following format: */sysbot_open_issue <repo_name> '
                    '<author_username>* * Title of issue * Issue Description * Issue Requirement Item * Estimation .\n'
                    '7. A slash command */sysbot_help* provides a list of all the commands and functionalities of the bot.\n'
                    '8. Each week prs which have been opened that week but have not been reviewed yet are collected and'
                    ' sent to respective Slack channels.\n'
                    '9. On the *intro, questions and newcomers* channels, the bot responds with list of projects based on'
                    ' the tech stack mentioned in the comments.\n'
                    '10. On the *intro and newcomers* channel, the bot responds to questions on *getting started and '
                    'about Systers, AnitaB, GSoC and other programs*, and replies with more information on these topics.'
                    '11. A slash command- /sysbot_label_issue <repo-name> <issue-number> [list of labels] to label an '
                    'issue directly from Slack. Access only to members of maintainers team. '
                    'Eg- /sysbot_label_issue sysbot-test 180 [bug, enhancement]'
                    '12. A slash command /sysbot_view_issue <repo-name> <issue-number> can be used to view issue content'
                    'on Slack. Eg- /sysbot_view_issue sysbot 140',
    'no_permission': 'You do not have permissions for this action.',
    'not_approved': 'This issue has not been approved yet. Please try a different issue.',
    'pr_to_unapproved_issue': 'Please send PRs only to approved issues.',
    'template_mismatch': 'Please make sure that your issue follows the provided template.',
    'list_of_unreviewed_prs': 'Following are the list of not reviewed PRs:\n %s',
    "issue_template": "Created via Slack by @%s \r\n ## Description\r\n"
                      "%s\r\n\r\n ## Acceptance Criteria\r\n"
                      "### Update [Required]\r\n - [ ] %s \r\n\r\n"
                      "## Definition of Done\r\n - [ ] All of the required "
                      "items are completed.\r\n - [ ] Approval by 1 mentor.\r\n\r\n"
                      "## Estimation\r\n %s hours.\r\n",
    "issue_template_feature": "**Is your feature request related to a problem? Please describe.**\r\n"
                              "%s\r\n\r\n **Describe the solution you'd like**\r\n %s \r\n\r\n"
                              "**Describe alternatives you've considered**\r\n %s",
    "issue_template_bug": "**Describe the bug**\r\n"
                          "%s\r\n\r\n **To Reproduce**\r\n"
                          "%s \r\n\r\n**Expected behavior**\r\n %s"
                          "\r\n **Desktop (please complete the following information):**\r\n\r\n"
                          "%s\r\n",
    'slack_team_message': 'For any doubt related to this project, mention <!subteam^%s|%s> in your queries.',
    'slack_team_DNE': 'I have no information about the team for this channel.',
    'wrong_query_format': 'Query format is wrong. Please read the docs or use /sysbot_help to know more',
    'no_answer': 'I have no answer for this query! Please type /sysbot_help to know more.',
    'answer_to_intro': "Hi! Welcome to Systers. Hope you have a good time here. Before you"
                       " start contributing, make sure you have read the welcome bot's messages"
                       " and contribution guidelines. %s",
    'no_project': "With the given information, I was unable to find any project for you. "
                  "Please mention the languages you are familiar with in this thread so "
                  "that I can suggest some projects.",
    'projects_message': "From the techstack you mentioned, I suggest you to look into the following "
                        "projects: You can go to www.github.com/systers and look for these projects -- %s",
    'pr_not_linked_to_issue': "This PR is not linked to any issue. Please follow the template and link it to an issue.",
    'pr_template_not_followed': "This PR does not follow the PR template",
    'error_view_command': "The parameters for view command are wrong. Please check again.",
    'incorrect_info_provided': "Information provided is wrong. Please check repo name and issue number.",
    'no_unreviewed_prs': "All PR reviews up to date. None pending."
}

ANSWERS_FAQS = {
    'getting_started': 'If you have given your intro in the <#C0CAF47RQ|intro> channel, you can get '
                       'started by going through the guidelines mentioned here: \n'
                       '1. http://systers.io/code-of-conduct.html \n'
                       '2. http://systers.io/reporting-guidelines \n\n'
                       'After reading the code of conduct, comment that you have done so in '
                       '<#C52CRK4HJ|code-of-conduct>. \nAfter that, go through the following links '
                       'to get familiar with the workflow and style guidelines: \n'
                       '1. https://udacity.github.io/git-styleguide/ \n'
                       '2. http://systers.io/open-source-workflow \n'
                       '3. http://systers.io/member-levels \n'
                       '4. http://systers.io/newcomers \n\n'
                       'As a newcomer, you may post your doubts on <#CAM6T4AGH|newcomers> and '
                       '<#C0S15BFNX|questions>. \nTo start contributing to projects, take a look here '
                       'http://systers.io/index.html#projects to know more, '
                       'and then you can find the respective repos here: www.github.com/systers',
    'contributor_gender': 'Systers is a community which was built with the vision to get more women '
                          'into technological field and hence is only available for women. However, '
                          'Systers Open Source, being an open source organisation is open to all for '
                          'participation. You are free to contribute to any project or the community '
                          'as you want. However certain OS programs, like - Outreachy, RGSoC and Moonshot '
                          'challenge are open only for women and under-represented communities. But GSoC '
                          'and GCI are open for all. Also, applications for mentoring these programs are '
                          'open for everyone.',
    'systers': 'Systers is an online community founded by Anita Borg that '
               'provides an encouraging atmosphere to all women who are '
               'interested in computer science. The members of the community '
               'collaborate with each other and give each other support while '
               'they continue with the development of their careers. Join their '
               'mailing list here - http://systers.anitab.org/mailman/listinfo/systers .'
               ' To find more about the community, go to http://systers.io/',
    'anita_borg': 'Anita Borg combined technical expertise with a fearless vision to inspire, '
                  'motivate, and move women in technology. Her legacy continues to touch and '
                  'change the lives of countless women in the fields of computing and beyond.\n '
                  'In 1987, computer scientist Anita Borg founded a digital community for women '
                  'in computing. Today, AnitaB.org works with technologists in more than 80 '
                  'countries, and partners with academic institutions and Fortune 500 companies '
                  'worldwide.\n AnitaB.org helps women make significant contributions to technical '
                  'fields. Our programs and awards highlight the accomplishments of women '
                  'technologists, while our events and communities enable women to establish '
                  'their peer networks. You can know more here https://anitab.org/',
    'gsoc_info': 'Google Summer of Code is a global program focused on bringing more student '
                 'developers into open source software development. Students work with an open source '
                 'organization on a 3 month programming project during their break from school. \n'
                 'Link: https://summerofcode.withgoogle.com/ ',
    'gci_info': 'Google CodeIn is a contest to introduce pre-university students '
                '(ages 13-17) to open source software development. Since 2010, 8,108 students from '
                '107 countries have completed over 40,100 open source tasks! \n'
                'Link: https://codein.withgoogle.com/archive/ ',
    'rgsoc_info': 'Rails Girls Summer of Code is a global fellowship program for women and '
                  'non-binary coders. Students receive a three-month scholarship to work on existing '
                  'Open Source projects and expand their skill set.\n Link: https://railsgirlssummerofcode.org/ \n',
    'outreachy': 'Outreachy: It provides three-month internships for people from groups traditionally '
                 'underrepresented in tech. Interns are paid a stipend of $5,500 and have a $500 travel '
                 'stipend available to them. Interns work remotely with mentors from Free and Open Source '
                 'Software (FOSS) communities on projects ranging from programming, user experience, '
                 'documentation, illustration and graphical design, to data science. Outreachy internships '
                 'are open internationally to women (cis and trans), trans men, and genderqueer people. '
                 'Internships are also open to residents and nationals of the United States of any gender '
                 'who are Black/African American, Hispanic/Latin, Native American/American Indian, Alaska '
                 'Native, Native Hawaiian, or Pacific Islander.\n Link: https://www.outreachy.org/'
}
