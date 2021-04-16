import asyncio
from graia.broadcast import Broadcast, BaseEvent, BaseDispatcher, DispatcherInterface
from loguru import logger
from graia.application.logger import LoggingLogger
from fastapi import FastAPI
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
def test_func(brain_power: int):  # 注意: 我们同时提供了特定的参数名称和特殊的类型注解
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
@app.get('/api/event/Hi')
async def _():
    broadcast.postEvent(Hi())
    
@app.get('/api/event/ExampleEvent')
async def _():
    broadcast.postEvent(ExampleEvent())
