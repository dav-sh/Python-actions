import pytest
from ..src.main import app


'''
        CONFIGURATION
'''
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

'''
        TEST
'''
def test_get_main(client):
    response = client.get('/')
    json_data = response.get_json()
    assert response.status_code == 200
    # assert json_data['message'] == 'hola'


'''
AUTHOR
'''
# GET
def test_get_list_authors(client):
    response = client.get('/author')
    json_data = response.get_json()
    print(json_data)
    assert response.status_code == 200
    assert json_data[0]['id'] == 1
    assert json_data[1]['name'] == 'Einstein'

# GET
def test_get_list_authors(client):
    response = client.get('/author')
    json_data = response.get_json()
    
    for tmp in json_data:
        if tmp.get('id') == 4:
            assert response.status_code == 200
            assert tmp.get('name') == 'Cerebron'

# GET BY ID
def test_get_author_by_id(client):
    id = 1
    response = client.get(f'/author/{id}')
    json_data = response.get_json()
    print(json_data)
    if json_data['id'] == id:
        assert response.status_code == 200
        assert json_data['name'] == 'Einstein'

# CREATE
def test_create_author(client):
    data ={
        "name" : "Jackie Chan"
    }
    response = client.post('/author', json=data)
    assert response.status_code == 201

# DELETE BY ID
def test_delete_author_by_id(client):
    id = 8
    response = client.delete(f'/author/{id}')
    # json_data = response.get_json()
    assert response.status_code == 404


# UPDATE
def test_update_author_by_id(client):
    id = 7
    data ={
        "name" : "Jackie Chan"
    }
    response = client.put(f'/author/{id}', json = data)
    # json_data = response.get_json()
    assert response.status_code == 200


'''
BOOK
'''

'''
AUTHOR
'''
# GET
def test_get_list_books(client):
    response = client.get('/book')
    json_data = response.get_json() #Returns a list with dictionaries
    print(json_data)
    assert response.status_code == 200
    assert json_data[0]['isbn'] == 2
    assert json_data[0]['title'] == 'Picapiedras 2'


# GET BY ID
def test_get_book_by_id(client):
    id = 2
    response = client.get(f'/book/{id}')
    json_data = response.get_json()
    print(json_data)
    if json_data[0]["isbn"] == id:
        assert response.status_code == 200
        assert json_data[0]['title'] == 'Picapiedras 2'

# INSERT
def test_create_book(client):
    data = {
        "title": "Picapiedras",
        "price": 100,
        "quantity": 5,
        "genre": {
            "id": 1
        },
        "author": {
            "id": 1
    }
}
    response = client.post('/book', json=data)
    assert response.status_code == 201

# DELETE BY ID
def test_delete_book_by_id(client):
    id = 20
    response = client.delete(f'/book/{id}')
    # json_data = response.get_json()
    assert response.status_code == 404


# UPDATE
def test_update_book_by_id(client):
    id = 2
    data = {
        "author": {
            "id": 1
        },
        "genre": {
            "id": 1
        },
        "price": 200.0,
        "quantity": "1",
        "title": "Picapiedras 2"
    }
    response = client.put(f'/book/{id}', json = data)
    # json_data = response.get_json()
    assert response.status_code == 200

'''
GENRE
'''
# GET
def test_get_list_genres(client):
    response = client.get('/genre')
    json_data = response.get_json()
    print(json_data)
    assert response.status_code == 200
    assert json_data[0]['id'] == 1
    assert json_data[1]['name'] == 'Fiction'

# GET
def test_get_list_genres(client):
    response = client.get('/genre')
    json_data = response.get_json()
    
    for tmp in json_data:
        if tmp.get('id') == 3:
            print(tmp)
            assert response.status_code == 200
            assert tmp.get('name') == 'Thriller'

# GET BY ID
def test_get_genre_by_id(client):
    id = 1
    response = client.get(f'/genre/{id}')
    json_data = response.get_json()
    print(json_data)
    if json_data['id'] == id:
        assert response.status_code == 200
        assert json_data['name'] == 'Fiction'

# CREATE
def test_create_genre(client):
    data ={
        "name" : "Fiction"
    }
    response = client.post('/genre', json=data)
    assert response.status_code == 201

# DELETE BY ID
def test_delete_genre_by_id(client):
    id = 8
    response = client.delete(f'/genre/{id}')
    # json_data = response.get_json()
    assert response.status_code == 404


# UPDATE
def test_update_genre_by_id(client):
    id = 4
    data ={
        "name" : "Comics"
    }
    response = client.put(f'/genre/{id}', json = data)
    # json_data = response.get_json()
    assert response.status_code == 200


def test_update_genre_by_id_error(client):
    id = 4
    data ={
        "nambre" : "Comics"
    }
    response = client.put(f'/genre/{id}', json = data)
    # json_data = response.get_json()
    assert response.status_code == 422


def test_update_genre_by_id_error_empty(client):
    id = 4
    data ={
        "name" : ""
    }
    response = client.put(f'/genre/{id}', json = data)
    # json_data = response.get_json()
    assert response.status_code == 422