import requests
import lxml.html
import datetime
import re
import traceback

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
		#print data
		doc = lxml.html.document_fromstring(data)
		# получаем индекс записи, в которой находится гороскоп, а не спам
		# гороскопная запись начинается с даты
		now = datetime.datetime.now()
		date = now.day
		answer = ""
		records = doc.xpath('//div[@class="wall_post_text"]')
		found = False
		found_record = None
		for record in records:
			line = str(record.text)
			print(line)
			# получаем из строки дату
			match = re.search(r'[0-9]+', line)
			if match and match.group(0) == str(date):
				found_record = record
				found = True
				break
		if not found:
			records = doc.xpath('//div[@class="wall_post_text zoom_text"]')
			for record in records:
				line = str(record.text)
				print(line)
				# получаем из строки дату
				match = re.search(r'[0-9]+', line)
				if match and match.group(0) == str(date):
					found_record = record
					found = True
					break
		if not found:
			records = doc.xpath('//div[@class="pi_text"]')
			for record in records:
				line = str(record.text)
				print(line)
				# получаем из строки дату
				match = re.search(r'[0-9]+', line)
				if match and match.group(0) == str(date):
					found_record = record
					found = True
					break
		if found:
			date = str(found_record.text)
			answer = str(found_record.text_content())
			#adding line break between date and horoscope text
			lines = answer.split(date)
			answer = date
			for line in lines:
				answer = answer + line + "\n"
			return(answer)
		else:
			return("Не найден гороскоп на сегодняшний день. Возможно, авторы не обновили его на странице ВКонтакте")
	except Exception as e:
		traceback.print_exc()
		return(str(e))
