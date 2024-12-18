import main
from fastapi import FastAPI
from typing import Optional


app = FastAPI()


@app.get("api/profile")  # путь апи
def profile_games(id: Optional[str] = None):
    if id is None:
        return "Variable 'id' is empty."
    else:
        try:
            return main.start_scrapping(id=id)
        except:
            return "500, Check your URL."
