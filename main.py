from fastapi import FastAPI
import scraper
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/")
def root():
    return RedirectResponse(url="/docs")


@app.get("/search/{query}")
def search_anime(query: str):
    return scraper.search(query)


@app.get("/anime/{anime_id}")
def get_anime_info(anime_id: str):
    return scraper.get_anime(anime_id)


@app.get("/new-season/{page_no}")
def get_new_season(page_no: int):
    return scraper.new_season(page_no)


@app.get("/streaming-link/{anime_id}/{episode_no}")
def get_streaming(anime_id: str, episode_no: int):
    return scraper.get_streaming_link(anime_id, episode_no)


@app.get("/home/{page}")
def get_home(page: int):
    return scraper.home(page)
