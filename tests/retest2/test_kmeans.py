import pytest
import numpy as np
from src.retest2.kmeans import KMeans


@pytest.mark.parametrize(
    "array, n_clusters, expected",
    [
        ([1], 1, {frozenset((0,))}),
        ([1, 2, 2.01], 2, {frozenset((1, 2)), frozenset((0,))}),
    ],
)
def test_kmeans_trivial(array, n_clusters, expected):
    arr = np.array(array).reshape((len(array), 1))
    model = KMeans(n_clusters, 1000)
    model.fit(arr)
    clusters = [set() for _ in range(n_clusters)]
    for i, x in enumerate(model.predict(arr)):
        clusters[x].add(i)
    for i in range(n_clusters):
        clusters[i] = frozenset(clusters[i])
    assert set(clusters) == expected
