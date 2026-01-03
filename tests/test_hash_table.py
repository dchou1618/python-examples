from Algorithms.datastructs.hash_table import RandomizedSet

def test_randomized_set():
    rs = RandomizedSet()

    # Insert 0, should return True
    assert rs.insert(0) == True
    # Remove 0, should return True
    assert rs.remove(0) == True
    # Remove 0 again, should return False (already removed)
    assert rs.remove(0) == False
    # Insert 0 again, should return True
    assert rs.insert(0) == True
    # getRandom should return 0 (only element)
    assert rs.getRandom() == 0
    # Remove 0, should return True
    assert rs.remove(0) == True
    # Insert -1, should return True
    assert rs.insert(-1) == True
    # Remove 0 (not present), should return False
    assert rs.remove(0) == False

    # Multiple getRandom calls — since only -1 is present, it should always return -1
    for _ in range(10):
        val = rs.getRandom()
        assert val == -1, f"Expected -1 but got {val}"

    # Remove -1, should return True
    assert rs.remove(-1) == True
    # Now getRandom on empty set — handle gracefully by catching exception or custom behavior
    try:
        rs.getRandom()
        print("getRandom on empty set did not raise error — consider adding handling for empty set.")
    except IndexError:
        print("getRandom on empty set raised IndexError as expected.")

    print("All tests passed!")

if __name__ == "__main__":
    test_randomized_set()