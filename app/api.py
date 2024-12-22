# основные импорты
import app.main as main
import logging
from fastapi import FastAPI, HTTPException
from typing import Optional


app = FastAPI()

# уровень логирования, пока что вносится вручную
logging.basicConfig(
    level="INFO",
    filename="api.log",
    format="%(asctime)s %(levelname)s %(message)s",
)


@app.get("/")  # путь апи
def start_screen():
    logging.info("Used start screen.")
    raise HTTPException(
        status_code=400, 
        detail="You need to use API with '/api/profile'")


@app.get("/api/profile")  # путь апи
def profile_games(id: Optional[int] = None):
    if id is None:
        logging.info('Empty "id" variable.')
        raise HTTPException(status_code=400, 
                            detail="Your 'id' variable is empty.")
    else:
        try:
            logging.info("User send request. "
                         f"DotaBuff id = {id}")
            return main.start_scrapping(id=id)
        except:
            logging.warning("User send bad request. "
                            f"DotaBuff id = {id}")
            raise HTTPException(status_code=400, 
                                detail="Check your 'id' variable.")
