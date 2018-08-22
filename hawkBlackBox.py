#!/usr/bin/env python3

import random
import sys


class Type:
    S = 'Scope'
    G = 'Generator'
    A = 'Armor'

    @classmethod
    def get_random(cls):
        return [cls.S, cls.G, cls.A][random.randint(0, 2)]


class Rank:
    C = 1
    B = 2
    A = 3
    S = 4

    @classmethod
    def get_random(cls):
        return random.randint(1, 4)

    @classmethod
    def verbose(cls, rank):
        return {Rank.C: 'C', Rank.B: 'B', Rank.A: 'A', Rank.S: 'S'}.get(rank)


class Device:
    def __init__(self, rank=None, type=None, stars=0):
        self.rank = rank or Rank.get_random()
        self.type = type or Type.get_random()
        self.stars = stars

    def __str__(self):
        return '%s-rank %s-star %s device' % (
            Rank.verbose(self.rank),
            self.stars, self.type
        )

    def __lt__(self, other):
        print(self.rank, other.rank)
        if self.rank == other.rank:
            if self.stars < other.stars:
                return True
        elif self.rank < other.rank:
            return True
        return False

    def __le__(self, other):
        if self.rank == other.rank:
            if self.stars <= other.stars:
                return True
        elif self.rank < other.rank:
            return True
        return False

    def __eq__(self, other):
        if self.rank == other.rank and self.stars == other.stars:
            return True
        return False

    def __ne__(self, other):
        if self.rank != other.rank or self.stars != other.stars:
            return True
        return False

    def __gt__(self, other):
        if self.rank == other.rank:
            if self.stars > other.stars:
                return True
        elif self.rank > other.rank:
            return True
        return False

    def __ge__(self, other):
        if self.rank == other.rank:
            if self.stars >= other.stars:
                return True
        elif self.rank > other.rank:
            return True
        return False


class Stock(list):
    def pop_device(self, rank=None, type=None, stars=None):
        return self.pop()

    def show(self):
        if self:
            for device in self:
                print(device)
        else:
            print('No devices')


class Probability:
    def __init__(self, c=0, b=0, a=0, s=0, extra=None, extra_cost=0):
        self.ranks = (
            (Rank.C, c),
            (Rank.B, b + c),
            (Rank.A, a + b + c),
            (Rank.S, s + a + b + c)
        )
        if extra:
            ec, eb, ea, es = extra
            self.extra_ranks = (
                (Rank.C, ec),
                (Rank.B, eb + ec),
                (Rank.A, ea + eb + ec),
                (Rank.S, es + ea + eb + ec)
            )
            self.extra_cost = extra_cost

    def get_rank(self, value, extra=False):
        ranks = self.extra_ranks if extra else self.ranks
        for rank in self.ranks:
            if value <= rank[1]:
                return rank[0]
        raise ValueError(str(value))


class Stabilizer:
    def __init__(self, level, probabilities):
        self.level = level
        self.probabilities = probabilities

    def __str__(self):
        return 'Stabilizer level ' + str(self.level)

    def get_probabilities(self, d1, d2, d3, d4):
        ranks = {Rank.C: 0, Rank.B: 0, Rank.A: 0, Rank.S: 0}
        ranks[d1.rank] += 1
        ranks[d2.rank] += 1
        ranks[d3.rank] += 1
        ranks[d4.rank] += 1
        return self.probabilities.get(
            (ranks[Rank.C], ranks[Rank.B], ranks[Rank.A], ranks[Rank.S])
        )


stabilizer0 = Stabilizer(0, {
    (4, 0, 0, 0): Probability(50, 50, 0, 0,   (0, 92, 8, 0),   46),
    (3, 1, 0, 0): Probability(39, 52, 8, 0,   (0, 75, 18, 7),  78),   # missing 1
    (3, 0, 1, 0): Probability(41, 40, 13, 6,  (0, 60, 25, 15), 96),   # guessed 41
    (3, 0, 0, 1): Probability(43, 43, 0, 14,  (0, 71, 8, 21),  123),
    (2, 2, 0, 0): Probability(27, 55, 17, 1,  (0, 67, 26, 7),  112),  # guessed 27
    (2, 1, 1, 0): Probability(29, 42, 23, 6,  (0, 54, 32, 14), 127),  # guessed 29
    (2, 1, 0, 1): Probability(30, 45, 10, 15, (0, 58, 18, 24), 154),  # guessed 30
    (2, 0, 2, 0): Probability(30, 29, 29, 12, (0, 40, 40, 21), 146),  # guessed 30, extra 1
    (2, 0, 1, 1): Probability(31, 31, 16, 22, (0, 43, 25, 32), 173),  # guessed first 31
    (2, 0, 0, 2): Probability(33, 33, 0, 33,  (0, 50, 8, 42),  196),  # missing 1
    (1, 3, 0, 0): Probability(15, 57, 27, 1,  (0, 61, 32, 7),  143),  # guessed 15
    (1, 2, 1, 0): Probability(15, 44, 34, 7,  (0, 49, 38, 13), 162),  # guessed 15
    (1, 2, 0, 1): Probability(16, 47, 20, 17, (0, 52, 26, 22), 185),  # guessed 16
    (1, 1, 2, 0): Probability(15, 31, 40, 14, (0, 36, 45, 19), 177),  # guessed 15
    (1, 1, 1, 1): Probability(16, 33, 27, 24, (0, 38, 32, 29), 204),  # guessed 16, missing 1
    (1, 1, 0, 2): Probability(18, 35, 11, 36, (0, 41, 18, 41), 227),  # guessed 18
    (1, 0, 3, 0): Probability(16, 16, 48, 20, (0, 22, 52, 26), 196),  # guessed first 16
    (1, 0, 2, 1): Probability(17, 17, 34, 32, (0, 23, 40, 37), 223),  # guessed first 17
    (1, 0, 1, 2): Probability(19, 18, 18, 45, (0, 25, 25, 50), 246),  # guessed 19
    (1, 0, 0, 3): Probability(20, 20, 0, 60,  (0, 29, 8, 62),  270),  # extra 1 with extra
    (0, 4, 0, 0): Probability(0, 60, 38, 2,   (0, 18, 69, 14), 173),
    (0, 3, 1, 0): Probability(0, 47, 45, 8,   (0, 0, 76, 24),  193),
    (0, 3, 0, 1): Probability(0, 50, 32, 18,  (0, 0, 56, 44),  216),
    (0, 2, 2, 0): Probability(0, 32, 53, 15,  (0, 0, 71, 29),  208),
    (0, 2, 1, 1): Probability(0, 35, 40, 26,  (0, 0, 55, 45),  235),  # extra 1
    (0, 2, 0, 2): Probability(0, 37, 24, 39,  (0, 0, 34, 66),  258),
    (0, 1, 3, 0): Probability(0, 17, 61, 22,  (0, 0, 68, 32),  227),
    (0, 1, 2, 1): Probability(0, 18, 48, 34,  (0, 0, 54, 46),  254),
    (0, 1, 1, 2): Probability(0, 20, 32, 48,  (0, 0, 36, 64),  277),
    (0, 1, 0, 3): Probability(0, 21, 14, 65,  (0, 0, 16, 84),  300),
    (0, 0, 4, 0): Probability(0, 0, 70, 30,   (0, 0, 40, 60),  246),
    (0, 0, 3, 1): Probability(0, 0, 57, 43,   (0, 0, 6, 94),   273),
    (0, 0, 2, 2): Probability(0, 0, 41, 59,   (0, 0, 0, 100),  296),
    (0, 0, 1, 3): Probability(0, 0, 23, 77,   (0, 0, 0, 100),  320),
    (0, 0, 0, 4): Probability(0, 0, 0, 100,   (0, 0, 0, 100),  343),
})


Stabilizers = {
    0: stabilizer0,
}


def get_stabilizer(level):
    try:
        return Stabilizers[level]
    except KeyError:
        raise ValueError('Sorry, the stabilizer level %d is not yet available' % level)


class Combiner:
    def __init__(self, stabilizer):
        self.stabilizer = stabilizer

    def get_random_value(self):
        return random.randint(1, 100)

    def get_new_type(self, d1, d2, d3, d4):
        if d1.type == d2.type == d3.type == d4.type:
            return d1.type
        # TODO: if 2 armor and 2 scope, 50% chance armor and 50% chance scope?
        return Type.get_random()

    def combine(self, d1, d2, d3, d4):
        best_device = max(d1, d2, d3, d4)

        probabilities = self.stabilizer.get_probabilities(d1, d2, d3, d4)
        value = self.get_random_value()
        new_rank = probabilities.get_rank(value)

        # Algorithm here. Fix when necessary.
        if new_rank <= best_device.rank:
            # Device's Rank was not upgraded (same or downgraded)

            # Number of stars is best device's stars + 1
            # For example:
            # 1-star B + 3x0-star B => 2-star B
            # 2-star B + 3x0-star C => 3-star C
            new_stars = best_device.stars + 1

            # If 5-stars and Rank lower than S (C, B or A), upgrade Rank, 0 stars
            # Some people say there are 50/50 chance of getting 0/1 star when upgrading
            # I did not implement this behavior here: we always upgrade with 0-star
            if new_stars == 5 and new_rank < Rank.S:
                new_rank += 1
                new_stars = 0
        else:
            # Device's Rank was upgraded (yay!): always 1-star
            new_stars = 1

        new_type = self.get_new_type(d1, d2, d3, d4)
        return Device(rank=new_rank, stars=new_stars, type=new_type)


class Strategy:
    code = ''
    name = ''
    description = ''

    def __init__(self, stabilizer, *args, **kwargs):
        if isinstance(stabilizer, str):
            stabilizer = int(stabilizer)

        if isinstance(stabilizer, int):
            try:
                self.stabilizer = get_stabilizer(stabilizer)
            except ValueError as e:
                print(str(e), file=sys.stderr)
                print('No stabilizer, aborting strategy', file=sys.stderr)
                return
        elif isinstance(stabilizer, Stabilizer):
            self.stabilizer = stabilizer
        else:
            print('Invalid stabilizer (%s:%s), aborting strategy' % (
                str(stabilizer), type(stabilizer)
            ), file=sys.stderr)
            return

        self.run(*args, **kwargs)

    def __str__(self):
        return '%s: %s\n%s' % (self.code, self.name, self.description)

    @classmethod
    def get_help(cls):
        return '%s: %s\n%s' % (cls.code, cls.name, cls.description)



class BtoS(Strategy):
    code = 'BtoS'
    name = 'From Rank B to Rank S, Same Rank / Random Type combinations'
    description = """
    This strategy always combines devices with the same Rank: 4xB, 4xA
    or 4xS. It does not take the type device's into account (they are
    picked randomly). It starts at Rank B and goes up to Rank S. It does
    not try to maximize the number of stars for the final S-Rank devices.

    Usage:
        ./hawkBlackBox.py  BtoS  stabilizer_level  number_of_green_devices_to_start_with

    Example:
        ./hawkBlackBox.py  BtoS  0  100000
    """

    def run(self, n_B_devices):
        n_B_devices = int(n_B_devices)

        print('Running "%s" strategy\nWith %s and %d B-rank devices' % (
            self.name, self.stabilizer, n_B_devices))
        print('')

        combinations = 0
        B_stock = Stock(Device(rank=Rank.B) for _ in range(n_B_devices))

        A0_stock = Stock()
        A1_stock = Stock()
        S0_stock = Stock()
        S1_stock = Stock()

        combiner = Combiner(self.stabilizer)

        base_device = B_stock.pop_device()
        while len(B_stock) >= 3:
            combinations += 1
            base_device = combiner.combine(
                base_device,
                B_stock.pop_device(),
                B_stock.pop_device(),
                B_stock.pop_device()
            )

            if base_device.rank > Rank.B:

                if base_device.rank == Rank.A:
                    if base_device.stars == 0:
                        A0_stock.append(base_device)
                    else:
                        A1_stock.append(base_device)
                elif base_device.rank == Rank.S:
                    if base_device.stars == 0:
                        S0_stock.append(base_device)
                    else:
                        S1_stock.append(base_device)

                if B_stock:
                    base_device = B_stock.pop_device()


        a0_obtained_phase1 = len(A0_stock)
        a1_obtained_phase1 = len(A1_stock)
        s1_obtained_phase1 = len(S1_stock)

        base_device = A1_stock.pop_device()
        while len(A0_stock) >= 3:
            combinations += 1
            base_device = combiner.combine(
                base_device,
                A0_stock.pop_device(),
                A0_stock.pop_device(),
                A0_stock.pop_device()
            )

            if base_device.rank == Rank.S:
                if base_device.stars == 0:
                    S0_stock.append(base_device)
                else:
                    S1_stock.append(base_device)

                if A1_stock:
                    base_device = A1_stock.pop_device()

        while len(A1_stock) >= 3:
            combinations += 1
            base_device = combiner.combine(
                base_device,
                A1_stock.pop_device(),
                A1_stock.pop_device(),
                A1_stock.pop_device()
            )

            if base_device.rank == Rank.S:
                if base_device.stars == 0:
                    S0_stock.append(base_device)
                else:
                    S1_stock.append(base_device)

                if A1_stock:
                    base_device = A1_stock.pop_device()

        print('Results phase 1')
        print('---------------')
        print('A-rank 0-star devices obtained: %d' % a0_obtained_phase1)
        print('A-rank 1-star devices obtained: %d' % a1_obtained_phase1)
        print('S-rank 1-star devices obtained: %d' % s1_obtained_phase1)
        print('')
        print('B-rank devices left:')
        B_stock.show()
        print('')

        print('Results phase 2')
        print('---------------')
        print('S-rank 0-star devices obtained: %d' % len(S0_stock))
        print('S-rank 1-star devices obtained: %d (total: %d)' % ((len(S1_stock) - s1_obtained_phase1), len(S1_stock)))
        print('')
        print('A-rank devices left:')
        A0_stock.extend(A1_stock)
        A0_stock.show()
        print('')

        print('Statistics')
        print('----------')
        print('B-rank devices used: %d' % (n_B_devices - len(B_stock)))
        print('Total combinations done: %d' % combinations)
        print('Average number of B-rank devices to get an S-rank device: %0.2f' % ((n_B_devices - len(B_stock)) / (len(S0_stock) + len(S1_stock))))



Strategies = {
    BtoS.code: BtoS,
    BtoS.code: BtoS,
}


if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            strategy = Strategies[sys.argv[1]]
            try:
                strategy(*sys.argv[2:])
            except TypeError as e:
                print(str(e))
                sys.exit(1)
            sys.exit(0)
        except KeyError:
            print('No such strategy\n', file=sys.stderr)

    print('AVAILABLE STRATEGIES')
    print('============================================')
    print('\n--------------------------------------------\n'.join(
        s.get_help() for s in sorted(Strategies.values(), key=lambda s: s.name)))
