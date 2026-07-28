# Day 2：CSV、文件路径、异常处理与哈希表

## 一、最终目录

```text
day02/
├── data/
│   ├── students.csv
│   ├── students_invalid_type.csv
│   ├── students_invalid_range.csv
│   ├── students_missing_name.csv
│   ├── students_duplicate_name.csv
│   ├── students_bad_header.csv
│   ├── students_missing_score.csv
│   ├── students_extra_column.csv
│   └── students_empty.csv
├── output/
│   └── student_report.csv          # 程序运行后生成
├── student_report.py
├── test_day02.py
├── leetcode_0242_valid_anagram.py
├── leetcode_0349_intersection.py   # 加做
├── day02_notes.md
└── internship_preparation.md
```

## 二、主任务：学生成绩 CSV 分析器

### 1. CSV 输入标准

表头必须完全等于：

```text
name,math,python,ml
```

要求：

- 表头字段名称和顺序都必须一致；
- 至少包含一条学生数据；
- 每行必须正好有 4 个字段；
- 允许 CSV 中存在空白行；
- 所有文本读取和写入均使用 UTF-8；
- 只能使用 Python 标准库。

### 2. 姓名标准

对姓名先执行首尾空格清理。

清理后必须满足：

- 不能为空；
- 长度为 1～30 个字符；
- 同一个文件中不能出现重复姓名；
- 重复判断按清理后的字符串进行，区分大小写。

错误示例：

```text
Row 3: invalid name ''
Row 4: duplicate name 'Alice'
```

### 3. 成绩标准

`math`、`python`、`ml` 均必须满足：

- 可以被 `int()` 转换；
- 必须是整数；
- 取值范围为 0～100，包含 0 和 100；
- 空字符串、浮点数文本、字母、负数、超过 100 均不合法。

错误信息必须包含：

- CSV 行号；
- 科目名称；
- 原始错误值。

示例：

```text
Row 3: invalid python score 'not_a_number'
Row 3: python score out of range '101'
```

### 4. 平均分和等级

学生原始平均分：

```text
(math + python + ml) / 3
```

等级按未四舍五入的原始平均分判断：

| 平均分 | 等级 |
|---|---|
| 90～100 | A |
| 80～不足90 | B |
| 70～不足80 | C |
| 60～不足70 | D |
| 低于60 | F |

报告中的 `average` 四舍五入保留 2 位小数。

### 5. 排序标准

报告排序规则：

1. 原始平均分降序；
2. 原始平均分完全相同时，姓名升序。

### 6. 输出 CSV 标准

输出路径：

```text
day02/output/student_report.csv
```

输出表头固定为：

```text
name,math,python,ml,average,grade
```

要求：

- 输出目录不存在时自动创建；
- `average` 始终写成两位小数，例如 `99.00`；
- 输入数据不得被函数原地修改。

### 7. 正常数据的预期终端结果

运行：

```powershell
python day02/student_report.py
```

应包含：

```text
Loaded students: 10
Math average: 80.90
Python average: 83.40
ML average: 81.80
Top 3 students:
1. Ivy - 99.00 - A
2. Eva - 95.00 - A
3. Alice - 90.67 - A
Report saved to: ...
```

### 8. 异常处理标准

`main()`只允许捕获：

```python
FileNotFoundError
ValueError
csv.Error
```

禁止：

```python
except:
except Exception:
```

发生错误时输出：

```text
Error: 具体错误信息
```

并以非零状态退出。

## 三、自动验收

运行：

```powershell
python day02/test_day02.py
```

通过标准：

```text
All Day 2 tests passed.
```

测试涵盖：

- 合法成绩 0、100、带首尾空格；
- 空值、浮点数字符串、字母、负数、101；
- 空姓名、超长姓名、重复姓名；
- 表头错误、缺失列、多余列、空数据；
- 文件不存在；
- 等级全部边界；
- 平均分；
- 排序与同分姓名顺序；
- 输出目录创建；
- 输出 CSV 表头与两位小数。

## 四、LeetCode 242：Valid Anagram

必须完成两个函数：

```python
is_anagram_sorting()
is_anagram_dict()
```

本练习约束：

- 字符串长度 1～50,000；
- 仅包含小写英文字母；
- 禁止使用 `collections.Counter`。

排序法要求：

- 时间复杂度：O(n log n)；
- 说明 `sorted()` 会创建新列表。

字典法要求：

- 平均时间复杂度：O(n)；
- 空间复杂度：O(k)，k 为不同字符数量；
- 手写字符计数；
- 长度不同应立即返回 `False`。

本地检查：

```powershell
python day02/leetcode_0242_valid_anagram.py
```

通过标准：

```text
LeetCode 242 local tests passed.
```

之后提交到 LeetCode，要求 Accepted。

## 五、加做：LeetCode 349

要求：

- 完成集合辅助版本；
- 完成遍历版本；
- 返回结果不得重复；
- 输出顺序不限；
- 不直接使用集合交集运算符 `&`。

运行：

```powershell
python day02/leetcode_0349_intersection.py
```

通过标准：

```text
LeetCode 349 local tests passed.
```

## 六、笔记


```text
day02/day02_notes.md
```

笔记不得保留空白问题，至少记录三个实际错误。

## 七、Git 提交标准

至少 4 次提交：

```powershell
git add day02/data day02/student_report.py day02/test_day02.py
git commit -m "feat: add Day 2 CSV report analyzer"

git add day02/leetcode_0242_valid_anagram.py
git commit -m "solve: add LeetCode 242 solutions"

git add day02/leetcode_0349_intersection.py
git commit -m "solve: add optional LeetCode 349 solutions"

git add day02/day02_notes.md day02/internship_preparation.md
git commit -m "docs: complete Day 2 notes and internship preparation"

git push
```

## 八、Day 2 最终提交材料

提交以下内容：

1. GitHub 仓库链接；
2. `python day02/test_day02.py` 输出；
3. `python day02/student_report.py` 输出；
4. 一种异常 CSV 的报错输出；
5. LeetCode 242 Accepted 截图或说明；
6. LeetCode 349 是否完成；
7. `day02_notes.md`；
9. `git log --oneline -8`；
10. 当天有效学习时长。

## 九、评分标准（100分）

| 项目 | 分值 |
|---|---:|
| CSV 读取与路径处理 | 15 |
| 数据验证完整性 | 20 |
| 报告计算与排序 | 15 |
| CSV 输出 | 10 |
| 异常处理 | 10 |
| 自动测试通过 | 10 |
| LeetCode 242 | 10 |
| 代码规范与类型标注 | 5 |
| 学习笔记与实习准备 | 5 |

加做 LeetCode 349 可获得额外 5 分，但总成绩最高为 100。
