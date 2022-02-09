import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

class PodcastStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print(self.room_name)
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data=None,bytes_data=None):
        print("room name : ",self.room_name)
        print("room grup name : ",self.room_group_name)
        if text_data != None :
            print(type(text_data))
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            username = text_data_json['username']
            channel_name = text_data_json['channel_name']
            audio_name = text_data_json['audio_name']

            if message == 'play':
                filename = 'Playlist/'+channel_name+'/'+audio_name+'.mp3'
                BUFFER_SIZE = 1048576
                with open(filename, "rb") as wf:
                    while True:
                        bytes_read = wf.read(BUFFER_SIZE)
                        if not bytes_read:
                            break
                        await self.channel_layer.group_send(
                            self.room_group_name,
                            {
                                'type': 'audio_stream',
                                'audio': bytes_read,
                            }
                        )
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chatroom_message',
                        'message': 'eof',
                        'username': username,
                    }
                )
            else :
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chatroom_message',
                        'message': message,
                        'username': username,
                    }
                )
        elif bytes_data != None :
            print(type(bytes_data))
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'audio_stream',
                    'audio': bytes_data,
                }
            )

    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    async def audio_stream(self, event):
        audio = event['audio']

        await self.send(bytes_data=audio
        )

class PodcastStudioConsumer(AsyncWebsocketConsumer):
    pass