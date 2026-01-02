from fastapi import FastAPI

app = FastAPI(title="Optimus Brain API")

@app.get("/health")
def health():
    return {"status": "online"}
