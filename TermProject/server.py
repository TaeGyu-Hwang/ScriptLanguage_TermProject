'''
server.py
모듈 간 데이터의 공유를 돕는 모듈입니다.
함수가 아닌 객체들로만 구성되어있습니다.
각 모듈에서 단순히 server를 import하면 필요한 정보를 제공받을 수 있습니다.

functions
- center_window
'''

# === import ===
import sys
from tkinter import *
from tkinter import font

# === main window ===
if not any(arg in sys.argv for arg in ('--no-gui', '-ng')) and 'telegram_bot' not in sys.argv[0]:
    window = Tk()
    window.title("가까운 동물병원")
    window.geometry("800x600+450+200")
    window.resizable(False, False)
    window.configure(bg='white')
else:
    window = None

# === center window ===
def center_window(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2) - 50  # 화면 상단으로 50픽셀 더 이동
    win.geometry(f'{width}x{height}+{x}+{y}')

# === load image ===
if window:
    searchImage = PhotoImage(file='image/search.png')               # search image
    filterImage = PhotoImage(file='image/filter_icon.png')          # filter image
    emailImage = PhotoImage(file='image/mail_icon3.png')            # mail image
    mapImage = PhotoImage(file='image/map_icon2.png')               # map image
    emptymarkImage = PhotoImage(file='image/white_bookmark.png')    # mark image
    markImage = PhotoImage(file='image/bookmark.png')               # mark image
    telegramImage = PhotoImage(file='image/telegram_icon.png')      # telegram image
    logoImage = PhotoImage(file='image/petlogo.png')                # logo image
    graphImage = PhotoImage(file='image/trend.png')                 # graph image
    noImage = PhotoImage(file='image/close.png')                    # no image
    labelImage = PhotoImage(file='image/label.png')                 # label image
    googleLinkImage = PhotoImage(file='image/google.png')           # label image
    naverImage = PhotoImage(file='image/naver.png')                 # label image
    naverMapImage = PhotoImage(file='image/google_map.png')         # label image
else:
    searchImage = None
    filterImage = None
    emailImage = None
    mapImage = None
    emptymarkImage = None
    markImage = None
    telegramImage = None
    logoImage = None
    graphImage = None
    noImage = None
    labelImage = None
    googleLinkImage = None
    naverImage = None
    naverMapImage = None

# === load font ===
if window:
    fontNormal = font.Font(window, size=14, family='G마켓 산스 TTF Medium')
    fontLabel = font.Font(window, size=20, family='G마켓 산스 TTF Bold')
    fontGaggunPet = font.Font(window, size=24, family='G마켓 산스 TTF Medium')
    fontInfo = font.Font(window, size=10, family='G마켓 산스 TTF Medium')
    fontList = font.Font(window, size=14, family='G마켓 산스 TTF Medium')
else:
    fontNormal = None
    fontLabel = None
    fontGaggunPet = None
    fontInfo = None
    fontList = None

# === shared datas ===
info_text = None        # 동물병원 정보
hospital_name = None    # 동물병원 이름
memo_text = None        # 메모
MarkDict = dict()       # 즐겨찾기 dict {동물병원명:동물병원정보}

latitude = 0.0      # 위도
longitude = 0.0     # 경도

city_list = ['선택안함', '가평군', '고양시', '과천시', '광명시', '광주시', '구리시', '군포시',
    '김포시', '남양주시', '동두천시', '부천시', '성남시', '수원시', '시흥시', '안산시', '안성시',
    '안양시', '양주시', '양평군', '여주시', '연천군', '오산시', '용인시', '의왕시', '의정부시',
    '이천시', '파주시', '평택시', '포천시', '하남시', '화성시']

hList = [0 for i in city_list]

# 마우스 좌표 정보 (graph.py에서 사용)
mouse_x = 0
mouse_y = 0

if __name__ == '__main__':
    print("server.py runned\n")
    if window:
        window.mainloop()
else:
    print("server.py imported\n")
