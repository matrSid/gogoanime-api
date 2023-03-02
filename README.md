

# GogoAnime API

This is a web scraper written using FastAPI and Python. It can be used to search and retrieve information related to Anime from the GogoAnime website.

The web scraper can be used by making HTTP requests to the various endpoints/routes. Each endpoint accepts different parameters, depending on the action it performs.



## Requirements

- Python 3.6+

- FastAPI

- uvicorn 


# Endpoints


- **/search/{query}** - Search for Anime by title

- **/anime/{anime_id}** - Get detailed information about an Anime

- **/new-season/{page_no}** - Get a list of Anime from the latest season

- **/streaming-link/{anime_id}/{episode_no}** - Get streaming link for a particular episode

- **/home/{page}** - Get a list of Anime from popular lists




## Installation


```bash
pip install -r requirements.txt
```

## Usage

```bash
uvicorn main:app --reload
```
## And Then Go to http://127.0.0.1:8000 for docs
