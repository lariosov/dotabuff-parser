# основные импорты
import app.main as main
import logging
from fastapi import FastAPI, HTTPException, Request, Response
from typing import Optional
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST


REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests')
app = FastAPI()

# уровень логирования, пока что вносится вручную
logging.basicConfig(
    level="INFO",
    filename="api.log",
    format="%(asctime)s %(levelname)s %(message)s",
)


@app.get("/")  # путь апи
def start_screen(request: Request):
    REQUEST_COUNT.inc()
    host_ip = request.client.host
    logging.info(f"{host_ip} : Used start screen.")
    raise HTTPException(
        status_code=400, 
        detail="You need to use API with '/api/profile'")


@app.get("/metrics")
def metrics(request: Request):
    client_ip = request.client.host
    if client_ip not in ["127.0.0.1", "::1"]:
        raise HTTPException(status_code=403, detail="Access forbidden")
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
        )


@app.get("/api/profile")  # путь апи
def profile_games(request: Request, id: Optional[int] = None):
    REQUEST_COUNT.inc()
    host_ip = request.client.host
    if id is None:
        logging.info(f'{host_ip} : Empty "id" variable.')
        raise HTTPException(status_code=400, 
                            detail="Your 'id' variable is empty.")
    else:
        try:
            logging.info(f"{host_ip} : request. "
                         f"DotaBuff id = {id}")
            return main.start_scrapping(id=id)
        except:
            logging.warning(f"{host_ip} bad request. "
                            f"DotaBuff id = {id}")
            raise HTTPException(status_code=400, 
                                detail="Check your 'id' variable.")
