from plone.server.api.service import Service
from zope.component import queryUtility
from pserver.mailer.interfaces import IMailer
from plone.server.browser import Response


class SendMail(Service):

    async def __call__(self):
        import pdb; pdb.set_trace()
        data = await self.request.json()
        mailer = queryUtility(IMailer)
        mailer.send(**data)
        return Response(response={}, status=204)