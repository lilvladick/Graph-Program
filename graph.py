class Graph:
    """Класс для представления взвешенного ориентированного графа."""

    def __init__(self, vertices):
        """
        Конструктор класса Graph.

        :param vertices: Количество вершин в графе.
        """
        self.V = vertices
        self.graph = []

    def add_edge(self, u, v, w):
        """
        Добавляет ребро в граф.

        :param u: Начальная вершина ребра.
        :param v: Конечная вершина ребра.
        :param w: Вес ребра.
        :raises ValueError: Если ребро уже существует.
        """
        if any(edge for edge in self.graph if edge[:2] == [u, v]):
            raise ValueError(f"Ребро между вершинами {u} и {v} уже существует")
        self.graph.append([u, v, w])

    def print_arr(self, dist):
        """
        Возвращает массив расстояний от начальной вершины до всех остальных.

        :param dist: Массив расстояний.
        :return: Словарь с индексами вершин и их расстояниями.
        """
        return {i: dist[i] for i in range(self.V)}

    def bellman_ford(self, src):
        """
        Алгоритм Беллмана-Форда для нахождения кратчайших путей.

        :param src: Начальная вершина.
        :return: Массив расстояний или строка с сообщением об ошибке.
        :raises ValueError: Если индекс начальной вершины выходит за пределы допустимого диапазона.
        """
        if src < 0 or src >= self.V:
            raise ValueError("Неверный индекс начальной вершины")

        dist = [float("Inf")] * self.V
        dist[src] = 0

        for _ in range(self.V - 1):
            for u, v, w in self.graph:
                if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w

        for u, v, w in self.graph:
            if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                return "Обнаружен отрицательный цикл!"

        return dist
