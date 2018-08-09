# Channel ids for each repo
repo_vs_channel_id_dict = {
    'sysbot': 'CAEDCBACW',
    'vms': 'C0FSZS007',
    'powerup-iOS': 'C0C9VK8UE',
    'powerup-android': 'C0C9VK8UE',
    'mentorship-backend': 'CAE8QK41L',
    'mentorship-android': 'CAE8QK41L',
    'portal': 'C0FGYV50U',
    'PC-Prep-Kit': 'C35G5QAFQ',
    'pchub': 'C0C9VKA8N',
    'language-translation': 'C0QKAE73K',
    'malaria-app-ios': 'C0BS7FC5U',
    'malaria-app-android': 'C0BS7FC5U',
    'mailman3': 'C0QK5PCNS',
    'systers.github.io': 'C99N86T43',
    'hyperkitty': 'CAU75GQLU',
    'macc': 'C0QJX393L',
    'mailmanclient': 'C0QK5PCNS'
}

# Slack team IDs and names for each channel
slack_team_vs_repo_dict = {
    'CAEDCBACW': ['SAQDWBCE7', 'sysbot-team'],
    'C0FSZS007': ['SBHJSJX0Q', 'vms-team'],
    'C0C9VK8UE': ['SBHJSB516', 'powerup-team'],
    'CAE8QK41L': ['SBJE07D6Z', 'mentorship-team'],
    'C0FGYV50U': ['SA5PHPK7D', 'portal-team'],
    'C35G5QAFQ': ['SBJ11K5FG', 'pc-prep-kit-team'],
    'C0C9VKA8N': ['SBK70EUNS', 'pc-hub-team'],
    'C0QKAE73K': ['SBJ9SJGMQ', 'language-translation-team'],
    'C0BS7FC5U': ['SBJ36LAUC', 'malaria-team'],
    'C0QK5PCNS': ['SBHP9AY5P', 'mailman3-team'],
    'C99N86T43': ['SBKBP1RB9', 'gh-pages-team'],
    'CAU75GQLU': ['SBHP9AY5P', 'mailman3-team'],
    'C0QJX393L': ['SBJ37KL84', 'macc-team']
}

# Projects versus technical stacks
techstack_vs_projects = {
    'HTML': ['slack-systers-opensource', 'vms', 'PC-Prep-Kit', 'systers.github.io', 'portal', 'macc',
             'slack-ghc', 'communities', 'pchub', 'language-translation', 'FirstAide-web'],
    'CSS': ['slack-systers-opensource', 'vms', 'PC-Prep-Kit', 'systers.github.io', 'portal', 'macc',
            'slack-ghc', 'communities', 'pchub', 'language-translation', 'FirstAide-web'],
    'JAVASCRIPT': ['slack-systers-opensource', 'vms', 'PC-Prep-Kit', 'systers.github.io', 'portal',
                   'powerup-story-designer', 'powerup-scenario-builder', 'macc', 'slack-ghc',
                   'communities', 'pchub', 'language-translation'],
    'JAVA': ['powerup-android', 'malaria-app-android', 'volunteers-android', 'conference-android',
             'mentorship-android', 'peacetrack-android', 'realtrack-android', 'FirstAide-Android'],
    'ANDROID': ['powerup-android', 'malaria-app-android', 'volunteers-android', 'conference-android',
                'mentorship-android', 'peacetrack-android', 'realtrack-android', 'FirstAide-Android'],
    'SWIFT': ['powerup-iOS', 'peacetrack-ios', 'realtrack-ios', 'malaria-app-ios', 'conference-iOS',
              'FirstAide-iOS'],
    'IOS': ['powerup-iOS', 'peacetrack-ios', 'realtrack-ios', 'malaria-app-ios', 'conference-iOS',
            'FirstAide-iOS'],
    'ANGULARJS': ['PC-Prep-Kit', 'systers.github.io', 'communities'],
    'WEB DEVELOPMENT': ['PC-Prep-Kit', 'systers.github.io', 'vms', 'hyperkitty', 'portal',
                        'slack-systers-opensource', 'systers.github.io', 'macc', 'postorius',
                        'slack-ghc', 'communities', 'pchub', 'language-translation', 'crowdmap',
                        'FirstAide-web'],
    'PYTHON': ['vms', 'sysbot', 'portal', 'hyperkitty', 'macc', 'postorius', 'mailmanclient',
               'mailman3', 'mentorship-backend'],
    'DJANGO': ['vms', 'portal', 'hyperkitty', 'macc', 'postorius', 'mailman3'],
    'FLASK': ['mentorship-backend', 'sysbot'],
    'NODEJS': ['PC-Prep-Kit', 'systers.github.io'],
    'BOTS': ['sysbot'],
    'RUBY': ['pchub', 'language-translation'],
    'PHP': ['crowdmap', 'FirstAide-web'],
    'MEAN STACK': ['communities', 'systers.github.io']
}

message_key_vs_list_of_alternatives = {
    'systers': ["systers", "systers community"],
    'anita_borg': ["anitab", "anita borg", "anitaborg institution", "anitab.org"],
    'outreachy': ["outreachy"],
    'gsoc_info': ["gsoc", "google summer of code"],
    'gci_info':  ["gci",  "google code-in", "google codein", "google code in"],
    'rgsoc_info': ["rgsoc", "rails girls summer of code"]
}

CHANNEL_LIST = {
    'intro': 'C0CAF47RQ',
    'questions': 'C0S15BFNX',
    'newcomers': 'CAM6T4AGH'
}