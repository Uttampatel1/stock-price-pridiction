import requests
headers = {
    'Content-Type': 'application/json'
}
requestResponse = requests.get("https://api.tiingo.com/tiingo/utilities/search?query=apple&token=a645fee24b4c7ff5222ad0b26aa9b8819d6788df", headers=headers)
print(requestResponse.json())