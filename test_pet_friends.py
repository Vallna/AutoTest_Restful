from api import PetFriends
from setting import valid_email, valid_password
import os



pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем, что запрос api-ключа возвращает статус 200 и в результате
    содержится слово key"""

    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
    print(result)


def test_get_all_pets_with_valid_key(filter=''):
    """Проверяем, что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api-ключ, сохраняем его в переменную auth_key.
    Далее, используя этот ключ, запрашиваем всех питомцев и проверяем , что
    список не пустой"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_info_about_new_pet_with_valid_data(name='Мая', animal_type='кошка', age='6',
                                                pet_photo='images/cat1.jpg'):
    """Проверяем, что можно добавить питомца с корректными данными"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_info_about_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_add_pet_without_photo_with_valid_data(name='Лиза', animal_type='кошка', age='2'):
    """Проверяем, что можно добавить питомца с корректными неполными данными (без фото)"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_pet_without_photo(auth_key, name, animal_type, age,)

    assert status == 200
    assert result['name'] == name


def test_add_photo_of_pet_with_valid_data(pet_photo='images/cat1.jpg'):
    """Проверяем, что можно добавить фотографию питомца с корректными данными"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_pet_without_photo(auth_key, name='Алиса', animal_type='кошка', age=6)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

    assert status == 200
    assert result['pet_photo'] != ""


def test_delete_pet_from_database_successful():
    """Проверяем возможность удаления питомца по указанному id"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_info_about_new_pet(auth_key, "Клепа", "кошка", "3", "images/cat3.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'] [0] ['id']
    status, result = pf.delete_pet_from_database(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_info_about_pet(name='КошаЛиза', animal_type='Cat', age='10'):
    """Проверяем возможность обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_info_about_pet(auth_key, my_pets['pets'][0]['id'],
                                                  name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_get_api_key_for_unregistered_user(email='unregistered@gmail.com', password='invalidpassword'):
    """Негативный тест:проверяем, что запрос api ключа возвращает статус 403 для
    незарегистрированного пользователя"""

    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_api_key_with_invalid_password(email=valid_password, password='invalidpassword'):
    """Негативный тест: проверяем, что запрос api ключа возвращает статус 403 для
    зарегистрированного пользователя, указавшего неверный пароль"""

    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_add_pet_without_photo_with_invalid_data(name='Лиза', animal_type='кошка', age='125364'):
    """Негативный тест: проверяем, что нельзя добавить питомца, если указать
    в параметре age слишком большое число. Запрос возвращает статус 400"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_pet_without_photo(auth_key, name, animal_type, age,)

    assert status == 400
    #Этот тест показывает баг! Питомец с возрастом 125364 добавляется (нет ограничения по возрасту)


def test_add_pet_without_photo_with_invalid_auth_key(name='Лиза', animal_type='кошка', age='2'):
    """Негативный тест: проверяем, что если 'key' имеет неверное значение  добавить питомца нельзя.
    Запрос возвращает статус 403"""

    auth_key = {'key': '4551255647878995545521'}
    status, result = pf.add_pet_without_photo(auth_key, name, animal_type, age,)

    assert status == 403























