from fastapi import FastAPI
import database
import api

def start_app():
    database.init_db()
    app = FastAPI()
    app.include_router(api.router)

    return app
def load_config():
    pass

def main():
    app = start_app()


if __name__=="__main__":
    main()
