from celery.task import Task
from sms.models import Message, Gateway
import logging


class SendMessage(Task):
    """
    Task to send SMS & update the message status on response
    """
    def run(self, message_id, gateway_id=None, **kwargs):
        logging.debug("About to send a message.")

        message = Message.objects.get(pk=message_id)

        if not gateway_id:
            if hasattr(message.billee, 'sms_gateway'):
                gateway = message.billee.sms_gateway
            else:
                gateway = Gateway.objects.all()[0]
        else:
            gateway = Gateway.objects.get(pk=gateway_id)

        response = gateway._send(message)

        logging.debug("Done sending message.")
