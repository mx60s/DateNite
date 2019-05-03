import http.client
import json

conn = http.client.HTTPSConnection("api.themoviedb.org")

payload = "{}"

conn.request("GET", "/3/movie/now_playing?page=1&language=en-US&api_key=4f8eb69d2b4817d88b7ca064921660c2", payload)

res = conn.getresponse()
data = res.read()

data = data.decode("utf-8")

data = json.loads(data)
for movies in data['results']:
      print(movies['title'], movies['popularity'])
