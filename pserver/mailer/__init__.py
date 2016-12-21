# -*- coding: utf-8 -*-

app_settings = {
    "mailer": {
        "default_sender": "foo@bar.com",
        "host": "localhost",
        "port": 25,
        "debug": False,
        "utility": "pserver.mailer.utility.MailerUtility",
        "use_html2text": True,
        "domain": None
    }
}


def includeme(root, settings):
    utility = settings.get('mailer', {}).get('utility',
                                             app_settings['mailer']['utility'])
    root.add_async_utility({
        "provides": "pserver.mailer.interfaces.IMailer",
        "factory": utility,
        "settings": settings.get('mailer', {})
    })
