"""LeetCode 242: Valid Anagram

本练习约束：
- 1 <= len(s), len(t) <= 50_000
- s 和 t 只包含小写英文字母
- 禁止使用 collections.Counter
- 必须完成排序法和手写字典计数法
"""


def is_anagram_sorting(s: str, t: str) -> bool:
    """排序法。

    要求写明：
    Time: O(n log n)
    Space: 说明 sorted() 会创建新列表
    """
    # TODO
    array1 = sorted(s)
    array2 = sorted(t)
    if array1 == array2:
        return True
    else:
        return False
    raise NotImplementedError


def is_anagram_dict(s: str, t: str) -> bool:
    """手写字典计数法。

    要求：
    - 平均时间复杂度 O(n)
    - 空间复杂度 O(k)，k 为不同字符数量
    - 禁止使用 Counter
    """
    # TODO
    if len(s) != len(t):
        return False
    temp = dict()
    for element in s:
        temp[element] = temp.get(element, 0) + 1
    for element in t:
        if element in temp and temp[element] > 0:
            temp[element] -= 1
        else:
            return False
    return True
    raise NotImplementedError


if __name__ == "__main__":
    cases = [
        ("anagram", "nagaram", True),
        ("rat", "car", False),
        ("a", "a", True),
        ("ab", "a", False),
        ("aacc", "ccac", False),
    ]

    for left, right, expected in cases:
        assert is_anagram_sorting(left, right) is expected
        assert is_anagram_dict(left, right) is expected

    print("LeetCode 242 local tests passed.")
