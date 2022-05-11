from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from typing import Optional
import uvicorn

app = FastAPI()

def search_anime(name):
    name_list = []
    episodes_list = []
    durations_list = []
    type_list = []
    languages_list = []
    r = requests.get(f"https://zoro.to/search?keyword={name}")
    soup = BeautifulSoup(r.text, "html.parser")
    search_list = soup.find("div", class_="tab-content")
    [name_list.append(anime.text) for anime in search_list.find_all("a", class_="dynamic-name")]
    episodes = [anime.text for anime in search_list.find_all("div", class_="tick rtl")]
    [episodes_list.append(episodes[i].replace('\n', '').strip()) for i in range(len(episodes))]
    durations = [anime.text for anime in search_list.find_all("span", class_="fdi-item fdi-duration")]
    [durations_list.append(durations[i].replace('\n', '').strip()) for i in range(len(durations))]
    types = [anime.text for anime in search_list.find_all("span", class_="fdi-item")]
    [type_list.append(types[i].replace('\n', '').strip()) for i in range(len(types))]
    languages = [anime.text for anime in search_list.find_all("div", class_="tick ltr")]
    [languages_list.append(languages[i].replace('\n', '').strip()) for i in range(len(languages))]
    data = {
        "results": [
            {
                "name": name_list[i],
                "episodes": episodes_list[i],
                "duration": durations_list[i],
                "type": type_list[i],
                "languages": languages_list[i]
            } for i in range(len(name_list))
        ]
    }
    return data

def get_most_popular(page):
    name_list = []
    episodes_list = []
    durations_list = []
    type_list = []
    languages_list = []
    r = requests.get(f"https://zoro.to/most-popular?page={page}")
    soup = BeautifulSoup(r.text, "html.parser")
    content_list = soup.find("div", class_="tab-content")
    [name_list.append(anime.text) for anime in content_list.find_all("h3")]
    episodes = [anime.text for anime in content_list.find_all("div", class_="tick rtl")]
    [episodes_list.append(episodes[i].replace('\n', '').strip()) for i in range(len(episodes))]
    durations = [anime.text for anime in content_list.find_all("span", class_="fdi-item fdi-duration")]
    [durations_list.append(durations[i].replace('\n', '').strip()) for i in range(len(durations))]
    types = [anime.text for anime in content_list.find_all("span", class_="fdi-item")]
    [type_list.append(types[i].replace('\n', '').strip()) for i in range(len(types))]
    languages = [anime.text for anime in content_list.find_all("div", class_="tick ltr")]
    [languages_list.append(languages[i].replace('\n', '').strip()) for i in range(len(languages))]
    data = {
        "page": page,
        "results": [
            {
                "name": name_list[i],
                "episodes": episodes_list[i],
                "duration": durations_list[i],
                "type": type_list[i],
                "languages": languages_list[i]
            } for i in range(len(name_list))
        ]
    }
    return data
    
    

@app.get("/")
def read_root():
    return "<p>Hello, World!</p>"

@app.get("/endpoints")
def read_endpoints():
    endpoints = {
        "info": "All the endpoints are listed here. | Required: <> , Optional: []",
        "endpoints": [
            {
                "search": "/search?name=<name>",
                "most-popular": "/most-popular?page=[page]",
            }
        ]
    }
    return endpoints


@app.get("/search")
def search(name: Optional[str] = None):
    return search_anime(name)

@app.get("/most-popular")
def most_popular(page: Optional[int] = None):
    if page is None:
        return get_most_popular(1)
    else:
        return get_most_popular(page)


if __name__ == "__main__":
  uvicorn.run("server.api:app", host="0.0.0.0", port=8000, reload=True)