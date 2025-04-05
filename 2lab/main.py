from fastapi import FastAPI
from app.api.router import router as api_router


app = FastAPI(title="Lab Project")

app.include_router(api_router)

#def main():
    # Ваш код здесь
#    pass

#if __name__ == "__main__":
#    main()

