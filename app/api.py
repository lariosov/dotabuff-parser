import main
from fastapi import FastAPI
from typing import Optional


app = FastAPI()


@app.get("/profile")  # путь апи
def profile_games(url: Optional[str] = None):
    if url is None:
        return "Variable 'URL' is empty."
    else:
        try:
            return main.start_scrapping(url=url)
        except:
            return "500, Check your URL."
