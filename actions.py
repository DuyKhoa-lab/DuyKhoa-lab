# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from bs4 import BeautifulSoup

from rasa_sdk.events import SlotSet
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.events import Restarted

import requests
import json
import feedparser
import urllib3
import random
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
#----------------------------------------------------------------------------------------------------------28/5/2020----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------Hủy nhận tin---------------------------------------------
class Action_Huy_ID(Action):
	def name(self) -> Text:
		return "Action_Huy_ID"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		conversation_id = tracker.sender_id
		conversation_id = str(conversation_id)
		#Get last name - firt name
		token = "EAADXVqpLOtMBACBEd8RiNxS0WCob7ZCGsut4NeMMU8aBPBg2nDAeJkfFCzaAmt0HsqrFx1kIGl0i9gQgcqLleymUtlsv6DWgTJneLQITiyEwptFQr55owuBYDldZB3fQhZB2zLxQfXyxCgZCtNuA5GJBh8C0wJukzECKTgFpT5FcqGZAuDQHIhymHUNuGMS8ZD"
		image_instagram = "https://graph.facebook.com/"+conversation_id+"?fields=first_name%2Clast_name&access_token="+token
		req_image = requests.get(image_instagram)
		convert_1 = req_image.text
		load_image = json.loads(convert_1)
		first_name = load_image['last_name']
		first_name +=" " + load_image['first_name']

		#Get_ID
		import gspread
		from oauth2client.service_account import ServiceAccountCredentials
		from datetime import datetime
		scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
		creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
		client = gspread.authorize(creds)
		sheet = client.open("BAR").sheet1
		data = sheet.get_all_records()
		try:
			List = sheet.find(conversation_id)
			List = str(List)
			strip = List.strip("<>Cell R")
			st = strip[:-21]
			sheet.delete_row(int(st))
			Text = "Chào " +first_name+ " bạn đã hủy nhận tin nhắn thành công"
			dispatcher.utter_message(text=Text)
		except:
			Error = "Bạn chưa đăng ký nhận tin"
			dispatcher.utter_message(text=Error)
		return []
#---------------------------------------------------Hủy nhận ti----------------------------------------------

class Action_Get_ID(Action):
	def name(self) -> Text:
		return "Action_Get_ID"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		conversation_id = tracker.sender_id
		conversation_id = str(conversation_id)
		#Get last name - firt name
		token = "EAADXVqpLOtMBACBEd8RiNxS0WCob7ZCGsut4NeMMU8aBPBg2nDAeJkfFCzaAmt0HsqrFx1kIGl0i9gQgcqLleymUtlsv6DWgTJneLQITiyEwptFQr55owuBYDldZB3fQhZB2zLxQfXyxCgZCtNuA5GJBh8C0wJukzECKTgFpT5FcqGZAuDQHIhymHUNuGMS8ZD"
		image_instagram = "https://graph.facebook.com/"+conversation_id+"?fields=first_name%2Clast_name&access_token="+token
		req_image = requests.get(image_instagram)
		convert_1 = req_image.text
		load_image = json.loads(convert_1)
		first_name = load_image['last_name']
		first_name +=" " + load_image['first_name']

		#Get_ID
		import gspread
		from oauth2client.service_account import ServiceAccountCredentials
		from datetime import datetime
		scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
		creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
		client = gspread.authorize(creds)
		sheet = client.open("BAR").sheet1
		data = sheet.get_all_records()
		now = datetime.now()
		now = str(now)
		col = sheet.col_values(2)
		insertRow = [now,conversation_id,first_name]
		if(conversation_id not in col):
			sheet.insert_row(insertRow, 2)

		Text = "Chào " +first_name+ " cảm ơn bạn đã đăng ký nhận tin. Tôi sẽ gửi đến bạn các diễn biến mới nhất của khoa Công nghệ thông tin - Robot và trí tuệ nhân tạo"
		dispatcher.utter_message(text=Text)
		return []
#----------------------------------------------------------------------------------------------------------28/5/2020----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Action_ThongTinTuyenSinh(Action):
	def name(self) -> Text:
		return "Action_ThongTinTuyenSinh"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		source = requests.get('https://tuyensinh.bdu.edu.vn/chuyen-muc/thong-bao-tuyen-sinh/dai-hoc-chinh-quy', verify = False).text
		soup = BeautifulSoup(source, 'html.parser')
		try:
			main_row = soup.find_all("div", class_="td-block-span6")
			template_items = []
			for i in range(0,6):
				numberimg = main_row[i].find("img")["src"]
				numbertitle = main_row[i].find("a")["title"]
				number1href = main_row[i].find("a")["href"]
				template_item = {
					"title": f"{numbertitle}",
					"image_url": f"{numberimg}",
					"default_action": {
						"type": "web_url",
						"url": f"{number1href}",
						"webview_height_ratio": "full",
					},
					"buttons": [
						{
							"type": "web_url",
							"url": f"{number1href}",
							"title": "🔍️Xem tin ngay"
						}
					]
				}
				template_items.append(template_item)

			message_str = {
				"attachment": {
					"type": "template",
					"payload": {
						"template_type": "generic",
						"elements": template_items
					}
				}
			}
		except:
			message_str = "Hệ thống đang cập nhật"

		dispatcher.utter_message(json_message=message_str)
		return []

#----------------------------------------------------------------------------------------------------------10/5/2020----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class action_unclear(Action):
	def name(self) -> Text:
		return "action_unclear"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		gt = {
			"attachment": {
				"type": "template",
				"payload": {
					"template_type": "generic",
					"elements": [
						{
							"title": "Thông tin khoa",
							"image_url": "https://www.upsieutoc.com/images/2020/05/05/Gioi-thieu-khoa.jpg",
							"subtitle": "Thông tin tuyển sinh, chuyên ngành đào tạo...",
							"default_action": {
								"type": "web_url",
								"url": "https://fit.bdu.edu.vn/",
								"webview_height_ratio": "full",
							},
							"buttons": [
								{
									"type": "postback",
									"title": "📄Giới thiệu khoa",
									"payload": "/Gioi_Thieu_Khoa"
								},
								{
									"type": "postback",
									"title": "📝️Chuyên ngành đào tạo",
									"payload": "/Chuong_Trinh_Dao_Tao"
								},
								#{
								#	"type": "postback",
								#	"title": "🏰️Giới thiệu khoa",
								#	"payload": "/Gioi_Thieu_Khoa"
								#},
								{
									"type": "web_url",
									"url": "https://docs.google.com/forms/d/e/1FAIpQLSfFQxxMv62asASsAycj2k2kiV5krKnKcB_lbHeq_zDjXXrhyg/viewform?usp=sf_link",
									"title": "✉Thông tin liên hệ",
									"webview_height_ratio": "full"
								}	
								
							]
						},
						{
							"title": "Khung Chương trình đào tạo, tuyển sinh",
							"image_url": "https://fit.bdu.edu.vn/wp-content/uploads/2019/06/training-324x152.jpg",
							"subtitle": "Khung chương trình đào tạo, Lộ trình đào tạo, Đăng ký xét tuyển online...",
							"default_action": {
								"type": "web_url",
								"url": "https://fit.bdu.edu.vn/",
								"webview_height_ratio": "full",
							},
							"buttons": [
								{
									"type": "postback",
									"title": "📖️Khung CTĐT",
									"payload": "/Khung_Chuong_Trinh_Dao_Tao"
								},
								{
									"type": "postback",
									"title": "📊Lộ trình đào tạo",
									"payload": "/Lo_Trinh_Dao_Tao"
								},
								{
									"type": "postback",
									"title": "📝Đăng ký xét tuyển online",
									"payload": "/Dang_Ky_Xet_tuyen_Online"
								}
								
							]
						},
						{
							"title": "Thông tin sự kiện, tin tức",
							"image_url": "https://www.upsieutoc.com/images/2020/04/25/unnamed-2.jpg",
							"subtitle": "Giới thiệu trường, sự kiện khoa, tin tức trường...",
							"default_action": {
								"type": "web_url",
								"url": "https://fit.bdu.edu.vn/",
								"webview_height_ratio": "full",
							},
							"buttons": [
								{
									"type": "postback",
									"title": "🏢️Giới thiệu trường",
									"payload": "/Gioi_Thieu_Truong"
								},
								{
									"type": "postback",
									"title": "📰️Tin tức trường",
									"payload": "/Tin_Tuc"
								},
								#{
								#	"type": "postback",
								#	"title": "📝️Sự kiện khoa",
								#	"payload": "/Su_Kien"
								#},
								{
									"type": "postback",
									"title": "📝️Thông tin tuyển sinh",
									"payload": "/Thong_Tin_Tuyen_Sinh"
								}

								#{
								#	"type": "postback",
								#	"title": "🧐️Công bố khoa học",
								#	"payload": "/Cong_Bo_Khoa_Hoc"
								#},
								
							]
						},
						{
							"title": "Thông tin hợp tác",
							"image_url": "https://www.bdu.edu.vn/wp-content/uploads/2019/12/Cisco-16.jpg",
							"subtitle": "Hợp tác trong nước-quốc tế, Lãnh đạo khoa",
							"default_action": {
								"type": "web_url",
								"url": "https://fit.bdu.edu.vn/",
								"webview_height_ratio": "full",
							},
							"buttons": [
								{
									"type": "postback",
									"title": "📝️Sự kiện khoa",
									"payload": "/Su_Kien"
								},
								{
									"type": "postback",
									"title": "🇻Công bố khoa học",
									"payload": "/Cong_Bo_Khoa_Hoc"
								},
								#{
								#	"type": "postback",
								#	"title": "🌍️Hợp tác quốc tế",
								#	"payload": "/Hop_Tac_Quoc_Te"
								#},
								{
									"type": "postback",
									"title": "👨‍👩‍👦‍👦️Hội nghị-hội thảo",
									"payload": "/HoiThao_HoiNgi"
								}
								
							]
						}
					]
				}
			}
		}

		dispatcher.utter_message(json_message=gt)
		return []

class action_default_fallback(Action):
	def name(self) -> Text:
		return "action_default_fallback"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		gt = {
			"attachment": {
				"type": "template",
				"payload": {
					"template_type": "generic",
					"elements": [
						{
							"title": "Thông tin khoa",
							"image_url": "https://www.upsieutoc.com/images/2020/05/05/Gioi-thieu-khoa.jpg",
							"subtitle": "Thông tin tuyển sinh, chuyên ngành đào tạo...",
							"default_action": {
								"type": "web_url",
								"url": "https://fit.bdu.edu.vn/",
								"webview_height_ratio": "full",
							},
							"buttons": [
								{
									"type": "postback",
									"title": "📄Giới thiệu khoa",
									"payload": "/Gioi_Thieu_Khoa"
								},
								{
									"type": "postback",
									"title": "📝️Chuyên ngành đào tạo",
									"payload": "/Chuong_Trinh_Dao_Tao"
								},
								#{
								#	"type": "postback",
								#	"title": "🏰️Giới thiệu khoa",
								#	"payload": "/Gioi_Thieu_Khoa"
								#},
								{
									"type": "web_url",
									"url": "https://docs.google.com/forms/d/e/1FAIpQLSfFQxxMv62asASsAycj2k2kiV5krKnKcB_lbHeq_zDjXXrhyg/viewform?usp=sf_link",
									"title": "✉Thông tin liên hệ",
									"webview_height_ratio": "full"
								}	
								
							]
						},
						{
							"title": "Khung Chương trình đào tạo, tuyển sinh",
							"image_url": "https://fit.bdu.edu.vn/wp-content/uploads/2019/06/training-324x152.jpg",
							"subtitle": "Khung chương trình đào tạo, Lộ trình đào tạo, Đăng ký xét tuyển online...",
							"default_action": {
								"type": "web_url",
								"url": "https://fit.bdu.edu.vn/",
								"webview_height_ratio": "full",
							},
							"buttons": [
								{
									"type": "postback",
									"title": "📖️Khung CTĐT",
									"payload": "/Khung_Chuong_Trinh_Dao_Tao"
								},
								{
									"type": "postback",
									"title": "📊Lộ trình đào tạo",
									"payload": "/Lo_Trinh_Dao_Tao"
								},
								{
									"type": "postback",
									"title": "📝Đăng ký xét tuyển online",
									"payload": "/Dang_Ky_Xet_tuyen_Online"
								}
								
							]
						},
						{
							"title": "Thông tin sự kiện, tin tức",
							"image_url": "https://www.upsieutoc.com/images/2020/04/25/unnamed-2.jpg",
							"subtitle": "Giới thiệu trường, sự kiện khoa, tin tức trường...",
							"default_action": {
								"type": "web_url",
								"url": "https://fit.bdu.edu.vn/",
								"webview_height_ratio": "full",
							},
							"buttons": [
								{
									"type": "postback",
									"title": "🏢️Giới thiệu trường",
									"payload": "/Gioi_Thieu_Truong"
								},
								{
									"type": "postback",
									"title": "📰️Tin tức trường",
									"payload": "/Tin_Tuc"
								},
								#{
								#	"type": "postback",
								#	"title": "📝️Sự kiện khoa",
								#	"payload": "/Su_Kien"
								#},
								{
									"type": "postback",
									"title": "📝️Thông tin tuyển sinh",
									"payload": "/Thong_Tin_Tuyen_Sinh"
								}

								#{
								#	"type": "postback",
								#	"title": "🧐️Công bố khoa học",
								#	"payload": "/Cong_Bo_Khoa_Hoc"
								#},
								
							]
						},
						{
							"title": "Thông tin hợp tác",
							"image_url": "https://www.bdu.edu.vn/wp-content/uploads/2019/12/Cisco-16.jpg",
							"subtitle": "Hợp tác trong nước-quốc tế, Lãnh đạo khoa",
							"default_action": {
								"type": "web_url",
								"url": "https://fit.bdu.edu.vn/",
								"webview_height_ratio": "full",
							},
							"buttons": [
								{
									"type": "postback",
									"title": "📝️Sự kiện khoa",
									"payload": "/Su_Kien"
								},
								{
									"type": "postback",
									"title": "🇻Công bố khoa học",
									"payload": "/Cong_Bo_Khoa_Hoc"
								},
								#{
								#	"type": "postback",
								#	"title": "🌍️Hợp tác quốc tế",
								#	"payload": "/Hop_Tac_Quoc_Te"
								#},
								{
									"type": "postback",
									"title": "👨‍👩‍👦‍👦️Hội nghị-hội thảo",
									"payload": "/HoiThao_HoiNgi"
								}
								
							]
						}
					]
				}
			}
		}

		dispatcher.utter_message(json_message=gt)
		return []
#----------------------------------------------------------------------------------------------------------10/5/2020----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------9/5/2020----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Action_Dang_Ky_Xet_Tuyen_Online(Action):
	def name(self) -> Text:
		return "Action_Dang_Ky_Xet_Tuyen_Online"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		Gioithieu = "🔵Cách thức đăng ký:\n🔹Cách 1: Chuyển phát nhanh qua đường bưu điện.\n🔹Cách 2: Nộp trực tiếp tại trường.\n🔹Cách 3:Đăng ký online tại website"
		gt = {
			"attachment": {
				"type": "template",
				"payload": {
					"template_type": "generic",
					"elements": [
						{
							"title": "Đăng ký xét tuyển online",
							"image_url": "https://www.upsieutoc.com/images/2020/05/10/tuyensinh.png",
							"subtitle": "Các ngành đào tạo và chỉ tiêu tuyển sinh: Chỉ tiêu theo Ngành/ Nhóm ngành/ Khối ngành, theo từng phương thức tuyển sinh và trình độ đào tạo",
							"default_action": {
								"type": "web_url",
								"url": "https://xettuyenonline.bdu.edu.vn/",
								"messenger_extensions": "true",
								"webview_height_ratio":"full"
							},
							"buttons": [
								{
									"type": "web_url",
									"url":"https://xettuyenonline.bdu.edu.vn/",
									"title": "🔍️Xem ngay",
									"messenger_extensions": "true",
									"webview_height_ratio":"full"
								}
							]
						}
					]
				}
			}
		}

		dispatcher.utter_message(text=Gioithieu,json_message=gt)
		return []



class Action_Robot_Co_Hoi_Viec_Lam(Action):
	def name(self) -> Text:
		return "Action_Robot_Co_Hoi_Viec_Lam"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		image_instagram = "http://firactdt2019.tk/jsonThongTinTruong.php"
		req_image = requests.get(image_instagram)
		convert_1 = req_image.text
		load_image = json.loads(convert_1)
		main_link = load_image['RobotvaTriTueNhanTao'][3]['thongTinRobot'] +"\n"
		main_link += load_image['RobotvaTriTueNhanTao'][3]['noiDungRobot']
		dispatcher.utter_message(text=main_link)
		return []


class Action_Robot_Kien_Thuc_Dat_Duoc(Action):
	def name(self) -> Text:
		return "Action_Robot_Kien_Thuc_Dat_Duoc"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		image_instagram = "http://firactdt2019.tk/jsonThongTinTruong.php"
		req_image = requests.get(image_instagram)
		convert_1 = req_image.text
		load_image = json.loads(convert_1)
		main_link = load_image['RobotvaTriTueNhanTao'][2]['thongTinRobot'] +"\n"
		main_link += load_image['RobotvaTriTueNhanTao'][2]['noiDungRobot']
		dispatcher.utter_message(text=main_link)
		return []


class Action_Robot_Ly_Do_Chon_Nganh(Action):
	def name(self) -> Text:
		return "Action_Robot_Ly_Do_Chon_Nganh"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		image_instagram = "http://firactdt2019.tk/jsonThongTinTruong.php"
		req_image = requests.get(image_instagram)
		convert_1 = req_image.text
		load_image = json.loads(convert_1)
		main_link = load_image['RobotvaTriTueNhanTao'][1]['thongTinRobot'] +"\n"
		main_link += load_image['RobotvaTriTueNhanTao'][1]['noiDungRobot']
		dispatcher.utter_message(text=main_link)
		return []


class Action_HTTT_Co_Hoi_Viec_Lam(Action):
	def name(self) -> Text:
		return "Action_HTTT_Co_Hoi_Viec_Lam"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		image_instagram = "http://firactdt2019.tk/jsonThongTinTruong.php"
		req_image = requests.get(image_instagram)
		convert_1 = req_image.text
		load_image = json.loads(convert_1)
		main_link = load_image['HeThongThongTin'][3]['thongTinHTTT'] +"\n"
		main_link += load_image['HeThongThongTin'][3]['noiDungHTTT']
		dispatcher.utter_message(text=main_link)
		return []


class Action_HTTT_Kien_Thuc_Dat_Duoc(Action):
	def name(self) -> Text:
		return "Action_HTTT_Kien_Thuc_Dat_Duoc"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		image_instagram = "http://firactdt2019.tk/jsonThongTinTruong.php"
		req_image = requests.get(image_instagram)
		convert_1 = req_image.text
		load_image = json.loads(convert_1)
		main_link = load_image['HeThongThongTin'][2]['thongTinHTTT'] +"\n"
		main_link += load_image['HeThongThongTin'][2]['noiDungHTTT']
		dispatcher.utter_message(text=main_link)
		return []

class Action_HTTT_Ly_Do_Chon_Nganh(Action):
	def name(self) -> Text:
		return "Action_HTTT_Ly_Do_Chon_Nganh"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		image_instagram = "http://firactdt2019.tk/jsonThongTinTruong.php"
		req_image = requests.get(image_instagram)
		convert_1 = req_image.text
		load_image = json.loads(convert_1)
		main_link = load_image['HeThongThongTin'][1]['thongTinHTTT'] +"\n"
		main_link += load_image['HeThongThongTin'][1]['noiDungHTTT']
		dispatcher.utter_message(text=main_link)
		return []


class Action_ATTT_Co_Hoi_Viec_Lam(Action):
	def name(self) -> Text:
		return "Action_ATTT_Co_Hoi_Viec_Lam"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		image_instagram = "http://firactdt2019.tk/jsonThongTinTruong.php"
		req_image = requests.get(image_instagram)
		convert_1 = req_image.text
		load_image = json.loads(convert_1)
		main_link = load_image['AnToanThongTin'][3]['thongTinRobot'] +"\n"
		main_link += load_image['AnToanThongTin'][3]['noiDungRobot']
		dispatcher.utter_message(text=main_link)
		return []


class Action_ATTT_Kien_Thuc_Dat_Duoc(Action):
	def name(self) -> Text:
		return "Action_ATTT_Kien_Thuc_Dat_Duoc"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		image_instagram = "http://firactdt2019.tk/jsonThongTinTruong.php"
		req_image = requests.get(image_instagram)
		convert_1 = req_image.text
		load_image = json.loads(convert_1)
		main_link = load_image['AnToanThongTin'][2]['thongTinRobot'] +"\n"
		main_link += load_image['AnToanThongTin'][2]['noiDungRobot']
		dispatcher.utter_message(text=main_link)
		return []


class Action_ATTT_Ly_Do_Chon_Nganh(Action):
	def name(self) -> Text:
		return "Action_ATTT_Ly_Do_Chon_Nganh"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		image_instagram = "http://firactdt2019.tk/jsonThongTinTruong.php"
		req_image = requests.get(image_instagram)
		convert_1 = req_image.text
		load_image = json.loads(convert_1)
		main_link = load_image['AnToanThongTin'][1]['thongTinRobot'] +"\n"
		main_link += load_image['AnToanThongTin'][1]['noiDungRobot']
		dispatcher.utter_message(text=main_link)
		return []


class Action_KTPM_Co_Hoi_Viec_Lam(Action):
	def name(self) -> Text:
		return "Action_KTPM_Co_Hoi_Viec_Lam"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		image_instagram = "http://firactdt2019.tk/jsonThongTinTruong.php"
		req_image = requests.get(image_instagram)
		convert_1 = req_image.text
		load_image = json.loads(convert_1)
		main_link = load_image['HeThongThongTin'][3]['thongTinHTTT'] +"\n"
		main_link += load_image['HeThongThongTin'][3]['noiDungHTTT']
		dispatcher.utter_message(text=main_link)
		return []

class Action_KTPM_Kien_Thuc_Dat_Duoc(Action):
	def name(self) -> Text:
		return "Action_KTPM_Kien_Thuc_Dat_Duoc"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		image_instagram = "http://firactdt2019.tk/jsonThongTinTruong.php"
		req_image = requests.get(image_instagram)
		convert_1 = req_image.text
		load_image = json.loads(convert_1)
		main_link = load_image['HeThongThongTin'][2]['thongTinHTTT'] +"\n"
		main_link += load_image['HeThongThongTin'][2]['noiDungHTTT']
		dispatcher.utter_message(text=main_link)
		return []

class Action_KTPM_Ly_Do_Chon_Nganh(Action):
	def name(self) -> Text:
		return "Action_KTPM_Ly_Do_Chon_Nganh"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		image_instagram = "http://firactdt2019.tk/jsonThongTinTruong.php"
		req_image = requests.get(image_instagram)
		convert_1 = req_image.text
		load_image = json.loads(convert_1)
		main_link = load_image['HeThongThongTin'][1]['thongTinHTTT'] +"\n"
		main_link += load_image['HeThongThongTin'][1]['noiDungHTTT']
		dispatcher.utter_message(text=main_link)
		return []


class Action_Chuyen_Nganh_Dao_Tao_KTPM(Action):
	def name(self) -> Text:
		return "Action_Chuyen_Nganh_Dao_Tao_KTPM"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		ChuyenNganh = "➡️Thời gian đào tạo:4 năm\n➡️Hệ đào tạo:Đại học CNTT (Mã ngành 7480201)\n➡️Hình thức tuyển sinh:06 phương thức xét tuyển\n➡️Học phí:bình quân 20 triệu đồng/năm"
		gt = {
			"attachment": {
				"type": "template",
				"payload": {
					"template_type": "generic",
					"elements": [
						{
							"title": "Kỹ thuật phần mềm",
							"image_url": "https://www.upsieutoc.com/images/2020/04/29/ktpm.png",
							"subtitle": "➡️Thời gian đào tạo:4 năm\n➡️Hệ đào tạo:Đại học CNTT (Mã ngành 7480201)\n➡️Hình thức tuyển sinh:06 phương thức xét tuyển\n➡️Học phí:bình quân 20 triệu đồng/năm",
							"default_action": {
								"type": "web_url",
								"url": "https://fit.bdu.edu.vn/",
								"webview_height_ratio": "full",
							},
							"buttons": [
								{
									"type": "postback",
									"title": "❓Lý do chọn ngành",
									"payload": "/KTPM_Ly_Do_Chon_Nganh"
								},
								{
									"type": "postback",
									"title": "✍Kiến thức đạt được",
									"payload": "/KTPM_Kien_Thuc_Dat_Duoc"
								},
								{
									"type": "postback",
									"title": "🗣Cơ hội việc làm",
									"payload": "/KTPM_Co_Hoi_Viec_Lam"
								}
								
							]
						}
					]
				}
			}
		}

		dispatcher.utter_message(text=ChuyenNganh,json_message=gt)
		return []


class Action_Chuyen_Nganh_Dao_Tao_ATTT(Action):
	def name(self) -> Text:
		return "Action_Chuyen_Nganh_Dao_Tao_ATTT"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		ChuyenNganh = "➡️Thời gian đào tạo:4 năm\n➡️Hệ đào tạo:Đại học CNTT (Mã ngành 7480201)\n➡️Hình thức tuyển sinh:06 phương thức xét tuyển\n➡️Học phí:bình quân 20 triệu đồng/năm"
		gt = {
			"attachment": {
				"type": "template",
				"payload": {
					"template_type": "generic",
					"elements": [
						{
							"title": "Mạng máy tính và An toàn thông tin",
							"image_url": "https://www.upsieutoc.com/images/2020/04/29/attt.png",
							"subtitle": "➡️Thời gian đào tạo:4 năm\n➡️Hệ đào tạo:Đại học CNTT (Mã ngành 7480201)\n➡️Hình thức tuyển sinh:06 phương thức xét tuyển\n➡️Học phí:bình quân 20 triệu đồng/năm",
							"default_action": {
								"type": "web_url",
								"url": "https://fit.bdu.edu.vn/",
								"webview_height_ratio": "full",
							},
							"buttons": [
								{
									"type": "postback",
									"title": "❓Lý do chọn ngành",
									"payload": "/ATTT_Ly_Do_Chon_Nganh"
								},
								{
									"type": "postback",
									"title": "✍Kiến thức đạt được",
									"payload": "/ATTT_Kien_Thuc_Dat_Duoc"
								},
								{
									"type": "postback",
									"title": "🗣Cơ hội việc làm",
									"payload": "/ATTT_Co_Hoi_Viec_Lam"
								}
								
							]
						}
					]
				}
			}
		}

		dispatcher.utter_message(text=ChuyenNganh,json_message=gt)
		return []

class Action_Chuyen_Nganh_Dao_Tao_HTTT(Action):
	def name(self) -> Text:
		return "Action_Chuyen_Nganh_Dao_Tao_HTTT"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		ChuyenNganh = "➡️Thời gian đào tạo:4 năm\n➡️Hệ đào tạo:Đại học CNTT (Mã ngành 7480201)\n➡️Hình thức tuyển sinh:06 phương thức xét tuyển\n➡️Học phí:bình quân 20 triệu đồng/năm"
		gt = {
			"attachment": {
				"type": "template",
				"payload": {
					"template_type": "generic",
					"elements": [
						{
							"title": "Hệ thống thông tin",
							"image_url": "https://www.upsieutoc.com/images/2020/04/29/httt.png",
							"subtitle": "➡️Thời gian đào tạo:4 năm\n➡️Hệ đào tạo:Đại học CNTT (Mã ngành 7480201)\n➡️Hình thức tuyển sinh:06 phương thức xét tuyển\n➡️Học phí:bình quân 20 triệu đồng/năm",
							"default_action": {
								"type": "web_url",
								"url": "https://fit.bdu.edu.vn/",
								"webview_height_ratio": "full",
							},
							"buttons": [
								{
									"type": "postback",
									"title": "❓Lý do chọn ngành",
									"payload": "/HTTT_Ly_Do_Chon_Nganh"
								},
								{
									"type": "postback",
									"title": "✍Kiến thức đạt được",
									"payload": "/HTTT_Kien_Thuc_Dat_Duoc"
								},
								{
									"type": "postback",
									"title": "🗣Cơ hội việc làm",
									"payload": "/HTTT_Co_Hoi_Viec_Lam"
								}
								
							]
						}
					]
				}
			}
		}

		dispatcher.utter_message(text=ChuyenNganh,json_message=gt)
		return []


class Action_Chuyen_Nganh_Dao_Tao_Robot_TTNT(Action):
	def name(self) -> Text:
		return "Action_Chuyen_Nganh_Dao_Tao_Robot_TTNT"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		ChuyenNganh = "➡️Thời gian đào tạo:4 năm\n➡️Hệ đào tạo:Đại học CNTT (Mã ngành 7480201)\n➡️Hình thức tuyển sinh:06 phương thức xét tuyển\n➡️Học phí:bình quân 20 triệu đồng/năm"
		gt = {
			"attachment": {
				"type": "template",
				"payload": {
					"template_type": "generic",
					"elements": [
						{
							"title": "Robot và trí tuệ nhân tạo",
							"image_url": "https://www.upsieutoc.com/images/2020/05/11/rsz_robotedit.png",
							"subtitle": "➡️Thời gian đào tạo:4 năm\n➡️Hệ đào tạo:Đại học CNTT (Mã ngành 7480201)\n➡️Hình thức tuyển sinh:06 phương thức xét tuyển\n➡️Học phí:bình quân 20 triệu đồng/năm",
							"default_action": {
								"type": "web_url",
								"url": "https://fit.bdu.edu.vn/",
								"webview_height_ratio": "full",
							},
							"buttons": [
								{
									"type": "postback",
									"title": "❓Lý do chọn ngành",
									"payload": "/Robot_Ly_Do_Chon_Nganh"
								},
								{
									"type": "postback",
									"title": "✍Kiến thức đạt được",
									"payload": "/Robot_Kien_Thuc_Dat_Duoc"
								},
								{
									"type": "postback",
									"title": "🗣Cơ hội việc làm",
									"payload": "/Robot_Co_Hoi_Viec_Lam"
								}
								
							]
						}
					]
				}
			}
		}

		dispatcher.utter_message(text=ChuyenNganh,json_message=gt)
		return []

#-----------------------------------------------------Không có dòng 20 triệu-----------------------------------------------------------------
class Action_Chuyen_Nganh_Dao_Tao_KTPM_LyDo_KT_CH(Action):
	def name(self) -> Text:
		return "Action_Chuyen_Nganh_Dao_Tao_KTPM_LyDo_KT_CH"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		gt = {
			"attachment": {
				"type": "template",
				"payload": {
					"template_type": "generic",
					"elements": [
						{
							"title": "Kỹ thuật phần mềm",
							"image_url": "https://www.upsieutoc.com/images/2020/04/29/ktpm.png",
							"subtitle": "➡️Thời gian đào tạo:4 năm\n➡️Hệ đào tạo:Đại học CNTT (Mã ngành 7480201)\n➡️Hình thức tuyển sinh:06 phương thức xét tuyển\n➡️Học phí:bình quân 20 triệu đồng/năm",
							"default_action": {
								"type": "web_url",
								"url": "https://fit.bdu.edu.vn/",
								"webview_height_ratio": "full",
							},
							"buttons": [
								{
									"type": "postback",
									"title": "❓Lý do chọn ngành",
									"payload": "/KTPM_Ly_Do_Chon_Nganh"
								},
								{
									"type": "postback",
									"title": "✍Kiến thức đạt được",
									"payload": "/KTPM_Kien_Thuc_Dat_Duoc"
								},
								{
									"type": "postback",
									"title": "🗣Cơ hội việc làm",
									"payload": "/KTPM_Co_Hoi_Viec_Lam"
								}
								
							]
						}
					]
				}
			}
		}

		dispatcher.utter_message(json_message=gt)
		return []

class Action_Chuyen_Nganh_Dao_Tao_ATTT_LyDo_KT_CH(Action):
	def name(self) -> Text:
		return "Action_Chuyen_Nganh_Dao_Tao_ATTT_LyDo_KT_CH"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		gt = {
			"attachment": {
				"type": "template",
				"payload": {
					"template_type": "generic",
					"elements": [
						{
							"title": "Mạng máy tính và An toàn thông tin",
							"image_url": "https://www.upsieutoc.com/images/2020/04/29/attt.png",
							"subtitle": "➡️Thời gian đào tạo:4 năm\n➡️Hệ đào tạo:Đại học CNTT (Mã ngành 7480201)\n➡️Hình thức tuyển sinh:06 phương thức xét tuyển\n➡️Học phí:bình quân 20 triệu đồng/năm",
							"default_action": {
								"type": "web_url",
								"url": "https://fit.bdu.edu.vn/",
								"webview_height_ratio": "full",
							},
							"buttons": [
								{
									"type": "postback",
									"title": "❓Lý do chọn ngành",
									"payload": "/ATTT_Ly_Do_Chon_Nganh"
								},
								{
									"type": "postback",
									"title": "✍Kiến thức đạt được",
									"payload": "/ATTT_Kien_Thuc_Dat_Duoc"
								},
								{
									"type": "postback",
									"title": "🗣Cơ hội việc làm",
									"payload": "/ATTT_Co_Hoi_Viec_Lam"
								}
								
							]
						}
					]
				}
			}
		}

		dispatcher.utter_message(json_message=gt)
		return []


class Action_Chuyen_Nganh_Dao_Tao_HTTT_LyDo_KT_CH(Action):
	def name(self) -> Text:
		return "Action_Chuyen_Nganh_Dao_Tao_HTTT_LyDo_KT_CH"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		gt = {
			"attachment": {
				"type": "template",
				"payload": {
					"template_type": "generic",
					"elements": [
						{
							"title": "Hệ thống thông tin",
							"image_url": "https://www.upsieutoc.com/images/2020/04/29/httt.png",
							"subtitle": "➡️Thời gian đào tạo:4 năm\n➡️Hệ đào tạo:Đại học CNTT (Mã ngành 7480201)\n➡️Hình thức tuyển sinh:06 phương thức xét tuyển\n➡️Học phí:bình quân 20 triệu đồng/năm",
							"default_action": {
								"type": "web_url",
								"url": "https://fit.bdu.edu.vn/",
								"webview_height_ratio": "full",
							},
							"buttons": [
								{
									"type": "postback",
									"title": "❓Lý do chọn ngành",
									"payload": "/HTTT_Ly_Do_Chon_Nganh"
								},
								{
									"type": "postback",
									"title": "✍Kiến thức đạt được",
									"payload": "/HTTT_Kien_Thuc_Dat_Duoc"
								},
								{
									"type": "postback",
									"title": "🗣Cơ hội việc làm",
									"payload": "/HTTT_Co_Hoi_Viec_Lam"
								}
								
							]
						}
					]
				}
			}
		}

		dispatcher.utter_message(json_message=gt)
		return []

class Action_Chuyen_Nganh_Dao_Tao_Robot_TTNT_LyDo_KT_CH(Action):
	def name(self) -> Text:
		return "Action_Chuyen_Nganh_Dao_Tao_Robot_TTNT_LyDo_KT_CH"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		gt = {
			"attachment": {
				"type": "template",
				"payload": {
					"template_type": "generic",
					"elements": [
						{
							"title": "Robot và trí tuệ nhân tạo",
							"image_url": "https://www.upsieutoc.com/images/2020/05/11/rsz_robotedit.png",
							"subtitle": "➡️Thời gian đào tạo:4 năm\n➡️Hệ đào tạo:Đại học CNTT (Mã ngành 7480201)\n➡️Hình thức tuyển sinh:06 phương thức xét tuyển\n➡️Học phí:bình quân 20 triệu đồng/năm",
							"default_action": {
								"type": "web_url",
								"url": "https://fit.bdu.edu.vn/",
								"webview_height_ratio": "full",
							},
							"buttons": [
								{
									"type": "postback",
									"title": "❓Lý do chọn ngành",
									"payload": "/Robot_Ly_Do_Chon_Nganh"
								},
								{
									"type": "postback",
									"title": "✍Kiến thức đạt được",
									"payload": "/Robot_Kien_Thuc_Dat_Duoc"
								},
								{
									"type": "postback",
									"title": "🗣Cơ hội việc làm",
									"payload": "/Robot_Co_Hoi_Viec_Lam"
								}
								
							]
						}
					]
				}
			}
		}

		dispatcher.utter_message(json_message=gt)
		return []
#-----------------------------------------------------Không có dòng 20 triệu-----------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------9/5/2020----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class action_Random(Action):
	def name(self):
		return "action_Random"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		randomThongTin = "Chúng tôi đang cung cấp thông tin về:"

		randumBT = [{"title": "📝️Chuyên ngành đào tạo", "payload": "/Chuong_Trinh_Dao_Tao"},{"title": "🏢️Giới thiệu trường", "payload": "/Gioi_Thieu_Truong"},{"title": "🏰️Giới thiệu khoa", "payload": "/Gioi_Thieu_Khoa"},{"title": "📝️Sự kiện khoa", "payload": "/Su_Kien"},{"title": "👨‍👩‍👦‍👦️Hội nghị-Hội thảo", "payload": "/HoiThao_HoiNgi"},{"title": "👋Thông tin tuyển sinh", "payload": "/Thong_Tin_Tuyen_Sinh"},{"title": "🔔Đăng ký nhận tin", "payload": "/Dang_Ky_Nhan_tin"}]
		randomBTChoice = random.choice(randumBT)

		randomBT1 = [{"title": "📰️Tin tức trường", "payload": "/Tin_Tuc"},{"title": "🌍️Công bố khoa học", "payload": "/Cong_Bo_Khoa_Hoc"},{"title": "📩Thông tin liên hệ", "payload": "/From_Dang_Ky"},{"title": "📊Lộ trình đào tạo", "payload": "/Lo_Trinh_Dao_Tao"},{"title": "📝Đăng ký xét tuyển online", "payload": "/Dang_Ky_Xet_tuyen_Online"},{"title": "🔔Đăng ký nhận tin", "payload": "/Dang_Ky_Nhan_tin"}]
		randomBTChoice1 = random.choice(randomBT1)

		randomBT2 = [{"title": "📖️Menu chính", "payload": "/Menu_chinh"}]
		randomBTChoice2 = random.choice(randomBT2)

		buttonss = [randomBTChoice, randomBTChoice1, randomBTChoice2]
		randomBD = [buttonss]
		randomBDN = random.choice(randomBD)
		dispatcher.utter_message(text=randomThongTin, buttons=randomBDN)
		return []


class Action_CTDTQuick_replies(Action):
	def name(self) -> Text:
		return "Action_CTDTQuick_replies"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		message = {
			"text": "📔️Ngành công nghệ thông tin đào tạo 04 chuyên ngành:\n 1⃣Robot và trí tuệ nhân tạo\n 2⃣Mạng máy tính\n 3⃣Kỹ thuật phần mềm\n 4⃣Hệ thống thông tin",
			"quick_replies": [
				{
					"content_type": "text",
					"title": "🤖️Robot và TTNT",
					"payload": "/ChuyenNganhDaoTao_Robot_TTNT",
				},
				{
					"content_type": "text",
					"title": "⚙️Hệ thống thông tin",
					"payload": "/ChuyenNganhDaoTao_HTTT",
				},
				{
					"content_type": "text",
					"title": "🖥️Mạng máy tính và ATTT",
					"payload": "/ChuyenNganhDaoTao_ATTT",
				},
				{
					"content_type": "text",
					"title": "💾️Kỹ thuật phần mềm",
					"payload": "/ChuyenNganhDaoTao_KTPM",
				},
			]
		}

		dispatcher.utter_message(json_message=message)
		return []

class Action_CTDT(Action):
	def name(self) -> Text:
		return "Action_CTDT"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		
		gt = {
			"attachment": {
				"type": "template",
				"payload": {
					"template_type": "generic",
					"elements": [
						{
							"title": "Thông tin khoa",
							"image_url": "https://www.upsieutoc.com/images/2020/05/05/Gioi-thieu-khoa.jpg",
							"subtitle": "Thông tin tuyển sinh, chuyên ngành đào tạo...",
							"default_action": {
								"type": "web_url",
								"url": "https://fit.bdu.edu.vn/",
								"webview_height_ratio": "full",
							},
							"buttons": [
								{
									"type": "postback",
									"title": "📄Giới thiệu khoa",
									"payload": "/Gioi_Thieu_Khoa"
								},
								{
									"type": "postback",
									"title": "📝️Chuyên ngành đào tạo",
									"payload": "/Chuong_Trinh_Dao_Tao"
								},
								#{
								#	"type": "postback",
								#	"title": "🏰️Giới thiệu khoa",
								#	"payload": "/Gioi_Thieu_Khoa"
								#},
								{
									"type": "web_url",
									"url": "https://docs.google.com/forms/d/e/1FAIpQLSfFQxxMv62asASsAycj2k2kiV5krKnKcB_lbHeq_zDjXXrhyg/viewform?usp=sf_link",
									"title": "✉Thông tin liên hệ",
									"webview_height_ratio": "full"
								}	
								
							]
						},
						{
							"title": "Khung Chương trình đào tạo, tuyển sinh",
							"image_url": "https://fit.bdu.edu.vn/wp-content/uploads/2019/06/training-324x152.jpg",
							"subtitle": "Khung chương trình đào tạo, Lộ trình đào tạo, Đăng ký xét tuyển online...",
							"default_action": {
								"type": "web_url",
								"url": "https://fit.bdu.edu.vn/",
								"webview_height_ratio": "full",
							},
							"buttons": [
								{
									"type": "postback",
									"title": "📖️Khung CTĐT",
									"payload": "/Khung_Chuong_Trinh_Dao_Tao"
								},
								{
									"type": "postback",
									"title": "📊Lộ trình đào tạo",
									"payload": "/Lo_Trinh_Dao_Tao"
								},
								{
									"type": "postback",
									"title": "📝Đăng ký xét tuyển online",
									"payload": "/Dang_Ky_Xet_tuyen_Online"
								}
								
							]
						},
						{
							"title": "Thông tin sự kiện, tin tức",
							"image_url": "https://www.upsieutoc.com/images/2020/04/25/unnamed-2.jpg",
							"subtitle": "Giới thiệu trường, sự kiện khoa, tin tức trường...",
							"default_action": {
								"type": "web_url",
								"url": "https://fit.bdu.edu.vn/",
								"webview_height_ratio": "full",
							},
							"buttons": [
								{
									"type": "postback",
									"title": "🏢️Giới thiệu trường",
									"payload": "/Gioi_Thieu_Truong"
								},
								{
									"type": "postback",
									"title": "📰️Tin tức trường",
									"payload": "/Tin_Tuc"
								},
								#{
								#	"type": "postback",
								#	"title": "📝️Sự kiện khoa",
								#	"payload": "/Su_Kien"
								#},
								{
									"type": "postback",
									"title": "📝️Thông tin tuyển sinh",
									"payload": "/Thong_Tin_Tuyen_Sinh"
								}

								#{
								#	"type": "postback",
								#	"title": "🧐️Công bố khoa học",
								#	"payload": "/Cong_Bo_Khoa_Hoc"
								#},
								
							]
						},
						{
							"title": "Thông tin hợp tác",
							"image_url": "https://www.bdu.edu.vn/wp-content/uploads/2019/12/Cisco-16.jpg",
							"subtitle": "Hợp tác trong nước-quốc tế, Lãnh đạo khoa",
							"default_action": {
								"type": "web_url",
								"url": "https://fit.bdu.edu.vn/",
								"webview_height_ratio": "full",
							},
							"buttons": [
								{
									"type": "postback",
									"title": "📝️Sự kiện khoa",
									"payload": "/Su_Kien"
								},
								{
									"type": "postback",
									"title": "🇻Công bố khoa học",
									"payload": "/Cong_Bo_Khoa_Hoc"
								},
								#{
								#	"type": "postback",
								#	"title": "🌍️Hợp tác quốc tế",
								#	"payload": "/Hop_Tac_Quoc_Te"
								#},
								{
									"type": "postback",
									"title": "👨‍👩‍👦‍👦️Hội nghị-hội thảo",
									"payload": "/HoiThao_HoiNgi"
								}
								
							]
						}
					]
				}
			}
		}

		dispatcher.utter_message(json_message=gt)
		return []


class Action_XinChao(Action):
	def name(self) -> Text:
		return "Action_XinChao"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		Xinchao = "Xin chào!!Tôi là trợ lý ảo được vận hành bởi SV Đại học Bình Dương - Khoa Công nghệ thông tin(https://fit.bdu.edu.vn/).Tôi ở đây để cung cấp cho bạn tất cả những thông tin về Khoa Công Nghệ Thông Tin Đại Học Bình Dương. Bạn có thể hỏi tôi về:\n- Chương trình đào tạo Khoa CNTT\n- Giới thiệu Khoa CNTT\n- Tin tức Khoa CNTT\n- Sự kiện Khoa CNTT\n- Khung Chương trình đào tạo\n- Thông tin tuyển sinh..."
		dispatcher.utter_message(text=Xinchao)
		return []


class Action_GioiThieuTruong(Action):
	def name(self) -> Text:
		return "Action_GioiThieuTruong"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		Gioithieu = "Giới thiệu trường đại học bình dương"
		gt = {
			"attachment": {
				"type": "template",
				"payload": {
					"template_type": "generic",
					"elements": [
						{
							"title": "Thông tin trường đại học bình dương",
							"image_url": "https://www.upsieutoc.com/images/2020/04/25/unnamed-1.jpg",
							"subtitle": "Sứ mệnh, tầm nhìn, mục tiêu, giá trị cốt lổi, tôn chỉ mục tiêu...",
							"default_action": {
								"type": "web_url",
								"url": "https://fit.bdu.edu.vn/",
								"webview_height_ratio": "full",
							},
							"buttons": [
								{
									"type": "postback",
									"title": "📝️Sứ mệnh, tầm nhìn, mục tiêu, giá trị cốt lõi",
									"payload": "/SM_TN_MT_GTCL_Truong"
								},
								{
									"type": "postback",
									"title": "📅️Tôn chỉ mục tiêu",
									"payload": "/Ton_Chi_Muc_Tieu"
								}
							]
						},
						{
							"title": "Thông tin trường đại học bình dương",
							"image_url": "https://www.upsieutoc.com/images/2020/04/25/6f22cab82a7d038c5c5441853f42f0ee.png",
							"subtitle": "Hình thức - cấp bậc đào tạo, Hợp tác quốc tế - cơ hội học bỗng...",
							"default_action": {
								"type": "web_url",
								"url": "https://fit.bdu.edu.vn/",
								"webview_height_ratio": "full",
							},
							"buttons": [
								{
									"type": "postback",
									"title": "📝️Hình thức-cấp bậc đào tạo",
									"payload": "/Hinh_Thuc_Dao_tao"
								},
								{
									"type": "postback",
									"title": "🌏️Hợp tác quốc tế-cơ hội học bỗng",
									"payload": "/Co_Hoi_Hoc_Bong"
								}
							]
						}
					]
				}
			}
		}

		dispatcher.utter_message(text=Gioithieu,json_message=gt)
		return []


class Action_GioiThieuKhoa(Action):
	def name(self) -> Text:
		return "Action_GioiThieuKhoa"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		Gioithieu = "Giới thiệu khoa Công nghệ thông tin đại học bình dương"
		gt = {
			"attachment": {
				"type": "template",
				"payload": {
					"template_type": "generic",
					"elements": [
						{
							"title": "Giới thiệu khoa",
							"image_url": "https://www.upsieutoc.com/images/2020/05/09/gioithieukhoa.png",
							"subtitle": "Thông tin khoa công nghệ thông tin...",
							"default_action": {
								"type": "web_url",
								"url": "https://www.yumpu.com/xx/document/read/63202182/brochure-fira-binh-duong-university",
								"webview_height_ratio": "full",
							},
							"buttons": [
								{
									"type": "web_url",
									"url": "https://www.yumpu.com/xx/document/read/63202182/brochure-fira-binh-duong-university",
									"title": "🔍Xem ngay"
									
								}
							]
						}
					]
				}
			}
		}

		dispatcher.utter_message(text=Gioithieu,json_message=gt)
		return []

class Action_TinTuc(Action):
	def name(self) -> Text:
		return "Action_TinTuc"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		source = requests.get('https://www.bdu.edu.vn/tin-tuc/tin-tuc-su-kien', verify = False).text
		soup = BeautifulSoup(source, 'html.parser')
		try:
			main_row = soup.find_all("div", class_="td-block-span6")
			template_items = []
			for i in range(0,5):
				numberimg = main_row[i].find("img")["data-img-url"]
				numbertitle = main_row[i].find("a")["title"]
				number1href = main_row[i].find("a")["href"]
				template_item = {
					"title": f"{numbertitle}",
					"image_url": f"{numberimg}",
					"default_action": {
						"type": "web_url",
						"url": "https://fit.bdu.edu.vn/",
						"webview_height_ratio": "full",
					},
					"buttons": [
						{
							"type": "web_url",
							"url": f"{number1href}",
							"title": "🔍️Xem tin ngay"
						}
					]
				}
				template_items.append(template_item)

			message_str = {
				"attachment": {
					"type": "template",
					"payload": {
						"template_type": "generic",
						"elements": template_items
					}
				}
			}
		except:
			message_str = "Hệ thống đang cập nhật"

		dispatcher.utter_message(json_message=message_str)
		return []


class Action_SuKien(Action):
	def name(self) -> Text:
		return "Action_SuKien"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		source = requests.get('https://fit.bdu.edu.vn/thong-tin/su-kien', verify = False).text
		soup = BeautifulSoup(source, 'html.parser')
		try:
			main_row = soup.find_all("div", class_="td-block-span6")
			template_items = []
			for i in range(0,5):
				numberimg = main_row[i].find("img")["data-img-url"]
				numbertitle = main_row[i].find("a")["title"]
				numbersubtitle = main_row[i].find("span", class_="td-post-date").text
				number1href = main_row[i].find("a")["href"]
				template_item = {
					"title": f"{numbertitle}",
					"image_url": f"{numberimg}",
					"subtitle": f"{numbersubtitle}",
					"default_action": {
						"type": "web_url",
						"url": "https://fit.bdu.edu.vn/",
						"webview_height_ratio": "full",
					},
					"buttons": [
						{
							"type": "web_url",
							"url": f"{number1href}",
							"title": "🔍️Xem tin ngay"
						}
					]
				}
				template_items.append(template_item)

			message_str = {
				"attachment": {
					"type": "template",
					"payload": {
						"template_type": "generic",
						"elements": template_items
					}
				}
			}
		except:
			message_str = "Hệ thống đang cập nhật"

		dispatcher.utter_message(json_message=message_str)
		return []


class Action_CongBoKhoaHoc(Action):
	def name(self) -> Text:
		return "Action_CongBoKhoaHoc"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		gt = {
			"attachment": {
				"type": "template",
				"payload": {
					"template_type": "generic",
					"elements": [
						{
							"title": "Công bố khoa học",
							"image_url": "https://www.upsieutoc.com/images/2020/05/11/cbkh.jpg",
							"subtitle": "Công bố khoa học...",
							"default_action": {
								"type": "web_url",
								"url": "https://fit.bdu.edu.vn/nghien-cuu-khoa-hoc/cong-bao-khoa-hoc.html",
								"webview_height_ratio":"full"
							},
							"buttons": [
								{
									"type": "web_url",
									"url":"https://fit.bdu.edu.vn/nghien-cuu-khoa-hoc/cong-bao-khoa-hoc.html",
									"title": "🔍️Xem ngay",
									"webview_height_ratio":"full"
								}
							]
						}
					]
				}
			}
		}

		dispatcher.utter_message(json_message=gt)
		return []


class Action_HopTacTrongNuoc(Action):
	def name(self) -> Text:
		return "Action_HopTacTrongNuoc"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		source = requests.get('https://fit.bdu.edu.vn/hop-tac/trong-nuoc', verify = False).text
		soup = BeautifulSoup(source, 'html.parser')
		try:
			main_row = soup.find_all("div", class_="td-block-span6")
			SoPhanTuTrongMang = len(main_row)
			template_items = []
			for i in range(0,SoPhanTuTrongMang):
				title = main_row[i].find("a")["title"]
				href = main_row[i].find("a")["href"]
				ngaydang = main_row[i].find("span", class_="td-post-date").text
				img = main_row[i].find("img")["data-img-url"]
				template_item = {
					"title": f"{title}",
					"image_url": f"{img}",
					"subtitle": f"{ngaydang}",
					"default_action": {
						"type": "web_url",
						"url": "https://fit.bdu.edu.vn/",
						"webview_height_ratio": "full",
					},
					"buttons": [
						{
							"type": "web_url",
							"url": f"{href}",
							"title": "🔍️Xem tin ngay"
						}
					]
				}
				template_items.append(template_item)

			message_str = {
				"attachment": {
					"type": "template",
					"payload": {
						"template_type": "generic",
						"elements": template_items
					}
				}
			}
		except:
			message_str = "Hệ thống đang cập nhật"

		dispatcher.utter_message(json_message=message_str)
		return []


class Action_HoiThaoHoiNghi(Action):
	def name(self) -> Text:
		return "Action_HoiThaoHoiNghi"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		source = requests.get('https://fit.bdu.edu.vn/nghien-cuu-khoa-hoc/hoi-thao-hoi-nghi', verify = False).text
		soup = BeautifulSoup(source, 'html.parser')
		try:
			main_row = soup.find_all("div", class_="td_module_10 td_module_wrap td-animation-stack")
			SoPhanTuTrongMang = len(main_row)
			main_rowtitle = soup.find_all("h3", class_="entry-title td-module-title")
			template_items = []
			for i in range(0,SoPhanTuTrongMang):
				img = main_row[i].find("img")["data-img-url"]
				subtitle = main_row[i].find("div", class_="td-excerpt").text
				href = main_rowtitle[i].find("a")["href"]
				title = main_rowtitle[i].find("a").text
				template_item = {
					"title": f"{title}",
					"image_url": f"{img}",
					"subtitle": f"{subtitle}",
					"default_action": {
						"type": "web_url",
						"url": "https://fit.bdu.edu.vn/",
						"webview_height_ratio": "full",
					},
					"buttons": [
						{
							"type": "web_url",
							"url": f"{href}",
							"title": "🔍️Xem tin ngay"
						}
					]
				}
				template_items.append(template_item)

			message_str = {
				"attachment": {
					"type": "template",
					"payload": {
						"template_type": "generic",
						"elements": template_items
					}
				}
			}
		except:
			message_str = "Hệ thống đang cập nhật"

		dispatcher.utter_message(json_message=message_str)
		return []

#------------------------------------------------------json-------------------------------------------
#START-------------------------------------------Thông tin trường-------------------------------------
class Action_SM_TN_MT_GTCL(Action):
	def name(self) -> Text:
		return "Action_SM_TN_MT_GTCL"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		try:
			image_instagram = "http://firactdt2019.tk/jsonThongTinTruong.php"
			req_image = requests.get(image_instagram)
			convert_1 = req_image.text
			load_image = json.loads(convert_1)
			main_link = load_image['ThongTinTruong'][0]['noiDungTruong'] + "\n"
			main_link += load_image['ThongTinTruong'][1]['noiDungTruong'] + "\n"
			main_link += load_image['ThongTinTruong'][2]['noiDungTruong'] + "\n"
			main_link += load_image['ThongTinTruong'][3]['noiDungTruong']
		except:
			main_link = "Hệ thống đang cập nhật"
		dispatcher.utter_message(text=main_link)
		return []


class Action_TonChiMucTieu(Action):
	def name(self) -> Text:
		return "Action_TonChiMucTieu"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		try:
			image_instagram = "http://firactdt2019.tk/jsonThongTinTruong.php"
			req_image = requests.get(image_instagram)
			convert_1 = req_image.text
			load_image = json.loads(convert_1)
			main_link = load_image['ThongTinTruong'][4]['noiDungTruong']
		except:
			main_link = "Hệ thống đang cập nhật"
		dispatcher.utter_message(text=main_link)
		return []


class Action_HinhThucDaoTao(Action):
	def name(self) -> Text:
		return "Action_HinhThucDaoTao"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		try:
			image_instagram = "http://firactdt2019.tk/jsonThongTinTruong.php"
			req_image = requests.get(image_instagram)
			convert_1 = req_image.text
			load_image = json.loads(convert_1)
			main_link = load_image['ThongTinTruong'][5]['noiDungTruong']
		except:
			main_link = "Hệ thống đang cập nhật"
		dispatcher.utter_message(text=main_link)
		return []


class Action_CoHoiHocBong(Action):
	def name(self) -> Text:
		return "Action_CoHoiHocBong"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		try:
			image_instagram = "http://firactdt2019.tk/jsonThongTinTruong.php"
			req_image = requests.get(image_instagram)
			convert_1 = req_image.text
			load_image = json.loads(convert_1)
			main_link = load_image['ThongTinTruong'][6]['noiDungTruong']
		except:
			main_link = "Hệ thống đang cập nhật"
		dispatcher.utter_message(text=main_link)
		return []

#END------------------------------------------------Thông tin trường----------------------------------------


##----------------------------------------------------json-----------------------------------------------------------
##----------------------------------------------------update---------------------------------------------------------


class Action_KhungChuongTrinhDaoTao(Action):
	def name(self) -> Text:
		return "Action_KhungChuongTrinhDaoTao"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		Gioithieu = "Khung chương trình đào tạo:"
		gt = {
			"attachment": {
				"type": "template",
				"payload": {
					"template_type": "generic",
					"elements": [
						{
							"title": "Khung chương trình đào tạo",
							"image_url": "https://www.upsieutoc.com/images/2020/05/10/khungchuongtrinhdaotao.jpg",
							"subtitle": "Khung chương trình đào tạo",
							"default_action": {
								"type": "web_url",
								"url": "https://fira2029.000webhostapp.com/KhungChuongTrinhDaoTao.html",
								"messenger_extensions": "true",
								"webview_height_ratio":"full"
							},
							"buttons": [
								{
									"type": "web_url",
									"url":"https://fira2029.000webhostapp.com/KhungChuongTrinhDaoTao.html",
									"title": "🔍️Xem ngay",
									"messenger_extensions": "true",
									"webview_height_ratio":"full"
								}
							]
						}
					]
				}
			}
		}

		dispatcher.utter_message(text=Gioithieu,json_message=gt)
		return []


class Action_LoTrinhDaoTao(Action):
	def name(self) -> Text:
		return "Action_LoTrinhDaoTao"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		dispatcher.utter_message(image="https://www.upsieutoc.com/images/2020/04/19/2707eeac4367cbecb.jpg")
		return []


class Action_FormDangKy(Action):
	def name(self) -> Text:
		return "Action_FormDangKy"
	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
		Gioithieu = "Form thông tin liên hệ:"
		gt = {
			"attachment": {
				"type": "template",
				"payload": {
					"template_type": "generic",
					"elements": [
						{
							"title": "Form thông tin liên hệ",
							"image_url": "https://www.upsieutoc.com/images/2020/04/30/form1.png",
							"subtitle": "Form điền đầy đủ thông tin để chúng tôi liên hệ với bạn...",
							"default_action": {
								"type": "web_url",
								"url": "https://forms.gle/kzmRGevuUpAZSGVj8",
								"webview_height_ratio":"full"
							},
							"buttons": [
								{
									"type": "web_url",
									"url":"https://forms.gle/kzmRGevuUpAZSGVj8",
									"title": "🔍️Xem ngay",
									"webview_height_ratio":"full"
								}
							]
						}
					]
				}
			}
		}
		dispatcher.utter_message(text=Gioithieu,json_message=gt)
		return []
