class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.N = 0
        self.winningPoint = 0

    def inHand(self):
        return self.N

    def addCard(self, c):
        self.cards.append(c)
        self.N += 1

    def reset(self):
        self.N = 0
        self.cards.clear()
        self.winningPoint = 0

    def getCards(self):
        cards = [[0, 0] for i in range(self.N)]
        for i in range(self.N):
            cards[i][0] = self.cards[i].getValue()
            cards[i][1] = self.cards[i].getShape()
        return cards

    def getCardsValue(self):
        cards = [[0] for i in range(self.N)]
        for i in range(self.N):
            cards[i] = self.cards[i].getValue()
        return cards

    def getCardsShape(self):
        cards = [[0] for i in range(self.N)]
        for i in range(self.N):
            cards[i] = self.cards[i].getShape()
        return cards
