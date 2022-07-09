import os
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
        "anime_name": name,
        "amount": len(name_list),
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
    
def get_genre(genre, page):
    name_list = []
    episodes_list = []
    durations_list = []
    type_list = []
    languages_list = []
    r = requests.get(f"https://zoro.to/genre/{genre}?page={page}")
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
        "genre": genre,
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
                "genre": "/genre?genre=<genre>&page=[page]",
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

@app.get("/genre")
def genre(genre: Optional[str] = None, page: Optional[int] = None):
    if genre is None:
        data = {
            "error": "Please specify a genre. Example: /genre?genre=<genre>&page=[page]",
            "genres": [
                "Action",
                "Adventure",
                "Cars",
                "Comedy",
                "Dementia",
                "Demons",
                "Drama",
                "Ecchi",
                "Fantasy",
                "Game",
                "Harem",
                "Historical",
                "Horror",
                "Isekai",
                "Josei",
                "Kids",
                "Magic",
                "Martial Arts",
                "Mecha",
                "Military",
                "Music",
                "Mystery",
                "Parody",
                "Police",
                "Psychological",
                "Romance",
                "Samurai",
                "School",
                "Sci-Fi",
                "Seinen",
                "Shoujo",
                "Shoujo Ai",
                "Shounen",
                "Shounen Ai",
                "Slice of Life",
                "Space",
                "Sports",
                "Super Power",
                "Supernatural",
                "Thriller",
                "Vampire",
                "Yaoi",
                "Yuri",
            ]
        }
        return data
    else:
        if page is None:
            return get_genre(genre, 1)
        else:
            return get_genre(genre, page)
        
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=os.getenv("PORT", default=5000), log_level="info")