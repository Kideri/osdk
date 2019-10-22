from dialog_bot_sdk.bot import DialogBot
import config.core as core_config
import grpc

def on_msg(*params):
    bot.messaging.send_message(
        params[0].peer,
        'I see your message'
    )


if __name__ == '__main__':
    bot = DialogBot.get_secure_bot(
        core_config.endpoint,
        grpc.ssl_channel_credentials(),
        core_config.token,
        verbose=True
    )

    bot.messaging.on_message(on_msg)