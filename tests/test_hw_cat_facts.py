from conftest import requests_api
import os
import json
from jsonschema.validators import validate
from conftest import resources_path

def test_cat_facts_breed_schema():
    with open(os.path.join(resources_path, 'cat_facts_breed_schema.json')) as file:
        schema = json.loads(file.read())

    response = requests_api(service='catfact', method='get', url='/breeds')
    validate(instance=response.json(), schema=schema)


def test_cat_facts_schema():
    with open(os.path.join(resources_path, 'catfacts_schema.json')) as file:
        schema = json.loads(file.read())

    response = requests_api(service='catfact', method='get', url='/fact')
    validate(instance=response.json(), schema=schema)



def test_get_breeds():
    limit = 18
    breed = 'American Shorthair'

    response = requests_api(service='catfact', method='get', url='/breeds', params={"limit": limit})

    assert response.status_code == 200
    assert response.json()['per_page'] == str(limit)
    assert len(response.json()['data']) == limit
    assert response.json()['data'][4]['breed'] == breed


def test_get_fact():
    len_max = 30
    response = requests_api(service='catfact', method='get', url='/fact', params={"max_length": len_max})

    assert response.status_code == 200
    assert response.json()['fact'] is not None
    assert response.json()['length'] <= len_max


def test_get_facts():
    default_limit = 10

    response = requests_api(service='catfact', method='get', url='/facts')

    assert response.status_code == 200
    assert response.json()['per_page'] == default_limit
    assert len(response.json()['data']) is not None
