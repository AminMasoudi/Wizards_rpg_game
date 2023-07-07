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
        
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        if text_data_json["type"] == "submit":
            self.player.last_action = text_data_json["action"]
            self.player.save()
            # check for both results
            l = self.game.player.all()
            p1 = l[0]
            p2 = l[1]
            if p1.last_action and p2.last_action :
                p1.calculate(p2)                    
                p2.calculate(p1)                    
                p1.last_action = ""
                p2.last_action = ""
                p1.save()
                p2.save()
                async_to_sync(self.channel_layer.group_send)(
                    str(self.game.pk),
                    {
                        "type" : "status",
                        "status": "new"
                    }
                )


        



    def status(self, event):
        type = event["type"]
        status = event["status"]
        self.send(json.dumps({
            "type" : type,
            "status" : status
        }))


