"""LeetCode 349: Intersection of Two Arrays（加做）

本练习约束：
- 1 <= len(nums1), len(nums2) <= 1_000
- 0 <= nums1[i], nums2[i] <= 1_000
- 结果中每个元素只能出现一次
- 结果顺序不限
"""


def intersection_set(nums1: list[int], nums2: list[int]) -> list[int]:
    """允许使用 set，但不要直接使用集合交集运算符 &。"""
    # TODO
    raise NotImplementedError


def intersection_manual(nums1: list[int], nums2: list[int]) -> list[int]:
    """遍历实现，结果不得重复。"""
    # TODO
    raise NotImplementedError


if __name__ == "__main__":
    cases = [
        ([1, 2, 2, 1], [2, 2], {2}),
        ([4, 9, 5], [9, 4, 9, 8, 4], {4, 9}),
        ([1], [2], set()),
    ]

    for nums1, nums2, expected in cases:
        assert set(intersection_set(nums1, nums2)) == expected
        assert set(intersection_manual(nums1, nums2)) == expected

    print("LeetCode 349 local tests passed.")
