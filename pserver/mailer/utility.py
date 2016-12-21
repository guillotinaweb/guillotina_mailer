# -*- coding: utf-8 -*-
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from html2text import html2text
from plone.server import app_settings
from plone.server.async import QueueUtility
from plone.server.utils import get_random_string
from pserver.mailer.interfaces import IMailer
from repoze.sendmail import encoding
from zope.interface import implementer

import aiosmtplib
import asyncio
import logging
import smtplib
import socket
import time


logger = logging.getLogger(__name__)


@implementer(IMailer)
class MailerUtility(QueueUtility):

    def __init__(self, settings):
        self._settings = settings
        super(MailerUtility, self).__init__(settings)
        self.smtp_mailer = self.get_smtp_mailer()

    @property
    def settings(self):
        settings = app_settings.get('mailer', {})
        settings.update(self._settings.get('mailer', {}))
        return settings

    async def _send(self, sender, recipients, message, retry=False):
        try:
            return await self.smtp_mailer.sendmail(sender, recipients, message.as_string())
        except aiosmtplib.errors.SMTPServerDisconnected:
            if retry:
                # we only retry once....
                # we could manage a retry queue and wait until server becomes
                # active if it is down...
                raise
            await self.connect()
            return await self._send(sender, recipients, message, retry=True)

    def get_smtp_mailer(self):
        mailer_settings = self.settings
        host = mailer_settings.get('host', 'localhost')
        port = mailer_settings.get('port', 25)
        self._exceptions = False
        return aiosmtplib.SMTP(hostname=host, port=port)

    async def connect(self):
        return await self.smtp_mailer.connect()

    async def initialize(self, app):
        self.app = app
        await self.connect()
        while True:
            got_obj = False
            try:
                priority, _, args = await self._queue.get()
                got_obj = True
                try:
                    await self._send(*args)
                except Exception as exc:
                    logger.error('Error sending mail', exc_info=True)
            except KeyboardInterrupt or MemoryError or SystemExit or asyncio.CancelledError:
                self._exceptions = True
                raise
            except:  # noqa
                self._exceptions = True
                logger.error('Worker call failed', exc_info=True)
            finally:
                if got_obj:
                    self._queue.task_done()

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
                    message=None, text=None, html=None, message_id=None):
        if message is None:
            message = MIMEMultipart('alternative')
            self.build_message(message, text, html)

        message['Subject'] = subject
        message['From'] = sender
        message['To'] = recipient
        if message_id is not None:
            message['Message-Id'] = message_id
        else:
            message['Message-Id'] = self.create_message_id()
        return message

    async def send(self, recipient=None, subject=None, message=None,
                   text=None, html=None, sender=None, message_id=None, priority=3):
        if sender is None:
            sender = self.settings.get('default_sender')
        message = self.get_message(recipient, subject, sender, message, text,
                                   html, message_id=message_id)
        await self._queue.put((priority, time.time(), (sender, [recipient], message)))

    async def send_immediately(self, recipient=None, subject=None, message=None,
                               text=None, html=None, sender=None, message_id=None,
                               fail_silently=False):
        if sender is None:
            sender = self.settings.get('default_sender')
        message = self.get_message(recipient, subject, sender, message, text,
                                   html, message_id=message_id)
        encoding.cleanup_message(message)
        if message['Date'] is None:
            message['Date'] = formatdate()

        try:
            return await self._send(sender, [recipient], message)
        except smtplib.socket.error:
            if not fail_silently:
                raise

    def create_message_id(self, _id=''):
        domain = self.settings['domain']
        if domain is None:
            domain = socket.gethostname()
        if not _id:
            _id = '%s-%s' % (str(time.time()), get_random_string(20))
        return '<%s@%s>' % (_id, domain)


@implementer(IMailer)
class PrintingMailerUtility(MailerUtility):

    def __init__(self, settings):
        self._queue = asyncio.Queue()
        self._settings = settings

    async def connect(self):
        pass

    async def _send(self, sender, recipients, message):
        print('DEBUG MAILER: \n {}'.format(message.as_string()))
