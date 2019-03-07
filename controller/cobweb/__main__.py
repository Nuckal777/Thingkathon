import asyncio
from itertools import product
from pathlib import Path
import logging
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from . import models
from . import controller


async def send_message(loop, url):
    from aio_pika import connect_robust, Message, DeliveryMode

    connection = await connect_robust(url, loop=loop)
    async with connection:
        channel = await connection.channel()

        message = Message(b'hello world',
                          delivery_mode=DeliveryMode.PERSISTENT)
        await channel.default_exchange.publish(message, routing_key='production')


def fixtures(session):
    apartments = [
        models.Apartment(id=0, name="Haushalt 0"),
        models.Apartment(id=1, name="Haushalt 1"),
        models.Apartment(id=2, name="Haushalt 2"),
        models.Apartment(id=3, name="Haushalt 3"),
    ]
    session.add_all(apartments)

    producers = [
        models.Producer(id=0),
        models.Producer(id=1),
        models.Producer(id=2),
        models.Producer(id=3),
    ]
    session.add_all(producers)

    for a, p in product(apartments, producers):
        ownership = models.Ownership(apartment=a,
                                     producer=p,
                                     percentage=1.0 / len(apartments))
        session.add(ownership)

    storages = [
        models.Storage(id=0, max_capacity=31, apartment=apartments[0]),
        models.Storage(id=1, max_capacity=31, apartment=apartments[1]),
        models.Storage(id=2, max_capacity=31, apartment=apartments[2]),
        models.Storage(id=3, max_capacity=31, apartment=apartments[3]),
    ]
    session.add_all(storages)

    session.commit()


def main():
    engine = create_engine('sqlite:///cobweb.db')
    session_factory = sessionmaker(engine)

    if not Path('cobweb.db').exists():
        models.Model.metadata.create_all(engine)
        fixtures(session_factory())

    loop = asyncio.get_event_loop()
    
    connection = loop.run_until_complete(controller.boot(loop, 'amqp://guest:guest@127.0.0.1/', session_factory))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(connection.close())
        loop.close()


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="%(message)s")
    main()
