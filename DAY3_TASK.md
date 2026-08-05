# Day 3：NumPy 与 AI 数据预处理基础

## 一、今天为什么学 NumPy

NumPy 是 Python 科学计算和机器学习的数据基础。

今天的知识会直接用于后续：

| 今天学习 | 后续用途 |
|---|---|
| `ndarray`、`shape`、`dtype` | 理解机器学习数据 `X` 和标签 `y` |
| `axis=0`、`axis=1` | 按特征或按样本计算统计量 |
| 切片和布尔索引 | 数据筛选、训练集抽取 |
| 广播机制 | 标准化、距离计算、神经网络张量运算 |
| 向量化 | 避免慢速 Python 循环 |
| 随机数生成器 | 打乱数据、训练集与测试集划分 |
| 标准化 | scikit-learn 和神经网络训练前的数据预处理 |
| mini-batch | PyTorch 模型训练的数据批次 |
| 最近质心分类 | 第一次实现一个简单机器学习分类器 |

后续会学习：

```text
NumPy
→ pandas
→ Matplotlib
→ scikit-learn
→ PyTorch Tensor
```

pandas 的底层大量依赖 NumPy；PyTorch Tensor 的维度、切片、广播和 NumPy 很相似。因此今天不是孤立练习，而是在为 AI 数据处理打基础。

---

## 二、安装与目录

在仓库根目录运行：

```powershell
python -m pip install numpy
```

将下面一行加入 `requirements.txt`：

```text
numpy
```

最终目录：

```text
day03/
├── numpy_dataset_preprocessor.py
├── test_day03.py
└── day03_notes.md
```

---

## 三、今日阅读内容（约 45 分钟）

只阅读指定部分，不需要通读全文。

1. NumPy Quickstart  
   https://numpy.org/doc/stable/user/quickstart.html

   重点：
   - `ndarray`
   - `ndim`
   - `shape`
   - `size`
   - `dtype`
   - `np.array`
   - `np.arange`
   - `reshape`
   - `axis`
   - `mean`、`std`

2. NumPy 索引  
   https://numpy.org/doc/stable/user/basics.indexing.html

   重点：
   - `x[row, column]`
   - 切片
   - 布尔索引
   - 切片可能返回 view

3. NumPy 广播  
   https://numpy.org/doc/stable/user/basics.broadcasting.html

   重点：
   - 从最右侧维度开始比较
   - 两个维度相等，或者其中一个为 1，才可以广播
   - 为什么 `(n, d) - (d,)` 可以工作

暂时不用深入：
- 线性代数高级函数
- 结构化数组
- 内存布局
- FFT
- C API

---

## 四、主任务：AI 数据集预处理器

完成：

```text
day03/numpy_dataset_preprocessor.py
```

只能使用：

```python
import numpy as np
```

禁止使用：

```text
pandas
scikit-learn
torch
```

### 任务 1：验证特征矩阵

完成：

```python
as_feature_matrix(data)
```

要求：

- 将输入转换为 `float64` NumPy 数组；
- 必须是二维数组；
- 至少有一行和一列；
- 不能包含 `NaN`、`inf` 或 `-inf`；
- 返回独立副本，修改返回值不能影响原输入数组。

示例：

```python
X = as_feature_matrix([[1, 2], [3, 4]])
```

预期：

```text
array([[1., 2.],
       [3., 4.]])
shape == (2, 2)
dtype == float64
```

---

### 任务 2：按列统计特征

完成：

```python
feature_statistics(features)
```

返回：

```python
{
    "mean": ...,
    "std": ...,
    "min": ...,
    "max": ...,
}
```

要求：

- 每个结果都是一维数组；
- 按列计算，即 `axis=0`；
- 标准差使用 NumPy 默认的总体标准差 `ddof=0`；
- 禁止逐列写 Python `for` 循环。

示例输入：

```python
X = np.array([
    [1, 10],
    [2, 20],
    [3, 30],
])
```

预期均值：

```text
[2.0, 20.0]
```

---

### 任务 3：特征标准化

完成：

```python
standardize_features(features)
```

返回：

```python
standardized, mean, std
```

公式：

```text
standardized = (X - mean) / std
```

要求：

- 使用广播完成；
- 不修改原数组；
- 普通特征标准化后均值约为 0、标准差约为 1；
- 如果某列标准差为 0，该列标准化结果必须全部为 0；
- 返回的 `std` 仍保存真实标准差 0，而不是替换后的 1；
- 禁止逐行或逐列 Python 循环。

为什么有用：

```text
不同特征的量纲可能差异很大。
标准化能避免数值较大的特征在距离和模型优化中占据不合理优势。
```

后续 `scikit-learn` 会使用：

```python
StandardScaler
```

但今天手写一次，理解它的原理。

---

### 任务 4：One-hot 编码

完成：

```python
one_hot_encode(labels, num_classes=None)
```

示例：

```python
labels = np.array([2, 0, 1, 2])
```

预期：

```text
[[0., 0., 1.],
 [1., 0., 0.],
 [0., 1., 0.],
 [0., 0., 1.]]
```

要求：

- 标签必须是一维非空整数数组；
- 标签不得为负数；
- 未提供 `num_classes` 时，类别数为 `max(label) + 1`；
- 提供的类别数不能小于实际需要；
- 输出类型为 `float64`。

为什么有用：

```text
神经网络多分类任务经常需要将类别编号转换为 one-hot 表示。
```

---

### 任务 5：训练集和测试集划分

完成：

```python
train_test_split(features, labels, test_ratio=0.2, seed=42)
```

返回：

```python
X_train, X_test, y_train, y_test
```

要求：

- `features` 行数必须与 `labels` 长度一致；
- `0 < test_ratio < 1`；
- 训练集和测试集都至少保留一个样本；
- 使用 `np.random.default_rng(seed)`；
- 使用随机排列后的索引进行划分；
- 测试集数量定义为：

```python
test_size = int(np.ceil(sample_count * test_ratio))
```

- 同一个 `seed` 必须得到相同结果；
- 不同 `seed` 通常应得到不同划分；
- 不修改输入数组。

后续 `scikit-learn` 会提供：

```python
sklearn.model_selection.train_test_split
```

---

### 任务 6：创建 mini-batch

完成：

```python
create_mini_batches(
    features,
    labels,
    batch_size,
    shuffle=True,
    seed=42,
)
```

返回：

```python
list[tuple[np.ndarray, np.ndarray]]
```

要求：

- `batch_size` 必须是正整数；
- 每个样本恰好出现一次；
- 最后一个 batch 可以小于 `batch_size`；
- `shuffle=False` 时保持原始顺序；
- `shuffle=True` 时使用 `default_rng(seed)`；
- 允许在这个函数中使用一个循环切分 batch。

示例：

```text
10 个样本，batch_size=4
→ batch 大小为 4、4、2
```

为什么有用：

```text
PyTorch 训练通常不是一次把全部数据送入模型，而是按 mini-batch 迭代。
```

后续 PyTorch 会使用：

```python
DataLoader
```

---

### 任务 7：最近质心分类器

完成：

```python
fit_nearest_centroid(features, labels)
predict_nearest_centroid(features, classes, centroids)
```

训练阶段：

```text
对每个类别计算其所有训练样本的特征均值，得到类别质心。
```

预测阶段：

```text
计算每个新样本到各类别质心的欧氏距离，
选择距离最小的质心对应的类别。
```

要求：

- `classes` 按升序排列；
- `centroids.shape == (类别数, 特征数)`；
- 预测距离必须使用广播；
- 预测函数禁止逐样本 Python 循环；
- 距离相同时，返回 `classes` 中较早的类别。

广播提示：

```python
X[:, None, :]          # (样本数, 1, 特征数)
centroids[None, :, :]  # (1, 类别数, 特征数)
```

两者相减后：

```text
(样本数, 类别数, 特征数)
```

这就是后续机器学习中非常常见的“批量距离计算”。

---

## 五、自动验收

运行：

```powershell
python day03/test_day03.py
```

全部通过时输出：

```text
All Day 3 tests passed.
```

再运行演示：

```powershell
python day03/numpy_dataset_preprocessor.py
```

预期包含：

```text
Feature matrix shape: (6, 2)
Standardized mean: [0. 0.]
Train size: 4
Test size: 2
Predictions: ...
```

浮点数显示可能存在极小误差，这是正常的，应使用 `np.allclose()` 比较，而不是直接使用 `==`。

---

## 六、代码要求

必须做到：

- 使用类型标注；
- 保留简洁 docstring；
- 删除完成后的 `TODO` 和不可达的 `NotImplementedError`；
- 不在统计、标准化和预测函数中写逐元素循环；
- 使用 `np.asarray`、`axis`、布尔判断、广播；
- 不能直接照搬完整答案，先自己实现并运行测试。

---

## 七、笔记要求

填写：

```text
day03/day03_notes.md
```

重点回答：

1. `shape`、`ndim`、`size`、`dtype`分别是什么？
2. `axis=0`与`axis=1`有什么区别？
3. 切片为什么可能修改原数组？
4. 广播的两个兼容条件是什么？
5. 为什么标准化要按列计算？
6. 为什么零方差列不能直接除以 0？
7. `default_rng(seed)`中的 seed 有什么作用？
8. mini-batch 为什么适合神经网络训练？
9. NumPy 数组与 Python 列表最大的差异是什么？
10. 今天哪一段代码真正使用了向量化？

---

## 八、建议时间安排

```text
官方文档阅读          45 分钟
NumPy 基础试验        35 分钟
完成验证与统计        40 分钟
完成标准化与 one-hot  45 分钟
完成划分与 batch      45 分钟
完成最近质心分类器    45 分钟
测试、笔记和 Git      30 分钟
```

总有效学习时间约 4 小时。

---

## 九、Git 提交建议

至少 3 次提交：

```powershell
git add requirements.txt day03/numpy_dataset_preprocessor.py
git commit -m "feat: add NumPy dataset preprocessing"

git add day03/test_day03.py
git commit -m "test: add Day 3 NumPy tests"

git add day03/day03_notes.md README.md
git commit -m "docs: complete Day 3 NumPy notes"

git push
```

README 完成后增加：

```text
- [x] Day 3: NumPy arrays, vectorization and AI data preprocessing
```

---

## 十、评分标准（100 分）

| 项目 | 分值 |
|---|---:|
| 数组转换与数据验证 | 15 |
| 特征统计 | 10 |
| 标准化与广播 | 20 |
| One-hot 编码 | 10 |
| 训练测试集划分 | 15 |
| Mini-batch | 10 |
| 最近质心分类器 | 10 |
| 自动测试 | 5 |
| 代码规范与笔记 | 5 |
