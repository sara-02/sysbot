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
    "repository": {
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
    "text": "sysbot-test 144 sys-bot",
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

pr_template_with_fixes_number = "### Description\r\n" \
                                "%s\r\n Fixes #123\r\n ### Type of Change:\r\n" \
                                "%s \r\n\r\n### How Has This Been Tested?\r\n" \
                                "%s \r\n### Checklist:\r\n " \
                                "- [ ] %s.\r\n"

pr_template_with_fixes_text = "### Description\r\n" \
                              "%s\r\n Fixes #abc\r\n ### Type of Change:\r\n" \
                              "%s \r\n\r\n### How Has This Been Tested?\r\n" \
                              "%s \r\n### Checklist:\r\n " \
                              "- [ ] %s.\r\n"

pr_template_without_fixes = "### Description\r\n" \
                            "%s\r\n ### Type of Change:\r\n" \
                            "%s \r\n\r\n### How Has This Been Tested?\r\n" \
                            "%s \r\n### Checklist:\r\n " \
                            "- [ ] %s.\r\n"

event_data_issue_opened = {
    "action": "opened",
    "issue": {
        "body": "Anything",
        "number": "151",
    },
    "repository": {
        "name": "sysbot-test",
        "owner": {
            "login": "systers"
        }
    }
}

event_data_comment = {
    "action": "created",
    "issue": {
        "body": "",
        "number": "151",
    },
    "repository": {
        "name": "sysbot-test",
        "owner": {
            "login": "systers"
        }
    },
    "comment": {
        "body": "Coverage decreased",
        "user": {
            "login": "coveralls"
        },
        "author_association": "USER"
    }
}

event_data_pr_opened = {
    "action": "opened",
    "pull_request": {
        "body": "### Description\r\n"
                "Some Description\r\n Fixes #151\r\n "
                "### Type of Change:\r\n"
                "Explain the changes \r\n"
                "### How Has This Been Tested?\r\n"
                "Tested \r\n### Checklist:\r\n"
                "- [ ] Checklist Point.\r\n",
        "number": "13",
    },
    "repository": {
        "name": "sysbot-test",
        "owner": {
            "login": "systers"
        }
    }
}

new_user_data = {
    "event": {
        "text": "Hello <@UASFP3GHW> How to get started?",
        "channel": "CAP9GA5MJ",
        "user": "U7KMRCS5Q"
    }
}

faq_sentence = "I am new here. Can anyone tell me about GSoC?"

slash_command_view_issue_data = {
    "channel_id": "CAP9GA5MJ",
    "channel_name": "sysbot-testing",
    "command": "/sysbot_view_issue",
    "response_url": "https://hooks.slack.com/commands/T08C86GE8/411060288517/Aj1nuE1p8x4bEbBRIfQ44hRT",
    "team_domain": "systers-opensource",
    "team_id": "T08C86GE8",
    "text": "sysbot-test 178",
    "token": "9WMeKrR9ig79X8PY1jGnzkn5",
    "trigger_id": "411060288533.8416220484.49610058e1a1a50a5f8231694862f9b5",
    "user_id": "U7KMRCS5Q",
    "user_name": "f2016165"
}

pr_approved_review_event_data = {
    "action": "submitted",
    "pull_request": {
        # PR number on which review was submitted
        "number": "29",
    },
    "repository": {
        "name": "sysbot-test",
        "owner": {
            "login": "systers"
        }
    },
    # Data about review
    "review": {
        "state": "approved",
        "author_association": "COLLABORATOR"
    }
}

pr_changes_requested_review_event_data = {
    "action": "submitted",
    "pull_request": {
        # PR number on which review was submitted
        "number": "29",
    },
    "repository": {
        "name": "sysbot-test",
        "owner": {
            "login": "systers"
        }
    },
    # Data about review
    "review": {
        "state": "changes_requested",
        "author_association": "COLLABORATOR"
    }
}

pr_review_error_event_data = {
    "action": "submitted",
    "pull_request": {
        # PR number on which review was submitted
        "number": "29",
    },
    "repository": {
        "name": "sysbot-testing",
        "owner": {
            "login": "systers"
        }
    },
    # Data about review
    "review": {
        "state": "changes_requested",
        "author_association": "COLLABORATOR"
    }
}

slash_command_label_issue_data = {
    "channel_id": "CAP9GA5MJ",
    "channel_name": "sysbot-testing",
    "command": "/sysbot_label_issue",
    "response_url": "https://hooks.slack.com/commands/T08C86GE8/411060288517/Aj1nuE1p8x4bEbBRIfQ44hRT",
    "team_domain": "systers-opensource",
    "team_id": "T08C86GE8",
    "text": "sysbot-test 181 [bug, enhancement]",
    "token": "9WMeKrR9ig79X8PY1jGnzkn5",
    "trigger_id": "411060288533.8416220484.49610058e1a1a50a5f8231694862f9b5",
    "user_id": "U7KMRCS5Q",
    "user_name": "f2016165"
}
