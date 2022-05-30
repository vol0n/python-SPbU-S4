import numpy as np
from scipy.linalg import norm
from PIL import Image
from typing import Optional


class KMeans:
    """
        kmeans++ model
    """

    def __init__(self, n_clusters: int, max_iter: int):
        """
        @param n_clusters: Число итоговых кластеров при кластеризации.
        @param max_iter: Максимальное число итераций для K-means.
        """
        self.n_clusters: int = n_clusters
        self.max_iter: int = max_iter
        self.centroids: Optional[np.array] = None

    def fit(self, x: np.array):
        """
        Ищет и запоминает центроиды кластеров для X.

        @param x: Набор данных, который необходимо кластеризовать.
        """
        assert self.n_clusters <= x.shape[0], f"{self.n_clusters} clusters for {x.shape[0]} points is too much!"

        self._init_centroids(x)

        for i in range(self.max_iter - 1):
            prev_centroids = self.centroids
            self._center_centroids(x, self._label_points(self._compute_distance(x)))
            if np.all(prev_centroids == self.centroids):
                break

    def _compute_distance(self, x):
        distance = np.zeros((x.shape[0], self.n_clusters))
        for i in range(self.n_clusters):
            distance[:, i] = norm(x - self.centroids[i], axis=1)
        return distance

    def _label_points(self, distance):
        return np.argmin(distance, axis=1)

    def _center_centroids(self, X, labeled_points):
        for i in range(self.n_clusters):
            self.centroids[i, :] = np.mean(X[labeled_points == i, :], axis=0)

    def _init_centroids(self, x):
        """
            init centroids so that each new centroid is far from other centroids
        """
        self.centroids = np.zeros((self.n_clusters, x.shape[1]))
        # initially choose random sample from data
        self.centroids[0, :] = x[np.random.choice(x.shape[0])]
        for i in range(1, self.n_clusters):
            # calculate the sum of distances from point to centroids, for each point
            dists = np.sum([np.sqrt(np.sum((x - centroid)**2, axis=1)) for centroid in self.centroids], axis=0)
            # normalise
            dists /= np.sum(dists)
            # choose new centroid randomly with probability proportional to sum of distances to centroids
            new_centroid_idx = np.random.choice(len(x), size=1, p=dists)
            self.centroids[i, :] = x[new_centroid_idx]

    def predict(self, x: np.array) -> np.array:
        """
        Для каждого элемента из X возвращает номер кластера,
        к которому относится данный элемент.

        @param x: Набор данных, для элементов которого находятся ближайшие кластера.
        @return labels: Вектор индексов ближайших кластеров
                        (по одному индексу для каждого элемента из X).
        """

        return self._label_points(self._compute_distance(x))


filename = 'cluster-tree'
ext = '.jpeg'
with Image.open(filename + ext) as im:
    width, height = im.size
    pixel_values = np.array(list(im.getdata()))

    n_clusters = 20
    n_iter = 100
    model = KMeans(n_clusters, n_iter)
    model.fit(pixel_values)

    labels = model.predict(pixel_values)
    pix = im.load()
    for i in range(len(pixel_values)):
        # as the centroid is calculated using mean, we should convert floats to int, because it rgb
        pix[i % width, i // width] = tuple(int(x) for x in model.centroids[labels[i]])
    im.save(f'after_{filename}{ext}')
