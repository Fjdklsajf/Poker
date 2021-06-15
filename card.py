import pygame


##
# ImageSprite class (inherits pygame.sprite.Sprite)
#  update sprite with image file
class ImageSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        """
        Initialize the image sprite with given coordinate and image file

        :param x: x coordinate of the top-left corner for the image
        :param y: y coordinate of the top-left corner for the image
        :param filename: image file name
        """

        super().__init__()
        self.loadImage(x, y, filename)

    def loadImage(self, x, y, filename):
        """
        Load image at the x,y coordinate

        :param x: x coordinate of the top-left corner for the image
        :param y: y coordinate of the top-left corner for the image
        :param filename: image file name
        """

        img = pygame.image.load(filename).convert()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - self.rect.height

    def moveBy(self, dx, dy):
        """
        Move the sprite by dx and dy

        :param dx: Number of pixels in the x direction
        :param dy: Number of pixels in the y direction
        """
        self.rect.x += dx
        self.rect.y += dy


##
# Card class (inherits ImageSprite)
#  A card sprite
class Card(ImageSprite):
    def __init__(self, suit, value, filename="", x=0, y=0):
        """
        initiate a card sprite with given parameters

        :param suit: suit of the card (s, h, c, d)
        :param value: value of the card (1 ~ 13)
        :param x: x coordinate of the top-left corner for the image
        :param y: y coordinate of the top-left corner for the image
        """

        self._suit = suit[0].lower()
        self._value = value
        if filename == "":
            self._filename = str(value) + self._suit + ".gif"
        else:
            self._filename = filename
        super().__init__(x, y, self._filename)

    def getSuit(self):
        """
        Get suit in its full form

        :return: string of suit
        """

        if self._suit == 's':
            return "Spades"
        elif self._suit == 'h':
            return "Hearts"
        elif self._suit == 'c':
            return "Clubs"
        elif self._suit == 'd':
            return "Diamonds"
        else:
            return ""

    def getValue(self):
        """
        get card value

        :return: int - card value
        """
        return self._value

    def getFilename(self):
        """
        get card sprite file name

        :return: string - file name
        """

        return self._filename

    def getWidth(self):
        """
        get card sprite width

        :return: int - card sprite width
        """

        return self.rect.width

    def getHeight(self):
        """
        get card sprite height

        :return: int - card sprite height
        """

        return self.rect.height

    def move(self, x, y):
        """
        move coordinate of card sprite

        :param x: x coordinate of the top-left corner for the image
        :param y: y coordinate of the top-left corner for the image
        """

        self.rect.x = x
        self.rect.y = y

    def getX(self):
        """
        Get the sprite x location

        :return: x coordinate of the card sprite
        """

        return self.rect.x

    def getY(self):
        """
        Get the sprite y location

        :return: y coordinate of the card sprite
        """

        return self.rect.y

    def __gt__(self, card):
        """
        self > card if the value is greater

        :param card: a card object
        :return: True or False
        """

        # Get greater card value
        if self._value == 1 and card.getValue() != 1:
            return True
        elif card.getValue() == 1 and self._value != 1:
            return False

        return self._value > card.getValue()

    def __lt__(self, card):
        """
        self < card if the value is less

        :param card: a card object
        :return: True or False
        """

        if card.getValue() == 1 and self._value != 1:
            return True
        elif self._value == 1 and card.getValue() != 1:
            return False

        return self._value < card.getValue()

    def eq(self, card):
        """
        Check if the card values are equal

        :param card: a card object
        :return: True or false
        """
        return card.getValue() == self._value

    def __repr__(self):
        """
        Get return string for the class

        :return: string - [value] of [suit]
        """

        if self._value == 1:
            val = "Ace"
        elif self._value == 11:
            val = "Jack"
        elif self._value == 12:
            val = "Queen"
        elif self._value == 13:
            val = "King"
        else:
            val = str(self._value)

        return val + " of " + self.getSuit()
