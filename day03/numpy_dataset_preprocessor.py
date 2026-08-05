"""Day 3: NumPy dataset preprocessing for AI.

完成后运行：
    python day03/test_day03.py
    python day03/numpy_dataset_preprocessor.py
"""

from __future__ import annotations

import numpy as np
from numpy.f2py.symbolic import integer_types
from numpy.ma.core import indices, floor


def as_feature_matrix(data) -> np.ndarray:
    """转换并验证二维 float64 特征矩阵，返回独立副本。"""
    try:
        res = np.array(data, dtype=np.float64).copy()
        if res.ndim == 2 and res.shape[0] > 0 and res.shape[1] >0 and np.isfinite(res).all():
            return res
        else:
            raise ValueError
    except Exception as e:
        raise  ValueError


def feature_statistics(features: np.ndarray) -> dict[str, np.ndarray]:
    """按列返回 mean、std、min、max。"""
    res = dict()
    res['mean'] = features.mean(axis=0)
    res['std'] = features.std(axis=0)
    res['min'] = features.min(axis=0)
    res['max'] = features.max(axis=0)
    return res


def standardize_features(
    features: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """按列标准化；零方差列标准化为全 0。"""
    data_mean = np.nanmean(features, axis=0)
    data_std = np.nanstd(features, axis=0)
    data_standardized = np.where(data_std != 0, (features - data_mean) / data_std, 0)
    return data_standardized, data_mean, data_std


def one_hot_encode(
    labels: np.ndarray,
    num_classes: int | None = None,
) -> np.ndarray:
    """将非负整数标签转换为 float64 one-hot 矩阵。"""
    if  labels.size == 0 or not np.isdtype(labels.dtype, np.integer):
        raise ValueError
    if not (0 <= labels).all() or not (labels < num_classes).all():
        raise ValueError
    if labels.ndim != 1:
        raise ValueError
    if num_classes is None:
        num_classes = labels.max() + 1
    res = np.zeros((len(labels), num_classes), dtype='float64')
    res[np.arange(len(labels)), labels] = 1.0
    return res


def train_test_split(
    features: np.ndarray,
    labels: np.ndarray,
    test_ratio: float = 0.2,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """使用随机索引划分训练集和测试集。"""
    if len(features) != len(labels) or not 0 < test_ratio < 1:
        raise ValueError
    rng = np.random.default_rng(seed)
    indices_ = rng.permutation(len(labels))
    res_X = features[indices_]
    res_Y = labels[indices_]
    test_size = int(np.ceil(len(res_X) * test_ratio))
    if test_size < 1 or test_size >= len(res_X):
        raise ValueError
    res_X = np.array_split(res_X, [int(np.floor(len(res_X) * (1 - test_ratio)))])
    res_Y = np.array_split(res_Y, [int(np.floor(len(res_Y) * (1 - test_ratio)))])
    X_train, X_test = res_X[0], res_X[1]
    Y_train, Y_test = res_Y[0], res_Y[1]
    return X_train, X_test, Y_train, Y_test


def create_mini_batches(
    features: np.ndarray,
    labels: np.ndarray,
    batch_size: int,
    shuffle: bool = True,
    seed: int = 42,
) -> list[tuple[np.ndarray, np.ndarray]]:
    """将数据切分成 mini-batch。"""
    if features.shape[0] != labels.shape[0]:
        raise ValueError
    if isinstance(batch_size, bool):
        raise ValueError
    if not isinstance(batch_size, (int, np.integer)):
        raise ValueError
    if batch_size <= 0 :
        raise ValueError
    res_feature = features.copy()
    res_label = labels.copy()
    if shuffle:
        rng = np.random.default_rng(seed=seed)
        indices_ = rng.permutation(len(features))
        res_feature = res_feature[indices_]
        res_label = res_label[indices_]
    batch_feature = []
    batch_label = []
    for i in range(0, len(res_feature), batch_size):
        batch_feature.append(res_feature[i: i+batch_size])
        batch_label.append(res_label[i: i+batch_size])
    return list(zip(batch_feature, batch_label))


def fit_nearest_centroid(
    features: np.ndarray,
    labels: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """计算每个类别的质心，返回 classes 和 centroids。"""
    #优化版：
    if features.shape[0] != labels.shape[0]:
        raise ValueError
    classes = np.array(sorted(list(set(labels))))
    centroid = []
    for i in sorted(list(set(labels))):
        centroid.append(features[labels == i].mean(axis=0))
    centroid = np.array(centroid)
    return classes, centroid


    # 最初版：
    # classes = np.array(sorted(list(set(labels))))
    # temp = dict()
    # for i in set(labels):
    #     temp[i] = []
    # for i in range(len(features)):
    #     temp[labels[i]].append(features[i])
    # temp = sorted(temp.items())
    # res = []
    # for i, element in temp:
    #     res.append(element.sum(axis=0) / len(element))
    # centroids = np.array(res)
    # return classes, centroids


def predict_nearest_centroid(
    features: np.ndarray,
    classes: np.ndarray,
    centroids: np.ndarray,
) -> np.ndarray:
    """使用批量欧氏距离预测类别。"""
    centroids_ = centroids.copy()
    features_ = features.copy()
    centroids_ = centroids_[:, None, :]
    features_ = features_[None, :, :]
    dist = ((features_-centroids_) ** 2).sum(axis=2)
    predict = dist.argmin(axis=0)
    return classes[predict]


def main() -> None:
    features = np.array(
        [
            [1.0, 1.0],
            [1.5, 2.0],
            [2.0, 1.5],
            [8.0, 8.0],
            [8.5, 9.0],
            [9.0, 8.5],
        ]
    )
    labels = np.array([0, 0, 0, 1, 1, 1])

    matrix = as_feature_matrix(features)
    standardized, _, _ = standardize_features(matrix)

    X_train, X_test, y_train, y_test = train_test_split(
        standardized,
        labels,
        test_ratio=1 / 3,
        seed=42,
    )

    classes, centroids = fit_nearest_centroid(X_train, y_train)
    predictions = predict_nearest_centroid(
        X_test,
        classes,
        centroids,
    )

    print(f"Feature matrix shape: {matrix.shape}")
    print(
        "Standardized mean:",
        np.round(standardized.mean(axis=0), 8),
    )
    print(f"Train size: {len(X_train)}")
    print(f"Test size: {len(X_test)}")
    print(f"Predictions: {predictions}")
    print(f"True labels: {y_test}")


if __name__ == "__main__":
    main()
