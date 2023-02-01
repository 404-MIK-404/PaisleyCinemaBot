import requests
from kinopoisk_unofficial.request.films.search_by_keyword_request import SearchByKeywordRequest
from config import config
import json


class KinopoiskApi:
    api_client = config.ConfigBot().getClientApiKinopoisk()
    current_id_film = 0

    def find_info_film(self, name_film):
        try:
            request = SearchByKeywordRequest(name_film)
            response = self.api_client.films.send_film_request(request)
            result_response = None
            for film in response.films:
                current_film = film
                print(current_film)
                if current_film.name_ru == name_film or current_film.name_en == name_film:
                    result_response = current_film
                    break
            return result_response or "film_not_find"
        except RuntimeError:
            return "film_not_find"

    @staticmethod
    def request_url_api(url, headers):
        return requests.get(url=url,
                            headers=headers)

    def get_list_await_films(self):
        response = self.request_url_api(
            url="https://kinopoiskapiunofficial.tech/api/v2.2/films/top?type=TOP_AWAIT_FILMS&page=1",
            headers={'X-API-KEY': '04cf1757-8fc4-4ed9-9ac0-08af7a7275f8', 'Content-Type': 'application/json'})
        result_request = json.loads(response.text)
        return result_request['films']

    def get_list_top_films(self):
        response = self.request_url_api(
            url="https://kinopoiskapiunofficial.tech/api/v2.2/films/top?page=1&type=TOP_100_POPULAR_FILMS",
            headers={'X-API-KEY': '04cf1757-8fc4-4ed9-9ac0-08af7a7275f8', 'Content-Type': 'application/json'})
        result_request = json.loads(response.text)
        return result_request['films']
