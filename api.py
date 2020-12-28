"""Итоговое практическое задание 19.7, Модуль 19"""
import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder



class PetFriends:
    """API-библиотека к веб приложению Pet Friends"""

    def __init__(self):
        self.base_url = "https://petfriends1.herokuapp.com/"

    def get_api_key(self, email: str, password: str) -> json:
        """Метод делает запрос к API сервера и возвращает
        статус запроса и результат в формате JSON с уникальным
        ключем пользователя, найденного по указанным email и password """

        headers = {
            'email': email,
            'password': password
        }

        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json:
        """Метод делает запрос к API сервера и возвращает
          статус запроса и рузультат в формате JSON со списком найденных питомцев,
          совпадающих с фильтром. На данный момент фильтр может иметь
           либо пустое значение, это значит получить список всех питомцев,
           либо 'my_pets', что значит получить список своих питомцев"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """Метод отправляет на сервер данные о добавляемом питомце без фото и возвращает
                статус запроса на сервер и результат в формате JSON с данными
                добавленного питомца"""
        headers = {'auth_key': auth_key['key']}
        formdata = {'name': name, 'animal_type': animal_type, 'age': age}

        res = requests.post(self.base_url+'api/create_pet_simple', headers=headers, data=formdata)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_info_about_new_pet(self, auth_key: json, name: str, animal_type: str,
                               age: str, pet_photo: str) -> json:
        """Метод отправляет на сервер данные о добавляемом питомце и возвращает
        статус запроса на сервер и результат в формате JSON с данными
        добавленного питомца"""

        data = MultipartEncoder(
            fields={'name': name,
                    'animal_type': animal_type,
                    'age': age,
                    'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
                    })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url+'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_photo_of_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод отправляет на сервер данные о добавлении фото питомца
        по указанному ID и возвращает статус запроса и result в формате JSON
        c обновленными данными"""
        data = MultipartEncoder(
            fields={'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
                    })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id,
                            headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def delete_pet_from_database(self, auth_key: json,
                                 pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление
        питомца по указанному ID и возвращает статус запроса
        в формате JSON с текстом об успешном удалении"""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url+'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except :
            result = res.text
        return status, result

    def update_info_about_pet(self, auth_key: json, pet_id: str, name: str,
                              animal_type: str, age: str) -> json:
        """Метод отправляет запрос на сервер об обновлении данных питомца
        по указанному ID и возвращает статус запроса и result в формате JSON
        c обновленными данными"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result




















