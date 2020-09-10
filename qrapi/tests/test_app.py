import pytest
import os

from ..app import app as flask_app


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    app.config['TESTING'] = True
    return app.test_client()


@pytest.mark.parametrize(
    ["authorization", "expected_code"],
    [
        [os.getenv('API_AUTHORIZATION_TOKEN'), 200],
        ['thistokeniscompletelywrongandmocke', 401]
    ]
)
def test_upload_pdf(client, authorization, expected_code):
    file_object = open('tests/files/example_paylogic.pdf', 'rb')

    headers = {
        'Authorization': authorization,
    }

    data = {
        'file[]': [(file_object, "example_paylogic.pdf")],
    }

    response = client.post(
        "/upload",
        data=data,
        headers=headers,
        follow_redirects=True,
        content_type='multipart/form-data'
    )
    file_object.close()

    assert response.status_code == expected_code

    if response.status_code == 200:
        assert response.get_json() == [{
            'content': [{'data': '5499944158390', 'page': 0, 'type': 'QRCODE'},
                        {'data': '5499944158390', 'page': 0, 'type': 'EAN13'}],
            'filename': 'example_paylogic.pdf',
            'num_pages': 1,
            'key': 'file[]'
        }]
