class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.N = 0
    def inHand(self):
        return self.N
    def addCard(self, c):
        self.cards.append(c)
        self.N += 1
    def reset(self):
        self.N = 0
        self.cards.clear()
    def value(self):
        total_value = 0
        ace_count = 0
        for card in self.cards:
            card_value = card.getValue()
            if card_value == 1:
                ace_count += 1
            total_value += card_value
        while ace_count > 0:
            if total_value + 10 <= 21:
                total_value += 10
            ace_count -= 1

        return total_value
