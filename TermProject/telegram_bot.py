'''
telegram_bot.py
텔레그램 메인 모듈

functions
- getStr
- getData
- getBookMark
- findHospital
- addBookMark
- sendMessage
- replyAptData
- handle
'''

# === import ===
import sys
sys.argv.append('from_telegram_bot')
from pprint import pprint  # 데이터를 읽기 쉽게 출력
from urllib.request import urlopen
import traceback
from xml.etree import ElementTree
from urllib.parse import quote

import time
import telepot
from datetime import date, datetime

import os
import pickle
import server

def getStr(s):  # utitlity function: 문자열 내용 있을 때만 사용
    return '정보없음' if not s else s

# === noti part ===
key = 'b40a9f7c2d06486a83a9fdbfa6e3437e'
TOKEN = ''
MAX_MSG_LENGTH = 300
baseurl = 'https://openapi.gg.go.kr/Animalhosptl?pSize=1000&pIndex=1&KEY=' + key
bot = telepot.Bot(TOKEN)

def getData(loc_param):  # 인자에 따라 RESTAPI에서 데이터를 가져옴
    res_list = []
    query = quote(loc_param)
    url = baseurl + '&SIGUN_NM=' + query  # 시군이름으로 검색 가능
    res_body = urlopen(url).read()
    strXml = res_body.decode('utf-8')
    tree = ElementTree.fromstring(strXml)

    items = tree.iter("row")
    for item in items:
        if item.find('BSN_STATE_NM').text == '정상':
            info = '[동물병원명]\n' + getStr(item.find('BIZPLC_NM').text) + \
                   '\n\n[상태]\n' + getStr(item.find('BSN_STATE_NM').text) + \
                   '\n\n[전화번호]\n' + getStr(item.find('LOCPLC_FACLT_TELNO').text) + \
                   '\n\n[도로명 주소]\n' + getStr(item.find('REFINE_ROADNM_ADDR').text) + \
                   '\n\n[지번 주소]\n' + getStr(item.find('REFINE_LOTNO_ADDR').text)
            res_list.append(info)
    return res_list

def getBookMark(chat_id):  # 피클 모듈을 사용해 즐겨찾기 목록 불러와 전송하는 함수
    dirpath = os.getcwd()
    if os.path.isfile(dirpath + '\mark'):
        f = open('mark', 'rb')
        dic = pickle.load(f)
        f.close()

        for value in dic.values():
            sendMessage(chat_id, value)

def findHospital(chat_id, name):
    key = "b40a9f7c2d06486a83a9fdbfa6e3437e"
    page = 1
    text = "null"

    while True:
        url = f"https://openapi.gg.go.kr/Animalhosptl?pSize=1000&pIndex={page}&KEY={key}"
        res_body = urlopen(url).read()
        strXml = res_body.decode('utf-8')
        tree = ElementTree.fromstring(strXml)

        elements = tree.iter("row")

        count = 0
        for item in elements:  # 'row' element들
            count += 1
            if item.find('BIZPLC_NM').text == name and item.find('BSN_STATE_NM').text == '정상':
                text = '[동물병원명]\n' + getStr(item.find('BIZPLC_NM').text) + \
                       '\n\n[상태]\n' + getStr(item.find('BSN_STATE_NM').text) + \
                       '\n\n[전화번호]\n' + getStr(item.find('LOCPLC_FACLT_TELNO').text) + \
                       '\n\n[도로명 주소]\n' + getStr(item.find('REFINE_ROADNM_ADDR').text) + \
                       '\n\n[지번 주소]\n' + getStr(item.find('REFINE_LOTNO_ADDR').text)
                server.hospital_name = getStr(item.find('BIZPLC_NM').text)
                print(f"Found hospital: {text}")
                break

        if text != "null" or count < 1000:
            break

        page += 1

    if text == "null":  # 예외 처리: API에 없는 동물병원을 입력했을 시
        sendMessage(chat_id, '해당 동물병원은 존재하지 않습니다')
        print("Hospital not found")
    else:
        sendMessage(chat_id, text)

def addBookMark(chat_id, name):
    key = "b40a9f7c2d06486a83a9fdbfa6e3437e"
    page = 1
    text = "null"

    while True:
        url = f"https://openapi.gg.go.kr/Animalhosptl?pSize=1000&pIndex={page}&KEY={key}"
        res_body = urlopen(url).read()
        strXml = res_body.decode('utf-8')
        tree = ElementTree.fromstring(strXml)

        elements = tree.iter("row")

        count = 0
        for item in elements:  # 'row' element들
            count += 1
            if item.find('BIZPLC_NM').text == name and item.find('BSN_STATE_NM').text == '정상':
                text = '[동물병원명]\n' + getStr(item.find('BIZPLC_NM').text) + \
                       '\n\n[상태]\n' + getStr(item.find('BSN_STATE_NM').text) + \
                       '\n\n[전화번호]\n' + getStr(item.find('LOCPLC_FACLT_TELNO').text) + \
                       '\n\n[도로명 주소]\n' + getStr(item.find('REFINE_ROADNM_ADDR').text) + \
                       '\n\n[지번 주소]\n' + getStr(item.find('REFINE_LOTNO_ADDR').text)
                server.hospital_name = getStr(item.find('BIZPLC_NM').text)
                print(f"Found hospital to bookmark: {text}")
                break

        if text != "null" or count < 1000:
            break

        page += 1

    if text == "null":  # 예외 처리: API에 없는 동물병원을 입력했을 시
        sendMessage(chat_id, '해당 동물병원은 존재하지 않습니다')
        print("Hospital not found for bookmark")
        return

    dirpath = os.getcwd()
    if os.path.isfile(dirpath + '\mark'):
        with open('mark', 'rb') as f:
            server.MarkDict = pickle.load(f)

        server.MarkDict[server.hospital_name] = text

        with open('mark', 'wb') as f:
            pickle.dump(server.MarkDict, f)

        with open('mark', 'rb') as f:
            server.MarkDict = pickle.load(f)

        print(f"Updated bookmark dictionary: {server.MarkDict}")
    else:
        server.MarkDict[server.hospital_name] = text
        with open('mark', 'wb') as f:
            pickle.dump(server.MarkDict, f)

        print(f"Created new bookmark dictionary: {server.MarkDict}")

    sendMessage(chat_id, '해당 동물병원을 즐겨찾기에 성공적으로 추가했습니다')

def sendMessage(user, msg):  # 메시지 전송 함수
    try:
        bot.sendMessage(user, msg)
    except:
        # 예외 정보와 스택 트레이스 항목을 인쇄.
        traceback.print_exception(*sys.exc_info(), file=sys.stdout)

# === teller part ===
# user: 사용자ID, loc_param:지역이름
def replyAptData(user, loc_param='연천군'):  # 입력한 시군에 해당하는 동물병원을 전송하는 함수
    print(user, loc_param)
    res_list = getData(loc_param)

    # 하나씩 보내면 메시지 개수가 너무 많아지므로
    # 300자까지는 하나의 메시지로 묶어서 보내기.
    msg = ''
    for r in res_list:
        print(str(datetime.now()).split('.')[0], r)
        if len(r + msg) + 1 > MAX_MSG_LENGTH:
            sendMessage(user, msg)
            msg = r + '\n'
        else:
            msg += r + '\n'
        print(msg)
    if msg:
        sendMessage(user, msg)
    else:
        sendMessage(user, '해당하는 데이터가 없습니다.')

def handle(msg):  # 대화에 반응하는 함수
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return
    text = msg['text']
    args = text.split(' ')

    region_list = ['가평군', '고양시', '과천시', '광명시', '광주시', '구리시', '군포시', '김포시', '남양주시',
                   '동두천시', '부천시', '성남시', '수원시', '시흥시', '안산시', '안성시', '안양시', '양주시',
                   '양평군', '여주시', '연천군', '오산시', '용인시', '의왕시', '의정부시', '이천시', '파주시',
                   '평택시', '포천시', '하남시', '화성시']

    if text in region_list:
        print('try to 시군', text)
        replyAptData(chat_id, text)
    elif any(text.startswith(keyword) for keyword in ['검색', '즐겨찾기', 'help']):
        if text.startswith('검색'):
            if len(args) > 1:
                print('try to 검색', args[1])
                findHospital(chat_id, args[1])
            else:
                sendMessage(chat_id, '검색할 동물병원명을 입력해주세요.')
        elif text.startswith('즐겨찾기'):
            if len(args) > 1:
                print('try to 즐겨찾기', args[1])
                addBookMark(chat_id, args[1])
            else:
                print('try to 즐겨찾기')
                getBookMark(chat_id)
        elif text.startswith('help'):
            guide = ("1. 'help'를 입력해 명령어를 찾아볼 수 있습니다. \n\n"
                     "2. 동물병원명을 입력하면 해당 동물병원 정보를 출력합니다.\n예) 배곧동물병원\n\n"
                     "3. 지역명을 입력하면 해당 지역 내에 있는 동물병원을 모두 출력합니다.\n예) 시흥시\n"
                     "지원하는 지역명: '가평군', '고양시', '과천시', '광명시', '광주시', '구리시', '군포시', '김포시', '남양주시', "
                     "'동두천시', '부천시', '성남시', '수원시', '시흥시', '안산시', '안성시', '안양시', '양주시', '양평군', '여주시', "
                     "'연천군', '오산시', '용인시', '의왕시', '의정부시', '이천시', '파주시', '평택시', '포천시', '하남시', '화성시'\n\n"
                     "4. '즐겨찾기'를 입력해 내 즐겨찾기에 저장된 동물병원 정보를 볼 수 있습니다.\n\n"
                     "5. 즐겨찾기 + '동물병원명'으로 입력하면 즐겨찾기에 동물병원을 저장할 수 있습니다. \n예) 즐겨찾기 배곧동물병원")
            sendMessage(chat_id, guide)
    else:
        if text:
            print('try to 검색', text)
            findHospital(chat_id, text)
        else:
            guide = ("1. 'help'를 입력해 명령어를 찾아볼 수 있습니다. \n\n"
                     "2. 동물병원명을 입력하면 해당 동물병원 정보를 출력합니다.\n예) 배곧동물병원\n\n"
                     "3. 지역명을 입력하면 해당 지역 내에 있는 동물병원을 모두 출력합니다.\n예) 시흥시\n"
                     "지원하는 지역명: '가평군', '고양시', '과천시', '광명시', '광주시', '구리시', '군포시', '김포시', '남양주시', "
                     "'동두천시', '부천시', '성남시', '수원시', '시흥시', '안산시', '안성시', '안양시', '양주시', '양평군', '여주시', "
                     "'연천군', '오산시', '용인시', '의왕시', '의정부시', '이천시', '파주시', '평택시', '포천시', '하남시', '화성시'\n\n"
                     "4. '즐겨찾기'를 입력해 내 즐겨찾기에 저장된 동물병원 정보를 볼 수 있습니다.\n\n"
                     "5. 즐겨찾기 + '동물병원명'으로 입력하면 즐겨찾기에 동물병원을 저장할 수 있습니다. \n예) 즐겨찾기 배곧동물병원")
            sendMessage(chat_id, guide)

today = date.today()
current_month = today.strftime('%Y%m')

print('[', today, ']received token :', TOKEN)

pprint(bot.getMe())

bot.message_loop(handle)

print('Listening...')
while 1:
    time.sleep(10)
