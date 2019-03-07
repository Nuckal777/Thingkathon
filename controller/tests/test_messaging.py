import asyncio
import datetime
import pytest
import struct
from aio_pika import Message, DeliveryMode
from cobweb.controller import boot
from cobweb.models import Production, Producer, Apartment, Consumption, Storage, Charge


@pytest.mark.asyncio
async def test_on_production(event_loop, amq_url, session_factory, channel):
    session = session_factory()
    session.add(Producer(id=2))
    session.commit()

    connection = await boot(event_loop, amq_url, session_factory)

    payload = (b'\x00\x00\x00\x02\x40\x27\x89\xb2\x9a\x92\x4b\x15'
               b'\x15\x89\x16\x99\xee\x91\x1f\x76')

    message = Message(payload,
                      delivery_mode=DeliveryMode.PERSISTENT)

    await channel.default_exchange.publish(message, routing_key='producer')
    await asyncio.sleep(0.1)

    prod = session.query(Production).first()
    assert prod is not None

    assert prod.producer_id == 2
    assert prod.energy == 11.76894076381499
    assert prod.time == datetime.datetime.fromtimestamp(1551796396994142070 / 1e9)

    await connection.close()


@pytest.mark.asyncio
async def test_on_consumption(event_loop, amq_url, session_factory, channel):
    now = datetime.datetime.now()
    apartment_id = 1
    energy = 2.0

    session = session_factory()
    session.add(Apartment(id=1, name="Apartment 1"))
    session.commit()

    payload = struct.pack('!IdQ', apartment_id, energy, int(now.timestamp() * 1e9))
    message = Message(payload, delivery_mode=DeliveryMode.PERSISTENT)

    connection = await boot(event_loop, amq_url, session_factory)
    await channel.default_exchange.publish(message, routing_key='consumption')
    await asyncio.sleep(0.1)
    await connection.close()

    consumption = session.query(Consumption).first()
    assert consumption is not None

    assert consumption.apartment_id == 1
    assert consumption.energy == 2.0
    assert consumption.time == now


@pytest.mark.asyncio
async def test_on_storage_status(event_loop, amq_url, session_factory, channel):
    now = datetime.datetime.now()
    storage_id = 1
    capacity = 0.25

    session = session_factory()
    session.add(Apartment(id=1, name="Apartment 1"))
    session.add(Storage(id=storage_id,
                        max_capacity=10,
                        capacity=0,
                        source='external',
                        price=0,
                        apartment_id=1))
    session.commit()

    payload = struct.pack('!IdQ', storage_id, capacity, int(now.timestamp() * 1e9))
    message = Message(payload, delivery_mode=DeliveryMode.PERSISTENT)

    connection = await boot(event_loop, amq_url, session_factory)
    await channel.default_exchange.publish(message, routing_key='storage_status')
    await asyncio.sleep(0.1)
    await connection.close()

    charge = session.query(Charge).first()
    assert charge is not None

    assert charge.storage_id == storage_id
    assert charge.capacity == capacity
    assert charge.time == now

    storage = session.query(Storage).get(storage_id)
    assert storage.capacity == capacity
    assert storage.price == 0.29 * capacity
