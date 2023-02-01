import requests
import json


request = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json() # Делаем запрос к ЦБ, он возвращает json со всеми курсами
# здесь информация о курсах
print(request['Valute'])
# дата и время на которое сформированы курсы
print(request['Date'])
# получить курс доллара
print(request['Valute']['USD']['Value'])
# получить курс доллара
print(request['Valute']['EUR']['Value'])

for key in request['Valute']:
    print (f"{key}   {request['Valute'][key]['Value']}")
