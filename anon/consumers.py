import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import Suser

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print('connected',event)
        usr = self.scope['user']
        chat_room = f'user_chatroom_{usr.id}'
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name,
                )
        await self.send({
                'type': 'websocket.accept'
            })

    async def websocket_receive(self,event):
        print('receive',event)
        received = json.loads(event['text'])
        msg = received.get('message')
        send_by_id = received.get('send_by')
        send_to_id = received.get('send_to')
        if not msg:
            print('Error')
            return False
        sent_by_user = await self.get_user_objects(send_by_id)
        sent_to_user = await self.get_user_objects(send_to_id)
        if not sent_by_user:
            print('Errorhey')
        other_user_chat_room = f'user_chatroom_{send_to_id}'
        self_user= self.scope['user']
        response={
            'message':msg,
            'sent_by':self_user.id
                }

        await self.channel_layer.group_send(
                other_user_chat_room,
                {
                    'type':'chat_message',
                    'text':json.dumps(response)
                }
            )
        await self.channel_layer.group_send(
                self.chat_room,
                {
                    'type':'chat_message',
                    'text':json.dumps(response)
                }
            )

    async def websocket_disconnect(self,event):
        print('disconnected',event)

    async def chat_message(self,event):
        print('chat_message',event)
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
            })


    @database_sync_to_async
    def get_user_objects(self, user_id):
        qs = Suser.objects.filter(id=user_id)
        if qs.exists():
            obj= qs.first()
        else:
            obj = None
        return obj
