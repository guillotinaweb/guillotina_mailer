# -*- coding: utf-8 -*-

app_settings = {
    "mailer": {
        "default_sender": "foo@bar.com",
        "host": "localhost",
        "port": 25,
        "debug": False,
        "utility": "pserver.mailer.utility.MailerUtility"
    }
}


def includeme(root):
    from plone.server import app_settings as main_app_settings
    root.add_async_utility({
        "provides": "pserver.mailer.interfaces.IMailer",
        "factory": main_app_settings['mailer']['utility'],
        "settings": {}
    })
