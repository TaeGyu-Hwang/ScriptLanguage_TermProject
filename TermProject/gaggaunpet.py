'''
gaggaunpet.py
프로그램의 메인모듈

functions
- InitScreen
- setCity
- resetFilter
- onSearch
- getStr
- saveMemo
- event_for_listbox
- SearchHospital
'''

from turtle import bgcolor
from urllib.request import urlopen
from server import window
from tkinter import *
from tkinter import font
import tkinter.scrolledtext as st
from tkinter.ttk import Notebook, Style
from xml.etree import ElementTree

from gmail_send import *
import server
from graph import *
from map import *
from telegram import *
from link import *
from book_mark import *


# === functions ===
def InitScreen():  # 메인 GUI 창을 시작하는 함수
    # === frame arrangement ===

    # GaggunPet 텍스트 + 로고 이미지
    title_frame = Frame(window, bg="white", relief="solid", bd=2)
    title_frame.place(x=395, y=10, width=318, height=72)  # GaggunPet 텍스트를 감싸는 박스

    title = Label(title_frame, text="GaggunPet", font=server.fontGaggunPet, bg="white", anchor="center")
    title.place(relx=0.5, rely=0.5, anchor="center", width=240, height=60)  # 텍스트를 박스 안에 위치

    logo_button = Button(window, image=server.logoImage, bg="white", command=onLogo, cursor="hand2", relief="solid",
                         bd=3, highlightthickness=2, highlightbackground="black", highlightcolor="black",
                         overrelief="ridge")
    logo_button.place(x=723, y=10, width=72, height=72)  # 로고를 박스 옆에 배치

    # 버튼 부분
    button_start_x = 395  # 시작 위치를 더 왼쪽으로 조정
    button_start_y = 90
    button_spacing = 82

    global MarkButton, MapButton, MailButton, GraphButton, TelegramButton
    MarkButton = Button(window, image=server.emptymarkImage, bg="white", command=onMarkPopup, activebackground="dark grey", cursor="hand2",
                        relief="raised", bd=2, overrelief="ridge")
    MarkButton.place(x=button_start_x, y=button_start_y, width=72, height=72)

    MapButton = Button(window, image=server.mapImage, bg="white", command=onMapPopup, activebackground="dark grey",
                       cursor="hand2", relief="raised", bd=2, overrelief="ridge")
    MapButton.place(x=button_start_x + button_spacing, y=button_start_y, width=72, height=72)

    MailButton = Button(window, image=server.emailImage, bg="white", command=onEmailPopup, activebackground="dark grey",
                        cursor="hand2", relief="raised", bd=2, overrelief="ridge")
    MailButton.place(x=button_start_x + 2 * button_spacing, y=button_start_y, width=72, height=72)

    GraphButton = Button(window, bg="white", image=server.graphImage, command=onGraphPopup,
                         activebackground="dark grey", cursor="hand2", relief="raised", bd=2, overrelief="ridge")
    GraphButton.place(x=button_start_x + 3 * button_spacing, y=button_start_y, width=72, height=72)

    TelegramButton = Button(window, image=server.telegramImage, bg="white", activebackground="dark grey",
                            cursor="hand2", relief="raised", bd=2, overrelief="ridge", command=sendSelectedInfo)
    TelegramButton.place(x=button_start_x + 4 * button_spacing, y=button_start_y, width=72, height=72)

    # 시(군) 선택 부분
    global CityLabel, CityListBox, clist
    CityLabel = Label(window, text="시/군", font=server.fontNormal, bg="white", image=server.labelImage, compound='center')
    CityLabel.place(x=10, y=10, width=100, height=70)

    CityScrollbar = Scrollbar(window)
    CityListBox = Listbox(window, activestyle='dotbox', relief='ridge', font=server.fontNormal,
                          yscrollcommand=CityScrollbar.set, cursor="hand2")
    global selectedCity
    selectedCity = [0]
    CityListBox.bind('<<ListboxSelect>>', setCity)
    clist = server.city_list

    for i, c in enumerate(clist):
        CityListBox.insert(i, c)

    CityListBox.place(x=110, y=10, width=253, height=70)

    CityScrollbar.config(command=CityListBox.yview, cursor="sb_v_double_arrow")
    CityScrollbar.place(x=362, y=10, width=20, height=70)

    # 사용자 입력부분
    global InputLabel
    InputLabel = Entry(window, font=server.fontNormal, width=36, borderwidth=3, relief='ridge', cursor="xterm")
    InputLabel.place(x=10, y=89, width=295, height=72)

    InputButton = Button(window, font=server.fontNormal, image=server.searchImage, command=onSearch, bg="white",
                         cursor="hand2", overrelief="groove", activebackground="dark grey")
    InputButton.place(x=310, y=90, width=72, height=72)

    # 병원 목록 부분
    global listBox
    ListScrollBar = Scrollbar(window)
    listBox = Listbox(window, selectmode='extended', font=server.fontList, width=10, height=15, borderwidth=5,
                      relief='ridge', yscrollcommand=ListScrollBar.set, cursor="hand2")
    listBox.bind('<<ListboxSelect>>', event_for_listbox)
    listBox.place(x=10, y=170, width=353, height=420)

    ListScrollBar.place(x=362, y=170, width=20, height=420)
    ListScrollBar.config(command=listBox.yview, cursor="sb_v_double_arrow")

    # 정보 부분 (notebook)
    global InfoLabel, ST, notebook
    style = Style()
    style.theme_use('default')
    style.configure('TNotebook.Tab', background="gray")
    style.map("TNotebook", background=[("selected", "gray")])

    notebook = Notebook(window)
    notebook.place(x=395, y=170, width=400, height=420)

    # notebook page1: 병원 정보 출력
    info_frame = Frame(window, bg="white")
    notebook.add(info_frame, text="정보")

    ST = st.ScrolledText(info_frame, font=server.fontInfo, cursor="arrow")
    ST.pack(fill=BOTH, expand=True)

    # 즐겨찾기 저장 버튼을 정보 창 안에 배치
    saveButton = Button(info_frame, text='즐겨찾기 저장', command=saveBookMark, font=server.fontInfo, cursor="hand2")
    saveButton.pack(fill=X)

    # notebook page2: 링크 모음
    frame2 = Frame(window, background='white', relief='flat', borderwidth=0)
    notebook.add(frame2, text="링크")
    link1 = Button(frame2, image=server.googleLinkImage, bg='white', relief="flat", command=onGoogleLink,
                   cursor="hand2")
    link2 = Button(frame2, image=server.naverImage, bg='white', relief="flat", command=onNaverLink, cursor="hand2")
    link3 = Button(frame2, image=server.naverMapImage, bg='white', relief="flat", command=onNaverMapLink,
                   cursor="hand2")

    link1.pack(pady=40)
    link2.pack(pady=10)
    link3.pack(pady=40)

    # # notebook page3: 메모
    # global memoST
    # frame3 = Frame(window, background='white', relief='flat', borderwidth=0)
    # memoST = st.ScrolledText(frame3, relief='raised', font=server.fontInfo)
    # memoST.place(x=0, y=0, width=398, height=366)
    # memoButton = Button(frame3, text='즐겨찾기 저장', command=saveMemo, font=server.fontInfo, cursor="hand2")
    # memoButton.place(x=0, y=366, width=398, height=30)
    # notebook.add(frame3, text="즐겨찾기")

    # bookmark data load
    dirpath = os.getcwd()
    if os.path.isfile(dirpath + '\mark'):
        f = open('mark', 'rb')
        dic = pickle.load(f)  # 파일에서 리스트 load
        f.close()
        server.MarkDict = dic


def setCity(event):  # command for city list box. 시군 필터
    global selectedCity, CityListBox, clist
    sel = event.widget.curselection()
    if sel:
        selectedCity = sel


def resetFilter():  # command for reset button. 필터 초기화
    global selectedCity, listBox
    selectedCity = [0]
    listBox.delete(0, listBox.size())


def onSearch():  # command for search button
    global CityListBox, clist
    global selectedCity

    cIdx = selectedCity[0]
    SearchHospital(clist[cIdx])


def getStr(s):  # utitlity function: 문자열 내용 있을 때만 사용
    return '정보없음' if not s else s


def saveBookMark():  # 즐겨찾기 저장 함수
    if server.hospital_name:
        makeBookMark()
    else:
        msgbox.showinfo("알림", "목록에서 동물병원을 먼저 선택해주십시오.")


def event_for_listbox(event):  # command for list box
    global InfoLabel, ST
    selection = event.widget.curselection()

    if selection:  # 리스트 박스에서 클릭 발생 시
        index = selection[0]
        data = event.widget.get(index)

        # REST API에서 해당 이름의 정보 검색 후 출력
        key = "b40a9f7c2d06486a83a9fdbfa6e3437e"
        info = "null"
        page = 1

        while True:
            url = f"https://openapi.gg.go.kr/Animalhosptl?pSize=1000&pIndex={page}&KEY={key}"
            res_body = urlopen(url).read()
            strXml = res_body.decode('utf-8')
            tree = ElementTree.fromstring(strXml)
            elements = tree.iter("row")

            count = 0
            for item in elements:
                count += 1
                if item.find('BIZPLC_NM').text == data and item.find('BSN_STATE_NM').text == '정상':
                    info = '[동물병원명]\n' + getStr(item.find('BIZPLC_NM').text) + \
                           '\n\n[상태]\n' + getStr(item.find('BSN_STATE_NM').text) + \
                           '\n\n[전화번호]\n' + getStr(item.find('LOCPLC_FACLT_TELNO').text) + \
                           '\n\n[도로명 주소]\n' + getStr(item.find('REFINE_ROADNM_ADDR').text) + \
                           '\n\n[지번 주소]\n' + getStr(item.find('REFINE_LOTNO_ADDR').text)
                    server.hospital_name = getStr(item.find('BIZPLC_NM').text)

                    # 지도를 위해 정보 가져옴
                    if item.find('REFINE_WGS84_LAT').text and item.find('REFINE_WGS84_LOGT').text:
                        server.latitude = float(item.find('REFINE_WGS84_LAT').text)
                        server.longitude = float(item.find('REFINE_WGS84_LOGT').text)
                        MapButton.configure(image=server.mapImage)
                    else:
                        server.latitude = 0.0
                        server.longitude = 0.0
                        MapButton.configure(image=server.noImage)

            if count < 1000:  # 마지막 페이지 도달
                break

            page += 1

        # 즐겨찾기 여부 표시
        if data in server.MarkDict:
            MarkButton.configure(image=server.markImage)
        else:
            MarkButton.configure(image=server.emptymarkImage)

        # 선택된 동물병원 정보 서버로 넘기기
        server.info_text = info

        # 동물병원 정보 출력
        ST.configure(state="normal")  # 수정 가능으로 풀어놨다가,
        ST.delete('1.0', END)
        ST.insert(INSERT, info)
        ST.configure(state="disabled")  # 수정 불가능(읽기 전용)으로 변경


def SearchHospital(city=''):  # 리스트 박스 구성을 위해 동물병원 목록을 만드는 함수
    global listBox
    listBox.delete(0, listBox.size())

    key = "b40a9f7c2d06486a83a9fdbfa6e3437e"
    i = 1
    page = 1

    while True:
        url = f"https://openapi.gg.go.kr/Animalhosptl?pSize=1000&pIndex={page}&KEY={key}"
        res_body = urlopen(url).read()
        strXml = res_body.decode('utf-8')
        tree = ElementTree.fromstring(strXml)
        elements = tree.iter("row")

        count = 0
        for item in elements:  # 'row' element들
            part_el = item.find('BIZPLC_NM')
            count += 1

            if InputLabel.get() not in part_el.text:
                continue

            if item.find('BSN_STATE_NM').text == '정상':
                # 시군 O
                if item.find('SIGUN_NM').text == city:
                    _text = getStr(item.find('BIZPLC_NM').text)
                    listBox.insert(i-1, _text)
                    i += 1

                # 시군 X
                elif city == "선택안함":
                    _text = getStr(item.find('BIZPLC_NM').text)
                    listBox.insert(i-1, _text)
                    i += 1

        if count < 1000:  # 마지막 페이지 도달
            break

        page += 1


if __name__ == '__main__':
    print("main laucher runned\n")
    InitScreen()
    window.mainloop()
else:
    print("main launcher imported\n")

