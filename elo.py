from random import randint, choice
import sys

INITIAL_SCORE = 1000
MAX_INCREASE = 50

class Player(object):

    def __init__(self, id, rating):
        self.id = id
        self.rating = rating
        self.wins = 0
        self.matches = 0

    def won(self, rating):
        self.matches += 1
        self.wins += 1
        self.rating += rating

    def lost(self, rating):
        self.matches += 1
        self.rating -= rating

    def __repr__(self):
        if self.matches:
            perc = float(self.wins) / float(self.matches) * 100
        else:
            perc = 0.0

        return 'Player: %2i (%4i) W:%3i L:%3i Games:%3i Perc:%2.1f %%' % (
            self.id,
            self.rating,
            self.wins,
            self.matches - self.wins,
            self.matches,
            perc,
        )

    def __eq__(self, other):
        return self.id == other.id


class Match(object):

    def __init__(self, player1, player2, score1, score2):
        self.player1 = player1
        self.player2 = player2
        self.score1 = score1
        self.score2 = score2

    def get_match_results(self):
        """returns winner, loser"""
        if self.score1 > self.score2:
            return self.player1, self.player2
        else:
            return self.player2, self.player1


class Elo(object):

    def __init__(self, players):
        self.players = players

    def calculate_rating(self, loser_rating, winner_rating):
        """returns new_rating based off participate's previous ratings"""
        return int(MAX_INCREASE * 1 / (1 + 10 ** (
            (winner_rating - loser_rating) / 400)))

    def update_players(self, match):
        winner, loser = match.get_match_results()
        calc_rating = self.calculate_rating(
            loser_rating=loser.rating,
            winner_rating=winner.rating,
        )
        winner.won(calc_rating)
        loser.lost(calc_rating)
        return winner, loser

    def print_ranks(self):
        """prints current players ranks and stats for testing"""
        print
        sorted_players = sorted(self.players, key=lambda a: a.rating)
        for player in reversed(sorted_players):
            print player

    def find_closely_rated_opponent(self, player):
        """find an opponent with a rating close to player"""
        rating_diff = sys.maxint
        best_choice = None
        for p in self.players:
            # skip player for which we're choosing opponent
            if p == player:
                continue

            current_diff = abs(p.rating - player.rating)
            # if the rating are the same, it's the best choice
            if current_diff == 0:
                return p

            # if opponent has a lower rating diff, it's the current best choice
            if current_diff < rating_diff:
                rating_diff = current_diff
                best_choice = p

        return best_choice


    def test_match(self):
        """creates fake matches for testing"""
        p1 = p2 = choice(self.players)
        p2 = self.find_closely_rated_opponent(p1)

        # if the scores are the same, assume p2 wins for testing
        m = Match(
            player1=p1,
            player2=p2,
            score1=randint(0,100),
            score2=randint(0,100),
        )
        print '...', p1
        print '......vs'
        print '...', p2
        print 'BEFORE: Player: %3i (%5i) ....Player: %3i (%5i)' % (
            p1.id, p1.rating,
            p2.id, p2.rating,
        )
        winner, loser = self.update_players(match=m)

        print 'AFTER: Player: %3i (%5i) ....Player: %3i (%5i)' % (
            winner.id, winner.rating,
            loser.id, loser.rating,
        )

def main():
    players = [Player(p, INITIAL_SCORE) for p in xrange(20)]
    elo = Elo(players)
    while True:
        elo.test_match()
        elo.print_ranks()
        raw_input()

if __name__ == '__main__':
    main()

