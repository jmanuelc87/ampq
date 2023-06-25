import datetime
import asyncio

import aiocoap.resource as resource
import aiocoap


class BlockResource(resource.Resource):

    def __init__(self):
        super().__init__()


    async def render_get(self, request):
        return aiocoap.Message(payload = b'Hello, World')
    

async def main():
    root = resource.Site()

    root.add_resource(['other', 'block'], BlockResource())

    await aiocoap.Context.create_server_context(root)

    #  Run forever
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    try:
       asyncio.run(main())
    except KeyboardInterrupt as e:
        print(f"{e}")