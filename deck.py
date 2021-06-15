from card import Card
import random


##
# Deck class
#  A deck with a list of cards
class Deck:
    def __init__(self):
        """
        Creates an empty list of cards
        """

        self._cards = []

    def setDefault(self):
        """
        Set deck to to the standard 52-cards deck
        """

        self.empty()
        for suit in ['s', 'h', 'c', 'd']:
            for val in range(1, 14):
                self._cards.append(Card(suit, val))

    def add(self, card, position=(-1, -1)):
        """
        Add a card to the deck with given coordinates

        :param card: A card object
        :param position: position of the card
        """
        x, y = position
        if x != -1 and y != -1:
            card.move(x, y)

        self._cards.append(card)

    def cards(self):
        """
        Get the list of cards in the deck

        :return: a list of cards
        """

        return self._cards

    def shuffle(self):
        """
        Shuffle the deck (randomize cards list)
        """

        random.shuffle(self._cards)

    def draw(self):
        """
        Draws the top card from the deck and remove it

        :return: Card - the last card in the cards list
        """

        # No cards left
        if len(self._cards) == 0:
            return None

        # Remove top card
        card = self._cards.pop()

        return card

    def empty(self):
        """
        Empty the deck
        """

        self._cards = []

    def size(self):
        """
        Get the number of cards in the deck

        :return: int - number of cards
        """

        return len(self._cards)

    def merge(self, deck):
        """
        Move all cards from other deck to this deck

        :param deck: Another deck of cards
        """

        for card in deck._cards:
            self._cards.append(card)

        deck.empty()

    def getCardBack(self):
        """
        Get a Card that has the card back sprite

        :return: A Card back sprite
        """

        return Card('s', 1, "cardBack.png")

    def __add__(self, deck):
        newDeck = Deck()
        for card in self._cards:
            newDeck.add(card)
        for card in deck:
            newDeck.add(card)
        return newDeck

    def __getitem__(self, num):
        """
        Gets a card given its position at the deck

        :param num: card number from bottom up
        :return: A Card
        """

        return self._cards[num]

    def __iter__(self):
        """
        Make Deck iterable

        :return: iterable list of cards
        """

        return iter(self._cards)
