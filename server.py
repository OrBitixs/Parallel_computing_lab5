import asyncio


class db_User:
    def __init__(self):
        self._db_users = {}         # login password
        self._db_logged_users = {}  # login peername


async def closing_socket(writer):
    print(f'connection: {writer.get_extra_info("peername")} closing')
    writer.write("closing".encode('utf8'))
    await writer.drain()
    writer.close()

async def log_out(writer):
    for login, peername in db_handle._db_logged_users.items():
        if peername == writer.get_extra_info("peername"):
            print(f'{peername} logged out')
            writer.write("logged out".encode('utf8'))
            await writer.drain()
            del db_handle._db_logged_users[login]
            break
    else:
        writer.write("you are not logged in".encode('utf8'))
        await writer.drain()


async def log_in(writer, reader):
    print(f'connection {writer.get_extra_info("peername")} trying to log in')
    writer.write("enter login password".encode('utf8'))
    await writer.drain()
    response = (await reader.read(255)).decode('utf8').split()
    if response.__len__() == 2:
        for login, peername in db_handle._db_logged_users.items():
            if peername == writer.get_extra_info("peername"):
                writer.write("you are already logged-in. Consider to log out".encode('utf8'))
                await writer.drain()
                break
        else:
            if (response[0] not in db_handle._db_users):
                writer.write("user does not exists".encode('utf8'))
                await writer.drain()
            else:
                if db_handle._db_users.get(response[0]) != response[1]:
                    writer.write("incorrect password".encode('utf8'))
                    await writer.drain()
                else:
                    if (response[0] in db_handle._db_logged_users):
                        writer.write("session already exists".encode('utf8'))
                        await writer.drain()
                    else:
                        db_handle._db_logged_users[response[0]] = writer.get_extra_info("peername")
                        print(f'connection: {writer.get_extra_info("peername")} logged in {response[0]}')
                        writer.write("logged in".encode('utf8'))
                        await writer.drain()


async def sign_up(writer, reader):
    writer.write("create login password".encode('utf8'))
    await writer.drain()
    response = (await reader.read(255)).decode('utf8').split()
    if response.__len__() == 2:
        if (response[0] in db_handle._db_users):
            writer.write("user already exists".encode('utf8'))
            await writer.drain()
        else:
            print(f'adding login: {response[0]} password: {response[1]}')
            db_handle._db_users[response[0]] = response[1]
            writer.write("successfully added new user".encode('utf8'))
            await writer.drain()
    else:
        writer.write("wrong number of arguments".encode('utf8'))
        await writer.drain()


async def show():
    print(db_handle._db_users)

async  def session():
    print(db_handle._db_logged_users)

async def handle_client(reader, writer):
    request = None
    writer.write("connection accepted".encode('utf8'))
    await writer.drain()
    print(f'connection accepted from {writer.get_extra_info("peername")}')
    while request != "turn off":
        request = (await reader.read(255)).decode('utf8')
        print(request)

        match request:
            case "disconnect":
                await asyncio.create_task(log_out(writer))
                await asyncio.create_task(closing_socket(writer))
                break
            case "log_in":
                await asyncio.create_task(log_in(writer, reader))
            case "sign_up":
                await asyncio.create_task(sign_up(writer, reader))
            case "log_out":
                await asyncio.create_task(log_out(writer))
            case "show":
                await asyncio.create_task(show())
            case "session":
                print(db_handle._db_logged_users)
            case "turn off":
                print("turning server off")
                raise KeyboardInterrupt


async def run_server():
    server = await asyncio.start_server(handle_client, 'localhost', 8000)
    async with server:
        await server.serve_forever()

if __name__=="__main__":
    db_handle = db_User()
    asyncio.run(run_server())