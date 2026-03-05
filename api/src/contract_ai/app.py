from fastapi import fastAPI
from contract_ai.models import DraftAmendmentRequest, DraftAmendmentResponse
from contract_ai.pipeline import run_pipeline

app = fastAPI()

@app.post("/draft-amendment", response_model=DraftAmendmentResponse)
def draft_amendment(req: DraftAmendmentRequest):
    return run_pipeline(req)