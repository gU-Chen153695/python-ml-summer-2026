class Solution:
    """def twoSum(self, nums: list[int], target: int) -> list[int]:
        array = nums.copy()
        for i in range(len(array)):
            for j in range(i+1, len(array)):
                if array[i] + array[j] == target:
                    return [i, j]"""

    def twoSum(self, nums: list[int], target: int) -> list[int]:
        array = nums.copy()
        temp = {}
        for i, item in enumerate(array):
            if target-item in temp:
                return [i, temp[target-item]]
            temp[item] = i
        return []