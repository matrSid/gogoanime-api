import httpx
from selectolax.parser import HTMLParser
from contextlib import suppress
from requests_cache import CachedSession, AnyResponse
from rich import print

BASE_URL = "https://www3.gogoanimes.fi/"


session = CachedSession("gogoanime_cache", expire_after=1 * 24 * 60 * 60)


def get_request_cache(url: str) -> AnyResponse:
    resp = session.get(url)
    print(f"From Cache : {resp.from_cache}")
    return resp


def get_request(url: str) -> httpx.Response:
    with httpx.Client() as client:
        return client.get(url)


def html_parser(html: str) -> HTMLParser:
    return HTMLParser(html)


def search(query: str) -> list[dict]:
    response = get_request(f"{BASE_URL}/search.html?keyword={query}")
    parser = html_parser(response.content)

    anime_list = []
    total_page = 1
    with suppress(Exception):
        total_page = int(
            parser.css_first(".pagination-list li:last-child a").attributes["data-page"]
        )
    for element in parser.css("div.last_episodes ul.items li"):
        name = element.css_first("p a").attributes["title"]
        img = element.css_first("div a img").attributes["src"]
        id_ = element.css_first("div a").attributes["href"].split("/")[-1]
        anime = {
            "total_page": total_page,
            "name": name,
            "img_url": img,
            "id": id_,
        }
        anime_list.append(anime)
    return anime_list


def get_anime(anime_id: str) -> dict:
    response = get_request(f"{BASE_URL}/category/{anime_id}")
    parser = html_parser(response.content)
    img_url = parser.css_first(".anime_info_body_bg img").attributes["src"]
    about = parser.css_first(".anime_info_body_bg p:nth-of-type(3)").text()
    name = parser.css_first("div.anime_info_body_bg h1").text()
    last_ep = int(
        parser.css_first("#episode_page li:last-child a").attributes["ep_end"]
    )
    episodes = list(range(1, last_ep + 1))
    return {"name": name, "img": img_url, "about": about, "episodes": episodes}


def new_season(page_no: int) -> list[dict]:
    anime_list = []
    response = get_request(f"{BASE_URL}/new-season.html?page={page_no}")
    parser = html_parser(response.content)

    for element in parser.css("div.main_body div.last_episodes ul.items li"):
        name = element.css_first("p a").text()
        img = element.css_first("div a img").attributes["src"]
        id_ = element.css_first("div a").attributes["href"].split("/")[-1]
        anime = {"name": name, "img": img, "id": id_}
        anime_list.append(anime)
    return anime_list


def get_streaming_links(anime_id: str, episode_no: int) -> str:
    response = get_request_cache(f"{BASE_URL}/{anime_id}-episode-{episode_no}")

    parser = html_parser(response.content)
    servers = parser.css(".anime_muti_link > ul > li")[1:]
    data = {}
    for server in servers:
        server_name = server.attributes["class"]
        stream_url = server.css_first("a").attributes["data-video"]
        print(server_name)
        print(stream_url)
        data[server_name] = stream_url
    data = dict(sorted(data.items(), key=lambda x: x[1]))
    return data


def home(page: int):
    response = get_request(
        f"https://ajax.gogo-load.com/ajax/page-recent-release.html?page={page}"
    )
    parser = html_parser(response.content)
    anime = []
    for li in parser.css("ul.items li"):
        img = li.css_first("div.img img").attributes["src"]
        episode_id = li.css_first("div.img a").attributes["href"][1:]
        name = li.css_first("div.img a").attributes["title"]
        episode_text = li.css_first("p.episode").text()
        anime.append(
            {
                "name": name,
                "episode_id": episode_id,
                "episode_text": episode_text,
                "img": img,
            }
        )
    return anime
