class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        array = nums.copy()
        for i in range(len(array)):
            for j in range(i+1, len(array)):
                if array[i] + array[j] == target:
                    return [i, j]
#哈希表的方法想不出来
