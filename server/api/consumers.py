import json

from channels.generic.websocket import WebsocketConsumer

from asgiref.sync import async_to_sync

from .models import Game, Player


class LobbyConsumer(WebsocketConsumer):

    def connect(self):
        
        self.player = Player.objects.get(pk=self.scope['user'].pk)
        self.game = self.player.game.first()
        self.game_group_name = str(self.game.pk)
        async_to_sync(self.channel_layer.group_add)(
            self.game_group_name,
            self.channel_name
        )

        self.accept()
        if self.game.status == "started":
            async_to_sync(self.channel_layer.group_send)(
                self.game_group_name,
                {
                    "type" : "status",
                    "status" : self.game.status
                }
            )
        

    def status(self, event):
        type = event["type"]
        status = event["status"]
        self.send(json.dumps({
            "type" : type,
            "status" : status
        }))



        