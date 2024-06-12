'''
map.py
런처에서 지도 버튼을 누르면 실행되는 모듈입니다.

functions
- onMapPopup
- get_coordinates
- onSearch
- onHospital
- add_marker_event
'''

# === import ===
from tkinter import *
import server
import tkintermapview
from tkinter import font
import tkinter.messagebox as msgbox
import requests
from tkinter import messagebox

# === load image ===
hospitalImage = PhotoImage(file='image/hospital.png')               # 병원 아이콘
searchImage = PhotoImage(file='image/little_search.png')            # 돋보기 아이콘

# === functions ===
def onMapPopup():
    # 런처에서 지도 버튼을 누를 경우 실행
    # 선택한 병원의 지도를 보여주는 팝업을 띄움
    if server.hospital_name == None:     # 예외처리: 사용자가 병원을 선택하지 않고, 버튼을 누를 경우
        msgbox.showinfo("알림", "목록에서 병원을 먼저 선택해주십시오.")
        return

    global popup
    popup = Toplevel()
    popup.geometry("800x600+100+100")
    popup.title("<" + server.hospital_name + "> 의 지도")

    fontNormal = font.Font(popup, size=18, family='G마켓 산스 TTF Medium')

    if server.latitude == 0 and server.longitude == 0:      # API에서 병원의 주소 정보를 제공하지 않는 경우
        emptyLabel = Label(popup, width=800, height=600, text="해당 병원의 지도 정보가 없습니다.", font=fontNormal)
        emptyLabel.pack()

    else:
        global map_widget, marker_1
        map_widget = tkintermapview.TkinterMapView(popup, width=800, height=550, corner_radius=0)
        map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        map_widget.place(x=0, y=0, width=800, height=550)
        map_widget.add_right_click_menu_command(label="위치 추가", command=add_marker_event, pass_coords=True)

        # 주소 위치지정
        marker_1 = map_widget.set_position(server.latitude, server.longitude, marker=True, marker_color_outside="black", marker_color_circle="white", text_color="black") # 위도,경도 위치지정
        marker_1.set_text(server.hospital_name) # set new text

        global addressLabel, InputButton, HospitalButton
        # 주소 입력 부분
        addressLabel = Entry(popup, font=fontNormal, width=800, borderwidth=3, relief='ridge')
        addressLabel.place(x=0, y=550, width=700, height=50)

        InputButton = Button(popup, font=fontNormal, image=searchImage, command=onSearch, bg="white", cursor="hand2")
        InputButton.place(x=700, y=550, width=50, height=50)

        # 병원 버튼
        HospitalButton = Button(popup, font=fontNormal, image=hospitalImage, command=onHospital, bg="white", cursor="hand2")
        HospitalButton.place(x=750, y=550, width=50, height=50)

        map_widget.set_zoom(15) # 0~19 (19 is the highest zoom level)

def get_coordinates(address):
    try:
        url = f"https://nominatim.openstreetmap.org/search"
        params = {
            'q': address,
            'format': 'json',
            'addressdetails': 1,
            'limit': 1
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()

        results = response.json()
        if results:
            return float(results[0]['lat']), float(results[0]['lon'])
        else:
            return None, None
    except requests.RequestException as e:
        print(f"Error fetching coordinates: {e}")
        return None, None


def onSearch():
    # 지도 팝업에서 주소 입력 시 실행
    # 새 주소에 마커 추가
    global destAddr, marker_2
    destAddr = addressLabel.get()
    lat, lon = get_coordinates(destAddr)

    if lat is not None and lon is not None:
        marker_2 = map_widget.set_marker(lat, lon, marker_color_outside="black", marker_color_circle="white",
                                         text_color="black")
        marker_2.set_text(destAddr)

        path_1 = map_widget.set_path([marker_1.position, marker_2.position])
        map_widget.set_position(server.latitude, server.longitude)
        map_widget.set_zoom(15)
    else:
        messagebox.showinfo("알림", "해당 주소를 찾을 수 없습니다.")

    addressLabel.delete(0, 'end')


def onHospital():   # 원래 병원 위치로 이동하는 함수
    map_widget.set_zoom(15)
    map_widget.set_position(marker_1.position[0], marker_1.position[1])

def add_marker_event(coords):       # 마우스 우클릭으로 마커를 추가하는 함수
    print("위치 추가:", coords)
    new_marker = map_widget.set_marker(coords[0], coords[1], text="현재 위치")
    map_widget.set_path([coords, marker_1.position])
    
if __name__ == '__main__':
    print("map.py runned\n")
else:
    print("map.py imported\n")
