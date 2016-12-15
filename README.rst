.. contents::

PSERVER.MAILER
==============


Configuration
-------------

config.json can include mailer section::

    "applications": ["pserver.mailer"],
    "mailer": {
      "default_sender": "foo@bar.com",
      "host": "localhost",
      "port": 25
    }


Printing mailer
---------------

For development/debugging, you can use a console print mailer::

    "applications": ["pserver.mailer"],
    "mailer": {
      "default_sender": "foo@bar.com",
      "host": "localhost",
      "port": 25,
      "utility": "pserver.mailer.utility.PrintingMailerUtility"
    }
