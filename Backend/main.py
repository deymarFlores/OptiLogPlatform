from src.server import Server

server = Server()
server.setup_middlewares()
server.setup_routes()

app = server.app