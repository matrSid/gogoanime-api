# import httpx
# from selectolax.parser import HTMLParser


# def main():
#     url = "https://gogoanime.llc/megami-no-cafe-terrace-episode-10"
#     resp = httpx.get(url)
#     parser = HTMLParser(resp.text)
#     servers = parser.css(".anime_muti_link > ul > li")[1:]
#     data = []
#     for server in servers:
#         server_name = server.attributes["class"]
#         stream_url = server.css_first("a").attributes["data-video"]
#         data.append({server_name: stream_url})


# if __name__ == "__main__":
#     main()
