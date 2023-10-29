import requests
url = ('https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=b9b1773270244c4d8434667cedaa09b7')
response = requests.get(url)
print(response[9])
                    