import datetime
import asyncio

import aiocoap.resource as resource
import aiocoap


class TimeResource(resource.ObservableResource):

    def __init__(self):
        super().__init__()
        self.handle = None

    def notify(self):
        self.updated_state()
        self.reschedule()

    def reschedule(self):
        self.handle = asyncio.get_event_loop().call_later(5, self.notify)

    def update_observation_count(self, count):
        if count and self.handle is None:
            self.reschedule()
        if count == 0 and self.handle:
            self.handle.cancel()
            self.handle = None

    async def render_get(self, request):
        payload = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").encode('ascii')
        return aiocoap.Message(payload = payload)


class BlockResource(resource.Resource):

    def __init__(self):
        super().__init__()

    async def render_get(self, request):
        return aiocoap.Message(payload=b'Hello, World')


async def main():
    root = resource.Site()

    root.add_resource(['time'], TimeResource())
    root.add_resource(['other', 'block'], BlockResource())

    await aiocoap.Context.create_server_context(root)

    #  Run forever
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        print(f"{e}")
