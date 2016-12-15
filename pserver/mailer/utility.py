# -*- coding: utf-8 -*-
from plone.server import app_settings
from pserver.mailer.interfaces import IMailer
from repoze.sendmail.delivery import DirectMailDelivery
from repoze.sendmail.mailer import SMTPMailer
from zope.interface import implementer
from email.message import Message
from repoze.sendmail import encoding
from email.utils import make_msgid
from email.utils import formatdate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from html2text import html2text
from pprint import pformat

import logging
import smtplib


logger = logging.getLogger(__name__)


@implementer(IMailer)
class MailerUtility(object):

    def __init__(self, settings):
        mailer_settings = self.settings
        host = mailer_settings.get('host', 'localhost')
        port = mailer_settings.get('port', 25)
        self.smtp_mailer = SMTPMailer(
            hostname=host,
            port=port)
        self.direct_delivery = DirectMailDelivery(self.smtp_mailer)

    @property
    def settings(self):
        return app_settings['mailer']

    async def initialize(self, app):
        self.app = app

    def build_message(self, message, text=None, html=None):
        if not text and html and self.settings.get('use_html2text', True):
            try:
                text = html2text(html)
            except:
                pass

        if text is not None:
            message.attach(MIMEText(text, 'plain'))
        if html is not None:
            message.attach(MIMEText(html, 'html'))

    def get_message(self, recipient, subject, sender,
                    message=None, text=None, html=None):
        if message is None:
            message = MIMEMultipart('alternative')
            self.build_message(message, text, html)

        message['Subject'] = subject
        message['From'] = sender
        message['To'] = recipient
        return message

    def send(self, recipient=None, subject=None, message=None,
             text=None, html=None, sender=None):
        if sender is None:
            sender = self.settings.get('default_sender')
        message = self.get_message(recipient, subject, sender, message, text, html)
        return self.direct_delivery.send(sender, [recipient], message)

    def send_immediately(self, recipient=None, subject=None, message=None,
                         text=None, html=None, sender=None, fail_silently=False):
        if sender is None:
            sender = self.settings.get('default_sender')
        message = self.get_message(recipient, subject, sender, message, text, html)
        encoding.cleanup_message(message)
        messageid = message['Message-Id']
        if messageid is None:
            messageid = message['Message-Id'] = make_msgid('repoze.sendmail')
        if message['Date'] is None:
            message['Date'] = formatdate()

        try:
            return self.smtp_mailer.send(sender, [recipient], message)
        except smtplib.socket.error:
            if not fail_silently:
                raise


@implementer(IMailer)
class PrintingMailerUtility(MailerUtility):

    def __init__(self, settings):
        pass

    async def initialize(self, app):
        pass

    def send(self, **kwargs):
        message = self.get_message(**kwargs)
        print('DEBUG MAILER: \n {}'.format(message.as_string()))

    send_immediately = send
