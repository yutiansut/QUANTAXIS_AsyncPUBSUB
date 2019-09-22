import asyncio
import aio_pika


async def main(loop):
    connection = await aio_pika.connect_robust(
        "amqp://admin:admin@127.0.0.1/", loop=loop
    )

    async with connection:
        queue_name = "test_queue"

        # Creating channel
        queue_name = "test_queue"
        routing_key = "test_queue"

        # Creating channel
        channel = await connection.channel()

        # Declaring exchange
        exchange = await channel.declare_exchange('tq_test', auto_delete=False)

        # Declaring queue
        queue = await channel.declare_queue(queue_name, auto_delete=True)

        # Binding queue
        await queue.bind(exchange, routing_key)

        async with queue.iterator() as queue_iter:
            # Cancel consuming after __aexit__
            async for message in queue_iter:
                async with message.process():
                    print(message.body)

                    # if queue.name in message.body.decode():
                    #     break


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()