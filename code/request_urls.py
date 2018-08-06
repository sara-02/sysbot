"""Github and slack urls."""

# FOR SLACK

# Slack API urls
dm_channel_open_url = 'https://slack.com/api/im.open'
dm_chat_post_message_url = 'https://slack.com/api/chat.postMessage'
get_maintainer_list = 'https://slack.com/api/usergroups.users.list'
get_user_profile_info_url = 'https://slack.com/api/users.profile.get'
chat_post_ephimeral_message_url = 'https://slack.com/api/chat.postEphemeral'

# FOR GITHUB

# URL FOR ADDING LABELS TO AN ISSUE
add_label_url = 'https://api.github.com/repos/%s/%s/issues/%s/labels'
send_team_invite = 'https://api.github.com/teams/%s/memberships/%s'
assign_issue_url = 'https://api.github.com/repos/%s/%s/issues/%s'
check_assignee_url = 'https://api.github.com/repos/%s/%s/assignees/%s'
github_comment_url = 'https://api.github.com/repos/%s/%s/issues/%s/comments'
get_issue_url = "https://api.github.com/repos/%s/%s/issues/%s"
open_issue_url = 'https://api.github.com/repos/%s/%s/issues'
remove_assignee_url = 'https://api.github.com/repos/%s/%s/issues/%s/assignees'
get_labels = 'https://api.github.com/repos/%s/%s/issues/%s/labels'
get_contributors = 'https://api.github.com/repos/%s/%s/contributors'
close_pull_request_url = 'https://api.github.com/repos/%s/%s/pulls/%s'
list_open_prs_url = 'https://api.github.com/repos/%s/%s/pulls?state=open'

# LUIS API URL
luis_agent_intent_classify_call = 'https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/%s?subscription-key=%s' \
                                  '&verbose=true&timezoneOffset=0&q=%s'
