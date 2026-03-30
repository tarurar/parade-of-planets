from parade.resonance import generate_resonance_pattern


class TestResonancePattern:
    def test_returns_list_of_correct_length_31(self):
        pattern = generate_resonance_pattern(b"\x00" * 32, 31)
        assert len(pattern) == 31

    def test_returns_list_of_correct_length_28(self):
        pattern = generate_resonance_pattern(b"\x00" * 32, 28)
        assert len(pattern) == 28

    def test_contains_all_days_exactly_once(self):
        pattern = generate_resonance_pattern(b"\x00" * 32, 31)
        assert sorted(pattern) == list(range(1, 32))

    def test_deterministic_same_seed(self):
        seed = b"\xab" * 32
        p1 = generate_resonance_pattern(seed, 31)
        p2 = generate_resonance_pattern(seed, 31)
        assert p1 == p2

    def test_different_seed_different_pattern(self):
        p1 = generate_resonance_pattern(b"\x00" * 32, 31)
        p2 = generate_resonance_pattern(b"\xff" * 32, 31)
        assert p1 != p2

    def test_is_a_permutation_not_identity(self):
        pattern = generate_resonance_pattern(b"\xab" * 32, 31)
        assert pattern != list(range(1, 32))

    def test_all_month_lengths(self):
        seed = b"\x42" * 32
        for days in (28, 29, 30, 31):
            pattern = generate_resonance_pattern(seed, days)
            assert len(pattern) == days
            assert sorted(pattern) == list(range(1, days + 1))

    def test_february_28_has_27_usable_positions(self):
        pattern = generate_resonance_pattern(b"\x00" * 32, 28)
        assert len(pattern) >= 27
