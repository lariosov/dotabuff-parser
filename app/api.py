# основные импорты
import app.main as main
import logging, os
from fastapi import FastAPI, HTTPException,\
        Request, Response, status, Depends
from fastapi.security import APIKeyHeader
from typing import Optional
from prometheus_client import Counter, generate_latest,\
        CONTENT_TYPE_LATEST, make_asgi_app
from dotenv import main


main.load_dotenv()


REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests',
                        ['method', 'endpoint', 'status_code'],)
app = FastAPI()
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


# уровень логирования, пока что вносится вручную
logging.basicConfig(
    level="INFO",
    filename="api.log",
    format="%(asctime)s %(levelname)s %(message)s",
)


async def validate_api_key(api_key: str = Depends(api_key_header)):
    valid_api_key = os.getenv("METRICS_API_KEY")
    if api_key != valid_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )


@app.middleware("http")
async def monitor_requests(request: Request,
                           call_next):
    method = request.method
    endpoint = request.url.path
    response = await call_next(request)
    REQUEST_COUNT.labels(
        method=method,
        endpoint=endpoint,
        status_code=response.status_code
    ).inc()
    return response


@app.get("/")  # путь апи
def start_screen(request: Request):
    host_ip = request.client.host
    logging.info(f"{host_ip} : Used start screen.")
    raise HTTPException(
        status_code=400, 
        detail="You need to use API with '/api/profile'")


@app.get("/metrics", dependencies=[Depends(validate_api_key)])
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
        )


@app.get("/api/profile")  # путь апи
def profile_games(request: Request, id: Optional[int] = None):
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
