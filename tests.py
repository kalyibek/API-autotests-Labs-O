import requests
import pytest

base_url = "http://194.152.37.7:4445/api/tutorials"

input_data = {
    "title": "Java Core tutorial",
    "description": "Learning Java Core for free!"
}

expected_data = {
    "title": "Java Core tutorial",
    "description": "Learning Java Core for free!",
    "published": False
}

updated_data = {
    "title": "Java Core tutorial (new)",
    "description": "Learning Java Core for free! (new)",
    "published": True
}

keyword = "Java Core"


@pytest.fixture
def unique_id():
    return requests.post(base_url, json=input_data).json()["id"]


def test_create_tutorial():
    response = requests.post(base_url, json=input_data)
    assert response.status_code == 201
    expected_data["id"] = response.json()["id"]
    assert response.json() == expected_data
    requests.delete(f"{base_url}/{unique_id}")


def test_get_all_tutorials():
    response = requests.get(base_url)
    assert response.status_code == 200
    resources = response.json()
    assert isinstance(resources, list)


def test_read_tutorial(unique_id):
    response = requests.get(f"{base_url}/{unique_id}")
    assert response.status_code == 200
    expected_data["id"] = unique_id
    assert response.json() == expected_data


def test_read_all_tutorials_by_keyword():
    response = requests.get(f"{base_url}?title={keyword}")
    assert response.status_code == 200
    tutorials = response.json()

    for tutorial in tutorials:
        title = tutorial["title"]
        assert keyword.lower() in title.lower()


def test_update_tutorial(unique_id):
    response = requests.put(f"{base_url}/{unique_id}", json=updated_data)
    assert response.status_code == 200
    updated_data["id"] = unique_id
    assert response.json() == updated_data


def test_read_all_published_tutorials():
    response = requests.get(f"{base_url}/published")
    assert response.status_code == 200
    tutorials = response.json()

    for tutorial in tutorials:
        assert tutorial["published"]


def test_delete_tutorial(unique_id):
    response = requests.delete(f"{base_url}/{unique_id}")
    assert response.status_code == 204

    response = requests.get(f"{base_url}/{unique_id}")
    assert response.status_code == 404


def test_delete_all_tutorials():
    response = requests.delete(base_url)
    assert response.status_code == 204


if __name__ == "__main__":
    pytest.main([__file__])
