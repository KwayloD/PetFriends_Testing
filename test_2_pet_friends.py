from api import PetFriends
from settings import *
import os

pf = PetFriends()

def test_get_api_key_for_invalid_user_email(email=invalid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_get_api_key_for_invalid_user_password(email=valid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_add_new_pet_with_invalid_photo(name='Вовка', animal_type='Кот', age='2', pet_photo='images/cat.png'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['pet_photo'] != pet_photo

def test_add_new_pet_with_invalid_data_with_photo(name='1040103', animal_type='000', age='два', pet_photo='images/P1040103.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_with_invalid_data_without_photo(name='P1040103', animal_type='0A0', age='два'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_add_photo_of_pet(pet_photo='images/P1040103.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    pet_id = my_pets['pets'][0]['id']

    if my_pets['pets'][0]['pet_photo'] == "":
        status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        print("У питомца уже есть фото")

def test_add_png_photo(pet_photo='images/cat.png'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)

        assert status == 500

def test_update_negative_age_self_pet(name='',animal_type='', age=-5):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
    else:
        raise Exception("Нет питомцев")

def test_update_zero_age_self_pet(name='',animal_type='', age=0):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][1]['id'], name, animal_type, age)

        assert status == 200
    else:
        raise Exception("Нет питомцев")

def test_update_str_age_self_pet(name='',animal_type='', age='семь'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][1]['id'], name, animal_type, age)

        assert status == 200
        assert type(result['age']) != int
    else:
        raise Exception("Нет питомцев")