import asyncio

async def closing_socket(writer):
    print('connection closed')
    writer.close()

async def sign_up(reader, writer):
    message = input()       # login password
    writer.write(message.encode('utf8'))
    responce = (await reader.read(255)).decode('utf8')
    print(responce)
    match responce:
        case "user already exists" | "wrong number of arguments":
            return -1
        case "successfuly added new user":
            return 0

async def log_in(reader, writer):
    message = input()       # login password
    writer.write(message.encode('utf8'))
    responce = (await reader.read(255)).decode('utf8')
    print(responce)
    match responce:
        case "logged in":
            return 0
        case _:
            return -1

async def tcp_echo_client():
    reader, writer = await asyncio.open_connection('localhost', 8000)
    data = await reader.read(100)
    data = data.decode('utf8')
    if (data == "connection accepted"):
        while True:
            message = input()
            match message:
                case "disconnect":
                    print(f'send: {message}')
                    writer.write(message.encode('utf8'))
                    await writer.drain()

                    data = (await reader.read(255)).decode('utf8')
                    print(f'Received: {data}')
                    if data == "logged out":
                        data = (await reader.read(255)).decode('utf8')

                    if data == "closing":
                        await closing_socket(writer)
                        break
                case "log_in":
                    print(f'send: {message}')
                    writer.write(message.encode('utf8'))
                    await writer.drain()

                    data = (await reader.read(255)).decode('utf8')
                    print(f'Received: {data}')
                    if data == "enter login password":
                        await asyncio.create_task(log_in(reader, writer))

                case "sign_up":
                    print(f'send: {message}')
                    writer.write(message.encode('utf8'))
                    await writer.drain()

                    data = (await reader.read(255)).decode('utf8')
                    print(f'Received: {data}')
                    if data == "create login password":
                        await asyncio.create_task(sign_up(reader, writer))

                case "log_out":
                    print(f'send: {message}')
                    writer.write(message.encode('utf8'))
                    await writer.drain()
                    data = (await reader.read(255)).decode('utf8')
                    print(f'Received: {data}')

                case "show":
                    print(f'send: {message}')
                    writer.write(message.encode('utf8'))
                    await writer.drain()

                case "session":
                    print(f'send: {message}')
                    writer.write(message.encode('utf8'))
                    await writer.drain()

                case "turn off":
                    print(f'send: {message}')
                    writer.write(message.encode('utf8'))
                    await writer.drain()

                case _:
                    print("wrong command")


    else:
        print("unexpected erroe ocured\nclosing connection")
        writer.close()


asyncio.run(tcp_echo_client())