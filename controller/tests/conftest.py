import sys
import os
sys.path.append(os.getcwd())

import pytest
import aio_pika
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cobweb.models import Model



@pytest.fixture(scope='function')
def engine():
    return create_engine('sqlite://')


@pytest.fixture(scope='function')
def session_factory(engine):
    Model.metadata.create_all(engine)
    return sessionmaker(engine)


@pytest.fixture(scope='module')
def amq_url():
    yield 'amqp://guest:guest@127.0.0.1/'


@pytest.fixture(scope='function')
async def channel(event_loop, amq_url):
    connection = await aio_pika.connect_robust(amq_url, loop=event_loop)

    async with connection:
        channel = await connection.channel()
        yield channel
