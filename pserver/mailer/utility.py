# -*- coding: utf-8 -*-
from plone.server import app_settings
from pserver.mailer.interfaces import IMailer
from repoze.sendmail.delivery import DirectMailDelivery
from repoze.sendmail.mailer import SMTPMailer
from zope.interface import implementer

import logging
import smtplib
import transaction


logger = logging.getLogger(__name__)


@implementer(IMailer)
class PrintingMailerUtility(object):
    def send(self, *message):
        print('DEBUG MAILER: \n {}'.format(message))

    def send_immediately(self, *message, fail_silently=False):
        print('DEBUG MAILER: \n {}'.format(message))


@implementer(IMailer)
class MailerUtility(object):

    def __init__(self, settings):
        mailer_settings = self.settings
        host = mailer_settings.get('host', 'localhost')
        port = mailer_settings.get('port', 25)
        self.smtp_mailer = SMTPMailer(
            hostname=host,
            port=port)
        self.direct_delivery = DirectMailDelivery(
            self.smtp_mailer, transaction_manager=transaction.manager)

    @property
    def settings(self):
        return app_settings['mailer']

    async def initialize(self, app):
        self.app = app

    def send(self, *message):
        return self.direct_delivery.send(*message)

    def send_immediately(self, *message, fail_silently=False):
        try:
            return self.smtp_mailer.send(*message)
        except smtplib.socket.error:
            if not fail_silently:
                raise
