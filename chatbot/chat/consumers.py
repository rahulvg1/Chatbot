import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .views import respond_to_websockets
from .models import ChatUsers

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = 'test-chat'
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

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
        message = text_data_json
        if(message['command']=='send'):
        # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'text': message['text']
                }
            )

    # Receive message from room group
    def chat_message(self, message):

        message_to_send_content = {
        'text': message['text'],
        'type': 'text',
        'source': 'CANDIDATE'
        }

        Chat_User_Current = ChatUsers.objects.get(User='User')
        
        if(message['text']=='fat'):
            Chat_User_Current.FatCalls +=1
            Chat_User_Current.save()
        elif(message['text']=='stupid'):
            Chat_User_Current.StupidCalls +=1
            Chat_User_Current.save()
        elif(message['text']=='dumb'):
            Chat_User_Current.DumbCalls +=1
            Chat_User_Current.save()
        self.send(text_data=json.dumps(message_to_send_content))

        response = respond_to_websockets(
            message
        )

        response['source'] = 'BOT'
        self.send(text_data=json.dumps(response))
