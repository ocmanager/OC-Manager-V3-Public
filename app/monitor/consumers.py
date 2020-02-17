from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
import time
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print('HOLAAAA')
        time.sleep(3)
        self.room_name = '123'
        print(self.room_name)
        self.room_group_name = 'monitor_%s' % self.room_name
        print(self.room_group_name)
        # # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        print('ERRORRRRRR')
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))