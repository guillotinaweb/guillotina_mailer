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


Sending mail
------------

POST http://localhost:8080/zodb/plone/@mailer

    {
      "sender": "foo@bar.com",
      "recipient": "john@doe.com",
      "subject": "Some subject",
      "text": "Hello"
    }


Permissions
-----------

`pserver.mailer` defines a permission `mailer.SendMail` which, by default,
only the `plone.SiteAdmin` role is assigned.


Using the mailer in code
------------------------

You can also directly use the mailer in your code::

    from zope.component import queryUtility
    from pserver.mailer.interfaces import IMailer
    mailer = queryUtility(IMailer)
    mailer.send(recipient='john@doe.com', subject='This is my subject', text='Body of email')
