import pygame
from deck import Deck
from text import Button, Text, InputBox


def checkHand(cards):
    """
    check hand and return the ranking and highest card in the rank
    rank 1 - 10 from single card to royal flush

    :param cards: a list of cards
    :return: rank and card
    """

    # 10 - royal flush
    card = royalFlush(cards)
    if card is not None:
        return 10, card

    # 9 - straight flush
    card = straightFlush(cards)
    if card is not None:
        return 9, card

    # 8 - four of a kind
    card = findRepeat(4, cards)
    if card is not None:
        return 8, card

    # 7 - full house
    card = fullHouse(cards)
    if card is not None:
        return 7, card

    # 6 - flush
    card = flush(cards)
    if card is not None:
        return 6, card

    # 5 - straight
    card = straight(cards)
    if card is not None:
        return 5, card

    # 4 - three of a kind
    card = findRepeat(3, cards)
    if card is not None:
        return 4, card

    # 3 - two pairs
    card = twoPair(cards)
    if card is not None:
        return 3, card

    # 2 - one pair
    card = findRepeat(2, cards)
    if card is not None:
        return 2, card

    # 1 - highest card
    card = findHighest(cards)
    return 1, card


def findHighest(cards):
    """
    Finds the highest card in the list

    :param cards: a list of cards
    :return: a card with the highest value
    """

    highest = 0
    for i in range(1, len(cards)):
        if cards[i] > cards[highest]:
            highest = i

    return cards[highest]


def findRepeat(minimum, cards):
    """
    Find multiples of a same card

    :param minimum: number of multiples to look for
    :param cards: a list of cards
    :return: one of the multiple cards if found
    """
    vals = []
    for i in range(13):
        vals.append([])

    # Sort cards by value, ace at the end
    for card in cards:
        val = card.getValue()
        if val == 1:
            vals[12].append(card)
        else:
            vals[val - 2].append(card)

    # Find highest value repeat:
    for val in reversed(vals):
        if len(val) >= minimum:
            return val[0]

    # Not enough repeats
    return None


def twoPair(cards):
    """
    Look for two pairs in the list

    :param cards: a list of cards
    :return: one of the cards of the highest pair
    """

    vals = []
    for i in range(13):
        vals.append([])

    # Sort cards by value, ace at the end
    for card in cards:
        val = card.getValue()
        if val == 1:
            vals[12].append(card)
        else:
            vals[val - 2].append(card)

    # Look for two pairs
    for i in reversed(range(13)):
        # First pair found
        if len(vals[i]) >= 2:
            temp = vals[i][0]
            # Look for second pair
            for j in reversed(range(i)):
                if len(vals[j]) >= 2:
                    return temp

    # Does not have 2 pairs
    return None


def straight(cards):
    """
    Look for a straight in the list of cards

    :param cards: a list of cards
    :return: the highest value card in the straight if found
    """

    # Sort cards by value
    sorted = []
    for i in range(14):
        sorted.append([])

    for card in cards:
        val = card.getValue()
        sorted[val - 1].append(card)
        # Add aces twice
        if val == 1:
            sorted[13].append(card)

    # Check for five in a row
    pos = 13
    while pos >= 4:
        temp = pos
        for i in range(5):
            # Not consecutive, update position
            if len(sorted[pos - i]) == 0:
                pos = pos - i - 1
                break

        # consecutive found
        if temp == pos:
            return sorted[pos][0]

    return None


def flush(cards):
    """
    Look of a flush in the list of cards

    :param cards: a list of cards
    :return: The highest value card in the flush
    """

    # Sort cards by suit
    suits = [[], [], [], []]
    for card in cards:
        suit = card.getSuit()
        if suit == "Spades":
            suits[0].append(card)
        elif suit == "Hearts":
            suits[1].append(card)
        elif suit == "Clubs":
            suits[2].append(card)
        elif suit == "Diamonds":
            suits[3].append(card)

    # Find 5 of the same suit
    for suit in suits:
        if len(suit) >= 5:
            # Return the highest value suit card
            return findHighest(suit)

    # No flush
    return None


def fullHouse(cards):
    """
    Look for a full house in the list of cards

    :param cards: a list of cards
    :return: the highest card of the triplet in the full house
    """
    # Look for three of a kind
    card = findRepeat(3, cards)
    if card is None:
        return None

    # Look for a pair
    newCards = []
    for c in cards:
        if c.getValue() != card.getValue():
            newCards.append(c)
    temp = findRepeat(2, newCards)

    if temp is None:
        return None
    else:
        return card


def straightFlush(cards):
    """
    Look for a straight flush in the list of cards

    :param cards: a list of cards
    :return: the highest value card in the straight flush
    """

    # Check for the suit
    card = flush(cards)
    if card is None:
        return None

    # Sort out cards with the suit
    suit = []
    for c in cards:
        if c.getSuit() == card.getSuit():
            suit.append(c)

    # Find straight and get highest value card
    return straight(suit)


def royalFlush(cards):
    """
    Look for a royal flush in the list of cards

    :param cards: a list of cards
    :return: return the ace  in the royal flush
    """

    # Check for straight flush
    card = straightFlush(cards)
    if card is None:
        return None

    if card.getValue() != 1:
        return None
    else:
        return card


def test():
    """
    Tests the check hand function
    """

    # Set up deck
    deck = Deck()
    deck.setDefault()
    deck.shuffle()

    # Draw random cards and simulate the game
    communityCards = []
    playerCards = []
    AICards = []

    for i in range(9):
        card = deck.draw()
        if i < 5:
            communityCards.append(card)
        elif i < 7:
            playerCards.append(card)
        else:
            AICards.append(card)

    # Display cards
    print("Testing...")
    print("Community Cards:")
    for card in communityCards:
        print(card)
    print("\nPlayer Cards:")
    for card in playerCards:
        print(card)
    print("\nAI Cards:")
    for card in AICards:
        print(card)

    # Show hands rank and highest card
    cards1 = communityCards + playerCards
    cards2 = communityCards + AICards

    rank1, card1 = checkHand(cards1)
    rank2, card2 = checkHand(cards2)

    print("\nPlayer hand rank:", rank1)
    print("Player best card:", card1)
    print("AI hand rank:", rank2)
    print("AI best card:", card2)


##
# Poker class
#  sets up and runs the poker game
class Poker:
    def __init__(self, width, height):
        """
        Set up pygame with given dimensions and initialize instance variables

        :param width: Width of the pygame window
        :param height: Length of the pygame window
        """

        # Set up pygame
        pygame.init()
        self._width = width
        self._height = height
        self._display = pygame.display.set_mode((self._width, self._height))
        self._clock = pygame.time.Clock()
        self._framesPerSecond = 30
        self._sprites = pygame.sprite.LayeredUpdates()
        self._ticks = 1
        pygame.key.set_repeat(1, 120)
        self._waitTime = 15

        # Set up cards
        self._deck = Deck()
        self._deck.setDefault()
        self._deck.shuffle()
        self._communityCards = Deck()
        self._playerCards = Deck()
        self._AICards = Deck()
        self._cardBacks = Deck()

        # Card info
        card = self._deck[0]
        cardWidth = card.getWidth()
        cardHeight = card.getHeight()

        # Set up community card positions (Based on card and window dimensions)
        self._communityCardPos = []
        tempX = (self._width - cardWidth * 5) // 2
        y = (self._height - cardHeight) // 2
        for i in range(5):
            x = tempX + cardWidth * i
            self._communityCardPos.append((x, y))

        # Set up player card positions
        self._playerCardPos = []
        x = (self._width - cardWidth * 2) // 2
        y = self._height // 4 * 3
        self._playerCardPos.append((x, y))
        self._playerCardPos.append((x + cardWidth, y))

        # Set up AI card positions
        self._AICardPos = []
        y = self._height // 4 - cardHeight
        self._AICardPos.append((x, y))
        self._AICardPos.append((x + cardWidth, y))

        # Set up Card back positions
        self._cardBacks.add(self._deck.getCardBack(), self._AICardPos[0])
        self._cardBacks.add(self._deck.getCardBack(), self._AICardPos[1])

        # 0 - title screen, 1 - setup screen, 2 - playing screen, 3 - round over screen
        self._gameState = 0

        # Set up buttons and input box
        x = self._width // 2
        y = self._height // 2
        self._playButton = Button(self._display, "Start Game", (x, y))

        x = (self._width - cardWidth * 5) // 5
        y = self._height // 2
        pad = self._height // 20
        self._checkButton = Button(self._display, "Check", (x, y))
        self._replayButton = Button(self._display, "Bet Again", (x, y))

        y -= self._checkButton.rect().h + pad
        self._raiseButton = Button(self._display, "Raise", (x, y))
        self._input = InputBox(self._display, 0, 0, 60, 25)
        self._input.setCenter((x, y - 30))

        y += 2 * (self._raiseButton.rect().h + pad)
        self._foldButton = Button(self._display, "Fold", (x, y))

        # Wage settings
        self._minWage = 20
        self._bank = 500
        self._pot = 0
        self._win = 0  # 0 - lost, 1 - win, 2 - draw

        # Set up text
        x = (self._width - cardWidth * 5) // 5
        y = self._height // 2 - self._replayButton.rect().h - 10
        self._winMessage = Text(self._display, "You win!", (x, y), "center")
        self._loseMessage = Text(self._display, "You lost...", (x, y), "center")
        self._drawMessage = Text(self._display, "Draw!", (x, y), "center")

        x = 5
        y = self._height - 30
        self._wagerText = Text(self._display, "Minimum wager: " + str(self._minWage), (x, y), "bottomleft", 14)

        y += 25
        self._bankText = Text(self._display, "bank: " + str(self._bank), (x, y), "bottomleft")

        x = self._width - 5
        self._potText = Text(self._display, "Pot: " + str(self._pot), (x, y), "bottomright")

    def mouseButtonDown(self, x, y):
        """
        Update game state when a button on the screen is pressed

        :param x: x coordinate of the mouse position
        :param y: y coordinate of the mouse position
        """

        # Start game
        if self._gameState == 0 and self._playButton.rect().collidepoint(x, y):
            # Update game state to setup
            self._gameState = 1
            self._ticks = 1

            # Update bank and pot
            self.wage(self._minWage)
        # One of three buttons are pressed during a round
        elif self._gameState == 2:
            # Fold and end round
            if self._foldButton.rect().collidepoint(x, y):
                self._pot = 0
                self._potText.setText("Pot: 0")
                # Round over
                self._gameState = 3
            elif self._checkButton.rect().collidepoint(x, y):
                # Update 4th or 5th community card
                if self._communityCards.size() < 5:
                    card = self._deck.draw()
                    pos = self._communityCardPos[self._communityCards.size()]
                    self._communityCards.add(card, pos)

                    self.add(card)
            elif self._raiseButton.rect().collidepoint(x, y):
                # Update pot if raised
                if self._raiseButton.rect().collidepoint(x, y):
                    wage = self._input.text()
                    # Validate input
                    if wage != "" and wage.isnumeric() and int(wage) <= self._bank:
                        self.wage(int(wage))
                        # Update 4th or 5th community card
                        if self._communityCards.size() < 5:
                            card = self._deck.draw()
                            pos = self._communityCardPos[self._communityCards.size()]
                            self._communityCards.add(card, pos)

                            self.add(card)
            # All community cards displayed
            if self._communityCards.size() == 5:
                # Show AI cards
                # remove card back sprites (not necessary)
                self._cardBacks[0].kill()
                self._cardBacks[1].kill()
                # Show cards
                self.add(self._AICards[0])
                self.add(self._AICards[1])

                # Determine winner and update bank
                playerScore, playerCard = checkHand((self._playerCards + self._communityCards).cards())
                AIScore, AICard = checkHand((self._AICards + self._communityCards).cards())

                self._win = 0
                # Win
                if playerScore > AIScore:
                    self._bank += self._pot
                    self._win = 1
                elif playerScore == AIScore:
                    # Same rank, win with better card
                    if playerCard > AICard:
                        self._bank += self._pot
                        self._win = 1
                    elif playerCard == AICard:
                        # Exact same cards, win with better hand
                        playerHand = findHighest(self._playerCards.cards())
                        AIHand = findHighest(self._AICards.cards())
                        if playerHand > AIHand:
                            self._bank += self._pot
                            self._win = 1
                        # Draw
                        elif playerHand.eq(AIHand):
                            self._bank += self._pot // 2
                            self._win = 2
                # Update bank info
                self._bankText.setText("Bank: " + str(self._bank))

                # Change game state to round over
                self._gameState = 3
        # Bet again when a round is over
        elif self._gameState == 3 and self._replayButton.rect().collidepoint(x, y):
            # Out of chips
            if self._bank <= self._minWage:
                return
            # Restart game, back to setup mode
            self._gameState = 1
            self._ticks = 1
            self._pot = 0
            # Update bank and pot
            self.wage(self._minWage)
            # Return cards to deck
            self._deck.merge(self._communityCards)
            self._deck.merge(self._playerCards)
            self._deck.merge(self._AICards)
            # Shuffle deck
            self._deck.shuffle()
            # Empty other piles
            self._communityCards.empty()
            self._playerCards.empty()
            self._AICards.empty()
            # Clear sprites
            self._sprites.empty()

    def wage(self, wage):
        """
        Update the pot and bank with given wage and update their texts

        :param wage: a wager that is <= to the bank
        """

        # Only wage if player have enough bank
        if self._bank >= wage:
            self._pot += 2 * wage
            self._bank -= wage
            self._potText.setText("Pot: " + str(self._pot))
            self._bankText.setText("Bank: " + str(self._bank))

    def update(self):
        """
        Update sprites and cards on the screen
        """

        # Deal initial cards during the setup phase
        if self._gameState == 1 and self._ticks % self._waitTime == 0:
            # Draw card
            card = self._deck.draw()

            # Add cards to the middle
            if self._communityCards.size() < 3:
                # Add card at coordinate
                pos = self._communityCardPos[self._communityCards.size()]
                self._communityCards.add(card, pos)

                # Add sprite
                self.add(card)
            # Add player cards
            elif self._playerCards.size() < 2:
                # Add card at coordinate
                pos = self._playerCardPos[self._playerCards.size()]
                self._playerCards.add(card, pos)

                # Add sprite
                self.add(card)
            # Add AI cards
            else:
                # Add card at coordinate
                pos = self._AICardPos[self._AICards.size()]
                self._AICards.add(card, pos)

                # Add card back sprite as placeholder
                self.add(self._cardBacks[self._AICards.size() - 1])

        # Update state to playing
        if self._gameState == 1 and self._deck.size() <= 45:
            self._gameState = 2

        # Update all sprites
        self._sprites.update()

    def draw(self):
        """
        Display all sprites on the pygame window
        """

        self._sprites.draw(self._display)

    def add(self, sprite):
        """
        Add a sprite to the sprite group

        :param sprite: A sprite object
        """

        self._sprites.add(sprite)

    def quit(self):
        """
        Quit the pygame window
        """

        pygame.quit()

    def run(self):
        """
        Runs the game
        """

        # # Test functions
        # test()
        # exit(1)

        # Run game
        while True:
            # Get events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouseButtonDown(event.pos[0], event.pos[1])

                if self._gameState == 2:
                    self._input.event(event)

            # Update everything
            self.update()
            GREEN = (53, 101, 77)
            self._display.fill(GREEN)

            # Show buttons & input box
            if self._gameState == 0:
                self._playButton.draw()
            elif self._gameState == 2:
                self._checkButton.draw()
                self._raiseButton.draw()
                self._foldButton.draw()
                self._input.draw()
            elif self._gameState == 3:
                self._replayButton.draw()

            # Show texts
            self._wagerText.draw()
            self._bankText.draw()
            self._potText.draw()
            if self._gameState == 3:
                if self._win == 0:
                    self._loseMessage.draw()
                elif self._win == 1:
                    self._winMessage.draw()
                else:
                    self._drawMessage.draw()

            self.draw()
            pygame.display.update()
            self._clock.tick(self._framesPerSecond)
            self._ticks += 1
