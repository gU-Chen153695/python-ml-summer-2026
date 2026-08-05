"""Day 3 automated tests.

运行：
    python day03/test_day03.py
"""

from __future__ import annotations

import numpy as np

from numpy_dataset_preprocessor import (
    as_feature_matrix,
    create_mini_batches,
    feature_statistics,
    fit_nearest_centroid,
    one_hot_encode,
    predict_nearest_centroid,
    standardize_features,
    train_test_split,
)


def assert_raises(expected_exception, function, *args, **kwargs) -> None:
    try:
        function(*args, **kwargs)
    except expected_exception:
        return
    except Exception as error:
        raise AssertionError(
            f"Expected {expected_exception.__name__}, "
            f"but got {type(error).__name__}: {error}"
        ) from error

    raise AssertionError(
        f"Expected {expected_exception.__name__}, "
        "but no error was raised"
    )


def run_tests() -> None:
    # 1. 特征矩阵转换与验证
    original = np.array([[1, 2], [3, 4]], dtype=np.int64)
    matrix = as_feature_matrix(original)

    assert isinstance(matrix, np.ndarray)
    assert matrix.shape == (2, 2)
    assert matrix.dtype == np.float64
    assert np.array_equal(matrix, np.array([[1.0, 2.0], [3.0, 4.0]]))

    matrix[0, 0] = 999
    assert original[0, 0] == 1

    assert_raises(ValueError, as_feature_matrix, [1, 2, 3])
    assert_raises(ValueError, as_feature_matrix, [])
    assert_raises(ValueError, as_feature_matrix, [[], []])
    assert_raises(
        ValueError,
        as_feature_matrix,
        [[1.0, np.nan], [2.0, 3.0]],
    )
    assert_raises(
        ValueError,
        as_feature_matrix,
        [[1.0, np.inf], [2.0, 3.0]],
    )

    # 2. 按列统计
    X = np.array(
        [
            [1.0, 10.0, 5.0],
            [2.0, 20.0, 5.0],
            [3.0, 30.0, 5.0],
            [4.0, 40.0, 5.0],
        ]
    )
    statistics = feature_statistics(X)

    assert set(statistics) == {"mean", "std", "min", "max"}
    assert np.allclose(statistics["mean"], [2.5, 25.0, 5.0])
    assert np.allclose(
        statistics["std"],
        [np.sqrt(1.25), np.sqrt(125.0), 0.0],
    )
    assert np.allclose(statistics["min"], [1.0, 10.0, 5.0])
    assert np.allclose(statistics["max"], [4.0, 40.0, 5.0])
    assert all(value.shape == (3,) for value in statistics.values())

    # 3. 标准化
    X_before = X.copy()
    standardized, mean, std = standardize_features(X)

    assert np.array_equal(X, X_before)
    assert np.allclose(mean, [2.5, 25.0, 5.0])
    assert np.allclose(
        std,
        [np.sqrt(1.25), np.sqrt(125.0), 0.0],
    )
    assert np.allclose(standardized[:, :2].mean(axis=0), [0.0, 0.0])
    assert np.allclose(standardized[:, :2].std(axis=0), [1.0, 1.0])
    assert np.allclose(standardized[:, 2], 0.0)
    assert np.isfinite(standardized).all()

    # 4. One-hot
    labels = np.array([2, 0, 1, 2], dtype=np.int64)
    encoded = one_hot_encode(labels)

    expected_encoded = np.array(
        [
            [0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    )
    assert encoded.dtype == np.float64
    assert np.array_equal(encoded, expected_encoded)
    assert one_hot_encode(labels, num_classes=4).shape == (4, 4)

    assert_raises(ValueError, one_hot_encode, np.array([]))
    assert_raises(ValueError, one_hot_encode, np.array([[0, 1]]))
    assert_raises(ValueError, one_hot_encode, np.array([0, -1]))
    assert_raises(ValueError, one_hot_encode, np.array([0.0, 1.0]))
    assert_raises(
        ValueError,
        one_hot_encode,
        labels,
        num_classes=2,
    )

    # 5. 训练测试集划分
    split_X = np.arange(20, dtype=np.float64).reshape(10, 2)
    split_y = np.arange(10, dtype=np.int64)

    result_1 = train_test_split(
        split_X,
        split_y,
        test_ratio=0.3,
        seed=7,
    )
    result_2 = train_test_split(
        split_X,
        split_y,
        test_ratio=0.3,
        seed=7,
    )

    X_train, X_test, y_train, y_test = result_1

    assert X_train.shape == (7, 2)
    assert X_test.shape == (3, 2)
    assert y_train.shape == (7,)
    assert y_test.shape == (3,)

    for left, right in zip(result_1, result_2):
        assert np.array_equal(left, right)

    assert set(y_train.tolist()).isdisjoint(set(y_test.tolist()))
    assert set(y_train.tolist()) | set(y_test.tolist()) == set(range(10))
    assert np.array_equal((X_train[:, 0] // 2).astype(int), y_train)
    assert np.array_equal((X_test[:, 0] // 2).astype(int), y_test)

    assert_raises(
        ValueError,
        train_test_split,
        split_X,
        split_y[:-1],
    )
    assert_raises(
        ValueError,
        train_test_split,
        split_X,
        split_y,
        test_ratio=0,
    )
    assert_raises(
        ValueError,
        train_test_split,
        split_X,
        split_y,
        test_ratio=1,
    )
    assert_raises(
        ValueError,
        train_test_split,
        np.array([[1.0, 2.0]]),
        np.array([0]),
        test_ratio=0.2,
    )

    # 6. Mini-batch
    batches = create_mini_batches(
        split_X,
        split_y,
        batch_size=4,
        shuffle=False,
    )

    assert [len(batch_y) for _, batch_y in batches] == [4, 4, 2]
    reconstructed_X = np.concatenate(
        [batch_X for batch_X, _ in batches],
        axis=0,
    )
    reconstructed_y = np.concatenate(
        [batch_y for _, batch_y in batches],
        axis=0,
    )
    assert np.array_equal(reconstructed_X, split_X)
    assert np.array_equal(reconstructed_y, split_y)

    shuffled_1 = create_mini_batches(
        split_X,
        split_y,
        batch_size=3,
        shuffle=True,
        seed=9,
    )
    shuffled_2 = create_mini_batches(
        split_X,
        split_y,
        batch_size=3,
        shuffle=True,
        seed=9,
    )
    shuffled_y_1 = np.concatenate([y for _, y in shuffled_1])
    shuffled_y_2 = np.concatenate([y for _, y in shuffled_2])
    assert np.array_equal(shuffled_y_1, shuffled_y_2)
    assert set(shuffled_y_1.tolist()) == set(range(10))

    assert_raises(
        ValueError,
        create_mini_batches,
        split_X,
        split_y,
        batch_size=0,
    )
    assert_raises(
        ValueError,
        create_mini_batches,
        split_X,
        split_y[:-1],
        batch_size=2,
    )

    # 7. 最近质心分类器
    train_X = np.array(
        [
            [0.0, 0.0],
            [0.0, 2.0],
            [10.0, 10.0],
            [10.0, 12.0],
        ]
    )
    train_y = np.array([0, 0, 1, 1])

    classes, centroids = fit_nearest_centroid(train_X, train_y)

    assert np.array_equal(classes, [0, 1])
    assert centroids.shape == (2, 2)
    assert np.allclose(centroids, [[0.0, 1.0], [10.0, 11.0]])

    predictions = predict_nearest_centroid(
        np.array([[0.0, 1.0], [9.0, 10.0], [5.0, 6.0]]),
        classes,
        centroids,
    )
    assert np.array_equal(predictions, [0, 1, 0])

    string_classes, string_centroids = fit_nearest_centroid(
        train_X,
        np.array(["cat", "cat", "dog", "dog"]),
    )
    assert np.array_equal(string_classes, ["cat", "dog"])
    assert np.array_equal(
        predict_nearest_centroid(
            np.array([[1.0, 1.0], [11.0, 11.0]]),
            string_classes,
            string_centroids,
        ),
        ["cat", "dog"],
    )

    assert_raises(
        ValueError,
        fit_nearest_centroid,
        train_X,
        train_y[:-1],
    )
    assert_raises(
        ValueError,
        predict_nearest_centroid,
        np.array([[1.0, 2.0, 3.0]]),
        classes,
        centroids,
    )

    print("All Day 3 tests passed.")


if __name__ == "__main__":
    run_tests()
