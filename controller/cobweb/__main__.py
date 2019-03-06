import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Model
from . import controller


async def send_message(loop, url):
    from aio_pika import connect_robust, Message, DeliveryMode

    connection = await connect_robust(url, loop=loop)
    async with connection:
        channel = await connection.channel()

        message = Message(b'hello world',
                          delivery_mode=DeliveryMode.PERSISTENT)
        await channel.default_exchange.publish(message, routing_key='production')


def main():
    engine = create_engine('sqlite:///cobweb.db')
    Model.metadata.create_all(engine)

    session_factory = sessionmaker(engine)
    loop = asyncio.get_event_loop()
    
    connection = loop.run_until_complete(controller.boot(loop, 'amqp://guest:guest@127.0.0.1/', session_factory))

    try:
        # loop.run_until_complete(send_message(loop, 'amqp://guest:guest@127.0.0.1/'))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(connection.close())
        loop.close()


if __name__ == '__main__':
    main()
