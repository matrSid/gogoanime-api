

GogoAnime API

This is a RESTful API built with FastAPI that scrapes data from an anime website to provide information about anime series and seasons. It provides several endpoints for searching for anime, retrieving information about specific anime, and getting information about the latest season of anime releases.
Installation

    Clone this repository: git clone 
    Navigate to the project directory: cd gogoanime-api
    Install the required dependencies: pip install -r requirements.txt

Usage

To start the server, run the following command in your terminal:

```
uvicorn app:app --reload
```

This will start the server on http://localhost:8000.
Endpoints

    /: Redirects to the /docs endpoint, which serves the FastAPI documentation.
    /search/{query}: Takes a query string parameter query, passes it to the scraper.search function, and returns the search results for anime matching the query.
    /anime/{anime_id}: Takes an anime ID parameter anime_id, passes it to the scraper.get_anime function, and returns information about the anime with that ID.
    /new-season/{page_no}: Takes a page number parameter page_no, passes it to the scraper.new_season function, and returns information about the latest season of anime releases.
    /streaming-link/{anime_id}/{episode_no}: Takes an anime ID parameter anime_id and an episode number parameter episode_no, passes them to the scraper.get_streaming_link function, and returns a streaming link for the specified episode of the specified anime.
    /home/{page}: Takes a page number parameter page, passes it to the scraper.home function, and returns information about the anime series on the specified page of the website.

Contributing

If you want to contribute to this project, feel free to fork the repository and submit a pull request.
