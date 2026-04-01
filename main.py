from fastapi import FastAPI, HTTPException

from models import PopulateRequest, PopulateResult
from service import populate_template

app = FastAPI(title="School Note Populator")


@app.post("/populate", response_model=PopulateResult)
def populate(request: PopulateRequest):
    try:
        return populate_template(request.conversation_history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok"}
