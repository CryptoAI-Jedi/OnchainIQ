from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="OnchainIQ API")

# CORS: browsers block cross-origin requests by default, and the Next.js
# frontend will run on a different origin (localhost:3000 in dev, a Vercel
# domain in prod) than this API. Without these response headers the browser
# refuses the fetch. Wide open for now; we narrow allow_origins to the real
# frontend URL in step 3.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# The API contract. AskResponse is intentionally minimal now and grows later
# without breaking callers: chart data in Week 2, sources/citations in Week 4.
class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    # Hardcoded for the walking skeleton. Echoing the question proves the
    # request body parsed end to end. The real agent replaces this in Week 3.
    return AskResponse(
        answer=f'You asked: "{request.question}". '
               "This is a hardcoded placeholder; the real onchain agent ships soon."
    )