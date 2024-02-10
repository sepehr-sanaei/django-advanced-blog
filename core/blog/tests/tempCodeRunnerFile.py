
        api_client.force_authenticate(user=user)
        response = api_client.post(url, data)
        print(response.content)
        assert response.status_code == 201
        