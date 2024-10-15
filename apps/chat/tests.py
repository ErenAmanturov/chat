from channels.testing import WebsocketCommunicator
from channels.testing import ChannelsLiveServerTestCase

# from django.test import TestCase

from config.asgi import application

from apps.user.models import User


class ChatTestCase(ChannelsLiveServerTestCase):
    def setUp(self):
        self.user = User.objects.create(phone_number='+996500800263', password='123')
    
    async def test_authenticated_connection(self):

        self.client.login(phone_number='+996500800263', password='123')

        communicator = WebsocketCommunicator(application, "ws/chat/testroom/")
        connected, supprotocol = await communicator.connect()

        self.assertTrue(connected)

        await communicator.send_json_to({
            'message': "test message"
        })

        response = await communicator.receive_json_from()

        self.assertEqual(response['message'], 'test message')

        await communicator.disconnect()

    async def test_unauthenticated_connection(self):
        communicator = WebsocketCommunicator(application, 'ws/chat/testroom/')

        connected, subprotocol = await communicator.connect()

        self.assertFalse(connected)

        await communicator.disconnect()
