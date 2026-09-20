from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get_app():
    return {"message":"hey"}
