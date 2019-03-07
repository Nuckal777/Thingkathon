import aio_pika
import struct
from functools import wraps
import datetime
from . import models


external_price = 0.29


def cal_internal_price():
    return 0.08


async def on_production(message, session):
    producer_id, energy, nanosecs = struct.unpack('!IdQ', message.body)
    timestamp = datetime.datetime.fromtimestamp(nanosecs / 1e9)

    producer = session.query(models.Producer).get(producer_id)

    if producer is None:
        message.nack()
        return

    production = models.Production(energy=energy,
                                   price=cal_internal_price(),
                                   time=timestamp,
                                   producer=producer)
    session.add(production)
    session.commit()

    message.ack()


async def on_consumption(message, session):
    apartment_id, energy, nanosecs = struct.unpack('!IdQ', message.body)
    timestamp = datetime.datetime.fromtimestamp(nanosecs / 1e9)

    apartment = session.query(models.Apartment).get(apartment_id)

    if apartment is None:
        message.nack()
        return

    consumption = models.Consumption(energy=energy,
                                     time=timestamp,
                                     origin='external',
                                     price=0.29,
                                     apartment=apartment)
    session.add(consumption)
    session.commit()

    message.ack()


async def on_storage_status(message, session):
    storage_id, capacity, nanosecs = struct.unpack('!IdQ', message.body)
    timestamp = datetime.datetime.fromtimestamp(nanosecs / 1e9)

    storage = session.query(models.Storage).get(storage_id)

    if storage is None:
        message.nack()
        return

    storage.capacity += capacity

    # Update price (value) of storage depending on the source of the current
    if storage.source == 'external':
        storage.price += external_price * capacity
    else:
        storage.price += cal_internal_price() * capacity

    charge = models.Charge(capacity=capacity,
                           time=timestamp,
                           storage=storage)
    session.add(charge)
    session.commit()

    message.ack()


def wrap_session(func, session_factory):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs, session=session_factory())
    return wrapper


async def boot(loop, amqp, session_factory):
    # Open connection
    connection = await aio_pika.connect_robust(amqp, loop=loop)

    # Create channel
    channel = await connection.channel()

    # Declare all queues
    producer = await channel.declare_queue('producer',
                                             durable=True,
                                             auto_delete=True)
    consumption = await channel.declare_queue('consumption',
                                             durable=True,
                                             auto_delete=True)
    storage_status = await channel.declare_queue('storage_status',
                                             durable=True,
                                             auto_delete=True)
    # change_charge = await channel.declare_queue('change_charge',
    #                                          durable=True,
    #                                          auto_delete=True)

    # Register message handlers
    await producer.consume(wrap_session(on_production, session_factory))
    await consumption.consume(wrap_session(on_consumption, session_factory))
    await storage_status.consume(wrap_session(on_storage_status, session_factory))
    # await change_charge.consume(wrap_session(on_change_charge, session_factory))

    return connection
