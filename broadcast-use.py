import asyncio
from graia.broadcast import Broadcast, BaseEvent, BaseDispatcher, DispatcherInterface
from loguru import logger
from graia.application.logger import LoggingLogger
from fastapi import FastAPI
from pydantic.networks import stricturl
loop = asyncio.get_event_loop()
lg = LoggingLogger()

broadcast = Broadcast(loop=loop)


class ExampleEvent(BaseEvent):
    class Dispatcher(BaseDispatcher):
        @staticmethod
        async def catch(interface):
            if interface.annotation is int:
                return 1


class ExampleDispatcher(BaseDispatcher):
    def __init__(self, text: str):
        self.text = text

    async def catch(self, interface: DispatcherInterface):
        if interface.name == "brain_power":
            return "OOOOOOOOOAAAAEEAAE"


@broadcast.receiver("ExampleEvent", dispatchers=[
    ExampleDispatcher('brain_power')
])
def test_func(brain_power: int):
    logger.info(f"brain_power={brain_power}")


class Hi(BaseEvent):
    class Dispatcher(BaseDispatcher):
        async def catch(self, interface: DispatcherInterface):
            pass


@broadcast.receiver(Hi)
async def qwq(hi: Hi):
    logger.info('Hi Event Receiver qwq Got Event')

    print(hi)


@broadcast.receiver(Hi)
async def owo():
    logger.info('Hi Event Receiver owo Got Event')

'''
for i in [0, 0, 0, 0, 0]:
    broadcast.postEvent(Hi())
    broadcast.postEvent(ExampleEvent())
'''


app = FastAPI()


@app.get('/api/event/new')
async def _1(event_name: str):
    events = {'ExampleEvent': ExampleEvent,
              'Hi': Hi
            }
    try:
        broadcast.postEvent(events[event_name]())
        return {event_name: 'Event Posted'}
    except Exception as e:
        return str(e)


@app.get('/api/event/find')
async def _2(event_name: str):
    return {event_name: str(broadcast.findEvent(event_name))}
'''
@app.get('/api/event/Hi')
async def _():
    broadcast.postEvent(Hi())
    
@app.get('/api/event/ExampleEvent')
async def _():
    broadcast.postEvent(ExampleEvent())
'''
