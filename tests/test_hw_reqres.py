from conftest import requests_api
import os
import json
from jsonschema.validators import validate
from conftest import resources_path


def test_all_users_schema():
    with open(os.path.join(resources_path, 'all_users_schema.json')) as file:
        schema = json.loads(file.read())

    response = requests_api(service='reqres', method='get', url='/api/users')
    validate(instance=response.json(), schema=schema)


def test_single_users_schema():
    with open(os.path.join(resources_path, 'single_user_schema.json')) as file:
        schema = json.loads(file.read())

    response = requests_api(service='reqres', method='get', url='/api/users/2')
    validate(instance=response.json(), schema=schema)


def test_get_all_users_list_is_200():
    resp = requests_api(service='reqres', method='get', url='/api/users')

    assert resp.status_code == 200


def test_users_per_page():
    per_page = 1

    resp = requests_api(
        service='reqres',
        method='get',
        url='/api/users',
        params={"per_page": per_page}
    )

    assert resp.status_code == 200
    assert resp.json()['per_page'] == per_page


def test_open_single_user_by_id():
    resp = requests_api(service='reqres',
                        method='get',
                        url='/api/users/5')

    assert resp.status_code == 200


def test_open_single_user_by_not_exist_id():
    resp = requests_api(service='reqres',
                        method='get',
                        url='/api/users/50')

    assert resp.status_code == 404


def test_create_user():
    name = "Kate"
    job = "QA"

    resp = requests_api(
        service='reqres',
        method='post',
        url='/api/users',
        data={"name": name, "job": job}
    )

    assert resp.status_code == 201
    assert resp.json()['name'] == name
    assert resp.json()['job'] == job


def test_user_register_successful():
    email = "eve.holt@reqres.in"
    password = "pistol"

    resp = requests_api(
        service='reqres',
        method='post',
        url='/api/register',
        data={"email": email, "password": password}
    )

    assert resp.status_code == 200


def test_user_register_not_successful():
    password = "pistol"

    resp = requests_api(
        service='reqres',
        method='post',
        url='/api/register',
        data={"password": password}
    )

    assert resp.status_code == 400
    assert resp.json()['error'] == 'Missing email or username'


def test_login_not_successful():
    email = "eve.holt@reqres"
    password = "pistol"

    resp = requests_api(
        service='reqres',
        method='post',
        url='/api/register',
        data={"email": email, "password": password}
    )

    assert resp.status_code == 400
    assert resp.json()['error'] == 'Note: Only defined users succeed registration'



def test_login_successful():
    email = "eve.holt@reqres.in"
    password = "cityslicka"

    resp = requests_api(
        service='reqres',
        method='post',
        url='/api/login',
        data={"email": email, "password": password}
    )

    assert resp.status_code == 200
