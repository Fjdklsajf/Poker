from poker import Poker


def main():
    # Set up game
    WIDTH = 600
    HEIGHT = 400
    game = Poker(WIDTH, HEIGHT)

    # Play game
    game.run()


if __name__ == "__main__":
    main()
