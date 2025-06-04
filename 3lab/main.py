from fastapi import FastAPI
from app.api.router import router as api_router
from app.api.ws import router as ws_router

app = FastAPI(title="Lab Project")

app.include_router(api_router)
app.include_router(ws_router) 
#def main():
    # Ваш код здесь
#    pass

#if __name__ == "__main__":
#    main()

