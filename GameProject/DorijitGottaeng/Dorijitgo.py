from tkinter import *
from tkinter import font
from winsound import *
from Card import *
from Player import *
from configuration import *
import random
import copy


class Dorijitgo:
    def __init__(self):
        self.window = Tk()
        self.window.title("도리짓고 땡")
        self.window.geometry("800x600")
        self.window.configure(bg="green")
        self.fontstyle = font.Font(self.window, size=24, weight='bold', family='Consolas')
        self.fontstyle2 = font.Font(self.window, size=16, weight='bold', family='Consolas')
        self.fontstyle3 = font.Font(self.window, size=16, weight='bold', family='Consolas')
        self.setupButton()
        self.setupLabel()
        self.player = [Player("player"), Player("player2"), Player("player3")]
        self.dealer = Player("dealer")
        self.betMoney = [0, 0, 0]
        self.playerMoney = 1000
        self.LcardsPlayer = [[], [], []]
        self.LcardsLabelPlayer = [[], [], []]
        self.LcardsDealer = []
        self.LcardsLabelDealer = []
        self.deckN = 0
        self.round = 0
        self.window.mainloop()

    def setupButton(self):
        self.Won5 = [Button(self.window, text="5만", width=4, height=1, font=self.fontstyle2,
                            command=lambda: self.pressedWon5(0)),
                     Button(self.window, text="5만", width=4, height=1, font=self.fontstyle2,
                            command=lambda: self.pressedWon5(1)),
                     Button(self.window, text="5만", width=4, height=1, font=self.fontstyle2,
                            command=lambda: self.pressedWon5(2))]

        self.Won1 = [Button(self.window, text="1만", width=4, height=1, font=self.fontstyle2,
                            command=lambda: self.pressedWon1(0)),
                     Button(self.window, text="1만", width=4, height=1, font=self.fontstyle2,
                            command=lambda: self.pressedWon1(1)),
                     Button(self.window, text="1만", width=4, height=1, font=self.fontstyle2,
                            command=lambda: self.pressedWon1(2))]
        for i in range(3):
            self.Won5[i].place(x=50 + (i * 200), y=550)
            self.Won1[i].place(x=120 + (i * 200), y=550)

        self.Deal = Button(self.window, text="Deal", width=6, height=1, font=self.fontstyle2, command=self.pressedDeal)
        self.Deal.place(x=600, y=550)
        self.Again = Button(self.window, text="Again", width=6, height=1, font=self.fontstyle2,
                            command=self.pressedAgain)
        self.Again.place(x=700, y=550)

        self.Deal['state'] = 'disabled'
        self.Deal['bg'] = 'gray'
        self.Again['state'] = 'disabled'
        self.Again['bg'] = 'gray'

        # self.test = Button(self.window, text="test", width=6, height=1, font=self.fontstyle2,
        #                    command=lambda: self.test1(0))
        # self.test.place(x=500, y=300)
        # self.test["state"] = "active"
        # self.test["bg"] = "white"

    def setupLabel(self):
        self.LbetMoney = [Label(text="0만", width=6, height=1, font=self.fontstyle, bg="green", fg="cyan"),
                          Label(text="0만", width=6, height=1, font=self.fontstyle, bg="green", fg="cyan"),
                          Label(text="0만", width=6, height=1, font=self.fontstyle, bg="green", fg="cyan")]

        self.LplayerRank = [Label(text="", width=20, height=1, font=self.fontstyle3, bg="green", fg="cyan"),
                            Label(text="", width=20, height=1, font=self.fontstyle3, bg="green", fg="cyan"),
                            Label(text="", width=20, height=1, font=self.fontstyle3, bg="green", fg="cyan")]
        self.Lstatus = [Label(text="", width=5, height=1, font=self.fontstyle, bg="green", fg="red"),
                        Label(text="", width=5, height=1, font=self.fontstyle, bg="green", fg="red"),
                        Label(text="", width=5, height=1, font=self.fontstyle, bg="green", fg="red")]

        for i in range(3):
            self.LbetMoney[i].place(x=60 + (i * 200), y=500)
            self.LplayerRank[i].place(x=30 + (i * 230), y=290)
            self.Lstatus[i].place(x=60 + (i * 230), y=250)

        self.LplayerMoney = Label(text="1000만", width=15, height=1, font=self.fontstyle, bg="green",
                                  fg="blue")
        self.LplayerMoney.place(x=560, y=500)

        self.LdealerRank = Label(text="", width=20, height=1, font=self.fontstyle3, bg="green", fg="cyan")
        self.LdealerRank.place(x=280, y=40)

    def pressedWon5(self, i):
        self.betMoney[i] += 5
        if self.playerMoney >= 5:
            self.LbetMoney[i].configure(text=str(self.betMoney[i]) + "만")
            self.playerMoney -= 5
            self.LplayerMoney.configure(text=str(self.playerMoney) + "만")
            self.Deal["state"] = "active"
            self.Deal["bg"] = "white"
            PlaySound('sounds/chip.wav', SND_FILENAME | SND_ASYNC | SND_ALIAS)
        else:
            self.betMoney[i] -= 5

    def pressedWon1(self, i):
        self.betMoney[i] += 1
        if self.playerMoney >= 1:
            self.LbetMoney[i].configure(text=str(self.betMoney[i]) + "만")
            self.playerMoney -= 1
            self.LplayerMoney.configure(text=str(self.playerMoney) + "만")
            self.Deal["state"] = "active"
            self.Deal["bg"] = "white"
            PlaySound('sounds/chip.wav', SND_FILENAME | SND_ASYNC | SND_ALIAS)
        else:
            self.betMoney[i] -= 1

    def deal(self):
        if self.round == 0:
            for i in range(3):
                self.player[i].reset()
            self.dealer.reset()  # 카드 덱 40장 셔플링 0,1,,.51
            self.cardDeck = [i for i in range(40)]
            random.shuffle(self.cardDeck)
            self.deckN = 0
            for i in range(3):
                self.hitPlayer(i, 0)
            self.hitDealerDown(0)
            PlaySound('sounds/cardFlip1.wav', SND_FILENAME | SND_ASYNC | SND_ALIAS)
        elif self.round == 1:
            for i in range(3):
                for j in range(3):
                    self.hitPlayer(j, i + 1)
                self.hitDealerDown(i + 1)
            PlaySound('sounds/cardFlip1.wav', SND_FILENAME | SND_ASYNC | SND_ALIAS)
        if self.round == 2:
            for j in range(3):
                self.hitPlayer(j, 4)
            self.hitDealerDown(4)
            self.round += 1
        elif self.round == 3:
            self.checkWinner()
        else:
            self.round += 1
            for i in range(3):
                self.Won5[i]['state'] = 'active'
                self.Won5[i]['bg'] = 'white'
                self.Won1[i]['state'] = 'active'
                self.Won1[i]['bg'] = 'white'
            self.Deal['state'] = 'disabled'
            self.Deal['bg'] = 'gray'

    def hitPlayer(self, i, n):
        newCard = Card(self.cardDeck[self.deckN])
        self.deckN += 1
        self.player[i].addCard(newCard)
        p = PhotoImage(file="cards/" + newCard.filename())
        self.LcardsPlayer[i].append(Label(self.window, image=p))
        # 파이썬은 라벨 이미지 레퍼런스를 갖고 있어야 이미지가 보임
        self.LcardsPlayer[i][self.player[i].inHand() - 1].image = p
        self.LcardsPlayer[i][self.player[i].inHand() - 1].place(x=50 + (i * 230) + n * 35, y=350)
        # 카드 숫자 라벨 출력
        self.LcardsLabelPlayer[i].append(
            Label(text=newCard.value, width=2, height=1, font=self.fontstyle2, bg="green", fg="white"))
        self.LcardsLabelPlayer[i][self.player[i].inHand() - 1].place(x=70 + (i * 230) + n * 35, y=320)

    def hitDealerDown(self, n):
        newCard = Card(self.cardDeck[self.deckN])
        self.deckN += 1
        self.dealer.addCard(newCard)
        p = PhotoImage(file="cards/cardback.gif")
        self.LcardsDealer.append(Label(self.window, image=p))
        # 파이썬은 라벨 이미지 레퍼런스를 갖고 있어야 이미지가 보임
        self.LcardsDealer[self.dealer.inHand() - 1].image = p
        self.LcardsDealer[self.dealer.inHand() - 1].place(x=300 + n * 35, y=100)
        # 카드 숫자 라벨 출력
        self.LcardsLabelDealer.append(
            Label(text=newCard.value, width=2, height=1, font=self.fontstyle2, bg="green", fg="white"))
        # PlaySound('sounds/cardFlip1.wav', SND_FILENAME)

    def pressedDeal(self):
        self.deal()

    def pressedAgain(self):
        self.LdealerRank.configure(text="")
        self.LplayerMoney.configure(text=str(self.playerMoney) + "만")
        self.betMoney = [0, 0, 0]
        for i in range(3):
            self.Lstatus[i].configure(text="")
            self.LplayerRank[i].configure(text="")
            self.LbetMoney[i].configure(text=str(self.betMoney[i]) + "만")
            for t in self.LcardsPlayer[i]:
                t.destroy()

        for t in self.LcardsDealer:
            t.destroy()
        self.LcardsPlayer = [[], [], []]

        for j in range(3):
            for i in self.LcardsLabelPlayer[j]:
                i.configure(text="")

        self.LcardsLabelPlayer = [[], [], []]
        self.LcardsDealer = []
        for i in self.LcardsLabelDealer:
            i.configure(text="")
        self.LcardsLabelDealer = []

        self.deckN = 0
        self.round = 0
        for i in range(3):
            self.Won5[i]['state'] = 'active'
            self.Won5[i]['bg'] = 'white'
            self.Won1[i]['state'] = 'active'
            self.Won1[i]['bg'] = 'white'
        self.Deal['state'] = 'disabled'
        self.Deal['bg'] = 'gray'
        self.Again['state'] = 'disabled'
        self.Again['bg'] = 'gray'
        PlaySound('sounds/ding.wav', SND_FILENAME | SND_ASYNC | SND_ALIAS)

    def madeTwo(self, two):
        two.sort()
        print(two)
        # ex) two = [[2,1], [3,2]]  앞은 숫자 뒤는 모양
        if two == [[3, 1], [8, 1]]:  # 38광땡
            return [100, "38광땡"]
        elif two == [[1, 1], [3, 1]]:  # 13광땡
            return [99, "13광땡"]
        elif two == [[1, 1], [8, 1]]:  # 18광땡
            return [98, "18광땡"]
        elif two[0][0] == two[1][0]:  # 땡
            return [two[0][0] + 70, str(two[0][0]) + "땡"]
        elif (two[0][0] + two[1][0]) % 10:  # 끗
            return [((two[0][0] + two[1][0]) % 10) + 10, str((two[0][0] + two[1][0]) % 10) + "끗"]
        elif two[0][0] + two[1][0] == 10:  # 망통
            return [two[1][0], "망통"]
        else:
            return [0, "뭐임"]

    def madeThree(self):
        made1 = ((1, 2, 7), (1, 3, 6), (1, 4, 5), (1, 9, 10),
                 (2, 3, 5), (2, 8, 10),
                 (3, 7, 10), (3, 8, 9),
                 (4, 6, 10), (4, 7, 9),
                 (5, 6, 9), (5, 7, 8))

        made2 = ((1, 1, 8),
                 (2, 2, 6),
                 (3, 3, 4),
                 (4, 4, 2),
                 (5, 5, 10),
                 (6, 6, 8),
                 (7, 7, 6),
                 (8, 8, 4),
                 (9, 9, 2))
        threeDict = {(1, 1, 8): "콩콩팔", (1, 2, 7): "삐리칠", (1, 3, 6): "물삼육", (1, 4, 5): "빽새오", (1, 9, 10): "삥구장",
                     (2, 2, 6): "니니육", (2, 3, 5): "이삼오", (2, 8, 10): "이판장", (3, 3, 4): "심심새", (3, 7, 10): "삼칠장",
                     (3, 8, 9): "삼빡구", (4, 4, 2): "살살이", (4, 6, 10): "사륙장", (4, 7, 9): "사칠구", (5, 5, 10): "꼬꼬장",
                     (5, 6, 9): "오륙구", (5, 7, 8): "오리발", (6, 6, 8): "쭉쭉팔", (7, 7, 6): "철철육", (8, 8, 4): "팍팍싸",
                     (9, 9, 2): "구구리"}
        # 플레이어 판단
        for i in range(len(self.player)):
            rdyNum = [i for i in range(5)]
            # 겹치는 친구가 없다면 5 == 5 made1
            if len(set(self.player[i].getCardsValue())) == 5:
                for j in range(len(made1)):

                    if all(card in self.player[i].getCardsValue() for card in made1[j]):
                        print(i, "번째 플레이어 있다1", made1[j])
                        insex = []
                        twoCards = []
                        for n in made1[j]:
                            insex.append(self.player[i].getCardsValue().index(n))
                        for tq in [num for num in rdyNum if num not in insex]:
                            twoCards.append(self.player[i].getCards()[tq])
                        result = self.madeTwo(twoCards)
                        self.player[i].winningPoint = result[0]
                        print("결과", result)
                        for n in insex:
                            self.LcardsPlayer[i][n].place(x=50 + (i * 230) + n * 35, y=370)
                            self.LcardsLabelPlayer[i][n].configure(fg="orange")

                        self.LplayerRank[i].configure(text=threeDict[made1[j]] + " " + result[1])
                        break
                    elif j == len(made1) - 1:
                        print(i, "번째 플레이어 노메이드1")
                        self.LplayerRank[i].configure(text="노메이드")
            # 겹치는 친구 1개 있다면 4 == 4 made2
            else:
                multiKey = 0
                c = dict()
                for z in self.player[i].getCardsValue():
                    try:
                        c[z] += 1
                    except:
                        c[z] = 0
                for key, value in c.items():
                    if value != 0:
                        multiKey = key

                if multiKey <= 9 and all(card in self.player[i].getCardsValue() for card in made2[multiKey - 1]):
                    print(i, "번째 플레이어 있다2", made2[multiKey - 1])
                    insex = []
                    twoCards = []
                    for n in made2[multiKey - 1]:
                        insex.append(self.player[i].getCardsValue().index(n))

                    for n in insex:
                        self.LcardsPlayer[i][n].place(x=50 + (i * 230) + n * 35, y=370)
                        self.LcardsLabelPlayer[i][n].configure(fg="orange")
                    Sarr = self.player[i].getCardsValue()
                    Sarr.remove(multiKey)
                    sexy = Sarr.index(multiKey)
                    self.LcardsPlayer[i][sexy + 1].place(x=50 + (i * 230) + (sexy + 1) * 35, y=370)
                    self.LcardsLabelPlayer[i][sexy + 1].configure(fg="orange")

                    insex2 = list(set(insex))
                    insex2.append(sexy + 1)

                    for tq in [num for num in rdyNum if num not in insex2]:
                        twoCards.append(self.player[i].getCards()[tq])
                    result = self.madeTwo(twoCards)
                    self.player[i].winningPoint = result[0]
                    print("결과2", result)
                    self.LplayerRank[i].configure(text=threeDict[made1[multiKey - 1]] + " " + result[1])

                else:
                    # 중복됬는데도 없는애들, 중복된애들이 10 이상인놈들
                    for j in range(len(made1)):
                        if all(card in set(self.player[i].getCardsValue()) for card in made1[j]):
                            print(i, "번째 플레이어 있다3", made1[j])
                            insex = []
                            twoCards = []
                            for n in made1[j]:
                                insex.append(self.player[i].getCardsValue().index(n))
                            for tq in [num for num in rdyNum if num not in insex]:
                                twoCards.append(self.player[i].getCards()[tq])
                            result = self.madeTwo(twoCards)
                            self.player[i].winningPoint = result[0]
                            print("결과3", result)
                            for n in insex:
                                self.LcardsPlayer[i][n].place(x=50 + (i * 230) + n * 35, y=370)
                                self.LcardsLabelPlayer[i][n].configure(fg="orange")
                            self.LplayerRank[i].configure(text=threeDict[made1[j]] + " " + result[1])
                            break
                        elif j == len(made1) - 1:
                            print(i, "번째 플레이어 노메이드2")
                            self.LplayerRank[i].configure(text="노메이드")

        # 딜러 판단
        rdyNum = [i for i in range(5)]
        if len(set(self.dealer.getCardsValue())) == 5:
            for j in range(len(made1)):
                if all(card in self.dealer.getCardsValue() for card in made1[j]):
                    print("딜러 있다1", made1[j])
                    insex = []
                    twoCards = []
                    for n in made1[j]:
                        insex.append(self.dealer.getCardsValue().index(n))
                    for tq in [num for num in rdyNum if num not in insex]:
                        twoCards.append(self.dealer.getCards()[tq])
                    result = self.madeTwo(twoCards)
                    self.dealer.winningPoint = result[0]
                    print("딜러 결과1", result)
                    for n in insex:
                        self.LcardsDealer[n].place(x=300 + n * 35, y=120)
                        self.LcardsLabelDealer[n].configure(fg="orange")
                    self.LdealerRank.configure(text=threeDict[made1[j]] + " " + result[1])
                    break
                elif j == len(made1) - 1:
                    print("딜러 노메이드1")
                    self.LdealerRank.configure(text="노메이드")
        # 겹치는 친구 1개 있다면 4 == 4 made2
        else:
            multiKey = 0
            c = dict()
            for z in self.dealer.getCardsValue():
                try:
                    c[z] += 1
                except:
                    c[z] = 0
            for key, value in c.items():
                if value != 0:
                    multiKey = key

            if multiKey <= 9 and all(card in self.dealer.getCardsValue() for card in made2[multiKey - 1]):
                print("딜러 있다2", made2[multiKey - 1])
                insex = []
                twoCards = []
                for n in made2[multiKey - 1]:
                    insex.append(self.dealer.getCardsValue().index(n))

                for n in insex:
                    self.LcardsDealer[n].place(x=300 + n * 35, y=120)
                    self.LcardsLabelDealer[n].configure(fg="orange")
                Sarr = self.dealer.getCardsValue()
                Sarr.remove(multiKey)
                sexy = Sarr.index(multiKey)
                self.LcardsDealer[sexy + 1].place(x=300 + (sexy + 1) * 35, y=120)
                self.LcardsLabelDealer[sexy + 1].configure(fg="orange")

                insex2 = list(set(insex))
                insex2.append(sexy + 1)

                for tq in [num for num in rdyNum if num not in insex2]:
                    twoCards.append(self.dealer.getCards()[tq])
                result = self.madeTwo(twoCards)
                self.dealer.winningPoint = result[0]
                print("딜러 결과2", result)
                self.LdealerRank.configure(text=threeDict[made1[multiKey - 1]] + " " + result[1])

            else:
                # 중복됬는데도 없는애들, 중복된애들이 10 이상인놈들
                for j in range(len(made1)):
                    if all(card in set(self.dealer.getCardsValue()) for card in made1[j]):
                        print("딜러 있다3", made1[j])
                        insex = []
                        twoCards = []
                        for n in made1[j]:
                            insex.append(self.dealer.getCardsValue().index(n))
                        for tq in [num for num in rdyNum if num not in insex]:
                            twoCards.append(self.dealer.getCards()[tq])
                        result = self.madeTwo(twoCards)
                        self.dealer.winningPoint = result[0]
                        print("딜러 결과3", result)
                        for n in insex:
                            self.LcardsDealer[n].place(x=300 + n * 35, y=120)
                            self.LcardsLabelDealer[n].configure(fg="orange")
                        self.LdealerRank.configure(text=threeDict[made1[j]] + " " + result[1])
                        break
                    elif j == len(made1) - 1:
                        print("딜러 노메이드1")
                        self.LdealerRank.configure(text="노메이드")

    def checkWinner(self):
        # 뒤집힌 카드를 다시 그린다.
        for i in range(5):
            p = PhotoImage(file="cards/" + self.dealer.cards[i].filename())
            self.LcardsDealer[i].configure(image=p)  # 이미지 레퍼런스 변경
            self.LcardsDealer[i].image = p  # 파이썬은 라벨 이미지 레퍼런스를 갖고 있어야 이미지가 보임
            self.LcardsLabelDealer[i].place(x=320 + i * 35, y=70)
        for i in range(3):
            self.LplayerRank[i].configure(text="테스트중임다")
        self.LdealerRank.configure(text="테스트중임다")

        # 승리판단
        self.madeThree()

        for i in range(3):
            if self.dealer.winningPoint < self.player[i].winningPoint:
                self.Lstatus[i].configure(text="승")
                self.playerMoney += self.betMoney[i] * 2
                PlaySound('sounds/win.wav', SND_FILENAME | SND_ASYNC | SND_ALIAS)
            elif self.dealer.winningPoint == self.player[i].winningPoint:
                self.Lstatus[i].configure(text="비김")
                self.playerMoney += self.betMoney[i]
            else:
                self.Lstatus[i].configure(text="패")
                PlaySound('sounds/wrong.wav', SND_FILENAME | SND_ASYNC | SND_ALIAS)


        for i in range(3):
            self.Won5[i]['state'] = 'disabled'
            self.Won5[i]['bg'] = 'gray'
            self.Won1[i]['state'] = 'disabled'
            self.Won1[i]['bg'] = 'gray'
        self.Deal['state'] = 'disabled'
        self.Deal['bg'] = 'gray'
        self.Again['state'] = 'active'
        self.Again['bg'] = 'white'


Dorijitgo()
