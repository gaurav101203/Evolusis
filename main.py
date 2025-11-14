from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from agent import handle_query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Evolusis Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    query: str

@app.post("/ask")
async def ask(q: Query):
    if not q.query or not q.query.strip():
        raise HTTPException(status_code=400, detail="query is required")
    response = await handle_query(q.query.strip())
    return response

if __name__ == "__main__":
    import os
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host=host, port=port, reload=True)
