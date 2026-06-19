from Algorithms.datastructs.hash_table.bucket_hash_table import AllOne

class TestAllOne:
    def test_basic_inc_max_min(self):
        ao = AllOne()
        ao.inc("hello")
        ao.inc("hello")

        assert ao.getMaxKey() == "hello"
        assert ao.getMinKey() == "hello"

    def test_two_keys_different_counts(self):
        ao = AllOne()
        ao.inc("a")
        ao.inc("a")
        ao.inc("b")

        assert ao.getMaxKey() == "a"
        assert ao.getMinKey() == "b"

    def test_tie_any_valid(self):
        ao = AllOne()
        ao.inc("a")
        ao.inc("b")

        max_key = ao.getMaxKey()
        min_key = ao.getMinKey()

        assert max_key in {"a", "b"}
        assert min_key in {"a", "b"}

    def test_dec_to_remove(self):
        ao = AllOne()
        ao.inc("a")
        ao.dec("a")

        assert ao.getMaxKey() == ""
        assert ao.getMinKey() == ""

    def test_dec_rebalance(self):
        ao = AllOne()
        ao.inc("a")
        ao.inc("a")
        ao.inc("b")
        ao.inc("b")
        ao.inc("b")

        ao.dec("b")  # b becomes 2

        assert ao.getMaxKey() == "b"
        assert ao.getMinKey() == "b"

    def test_multiple_keys_complex(self):
        ao = AllOne()
        ops = [
            ("inc", "a"),
            ("inc", "b"),
            ("inc", "c"),
            ("inc", "a"),
            ("inc", "b"),
            ("dec", "a"),
            ("inc", "c"),
            ("inc", "c"),
        ]

        for op, key in ops:
            getattr(ao, op)(key)

        max_key = ao.getMaxKey()
        min_key = ao.getMinKey()

        # final counts:
        # a = 1
        # b = 2
        # c = 3
        assert max_key == "c"
        assert min_key == "a"

    def test_all_same_key(self):
        ao = AllOne()
        for _ in range(10):
            ao.inc("x")

        assert ao.getMaxKey() == "x"
        assert ao.getMinKey() == "x"

    def test_oscillation(self):
        ao = AllOne()
        ao.inc("a")
        ao.inc("b")
        ao.inc("a")
        ao.dec("a")
        ao.dec("b")

        # only "a" remains with count 1
        assert ao.getMaxKey() == "a"
        assert ao.getMinKey() == "a"

    def test_empty_after_many_ops(self):
        ao = AllOne()
        ao.inc("a")
        ao.inc("b")
        ao.dec("a")
        ao.dec("b")

        assert ao.getMaxKey() == ""
        assert ao.getMinKey() == ""

    def test_interleaved_growth(self):
        ao = AllOne()
        ao.inc("a")
        ao.inc("b")
        ao.inc("c")
        ao.inc("b")
        ao.inc("b")
        ao.inc("c")

        # a=1, b=3, c=2
        assert ao.getMaxKey() == "b"
        assert ao.getMinKey() == "a"