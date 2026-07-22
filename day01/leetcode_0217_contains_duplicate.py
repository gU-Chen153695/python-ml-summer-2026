class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:#时间复杂度O(n)
        if len(set(nums)) < len(nums):
            return True
        return False

    """
    暴力：
    def containsDuplicate(self, nums: list[int]) -> bool:#时间复杂度O(n^2)
        array = nums.copy()
        for item in array:
            if array.count(item) > 1:
                return True
        return False
                
    """