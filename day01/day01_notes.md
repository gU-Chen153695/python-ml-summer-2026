# Day 1 Notes

## 1. Python列表、元组、集合和字典分别适合什么场景？
列表类似C++数组，比较泛用；元组适合二元场景；集合适合无序不重复；字典适合一一对应且key可为string

## 2. Python切片的 start、stop、step 分别代表什么？
start是开始下标；stop是结束下标加一；step是步长

## 3. 为什么保持顺序去重不能简单使用 list(set(items))？
set是无序的，转换为set的时候会打乱顺序

## 4. LeetCode 217中，set版本为什么比双重循环更好？
时间复杂度更优

## 5. LeetCode 1中，哈希表保存了什么信息？
哈希表保存已经遍历过的数字及其下标，即：
数字 -> 下标。

遍历当前数字 number 时，计算 complement = target - number。
如果 complement 已经在哈希表中，就返回 complement 对应的旧下标和当前下标。

## 6. 今天哪些Python语法需要查文档？
sorted()函数，哈希表和列表的增删改查需要

## 7. 今天在哪些地方使用了AI？
写清楚问题和AI提供了什么帮助。
函数和数据结构的各种操作使用了ai查文档

## 8. 哪一段代码是在关闭资料后重新写出的？
都是关闭资料写的

## 9. 今天遇到的三个错误及解决办法
1. LeetCode 217审题错误，没有返回下标而是直接返回了数字

2. count_words处理空字符串和纯标点字符串时，清理后列表为空，继续访问txt[0]会报错；加入if not txt: return {}。

3. create_batches最初只判断batch_size == 0，没有处理负数；改为batch_size <= 0并抛出ValueError。

## 10. 自我评分
- Python syntax: 6/10
- Problem solving: 8/10
- Debugging: 8/10
- Independence: 6/10