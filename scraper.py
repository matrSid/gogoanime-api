from typing import Dict, Final, List
from selectolax.parser import HTMLParser
from contextlib import suppress
from rich import print
import aiohttp

BASE_URL: Final[str] = "https://www3.gogoanimes.fi/"


async def get_request(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print("Status:", response.status)
            return await response.text()


def html_parser(html: str) -> HTMLParser:
    return HTMLParser(html)


async def search(query: str) -> List[Dict[str, str]]:
    html = await get_request(f"{BASE_URL}/search.html?keyword={query}")
    parser = html_parser(html)

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


async def get_anime(anime_id: str) -> Dict[str, str]:
    html = await get_request(f"{BASE_URL}/category/{anime_id}")
    parser = html_parser(html)
    img_url = parser.css_first(".anime_info_body_bg img").attributes["src"]
    about = parser.css_first(".anime_info_body_bg div:nth-of-type(1)").text()
    name = parser.css_first("div.anime_info_body_bg h1").text()

    genre_section = parser.css_first("p:contains('Genre:')")
    genre_links = genre_section.css("a")
    genre = ", ".join([link.text for link in genre_links])

    released_text = parser.css_first("div.anime_info_body_bg p:nth-of-type(5)").text()
    released = released_text.split(":")[-1].strip()
    status = parser.css_first("div.anime_info_body_bg p:nth-of-type(6)").text()
    last_ep = int(
        parser.css_first("#episode_page li:last-child a").attributes["ep_end"]
    )
    episodes = list(range(1, last_ep + 1))
    return {"name": name, "img": img_url, "about": about, "genre": genre, "released": released, "status": status, "episodes": episodes}


async def new_season(page_no: int) -> List[Dict[str, str]]:
    anime_list = []
    html = await get_request(f"{BASE_URL}/new-season.html?page={page_no}")
    parser = html_parser(html)

    for element in parser.css("div.main_body div.last_episodes ul.items li"):
        name = element.css_first("p a").text()
        img = element.css_first("div a img").attributes["src"]
        id_ = element.css_first("div a").attributes["href"].split("/")[-1]
        anime = {"name": name, "img": img, "id": id_}
        anime_list.append(anime)
    return anime_list


async def get_streaming_links(anime_id: str, episode_no: int) -> str:
    html = await get_request(f"{BASE_URL}/{anime_id}-episode-{episode_no}")

    parser = html_parser(html)
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


async def home(page: int) -> List[Dict[str, str]]:
    html = await get_request(
        f"https://ajax.gogo-load.com/ajax/page-recent-release.html?page={page}"
    )
    parser = html_parser(html)
    animes: List[Dict[str, str]] = []
    for li in parser.css("ul.items li"):
        img: str = li.css_first("div.img img").attributes["src"]
        episode_id: str = li.css_first("div.img a").attributes["href"][1:]
        name: str = li.css_first("div.img a").attributes["title"]
        episode_text: str = li.css_first("p.episode").text()
        animes.append(
            {
                "name": name,
                "episode_id": episode_id,
                "episode_text": episode_text,
                "img": img,
            }
        )
    return animes
