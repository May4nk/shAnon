import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import Suser,Messages,Chat

class ChatConsumer(AsyncConsumer):
    
    async def websocket_connect(self,e):
        print('connect',e)
        usr = self.scope['user']
        chat_room = f'user_chatroom_{usr.id}'
        self.chat_room = chat_room
        
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        
        await self.send({
            'type':'websocket.accept'
        })
    
    
    async def websocket_receive(self,event):
        print('receive',event)
        received_data = json.loads(event['text'])
        msg = received_data.get('message')
        sent_by = received_data.get('sent_by')
        sent_to = received_data.get('sent_to')
        
        if not msg:
            print('Error:msg')
            return False

        sent_by_user = await self.get_usr(sent_by)
        sent_to_user = await self.get_usr(sent_to)
        thread_obj = await self.get_thread(sent_by,sent_to)
        
        if not sent_to_user:
            print('Error:sent_to_user')
        
        if not sent_by_user:
            print('Error:sent_by_user')

        await self.create_msg(thread_obj,sent_by_user,msg)
        other_user_croom = f'user_chatroom_{sent_to}'
        self_user = self.scope['user']

        response = {
            'message': msg,
            'sent_by': self_user.id,
        }

        await self.channel_layer.group_send(
            other_user_croom,
            {
                'type': 'chat_message',
                'text': json.dumps(response),
            }
        )
        
        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response),
            }
        )

    
    async def websocket_disconnect(self,e):
        print('disconnect',e)

    async def chat_message(self,e):
        print('chat_message',e)
        await self.send({
            'type': 'websocket.send',
            'text': e['text']
            })


    @database_sync_to_async
    def get_usr(self,user_id):
        q = Suser.objects.filter(id=user_id)
        if q.exists():
            obj = q.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def get_thread(self,usr_id,usr):
        qs = Chat.objects.get(first=usr_id,second=usr).id
        q = Chat.objects.get(id=qs)
        return q
    
    @database_sync_to_async
    def create_msg(self,thread,usr,msg):
        Messages.objects.create(thread=thread,usr=usr,message=msg)
