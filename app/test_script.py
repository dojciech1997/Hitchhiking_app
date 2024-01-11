# test_script.py
import requests


def test_add_person():
    url = 'http://localhost:5000/add_person'
    data = {
        'name': 'John Doe',
        'photo_url': 'https://yt3.googleusercontent.com/DDyvCUTNdp8LNaNz6aRIt16mvJ_anRJ0mi8IejIl1EzNRXlPnXFL09lHkOfz8RLKNNw8ELFgKQ=s900-c-k-c0x00ffffff-no-rj',
        'description': 'A test person for testing purposes',
        'tags': 'test,example'
    }

    response = requests.post(url, data=data)

    print(f"Status code: {response.status_code}")
    print(f"Response content: {response.content}")

    if response.status_code != 302:
        print("Test failed!")
    #assert response.status_code == 302

if __name__ == "__main__":
    test_add_person()