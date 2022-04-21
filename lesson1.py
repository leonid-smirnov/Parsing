import requests
import json

url = 'https://api.github.com/users/octocat/repos'  # Обозначаем переменную url и указываем путь к API

req = requests.get(url)  # Посылаем запрос к API
data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
req.close()

jsObj = json.loads(data)  # Переводим в JSON

# Создаем новый документ, записываем в него ответ запроса, после закрываем
FileName = './file.json'
f = open(FileName, mode='w', encoding='utf8')
f.write(json.dumps(jsObj, ensure_ascii=False))
f.close()
print(jsObj)
