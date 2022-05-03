async def test_access_success(client, student_token):
    _, token = student_token

    response = client.get(
        '/api/profile/courses',
        headers={'Authorization': f"Bearer {token['access_token']}"},
    )

    assert response.status_code == 200


async def test_refresh_success(client, student_token):
    _, token = student_token

    access_token = client.post(
        '/api/auth/login/refresh',
        headers={'Authorization': f"Bearer {token['refresh_token']}"},
    ).json()['access_token']

    response = client.get(
        '/api/profile/courses', headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == 200


async def test_access_missing_token_error(client):
    response = client.get(
        '/api/profile/courses',
    )

    assert response.status_code == 403


async def test_access_wrong_role(client, student_token):
    _, token = student_token

    response = client.put(
        '/api/profile/solutions/1',
        json={'review': 'review', 'score': 10},
        headers={'Authorization': f"Bearer {token['access_token']}"},
    )

    assert response.status_code == 403


async def test_access_invalid_token(client, student_token):
    _, token = student_token

    invalid_token = token['access_token'][:-1]
    response = client.get(
        '/api/profile/courses', headers={'Authorization': f'Bearer {invalid_token}'}
    )
    print(response.json())
    assert response.status_code == 422
