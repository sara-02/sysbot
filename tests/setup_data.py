# For GitHub Functions

# Data with correct issue details
correct_issue_data = {
    "issue": {
        "number": 99
    },
    "repository": {
        "name": "sysbot-test",
        "owner": {
            "login": "systers"
        }
    }
}

# Data with wrong owner and repo names
wrong_issue_data = {
    "issue": {
        "number": 99
    },
    "repository":{
        "name": "sysbot-testing",
        "owner": {
            "login": "syster"
        }
    }
}

# Data with missing parameters
missing_params_issue_data = {
    "issue": {},
    "repository": {
        "name": "sysbot-test",
        "owner": {}
    }
}

# For Slack Functions
# Slack profile
profile_with_github = {
    "ok": True,
    "profile": {
        "title": "GSoC 2018 Student - Sysbot",
        "phone": "https://www.github.com/sammy1997",
        "skype": "",
        "real_name": "Sombuddha Chakravarty",
        "real_name_normalized": "Sombuddha Chakravarty",
        "display_name": "Sammy",
        "display_name_normalized": "Sammy",
        "fields": {
            "Xf98V979NV": {
                "value": "https://www.github.com/sammy1997",
                "alt": "Github",
                "label": "GitHub"
            },
            "Xf9LR9ER6Z": {
                "value": "1997-09-30",
                "alt": "September 30th, 1997",
                "label": "Birthdate"
            }
        },
        "status_text": "GSoC'18 Student - Sysbot",
        "status_emoji": ":gsoc:",
        "status_expiration": 0,
        "avatar_hash": "f45be70a3aa2",
        "image_original": "https://avatars.slack-edge.com/2018-07-04/393013360946_f45be70a3aa2ad056501_original.jpg",
        "email": "f2016165@pilani.bits-pilani.ac.in",
        "first_name": "Sombuddha",
        "last_name": "Chakravarty",
        "image_24": "https://avatars.slack-edge.com/2018-07-04/393013360946_f45be70a3aa2ad056501_24.jpg",
        "image_32": "https://avatars.slack-edge.com/2018-07-04/393013360946_f45be70a3aa2ad056501_32.jpg",
        "image_48": "https://avatars.slack-edge.com/2018-07-04/393013360946_f45be70a3aa2ad056501_48.jpg",
        "image_72": "https://avatars.slack-edge.com/2018-07-04/393013360946_f45be70a3aa2ad056501_72.jpg",
        "image_192": "https://avatars.slack-edge.com/2018-07-04/393013360946_f45be70a3aa2ad056501_192.jpg",
        "image_512": "https://avatars.slack-edge.com/2018-07-04/393013360946_f45be70a3aa2ad056501_512.jpg",
        "image_1024": "https://avatars.slack-edge.com/2018-07-04/393013360946_f45be70a3aa2ad056501_1024.jpg",
        "status_text_canonical": ""
    }
}

profile_without_github = {
    "ok": True,
    "profile": {
        "title": "GSoC 2018 Student - Sysbot",
        "phone": "https://www.github.com/sammy1997",
        "skype": "",
        "real_name": "Sombuddha Chakravarty",
        "real_name_normalized": "Sombuddha Chakravarty",
        "display_name": "Sammy",
        "display_name_normalized": "Sammy",
        "fields": {
            "Xf98V979NV": {
                "value": "",
                "alt": "Github",
                "label": "GitHub"
            },
            "Xf9LR9ER6Z": {
                "value": "1997-09-30",
                "alt": "September 30th, 1997",
                "label": "Birthdate"
            }
        },
        "status_text": "GSoC'18 Student - Sysbot",
        "status_emoji": ":gsoc:",
        "status_expiration": 0,
        "avatar_hash": "3a01ba990c78",
        "image_original": "https://avatars.slack-edge.com/2018-06-07/376983890002_3a01ba990c78f00e6c53_original.jpg",
        "email": "f2016165@pilani.bits-pilani.ac.in",
        "first_name": "Sombuddha",
        "last_name": "Chakravarty",
        "image_24": "https://avatars.slack-edge.com/2018-06-07/376983890002_3a01ba990c78f00e6c53_24.jpg",
        "image_32": "https://avatars.slack-edge.com/2018-06-07/376983890002_3a01ba990c78f00e6c53_32.jpg",
        "image_48": "https://avatars.slack-edge.com/2018-06-07/376983890002_3a01ba990c78f00e6c53_48.jpg",
        "image_72": "https://avatars.slack-edge.com/2018-06-07/376983890002_3a01ba990c78f00e6c53_72.jpg",
        "image_192": "https://avatars.slack-edge.com/2018-06-07/376983890002_3a01ba990c78f00e6c53_192.jpg",
        "image_512": "https://avatars.slack-edge.com/2018-06-07/376983890002_3a01ba990c78f00e6c53_512.jpg",
        "image_1024": "https://avatars.slack-edge.com/2018-06-07/376983890002_3a01ba990c78f00e6c53_1024.jpg",
        "status_text_canonical": ""
    }
}

slash_command_help_data = {
    "channel_id": "CAP9GA5MJ",
    "channel_name": "sysbot-testing",
    "command": "/sysbot_help",
    "response_url": "https://hooks.slack.com/commands/T08C86GE8/392362793973/VpLXVTSsEwMsMmTMfBL0OJ8Y",
    "team_domain": "systers-opensource",
    "team_id": "T08C86GE8",
    "text": "sysbot-test sammy1997 *Test issue from Slack* Sample issue description * Requirement * 1",
    "token": "9WMeKrR9ig79X8PY1jGnzkn5",
    "trigger_id": "393282244247.8416220484.c13108a9fb90e2f6da8d76c04f2823e9",
    "user_id": "U7KMRCS5Q",
    "user_name": "f2016165"
}

slash_command_data_wrong_info = {
    "channel_id": "CAP9GA5MJ",
    "channel_name": "sysbot-testing",
    "command": "/sysbot_help",
    "response_url": "https://hooks.slack.com/commands/T08C86GE8/392362793973/VpLXVTSsEwMsMmTMfBL0OJ8Y",
    "team_domain": "systers-opensource",
    "team_id": "T08C86GE8",
    "text": "sysbot-testing sammy1997 *Test issue from Slack* Sample issue description * Requirement * 1",
    "token": "9WMeKrR9ig79X8PY1jGnzkn5",
    "trigger_id": "393282244247.8416220484.c13108a9fb90e2f6da8d76c04f2823e9",
    "user_id": "U7KMRCS5Q",
    "user_name": "f2016165"
}

slash_command_data_command_params_missing = {
    "channel_id": "CAP9GA5MJ",
    "channel_name": "sysbot-testing",
    "command": "/sysbot_help",
    "response_url": "https://hooks.slack.com/commands/T08C86GE8/392362793973/VpLXVTSsEwMsMmTMfBL0OJ8Y",
    "team_domain": "systers-opensource",
    "team_id": "T08C86GE8",
    "text": "",
    "token": "9WMeKrR9ig79X8PY1jGnzkn5",
    "trigger_id": "393282244247.8416220484.c13108a9fb90e2f6da8d76c04f2823e9",
    "user_id": "U7KMRCS5Q",
    "user_name": "f2016165"
}

sentence = "Approve approved approving"

slash_command_open_issue_data = {
    "channel_id": "CAP9GA5MJ",
    "channel_name": "sysbot-testing",
    "command": "/sysbot_open_issue",
    "response_url": "https://hooks.slack.com/commands/T08C86GE8/392362793973/VpLXVTSsEwMsMmTMfBL0OJ8Y",
    "team_domain": "systers-opensource",
    "team_id": "T08C86GE8",
    "text": "sysbot-test sammy1997 *Test issue from Slack* Sample issue description * Requirement * 1",
    "token": "9WMeKrR9ig79X8PY1jGnzkn5",
    "trigger_id": "393282244247.8416220484.c13108a9fb90e2f6da8d76c04f2823e9",
    "user_id": "U7KMRCS5Q",
    "user_name": "f2016165"
}

slash_command_claim_data = {
    "channel_id": "CAP9GA5MJ",
    "channel_name": "sysbot-testing",
    "command": "/sysbot_claim",
    "response_url": "https://hooks.slack.com/commands/T08C86GE8/392362793973/VpLXVTSsEwMsMmTMfBL0OJ8Y",
    "team_domain": "systers-opensource",
    "team_id": "T08C86GE8",
    "text": "sysbot-test 144",
    "token": "9WMeKrR9ig79X8PY1jGnzkn5",
    "trigger_id": "393282244247.8416220484.c13108a9fb90e2f6da8d76c04f2823e9",
    "user_id": "U7KMRCS5Q",
    "user_name": "f2016165"
}

slash_command_assign_issue_data = {
    "channel_id": "CAP9GA5MJ",
    "channel_name": "sysbot-testing",
    "command": "/sysbot_assign_issue",
    "response_url": "https://hooks.slack.com/commands/T08C86GE8/392362793973/VpLXVTSsEwMsMmTMfBL0OJ8Y",
    "team_domain": "systers-opensource",
    "team_id": "T08C86GE8",
    "text": "sysbot-test 144 sammy1997",
    "token": "9WMeKrR9ig79X8PY1jGnzkn5",
    "trigger_id": "393282244247.8416220484.c13108a9fb90e2f6da8d76c04f2823e9",
    "user_id": "U7KMRCS5Q",
    "user_name": "f2016165"
}

slash_command_approve_issue_data = {
    "channel_id": "CAP9GA5MJ",
    "channel_name": "sysbot-testing",
    "command": "/sysbot_approve_issue",
    "response_url": "https://hooks.slack.com/commands/T08C86GE8/392362793973/VpLXVTSsEwMsMmTMfBL0OJ8Y",
    "team_domain": "systers-opensource",
    "team_id": "T08C86GE8",
    "text": "sysbot-test 144",
    "token": "9WMeKrR9ig79X8PY1jGnzkn5",
    "trigger_id": "393282244247.8416220484.c13108a9fb90e2f6da8d76c04f2823e9",
    "user_id": "U7KMRCS5Q",
    "user_name": "f2016165"
}

slash_command_invite_data = {
    "channel_id": "CAP9GA5MJ",
    "channel_name": "sysbot-testing",
    "command": "/sysbot_invite",
    "response_url": "https://hooks.slack.com/commands/T08C86GE8/392362793973/VpLXVTSsEwMsMmTMfBL0OJ8Y",
    "team_domain": "systers-opensource",
    "team_id": "T08C86GE8",
    "text": "",
    "token": "9WMeKrR9ig79X8PY1jGnzkn5",
    "trigger_id": "393282244247.8416220484.c13108a9fb90e2f6da8d76c04f2823e9",
    "user_id": "U7KMRCS5Q",
    "user_name": "f2016165"
}

data_with_challenge_token = {
    "challenge": "abcde12345"
}

data_member_joined_channel = {
    "event": {
        "type": "member_joined_channel",
        "channel": "C08C8DE01"
    }
}

data_app_mention_channel = {
    "event": {
        "type": "app_mention",
        "channel": "C08C8DE01",
        "text": "<@UASFP3GHW>"
    }
}

data_message_reply = {
    "event": {
        "type": "message",
        "channel": "CAM6T4AGH",
        "user": "UXAB234CQ",
        "channel_type": "channel"
    }
}

query_getting_started = "Can someone guide me on how to start contributing?"
query_gender_participation = "Are female participants preferred over male at Systers?"
