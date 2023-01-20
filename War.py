import random

SUITS = ['C', 'D', 'H', 'S']
VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

SUITS_DICT = {'C': 'clubs', 'D': 'diamonds', 'H': 'hearts', 'S': 'spades'}
SCORES = {str(i): i for i in range(2,11)}
SCORES['J'], SCORES['Q'], SCORES['K'], SCORES['A'] = 10, 10, 10, 11
STRICT_SCORES = SCORES.copy()
STRICT_SCORES['J'], STRICT_SCORES['Q'], STRICT_SCORES['K'] = 10.1, 10.2, 10.3
WORD_DICT = {0: 'I', 1: 'DE', 2: 'CLARE', 3: 'WAR!'}

class Card(object):
    def __init__(self, value, suit):
        self._value = value
        self._suit = suit

    def get_value(self):
        return self._value

    def get_suit(self):
        return self._suit

    def __repr__(self):
        try:
            return f'Card[value={self.get_value()}, suit={SUITS_DICT[self.get_suit()]}]'
        except KeyError:
            return f'Card[value={self.get_value()}, suit={self.get_suit()}]'

    def __eq__(self, card):
        if type(card) != Card:
            raise ValueError('argument must be of type Card.')
        return self.get_suit() == card.get_suit() and self.get_value() == card.get_value()

    def score(self, strict=False):
        if not strict:
            return SCORES[self.get_value()]
        else:
            return STRICT_SCORES[self.get_value()]

    def compare(self, card, trump=None, face_compare=False):
        score1, score2 = self.score(face_compare), card.score(face_compare)
        if score1 > score2:
            return self
        elif score2 > score1:
            return card
        elif score1 == score2:
            if self.get_suit() == trump:
                return self
            elif card.get_suit() == trump:
                return card
            else:
                return Card('T', 'T')

class Deck(object):
    def __init__(self, name, cards):
        self.name = name
        self.cards = cards
        self.size = len(cards)
        self._current_index = 0

    def __repr__(self):
        return self.name + ' ' + str([card for card in self.cards])

    def __iter__(self):
        return self

    def __next__(self):
        if self._current_index < self.size:
            card = self.cards[self._current_index]
            self._current_index += 1
            return card
        raise StopIteration

    def __add__(self, deck):
        self.cards += deck.cards
        return Deck(self.name, self.cards)

    def flip(self):
        try:
            return self.cards.pop(0)
        except IndexError:
            raise IndexError('No cards left.')

    def add_card(self, card):
        self.cards.append(card)

    def remove(self, card):
        for deck_card in self.cards:
            if card == deck_card:
                self.cards.remove(card)
            else:
                raise ValueError(f'Card {card} not in deck.')

    def remove_many(self, cards):
        for card in cards:
            self.cards.remove(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def split(self, ratio=0.5):
        num_cards = int(ratio*self.size)
        return Deck(self.name + '1', self.cards[:num_cards]), Deck(self.name + '2', self.cards[num_cards:])


ALL_CARDS = []
for suit in SUITS:
    for value in VALUES:
        ALL_CARDS.append(Card(value, suit))

TIE_CARD = Card('T', 'T')


class Game(object):
    def __init__(self):
        self.deck = Deck('deck', ALL_CARDS)
        self.pile = Deck('pile', [])

    def start(self):
        self.deck.shuffle()
        self.deck1, self.deck2 = self.deck.split()

    def i_declare_war(self):
        empty = False
        i = 0
        while i < 4 and self.deck1.cards and self.deck2.cards:
            p1_card = self.deck1.flip()
            p2_card = self.deck2.flip()
            self.pile.add_card(p1_card)
            self.pile.add_card(p2_card)
            print(WORD_DICT[i], p1_card, p2_card)
            i += 1
        if i < 3:
            print("EMPTY!!", i)
            if self.deck1.cards:
                result  = p1_card
            elif self.deck2.cards:
                result = p2_card
        else:
            result = p1_card.compare(p2_card, face_compare=True)
        if result == p1_card:
            print("Player1 won the war.")
            self.deck1 += self.pile
            self.pile = Deck('pile', [])
        elif result == p2_card:
            print("Player2 won the war.")
            self.deck2 += self.pile
            self.pile = Deck('pile', [])
        elif result == TIE_CARD:
            print("...")
            self.i_declare_war()

    def war(self):
        empty = False
        try:
            p1_card, p2_card = self.deck1.flip(), self.deck2.flip()
            self.pile.add_card(p1_card)
            self.pile.add_card(p2_card)
        except:
            empty = True
        if not empty:
            result = p1_card.compare(p2_card, face_compare=True)
            print(p1_card, 'vs.', p2_card)
            print(result)
            if result == p1_card:
                print(result == p1_card)
                print("Player1 won the hand.")
                self.deck1 += self.pile
                self.pile = Deck('pile', [])
            elif result == p2_card:
                print(result, p2_card)
                print("Player2 won the hand.")
                self.deck2 += self.pile
                self.pile = Deck('pile', [])
            elif result == TIE_CARD:
                print("...")
                self.i_declare_war()


if __name__ == "__main__":
    game = Game()
    game.start()
    turns = 0
    while True:
        game.war()
        turns += 1
        if game.deck1.cards == [] or game.deck2.cards == []:
            break
    if game.deck1.cards != []:
        print('Player1 wins!')
    if game.deck2.cards != []:
        print('Player2 wins!')






