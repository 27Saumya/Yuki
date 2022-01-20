import giphy_client
import config
import random

giphy = giphy_client.DefaultApi()

results = giphy.gifs_search_get(config.GIPHY_API_KEY, "hello", limit=10)

listR = list(results.data)

gifID = random.choice(listR)

gif = giphy_client.Gif(id=gifID)

print(gif.content_url)