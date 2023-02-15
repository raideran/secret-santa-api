import requests

BASE = 'http://127.0.0.1:5000/'
# BASE = 'http://ssapi.japscr.com/'

all_data = [
    {'name': 'Beethoven', 'likes': 10, 'views': 150},
    {'name': 'Batman', 'likes': 10, 'views': 150},
    {'name': 'Wonder Woman', 'likes': 10, 'views': 150},
    {'name': 'Aquaman', 'likes': 10, 'views': 150},
]

for index in range(len(all_data)):
    response = requests.put(BASE + 'video/'+str(index), data=all_data[index])
    print(response.json(), "Code: ", response.status_code)

# response = requests.get(BASE + 'video/2')
# print(response.json(), "Code: ", response.status_code)
# response = requests.get(BASE + 'video/10')
# print(response.json(), "Code: ", response.status_code)

# response = requests.delete(BASE + 'video/2')
# print(response.json(), "Code: ", response.status_code)
# response = requests.get(BASE + 'video/2')
# print(response.json(), "Code: ", response.status_code)
# response = requests.get(BASE + 'video/2')
# print(response.json(), "Code: ", response.status_code)
#
#
