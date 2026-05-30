from fastapi import FastAPI
from src.modules.router import router as AppRouter
from fastapi.middleware.cors import CORSMiddleware


class Server:
    def __init__(self, port: int = 8000):
        self.port = port
        self.app = FastAPI(title="Mi API", version="1.0.0")
        self._add_startup_event()

    def _add_startup_event(self):
        @self.app.on_event("startup")
        async def startup_event():
            print(f"Server running on port {self.port}")
            print(f"Docs: http://127.0.0.1:{self.port}/docs")

    def setup_middlewares(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                "http://localhost:5173",
                "http://127.0.0.1:5173",
                "http://localhost:3000",
                "http://localhost:8080",
                "http://127.0.0.1:8000",
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=["*"],
            max_age=3600,
        )

    def setup_routes(self):
        self.app.include_router(AppRouter)

    def start(self):
        self.setup_middlewares()
        self.setup_routes()

        import uvicorn

        uvicorn.run(self.app, host="0.0.0.0", port=self.port)
