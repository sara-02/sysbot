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
