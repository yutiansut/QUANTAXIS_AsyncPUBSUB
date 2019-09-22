import asyncio
from aio_pika import connect_robust, Message
from QAAsyncPubSub.setting import qapubsub_ip, qapubsub_port, qapubsub_user, qapubsub_password


class base_ps():

    def __init__(self, host=qapubsub_ip, port=qapubsub_port, user=qapubsub_user, password=qapubsub_password, channel_number=1, queue_name='', routing_key='default',  exchange='', exchange_type='fanout'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

        self.queue_name = queue_name
        self.exchange = exchange
        self.routing_key = routing_key
        self.exchange_type = exchange_type
        self.channel_number = channel_number
        # fixed: login with other user, pass failure @zhongjy
        credentials = pika.PlainCredentials(
            self.user, self.password, erase_on_connect=True)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, port=self.port,
                                      credentials=credentials, heartbeat=0, socket_timeout=5,
                                      )
        )

        self.channel = self.connection.channel(
            channel_number=self.channel_number)







async def main(loop):
    connection = await connect_robust(
        "amqp://admin:admin@127.0.0.1/",
        loop=loop
    )

    queue_name = "test_queue"
    routing_key = "test_queue"

    # Creating channel
    channel = await connection.channel()

    # Declaring exchange
    exchange = await channel.declare_exchange('direct', auto_delete=True)

    # Declaring queue
    queue = await channel.declare_queue(queue_name, auto_delete=True)

    # Binding queue
    await queue.bind(exchange, routing_key)

    await exchange.publish(
        Message(
            bytes('Hello', 'utf-8'),
            content_type='text/plain',
            headers={'foo': 'bar'}
        ),
        routing_key
    )

    # Receiving message
    incoming_message = await queue.get(timeout=5)

    # Confirm message
    await incoming_message.ack()

    await queue.unbind(exchange, routing_key)
    await queue.delete()
    await connection.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
