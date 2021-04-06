import random
import time
import argparse

random.seed(0)


class Die:
    def __init__(self):
        self.roll()

    def roll(self):
        self.face = random.randint(1, 6)
        return self.face


class Player:
    def __init__(self, name):
        self.name = name
        self.player_type = None
        self.score = 0
        self.die = Die()

    def getType(self):
        return self.player_type

class HumanPlayer(Player):
    def decide(self):
        turn_score = 0
        decision = "r"

        while decision == "r":
            self.die.roll()
            roll = self.die.face
            if roll == 1:
                turn_score = 0
                current_total_score = self.score + turn_score
                print("{} rolled a 1. Your score for this turn is 0. Your total score for the game is {}".format(self.name, current_total_score))
                decision = "h"
            else:
                turn_score = turn_score + roll
                current_total_score = self.score + turn_score
                print("{} rolled a {}. Your current score for this turn is {}.  Your total score for the game is {}.".format(self.name, roll, turn_score, current_total_score))
                if current_total_score >= 100:
                    break
                else:
                    decision = input("Roll again or hold? Please enter r to roll again or h to hold.")
        self.score += turn_score

class ComputerPlayer(Player):
    def decide(self):
        turn_score = 0
        decision = "r"

        while decision == "r":
            self.die.roll()
            roll = self.die.face
            if roll == 1:
                turn_score = 0
                current_total_score = self.score + turn_score
                print("{} rolled a 1. Your score for this turn is 0. Your total score for the game is {}".format(self.name, current_total_score))
                decision = "h"
            else:
                turn_score = turn_score + roll
                current_total_score = self.score + turn_score
                print("{} rolled a {}. Your current score for this turn is {}.  Your total score for the game is {}.".format(self.name, roll, turn_score, current_total_score))
                if current_total_score >= 100:
                    break
                else:
                    limit_one = 25
                    limit_two = 100 - current_total_score
                    if limit_one < limit_two:
                        hold_limit = limit_one
                    else:
                        hold_limit = limit_two
                    if current_total_score < hold_limit:
                        decision = "r"
                    else:
                        decision = "h"
        self.score += turn_score


class PlayerFactory:
    def getPlayer(self, name, player_type):
        if player_type == "human":
            return HumanPlayer(name)
        elif player_type == "computer":
            return ComputerPlayer(name)


class Game:
    def __init__(self, player_one, player_two):
        self.die = Die()
        #Not sure if there's a way to get argument for player type to be used here so they're set manually to computer
        self.player_one = PlayerFactory.getPlayer(self,"Player 1", "computer")
        self.player_two = PlayerFactory.getPlayer(self, "Player 2", "computer")

    def play(self):
        while self.player_one.score < 100 and self.player_two.score < 100:
            self.player_one.decide()
            if self.player_one.score < 100:
                self.player_two.decide()
        if self.player_one.score >= 100:
            print("Player 1 wins! Game over.")
        elif self.player_two.score >= 100:
            print("Player 2 wins! Game over.")


class TimedGameProxy(Game):
    def __init__(self, player_one, player_two):
        #Not sure if there's a way to get argument for player type to be used here so they're set manually to computer
        self.player_one = PlayerFactory.getPlayer(self,"Player 1", "computer")
        self.player_two = PlayerFactory.getPlayer(self, "Player 2", "computer")
        self.start_time = time.time()

    def game_timer(self):
        if time.time() - self.start_time >= 60:
            if self.player_one.score > self.player_two.score:
                print("Time is up. Player 1 wins.")
            else:
                print("Time is up. Player 2 wins.")
        else:
            time_elapsed = time.time() - self.start_time
            time_remaining = 60 - time_elapsed
            print("There are still {} seconds remaining. Continue playing!").format(time_remaining)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--player1", type=str, help="Choose player type: human or computer", required=True)
    parser.add_argument("--player2", type=str, help="Choose player type: human or computer", required=True)
    parser.add_argument("--timed", type=str, help="Choose yes or no for timed game", required=False)
    args = parser.parse_args()

    factory = PlayerFactory()
    player_one = factory.getPlayer("Player 1", args.player1)
    player_two = factory.getPlayer("Player 2", args.player2)

    if args.timed:
        game = TimedGameProxy(player_one, player_two)
        game.play()
    else:
        game = Game("Player 1", "Player 2")
        game.play()


if __name__ == "__main__":
    main()
