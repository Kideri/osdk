from dialog_bot_sdk.bot import DialogBot
import grpc

token = 'f066f5dc53d0daf380533825fca65e67f6baebf1'
endpoint = 'hackathon-mob.transmit.im'
bot = DialogBot.get_secure_bot(
    endpoint,
    grpc.ssl_channel_credentials(),
    token,
    verbose=True
)

DBHOST = 'localhost'
BDPORT = 27017
DBNAME = 'bot3'