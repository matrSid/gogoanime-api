from fastapi import FastAPI
import scraper
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.get("/search/{query}")
async def search_anime(query: str):
    return await scraper.search(query)


@app.get("/anime/{anime_id}")
async def get_anime_info(anime_id: str):
    return await scraper.get_anime(anime_id)


@app.get("/new-season/{page_no}")
async def get_new_season(page_no: int):
    return await scraper.new_season(page_no)


@app.get("/streaming-links/{anime_id}/{episode_no}")
async def get_streaming(anime_id: str, episode_no: int):
    return await scraper.get_streaming_links(anime_id, episode_no)


@app.get("/home/{page}")
async def get_home(page: int):
    return await scraper.home(page)
