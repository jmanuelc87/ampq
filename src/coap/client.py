import asyncio

from aiocoap import *


async def main():
    protocol = await Context.create_client_context()

    request = Message(code = GET, uri='coap://localhost/time')
    response = await protocol.request(request).response

    print(f"Result: {response.code} {response.payload}")

if __name__ == "__main__":
    asyncio.run(main())