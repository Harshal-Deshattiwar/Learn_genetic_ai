
from fastapi import FastAPI, Query
from .client.rq_client import queue
from .queues.worker import process_query
app = FastAPI()


# {
#   "status": "queued",
#   "job_id": "504a5a62-7bb5-41b5-9e6a-96babdc2a58a"
# }

# {
#   "status": "queued",
#   "job_id": "fa3b6eda-399b-4b32-a9e4-8f31ff80baec"
# }

@app.get("/")
def root():
    return {"Hello": "World server is up and running"}

@app.post("/chat")
def chat(query: str = Query(...,description="The chat query of user")):
    job = queue.enqueue(process_query,query)
    return {"status": "queued", "job_id": job.id}

@app.get("/job-status")
def get_result(
        job_id: str = Query(...,description="Job id")
):
    job = queue.fetch_job(job_id=job_id)
    result = job.return_value()
    return {"result": result}
