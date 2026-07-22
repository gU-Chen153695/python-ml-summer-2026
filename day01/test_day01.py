from python_basics import analyze_numbers, create_batches, count_words, unique_keep_order

assert analyze_numbers([])["count"] == 0
assert analyze_numbers([1, 1, 2])["unique_count"] == 2

assert count_words("") == {}
assert count_words("!!!!@#") == {}
assert count_words("Python python.")["python"] == 2

assert unique_keep_order([]) == []
assert unique_keep_order([1, 1, 2, 1]) == [1, 2]

assert create_batches([], 3) == []
assert create_batches([1, 2, 3, 4, 5, 6], 3) == [[1, 2, 3], [4, 5, 6]]
assert create_batches([1, 2, 3, 4], 3) == [[1, 2, 3], [4]]
try:
    create_batches([1, 2], 0)
    assert False
except ValueError:
    pass
print("All Day 1 tests passed.")