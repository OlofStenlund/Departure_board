
# To generate token
token_generation_base_url = "https://ext-api.vasttrafik.se/token"
token_generation_headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Basic UWhsYjd6VGVvNHhUbHNIbXhVZ0lOTzIzamh3YTpiMXZtekJEUU1jUTNzQmJOWGJDUlBkX0JRc2dh'}


# To establish connection
stop = "Brunnsbotorget"
connection_base_url = "https://ext-api.vasttrafik.se/pr/v4"
connection_url = f"/locations/by-text?q={stop}&limit=10&offset=0"