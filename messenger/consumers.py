from channels.generic.websocket import WebsocketConsumer
from messenger.models import ChatRoom, ChatroomMessage
from django.shortcuts import get_object_or_404
from .serializers import ChatroomMessageSerializer
from asgiref.sync import async_to_sync
import json
import logging

# Configuration du logger
logger = logging.getLogger(__name__)

class ChatRoomConsumer(WebsocketConsumer):

    def connect(self):
        print("Tentative de connexion WebSocket.")
        try:
            self.user = self.scope['user']
            self.chatroom_name = self.scope['url_route']['kwargs']['chatroom__name']
            self.chatroom = get_object_or_404(ChatRoom, name=self.chatroom_name)

            print(f"Utilisateur: {self.user}, Chatroom: {self.chatroom_name}")

            if not self.user.is_authenticated:
                print(f"Utilisateur non authentifié pour le salon {self.chatroom_name}")
                logger.warning(f"Tentative de connexion non authentifiée pour le salon {self.chatroom_name}")
                self.close(code=4001)
                return

            if self.user not in self.chatroom.members.all():
                print(f"L'utilisateur {self.user.username} n'est pas membre du salon {self.chatroom_name}")
                logger.warning(f"L'utilisateur {self.user.username} n'est pas membre du salon {self.chatroom_name}")
                self.close(code=4002)
                return

            async_to_sync(self.channel_layer.group_add)(
                self.chatroom_name, self.channel_name
            )
            self.accept()
            print(f"Connexion WebSocket établie pour l'utilisateur {self.user.username} dans le salon {self.chatroom_name}")
            logger.info(f"Connexion WebSocket établie pour l'utilisateur {self.user.username} dans le salon {self.chatroom_name}")

        except Exception as e:
            print(f"Erreur lors de la connexion WebSocket: {str(e)}")
            logger.error(f"Erreur lors de la connexion WebSocket: {str(e)}")
            self.close(code=4000)

    def receive(self, text_data=None, bytes_data=None):
        print("Réception d'un message WebSocket.")
        try:
            text_data_json = json.loads(text_data)
            sender = self.user
            msg_type = text_data_json.get('type', 'text')
            content = text_data_json.get('content', None)

            print(f"Message reçu : {content} de {sender}")

            message = ChatroomMessage.objects.create(
                sender=sender,
                type=msg_type,
                content=content,
                chatroom=self.chatroom
            )
            self.update_last_message(message)
            
            event = {
                'type': 'message_handler',
                'message_pk': message.pk
            }
            async_to_sync(self.channel_layer.group_send)(
                self.chatroom_name, event
            )

        except Exception as e:
            print(f"Erreur lors de la réception du message: {str(e)}")
            logger.error(f"Erreur lors de la réception du message: {str(e)}")

    def message_handler(self, event):
        print("Traitement d'un message WebSocket.")
        try:
            message_pk = event['message_pk']
            message = ChatroomMessage.objects.get(pk=message_pk)
            serialized = ChatroomMessageSerializer(message).data
            self.send(text_data=json.dumps({
                'message': serialized
            }))
            print(f"Message envoyé : {serialized}")
        except Exception as e:
            print(f"Erreur lors du traitement du message: {str(e)}")
            logger.error(f"Erreur lors du traitement du message: {str(e)}")

    def disconnect(self, close_code):
        print(f"Tentative de déconnexion WebSocket. Code de fermeture: {close_code}")
        try:
            async_to_sync(self.channel_layer.group_discard)(
                self.chatroom_name, self.channel_name
            )
            print(f"Déconnexion WebSocket pour l'utilisateur {self.user.username} du salon {self.chatroom_name}. Code: {close_code}")
            logger.info(f"Déconnexion WebSocket pour l'utilisateur {self.user.username} du salon {self.chatroom_name}. Code: {close_code}")
        except Exception as e:
            print(f"Erreur lors de la déconnexion: {str(e)}")
            logger.error(f"Erreur lors de la déconnexion: {str(e)}")

    def update_last_message(self, message):
        print("Mise à jour du dernier message du salon.")
        try:
            self.chatroom.last_message = {
                'content': message.content,
                'created_at': message.created_at.isoformat(),
                'type': message.type
            }
            self.chatroom.last_message_by = message.sender
            self.chatroom.save()
            print(f"Dernier message mis à jour : {message.content}")
        except Exception as e:
            print(f"Erreur lors de la mise à jour du dernier message: {str(e)}")
            logger.error(f"Erreur lors de la mise à jour du dernier message: {str(e)}")
