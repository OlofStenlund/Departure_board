if __name__ == '__main__':
    import requests
    from main import token_generation_headers, token_generation_base_url
    resp = requests.post(token_generation_base_url, data='grant_type=client_credentials', headers = token_generation_headers)
    data = resp.json()
    token = data['access_token']
    def save_token(token):
        with open("token.txt", "w") as file:
            file.write(token)
    save_token(token)