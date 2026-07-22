import string
from math import ceil


def analyze_numbers(numbers: list[int]) -> dict:
    array = numbers.copy()
    dict1 = {'count': len(array)}
    sorted_array = sorted(array)
    if len(array) > 0:
        dict1['sum'] = sum(array)
        dict1['mean'] = sum(array) / len(array)
        dict1['max'] = max(array)
        dict1['min'] = min(array)
        unique_count = 1
        for i in range(1, len(array)):
            if sorted_array[i] != sorted_array[i - 1]:
                unique_count += 1
    else:
        unique_count = 0
    dict1['unique_count'] = unique_count
    dict1['sorted_numbers'] = sorted_array
    return dict1
    #时间复杂度O(n log n)


def count_words(text: str) -> dict[str, int]:
    if text == '':
        return {}
    txt = text.lower()
    txt = txt.split()
    for i, word in enumerate(txt):
        word = word.strip()
        word = word.strip(string.punctuation)
        word = word.strip()
        txt[i] = word
    for i in range(len(txt)-1 ,-1, -1):
        if txt[i] == '':
            txt.pop(i)
    txt.sort()

    dict1 = {txt[0]: txt.count(txt[0])}
    for i in range(1, len(txt)):
        if txt[i] != txt[i - 1]:
            dict1[txt[i]] = txt.count(txt[i])
    dict1 = sorted(dict1.items(), key = lambda x: (x[1], x[0]),reverse = True)
    dict1 = dict(dict1)
    return dict1


def unique_keep_order(items: list[int]) -> list[int]:
    array = items.copy()
    check = set()
    res = []
    for element in array:
        if element not in check:
            check.add(element)
            res += [element]
    return res
    #因为set是无序的，也就是说list(set(items))没有办法保证最终的顺序和开始一样


def group_students(records: list[tuple[str, int]]) -> dict[str, list[str]]:
    rec = records.copy()
    rec = sorted(rec, key=lambda x: (-x[1], x[0]))
    res = {'A': [], 'B': [], 'C': [], 'D': [], 'F': []}
    for item in rec:
        if 90 <= item[1] <= 100:
            res['A'].append(item[0])
            continue
        if 80 <= item[1] < 90:
            res['B'].append(item[0])
            continue
        if 70 <= item[1] < 80:
            res['C'].append(item[0])
            continue
        if 60 <= item[1] < 70:
            res['D'].append(item[0])
            continue
        if 0 <= item[1] < 60:
            res['F'].append(item[0])
            continue
        raise ValueError()
    return res


def create_batches(data: list, batch_size: int) -> list[list]:
    res = []
    if batch_size == 0:
        raise ValueError
    for i in range(0, len(data), batch_size):
        res.append(data[i: i+batch_size])
    return res
    #相似之处在于都能够将列表变形，便于前向传递



if __name__ == '__main__':
    print(count_words(''))