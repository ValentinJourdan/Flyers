from Flow.models import Event
from django import template
import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from django.utils.timesince import timesince
from .models import Message, Room
register = template.Library()


# @register.filter(user_name='initials')
# def initials(value):
#     initials = ''

#     for name in value.split(' '):
#         if name and len(initials) < 3:
#             initials += name[0].upper()

#     return initials


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.eId = self.scope['url_route']['kwargs']['eId']
        self.group_event_id = f'chat_{self.eId}'
        user = self.scope['user']
        user_id = user.id if user.is_authenticated else None
        await self.accept()

        await self.get_room()
        await self.channel_layer.group_add(self.group_event_id, self.channel_name)
        await self.send(text_data=json.dumps({'user_id': user_id}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_event_id, self.channel_name)

    async def receive(self, text_data):
        # receive message from websocket
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        message = text_data_json['message']
        user = self.scope['user']
        user_name = user.username

        print('Receive', type)
# PAS OUBLIER D'ENVOYER DEPUIS LE FRONTEND L'ID DE L'UTILISATEUR CONNECTE !
# typiquement : { "content": "Contenu du message","user_id": 123 // Identifiant de l'utilisateur
        if type == 'message':
            new_message = await self.create_message(user_name, user, message)
            await self.channel_layer.group_send(
                self.group_event_id, {
                    'type': 'chat_message',
                    'message': message,
                    'user_name': user_name,
                    'created_at': timesince(new_message.created_at)}
            )

        elif type == 'image':
            await self.channel_layer.group_send(
                self.group_event_id, {
                    'type': 'chat_image',
                    'image': message,
                    'user_name': user_name, }
            )

        elif type == 'notification':
            await self.channel_layer.group_send(
                self.group_event_id, {
                    'type': 'chat_notification',
                    'notification': message,
                    'user_name': user_name, }
            )

        elif type == 'create_poll':
            # Code pour créer un sondage et l'envoyer à la chatroom
            await self.send(text_data=json.dumps({
                'type': 'poll_created',
                # Autres données du sondage
            }))

        elif type == 'vote':
            # Code pour enregistrer le vote et mettre à jour les résultats du sondage
            await self.send(text_data=json.dumps({
                'type': 'vote_updated',
                # Données mises à jour du sondage
            }))

        elif type == 'update':
            print('is update')
            await self.channel_layer.group_send(
                self.group_event_id, {
                    'type': 'writting_active',
                    'message': message,
                    'user_name': user_name,
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message'],
            'user_name': event['user_name'],
            'created_at': event['created_at']
        }))

    async def chat_image(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'image': event['image'],
            'user_name': event['user_name'],
        }))

    async def chat_notification(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message'],
            'user_name': event['user_name'],
            'initials': event['initials'],
        }))

    async def poll_created(self, event):
        # Envoyer les détails du sondage aux clients dans la chatroom
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'question': event['question'],
            'options': event['options'],  # LIST
            # Autres données du sondage
        }))

    async def vote_updated(self, event):
        # Envoyer les résultats mis à jour du sondage aux clients dans la chatroom
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'sondage_id': event['sondage_id'],
            'results': event['results'],
            # Autres données mises à jour du sondage
        }))

    async def writting_active(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message'],
            'user_name': event['user_name'],

        }))

    @sync_to_async
    def get_room(self):
        self.room = Room.objects.get(eId=self.eId)

    @sync_to_async
    def create_message(self, user_name, user, mess):
        message = Message.objects.create(
            body=mess, sent_by=user_name, created_by=user)
        self.room.messages.add(message)
        return message


# user_name -> nom du sender /
#!!!!LORS DE L'ENVOI DE MESSAGES : récupérer le nom du groupe !


# def get_connected_members(request):
#     # Récupérer les membres connectés au groupe de la salle de chat
#     channel_layer = get_channel_layer()
#     eId = "eId"
#     connected_members = async_to_sync(channel_layer.group_channels)(eId)

#     # Vous pouvez formater les informations des membres connectés comme nécessaire
#     members_info = []
#     for channel_name in connected_members:
#         # Extraire les informations des membres connectés
#         # Par exemple, vous pouvez obtenir l'ID de l'utilisateur à partir du channel_name
#         # et récupérer les détails de l'utilisateur pour l'affichage
#         # Ajoutez ces informations à la liste members_info
#         user_id = ...  # Extraire l'ID utilisateur du channel_name
#         user_info = ...
