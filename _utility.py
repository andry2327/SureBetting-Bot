# get json API response

from requests import get
import json

url = "https://api.wheretheiss.at/v1/satellites/25544"
response = get(url)

# dump response into json
result = response.content.decode('utf-8')
result = json.loads(result)
print(result)  # print raw json

# print as key-value pairs
for item in result:
    print("{0} : {1}".format(item, result[item]))
