import numpy as np
from PIL import Image


def dist(x: np.array, y: np.array):
    return np.sqrt(np.sum((x - y) ** 2))


class KMeans:
    """
        kmeans++ model
    """

    def __init__(self, n_clusters: int, max_iter: int):
        """
        @param n_clusters: Число итоговых кластеров при кластеризации.
        @param max_iter: Максимальное число итераций для K-means.
        """
        self.n_clusters = n_clusters
        self.max_iter = max_iter

    def fit(self, x: np.array):
        """
        Ищет и запоминает центроиды кластеров для X.

        @param x: Набор данных, который необходимо кластеризовать.
        """

        assert self.n_clusters <= x.shape[0], f"{self.n_clusters} clusters for {x.shape[0]} points is too much!"

        # self.centroids = x[np.random.choice(x.shape[0], self.n_clusters, replace=False)]
        self._init_centroids(x)

        for i in range(self.max_iter - 1):
            clusters = [[] for _ in range(len(self.centroids))]
            for sample in x:
                clusters[self.get_closest_centroid(sample)].append(sample)

            prev_centroids = self.centroids
            for j, cluster in enumerate(clusters):
                # if centroid has any points
                if cluster:
                    self.centroids[j] = np.mean(cluster, axis=0)

            if np.equal(self.centroids, prev_centroids).all():
                break

    def _init_centroids(self, x):
        """
            init centroids so that each new centroid is far from other centroids
        """
        # initially choose random sample from data
        self.centroids = [x[np.random.choice(x.shape[0])]]
        for _ in range(self.n_clusters-1):
            # calculate the sum of distances from point to centroids, for each point
            dists = np.sum([np.sqrt(np.sum((x - centroid)**2, axis=1)) for centroid in self.centroids], axis=0)
            # normalise
            dists /= np.sum(dists)
            # choose new centroid randomly with probability proportional to sum of distances to centroids
            new_centroid_idx = np.random.choice(len(x), size=1, p=dists)
            self.centroids += [x[new_centroid_idx]]

    def get_closest_centroid(self, point: np.array) -> int:
        min_idx = 0
        min_dist = dist(point, self.centroids[0])
        for i in range(1, len(self.centroids)):
            d = dist(point, self.centroids[i])
            if d < min_dist:
                min_idx = i
                min_dist = d
        return min_idx

    def predict(self, x: np.array) -> np.array:
        """
        Для каждого элемента из X возвращает номер кластера,
        к которому относится данный элемент.

        @param x: Набор данных, для элементов которого находятся ближайшие кластера.
        @return labels: Вектор индексов ближайших кластеров
                        (по одному индексу для каждого элемента из X).
        """

        return np.array([self.get_closest_centroid(sample) for sample in x])


with Image.open('before.jpeg') as im:
    width, height = im.size
    pixel_values = np.array([(i % width, i // width) + c for i, c in enumerate(list(im.getdata()))])

    n_clusters = 11
    n_iter = 10
    model = KMeans(n_clusters, n_iter)
    model.fit(pixel_values)

    labels = model.predict(pixel_values)
    pix = im.load()
    for i in range(len(pixel_values)):
        # as the centroid is calculated using mean, we should convert floats to int, because it rgb
        pix[pixel_values[i][0], pixel_values[i][1]] = tuple(int(x) for x in model.centroids[labels[i]][2:])
    im.save('after.png')
