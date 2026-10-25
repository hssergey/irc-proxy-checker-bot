import requests
import lxml.html
import datetime
import re
import traceback
import json

MAIN_URL = "http://vk.com/public"

SIGNS = {
	"ева": 		"38522059",
	"ев": 		"38522045",
	"ак": 		"38521969",
	"лизнецы": 	"38521907",
	"вен": 		"38521859",
	"елец": 	"38521895",
	"корпион":	"38522062",
	"ыбы":		"38522233",
	"одолей":	"38522220",
	"озерог":	"38522196",
	"есы":		"38522067",
	"трелец":	"38522190",
}


months = [
	'января',
	'февраля',
	'марта',
	'апреля',
	'мая',
	'июня',
	'июля',
	'августа',
	'сентября',
	'октября',
	'ноября',
	'декабря'
]


def vkhoroscope(body):
	try:
		body = body.split(" ")
		if len(body) < 2:
			return(u'Необходимо указать знак зодиака')
		sign = body[1].lower()[1:]
# 		print(sign)
		try:
			vkGroup = SIGNS[sign]
		except Exception as e:
			return('Не найден URL группы ВКонтакте. Проверьте правильность написания знака зодиака: ' + body[1])
		headers = {
		    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/106.0",
		}
		url = MAIN_URL + vkGroup
		response = requests.get(url, headers = headers)
		data = response.text
# 		data = data.decode('windows-1251')
		# print(data)
		doc = lxml.html.document_fromstring(data)
		# получаем индекс записи, в которой находится гороскоп, а не спам
		# гороскопная запись начинается с даты
		now = datetime.datetime.now()
		# print(f'month = {now.month}')
		date = f'{now.day} {months[now.month-1]}'
		records = doc.xpath('//div[@class="PostContentContainer__root PostContentContainer"]')
		for root_record in records:
			data = root_record.get('data-exec')
			unquoted_data = requests.utils.unquote(data)
			data_obj = json.loads(unquoted_data)
			text = data_obj['PostContentContainer/init']['item']['text']
			if date in text:
				text = text.replace("<br>", "\n").replace('&#33;', '!')
				return text
		return("Не найден гороскоп на сегодняшний день. Возможно, авторы не обновили его на странице ВКонтакте")
	except Exception as e:
		traceback.print_exc()
		return(str(e))
