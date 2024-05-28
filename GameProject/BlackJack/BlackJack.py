from tkinter import *
from tkinter import font
from winsound import *
from Card import *
from Player import *
import random
class BlackJack:
    def pressedAgain(self):
        self.player.reset()
        self.dealer.reset()
        self.deckN = 0
        random.shuffle(self.cardDeck)
        self.betMoney = 0
        self.LbetMoney.configure(text="$0")
        self.LplayerPts.configure(text="")
        self.LdealerPts.configure(text="")
        self.Lstatus.configure(text="")

        for label in self.LcardsPlayer:
            label.destroy()
        self.LcardsPlayer = []

        for label in self.LcardsDealer:
            label.destroy()
        self.LcardsDealer = []

        self.B50['state'] = 'normal'
        self.B50['bg'] = 'white'
        self.B10['state'] = 'normal'
        self.B10['bg'] = 'white'
        self.B1['state'] = 'normal'
        self.B1['bg'] = 'white'
        self.Deal['state'] = 'active'
        self.Deal['bg'] = 'white'
        self.Hit['state'] = 'disabled'
        self.Hit['bg'] = 'gray'
        self.Stay['state'] = 'disabled'
        self.Stay['bg'] = 'gray'
        self.Again['state'] = 'disabled'
        self.Again['bg'] = 'gray'

        # 재생할 소리 파일 추가
        PlaySound('sounds/ding.wav', SND_FILENAME | SND_ASYNC)

    def pressedStay(self):
        # 첫 번째 카드를 뒤집습니다.
        first_card_image = PhotoImage(file="cards/" + self.dealer.cards[0].filename())
        self.LcardsDealer[0].configure(image=first_card_image)
        self.LcardsDealer[0].image = first_card_image

        # 모든 카드가 공개된 후에 딜러의 점수를 업데이트합니다.
        self.LdealerPts.configure(text=str(self.dealer.value()))

        # 딜러의 추가 카드를 뽑습니다.
        while self.dealer.value() < 17:
            self.hitDealer(True)

        self.checkWinner()  # 승자 확인

    def pressedB10(self):
        if self.playerMoney >= 10:
            self.betMoney += 10
            self.playerMoney -= 10
            self.LbetMoney.configure(text="$" + str(self.betMoney))
            self.LplayerMoney.configure(text="You have $" + str(self.playerMoney))
            self.Deal["state"] = "active"
            self.Deal["bg"] = "white"
            PlaySound('sounds/chip.wav', SND_FILENAME)
        else:
            self.Lstatus.configure(text="Not enough money!")

    def pressedB1(self):
        if self.playerMoney >= 1:
            self.betMoney += 1
            self.playerMoney -= 1
            self.LbetMoney.configure(text="$" + str(self.betMoney))
            self.LplayerMoney.configure(text="You have $" + str(self.playerMoney))
            self.Deal["state"] = "active"
            self.Deal["bg"] = "white"
            PlaySound('sounds/chip.wav', SND_FILENAME)
        else:
            self.Lstatus.configure(text="Not enough money!")

    def hitDealer(self, face_up=True):
        newCard = Card(self.cardDeck[self.deckN])
        self.deckN += 1
        self.dealer.addCard(newCard)
        if face_up:
            img = PhotoImage(file="cards/" + newCard.filename())
        else:
            img = PhotoImage(file="cards/b1fv.png")  # 뒷면 카드 이미지
        label = Label(self.window, image=img)
        label.image = img  # 이미지 레퍼런스 유지
        self.LcardsDealer.append(label)
        label.place(x=250 + self.nCardsDealer * 30, y=150)
        if face_up or self.nCardsDealer > 0:  # 첫 번째 카드가 아니면 위치 조정
            label.place(x=250 + self.nCardsDealer * 30, y=150)
        self.nCardsDealer += 1
        PlaySound('sounds/cardFlip1.wav', SND_FILENAME)

    def hitPlayer(self, n):
        newCard = Card(self.cardDeck[self.deckN])
        self.deckN += 1
        self.player.addCard(newCard)
        p = PhotoImage(file="cards/" + newCard.filename())
        self.LcardsPlayer.append(Label(self.window, image=p))
        # 파이썬은 라벨 이미지 레퍼런스를 갖고 있어야 이미지가 보임
        self.LcardsPlayer[self.player.inHand() - 1].image = p
        self.LcardsPlayer[self.player.inHand() - 1].place(x=250 + n * 30, y=350)
        self.LplayerPts.configure(text=str(self.player.value()))
        PlaySound('sounds/cardFlip1.wav', SND_FILENAME)

    def pressedDeal(self):
        self.deal()
        self.hitDealer(False)  # 딜러의 카드 한장은 덮고
        self.hitDealer(True)  # 남은 한장은 오픈
        self.B50['state'] = 'normal'
        self.B50['bg'] = 'white'
        self.B10['state'] = 'normal'
        self.B10['bg'] = 'white'
        self.B1['state'] = 'normal'
        self.B1['bg'] = 'white'
        self.Hit['state'] = 'normal'
        self.Hit['bg'] = 'white'
        self.Stay['state'] = 'normal'
        self.Stay['bg'] = 'white'
        self.Deal['state'] = 'disabled'
        self.Deal['bg'] = 'gray'
        self.Again['state'] = 'disabled'
        self.Again['bg'] = 'gray'

    # def checkWinner(self):
    #     # 뒤집힌 카드를 다시 그린다.
    #     p = PhotoImage(file="cards/" + self.dealer.cards[0].filename())
    #     self.LcardsDealer[0].configure(image=p)  # 이미지 레퍼런스 변경
    #     self.LcardsDealer[0].image = p  # 파이썬은 라벨 이미지 레퍼런스를 갖고 있어야 이미지가 보임
    #     self.LdealerPts.configure(text=str(self.dealer.value()))
    #     if self.player.value() > 21:
    #         self.Lstatus.configure(text="Player Busts")
    #         PlaySound('sounds/wrong.wav', SND_FILENAME)
    #     elif self.dealer.value() > 21:
    #         self.Lstatus.configure(text="Dealer Busts")
    #         self.playerMoney += self.betMoney * 2
    #         PlaySound('sounds/win.wav', SND_FILENAME)
    #     elif self.dealer.value() == self.player.value():
    #         self.Lstatus.configure(text="Push")
    #         self.playerMoney += self.betMoney
    #     elif self.dealer.value() < self.player.value():
    #         self.Lstatus.configure(text="You won!!")
    #         self.playerMoney += self.betMoney * 2
    #         PlaySound('sounds/win.wav', SND_FILENAME)
    #     else:
    #         self.Lstatus.configure(text="Sorry you lost!")
    #         PlaySound('sounds/wrong.wav', SND_FILENAME)
    #     self.betMoney = 0
    #     self.LplayerMoney.configure(text="You have $" + str(self.playerMoney))
    #     self.LbetMoney.configure(text="$" + str(self.betMoney))
    #     self.B50['state'] = 'disabled'
    #     self.B50['bg'] = 'gray'
    #     self.B10['state'] = 'disabled'
    #     self.B10['bg'] = 'gray'
    #     self.B1['state'] = 'disabled'
    #     self.B1['bg'] = 'gray'
    #     self.Hit['state'] = 'disabled'
    #     self.Hit['bg'] = 'gray'
    #     self.Stay['state'] = 'disabled'
    #     self.Stay['bg'] = 'gray'
    #     self.Deal['state'] = 'disabled'
    #     self.Deal['bg'] = 'gray'
    #     self.Again['state'] = 'active'
    #     self.Again['bg'] = 'white'

    def checkWinner(self):
        # 뒤집힌 카드를 다시 그린다.
        p = PhotoImage(file="cards/" + self.dealer.cards[0].filename())
        self.LcardsDealer[0].configure(image=p)  # 이미지 레퍼런스 변경
        self.LcardsDealer[0].image = p  # 파이썬은 라벨 이미지 레퍼런스를 갖고 있어야 이미지가 보임
        self.LdealerPts.configure(text=str(self.dealer.value()))

        if self.player.value() > 21:
            self.Lstatus.configure(text="Player Busts")
            self.playSound('sounds/wrong.wav')  # 음악 재생 함수 호출
        elif self.dealer.value() > 21:
            self.Lstatus.configure(text="Dealer Busts")
            self.playerMoney += self.betMoney * 2
            self.playSound('sounds/win.wav')  # 음악 재생 함수 호출
        elif self.dealer.value() == self.player.value():
            self.Lstatus.configure(text="Push")
            self.playerMoney += self.betMoney
        elif self.dealer.value() < self.player.value():
            self.Lstatus.configure(text="You won!!")
            self.playerMoney += self.betMoney * 2
            self.playSound('sounds/win.wav')  # 음악 재생 함수 호출
        else:
            self.Lstatus.configure(text="Sorry you lost!")
            self.playSound('sounds/wrong.wav')  # 음악 재생 함수 호출

        self.betMoney = 0
        self.LplayerMoney.configure(text="You have $" + str(self.playerMoney))
        self.LbetMoney.configure(text="$" + str(self.betMoney))
        self.B50['state'] = 'disabled'
        self.B50['bg'] = 'gray'
        self.B10['state'] = 'disabled'
        self.B10['bg'] = 'gray'
        self.B1['state'] = 'disabled'
        self.B1['bg'] = 'gray'
        self.Hit['state'] = 'disabled'
        self.Hit['bg'] = 'gray'
        self.Stay['state'] = 'disabled'
        self.Stay['bg'] = 'gray'
        self.Deal['state'] = 'disabled'
        self.Deal['bg'] = 'gray'
        self.Again['state'] = 'active'
        self.Again['bg'] = 'white'

    def playSound(self, sound_file):
        PlaySound(sound_file, SND_FILENAME | SND_ASYNC)

    def pressedHit(self):
        self.nCardsPlayer += 1
        self.hitPlayer(self.nCardsPlayer)
        if self.player.value() > 21:
            self.checkWinner()

    def deal(self):
        self.player.reset()
        self.dealer.reset()
        # 카드 덱 52장 셔플링 0,1,,.51
        self.cardDeck = [i for i in range(52)]
        random.shuffle(self.cardDeck)
        self.deckN = 0
        self.hitPlayer(0)
        # self.hitDealerDown()
        self.hitPlayer(1)
        # self.hitDealer(0)
        self.nCardsPlayer = 1
        self.nCardsDealer = 0
        self.B50['state'] = 'disabled'
        self.B50['bg'] = 'gray'
        self.B10['state'] = 'disabled'
        self.B10['bg'] = 'gray'
        self.B1['state'] = 'disabled'
        self.B1['bg'] = 'gray'
    def pressedB50(self):
        self.betMoney += 50
        if 50 <= self.playerMoney:
            self.LbetMoney.configure(text="$" + str(self.betMoney))
            self.playerMoney -= 50
            self.LplayerMoney.configure(text="You have $" + str(self.playerMoney))
            self.Deal["state"] = "active"
            self.Deal["bg"] = "white"
            PlaySound('sounds/chip.wav', SND_FILENAME)
        else:
            self.betMoney -= 50
    def setupLabel(self):
        self.LbetMoney = Label(text="$0", width=4, height=1, font=self.fontstyle, bg="green", fg="cyan")
        self.LbetMoney.place(x=200, y=450)
        self.LplayerMoney = Label(text="You have $1000", width=15, height=1, font=self.fontstyle, bg="green", fg="cyan")
        self.LplayerMoney.place(x=500, y=450)
        self.LplayerPts = Label(text="", width=2, height=1, font=self.fontstyle2, bg="green", fg="white")
        self.LplayerPts.place(x=300, y=300)
        self.LdealerPts = Label(text="", width=2, height=1, font=self.fontstyle2, bg="green", fg="white")
        self.LdealerPts.place(x=300, y=100)
        self.Lstatus = Label(text="", width=15, height=1, font=self.fontstyle, bg="green", fg="white")
        self.Lstatus.place(x=500, y=300)
    def setupButton(self):
        self.B50 = Button(self.window, text="Bet 50", width=6, height=1, font=self.fontstyle2, command=self.pressedB50)
        self.B50.place(x=50, y=500)
        self.B10 = Button(self.window, text="Bet 10", width=6, height=1, font=self.fontstyle2, command=self.pressedB10)
        self.B10.place(x=150, y=500)
        self.B1 = Button(self.window, text="Bet 1", width=6, height=1, font=self.fontstyle2, command=self.pressedB1)
        self.B1.place(x=250, y=500)
        self.Hit = Button(self.window, text="Hit", width=6, height=1, font=self.fontstyle2, command=self.pressedHit)
        self.Hit.place(x=400, y=500)
        self.Stay = Button(self.window, text="Stay", width=6, height=1, font=self.fontstyle2, command=self.pressedStay)
        self.Stay.place(x=500, y=500)
        self.Deal = Button(self.window, text="Deal", width=6, height=1, font=self.fontstyle2, command=self.pressedDeal)
        self.Deal.place(x=600, y=500)
        self.Again = Button(self.window, text="Again", width=6, height=1, font=self.fontstyle2,
                            command=self.pressedAgain)
        self.Again.place(x=700, y=500)
        self.Hit['state'] = 'disabled'
        self.Hit['bg'] = 'gray'
        self.Stay['state'] = 'disabled'
        self.Stay['bg'] = 'gray'
        self.Deal['state'] = 'disabled'
        self.Deal['bg'] = 'gray'
        self.Again['state'] = 'disabled'
        self.Again['bg'] = 'gray'
    def __init__(self):
        self.window = Tk()
        self.window.title("Black Jack")
        self.window.geometry("902x600")
        self.window.configure(bg="green")
        # 배경 이미지 설정
        self.bg_image = PhotoImage(file="cards/table.gif")  # 배경 이미지 로드
        self.bg_label = Label(self.window, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # 창 전체에 이미지를 맞춤

        self.fontstyle = font.Font(self.window, size=24, weight='bold', family='Consolas')
        self.fontstyle2 = font.Font(self.window, size=16, weight='bold', family='Consolas')
        self.setupButton()
        self.setupLabel()
        self.player = Player("player")
        self.dealer = Player("dealer")
        self.betMoney = 0
        self.playerMoney = 1000
        self.nCardsDealer = 0
        self.nCardsPlayer = 0
        self.LcardsPlayer = []
        self.LcardsDealer = []
        self.deckN = 0
        self.window.mainloop()

BlackJack()
