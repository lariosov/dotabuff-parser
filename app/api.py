import main
from fastapi import FastAPI
from typing import Optional


app = FastAPI()

@app.get('/profile') # путь апи
def games_my(url: Optional[str] = None):
    if url is None:
        return "Variable 'URL' is empty."
    else:
        return main.start_scrapping(url=url)
