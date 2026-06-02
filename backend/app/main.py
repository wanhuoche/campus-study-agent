from fastapi import FastAPI

app = FastAPI(title="campus-study-agent", version="0.1.0")


@app.get("/health")
def health_check():
    return {"status": "ok"}
