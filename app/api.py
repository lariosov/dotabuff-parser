# основные импорты
import app.main as main
import logging, time
from fastapi import FastAPI, HTTPException, Request, Response
from typing import Optional
from prometheus_client import Counter, generate_latest,\
    CONTENT_TYPE_LATEST, make_asgi_app, Histogram


REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests',
                        ['method', 'endpoint', 'status_code'],)
REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'Duration of HTTP requests in seconds',
    ['method', 'endpoint', 'status_code'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1, 5]
)
app = FastAPI()

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


# уровень логирования, пока что вносится вручную
logging.basicConfig(
    level="INFO",
    filename="api.log",
    format="%(asctime)s %(levelname)s %(message)s",
)


@app.middleware("http")
async def monitor_requests(request: Request,
                           call_next):
    # Сохраняем информацию о запросе ДО обработки
    start_time = time.monotonic()
    method = request.method
    endpoint = request.url.path
    
    # Выполняем запрос и получаем ответ
    response = await call_next(request)
    duration = time.monotonic() - start_time
    
    # Регистрируем метрики ПОСЛЕ получения ответа
    REQUEST_COUNT.labels(
        method=method,
        endpoint=endpoint,
        status_code=response.status_code
    ).inc()
    REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code
    ).observe(duration)
    
    return response


@app.get("/")  # путь апи
def start_screen(request: Request):
    host_ip = request.client.host
    logging.info(f"{host_ip} : Used start screen.")
    raise HTTPException(
        status_code=400, 
        detail="You need to use API with '/api/profile'")


@app.get("/metrics")
def metrics(request: Request):
    client_ip = request.client.host
    if client_ip not in ["127.0.0.1", "::1", "172.17.0.1", "138.124.114.181"]:
        raise HTTPException(status_code=403, detail="Access forbidden")
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
