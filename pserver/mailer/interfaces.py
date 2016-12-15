from zope.interface import Interface


class IMailer(Interface):
    """
    """
    def __init__(settings):
        pass

    async def initialize(app):
        pass

    def send(*message):
        pass

    def send_immediately(*message, fail_silently=False):
        pass
