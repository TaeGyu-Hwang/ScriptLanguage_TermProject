class Card:
    def __init__(self, temp):  # 렌덤 넘버0..40 값을 입력받아서 카드 객체 생성
        self.value = temp % 10 + 1  # 1..13
        self.x = temp // 10  # 0..3 카드 무늬suit 결정

    def getValue(self):
            return self.value

    def getShape(self):
        return self.x

    def getsuit(self):  # 카드 무늬 결정
        if self.x == 0:
            self.suit = "Clubs"
        elif self.x == 1:
            self.suit = "Spades"
        elif self.x == 2:
            self.suit = "Hearts"
        else:
            self.suit = "Diamonds"
        return self.suit

    def filename(self):  # 카드 이미지 파일 이름
        return str(self.value) + '.' + str(self.x + 1) + ".gif"


if __name__ == "__main__":
    cardDeck = [i for i in range(48)]
    for i in range(40):
        hi = Card(cardDeck[i])
        print(hi.filename())
