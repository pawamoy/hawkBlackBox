import unittest

from hawkBlackBox import Combiner, Device, Rank, Type, stabilizer0, Probability


class TestCombiner(unittest.TestCase):
    def setUp(self):
        self.combiner = Combiner(stabilizer0)

    def test_devices_comparison(self):
        assert Device(rank=Rank.S, stars=2) < Device(rank=Rank.S, stars=3)

        assert Device(rank=Rank.C, stars=4) < Device(rank=Rank.B, stars=0)
        assert Device(rank=Rank.C, stars=4) <= Device(rank=Rank.A, stars=0)
        assert Device(rank=Rank.C, stars=4) <= Device(rank=Rank.C, stars=4)
        assert Device(rank=Rank.C, stars=4) < Device(rank=Rank.S, stars=0)
        assert Device(rank=Rank.B, stars=4) < Device(rank=Rank.A, stars=0)
        assert Device(rank=Rank.B, stars=4) < Device(rank=Rank.S, stars=0)
        assert Device(rank=Rank.A, stars=4) < Device(rank=Rank.S, stars=0)

        assert Device(rank=Rank.S, stars=0) > Device(rank=Rank.A, stars=4)
        assert Device(rank=Rank.S, stars=0) >= Device(rank=Rank.S, stars=0)

        assert Device(rank=Rank.A, stars=2, type=Type.S) == Device(rank=Rank.A, stars=2, type=Type.A)
        assert Device(rank=Rank.A, stars=2, type=Type.S) != Device(rank=Rank.C, stars=2, type=Type.S)

    def test_best_device(self):
        d1 = Device(rank=Rank.B, stars=1)
        d2 = Device(rank=Rank.B, stars=0)

        assert max(d1, d2) == d1

        d1.stars += 1
        d2.stars += 1

        assert max(d1, d2) == d1

        d1.rank += 1
        d2.stars += 1

        assert max(d1, d2) == d1

        d2.stars += 1

        assert max(d1, d2) == d1

    def test_star_increase(self):
        d2 = Device(rank=Rank.B, stars=0)
        d3 = Device(rank=Rank.B, stars=0)
        d4 = Device(rank=Rank.B, stars=0)

        self.combiner.stabilizer.probabilities[(0, 4, 0, 0)] = Probability(0, 100, 0, 0)

        for stars in (0, 1, 2, 3):
            print(d2.stars, d3.stars, d4.stars)
            assert self.combiner.combine(
                Device(rank=Rank.B, stars=stars), d2, d3, d4
            ).stars == stars + 1

        new_device = self.combiner.combine(
            Device(rank=Rank.B, stars=4), d2, d3, d4)
        assert new_device.stars == 0
        assert new_device.rank == Rank.A

    def test_probability_rank(self):
        p = Probability(10, 25, 50, 15)

        assert p.get_rank(0) == Rank.C
        assert p.get_rank(5) == Rank.C
        assert p.get_rank(10) == Rank.C
        assert p.get_rank(11) == Rank.B
        assert p.get_rank(35) == Rank.B
        assert p.get_rank(40) == Rank.A
        assert p.get_rank(84) == Rank.A
        assert p.get_rank(85) == Rank.A
        assert p.get_rank(86) == Rank.S
        assert p.get_rank(100) == Rank.S

    def test_stabilizer_probabilities(self):
        assert self.combiner.stabilizer.get_probabilities(
            *[Device(rank=Rank.B)] * 4
        ) == self.combiner.stabilizer.probabilities[(0, 4, 0, 0)]
        assert self.combiner.stabilizer.get_probabilities(
            *[Device(rank=Rank.B)] * 2, Device(rank=Rank.A), Device(rank=Rank.S)
        ) == self.combiner.stabilizer.probabilities[(0, 2, 1, 1)]

    def tearDown(self):
        del self.combiner
