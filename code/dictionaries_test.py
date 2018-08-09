# Channel ids for each repo
repo_vs_channel_id_dict = {
    'sysbot': 'CBW0C9Z7B',
    'vms': 'CBXHS9TEK',
    'powerup-iOS': 'CBWCRP22X',
    'powerup-android': 'CBWCRP22X',
    'mentorship-backend': 'CBXHSJNMV',
    'mentorship-android': 'CBXHSJNMV',
    'portal': 'CBVR34LMN',
    'PC-Prep-Kit': 'CBWCSAY67',
    'pchub': 'CBVR3C7L0',
    'language-translation': 'CBW9KR3U4',
    'malaria-app-ios': 'CBWLTJ8LV',
    'malaria-app-android': 'CBWLTJ8LV',
    'mailman3': 'CBWLTMCTX',
    'systers.github.io': 'CBWGRSJPL',
    'hyperkitty': 'CBW9MNM5J',
    'macc': 'CBVR51TBJ',
    'mailmanclient': 'CBWLTMCTX'
}

# Slack team IDs and names for each channel
slack_team_vs_repo_dict = {
    'CBW0C9Z7B': ['SAQDWBCE7', 'sysbot-team'],
    'CBXHS9TEK': ['SBHJSJX0Q', 'vms-team'],
    'CBWCRP22X': ['SBHJSB516', 'powerup-team'],
    'CBXHSJNMV': ['SBJE07D6Z', 'mentorship-team'],
    'CBVR34LMN': ['SA5PHPK7D', 'portal-team'],
    'CBWCSAY67': ['SBJ11K5FG', 'pc-prep-kit-team'],
    'CBVR3C7L0': ['SBK70EUNS', 'pc-hub-team'],
    'CBW9KR3U4': ['SBJ9SJGMQ', 'language-translation-team'],
    'CBWLTJ8LV': ['SBJ36LAUC', 'malaria-team'],
    'CBWLTMCTX': ['SBHP9AY5P', 'mailman3-team'],
    'CBWGRSJPL': ['SBKBP1RB9', 'gh-pages-team'],
    'CBW9MNM5J': ['SBHP9AY5P', 'mailman3-team'],
    'CBVR51TBJ': ['SBJ37KL84', 'macc-team']
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
    'PHP': ['crowdmap', 'FirstAide-web']
}

message_key_vs_list_of_alternatives = {
    'systers': ["systers", "systers community"],
    'anita_borg': ["anitab", "anita borg", "anitaborg institution", "anitab.org"],
    'outreachy': ["outreachy"],
    'gsoc_info': ["gsoc", "google summer of code"],
    'gci_info': ["gci", "google code-in", "google codein", "google code in"],
    'rgsoc_info': ["rgsoc", "rails girls summer of code"]
}

CHANNEL_LIST = {
    'intro': 'CC5PCAX6K',
    'questions': 'CC5PCK6MV',
    'newcomers': 'CC5PDJVFH'
}
