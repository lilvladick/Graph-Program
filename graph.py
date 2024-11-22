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
        """

        self.graph.append([u, v, w])

    def print_arr(self, dist):
        """
        Печать массива расстояний.

        :param dist: Массив расстояний от начальной вершины до всех остальных.
        """

        for i in range(self.V):
            print("% d \t\t % d" % (i, dist[i]))

    def bellman_ford(self, src):
        """
        Реализация алгоритма Белмана-Форда для нахождения кратчайших путей от начальной вершины до всех остальных.

        :param src: Индекс начальной вершины.
        :raises ValueError: Если индекс начальной вершины выходит за пределы допустимого диапазона.
        """

        if src < 0 or src >= self.V:
            raise ValueError("Неверный индекс начальной вершины")

        dist = [float("Inf")] * self.V
        dist[src] = 0

        max_iterations = self.V - 1

        for _ in range(max_iterations):
            updated = False
            for u, v, w in self.graph:
                if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    updated = True

            if not updated:
                break

        for u, v, w in self.graph:
            if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                print("Отрицательный цикл обнаружен!")
                return

        self.print_arr(dist)


if __name__ == "__main__":
    graph = Graph(5)
    graph.add_edge(0, 1, -1)
    graph.add_edge(0, 2, 4)
    graph.add_edge(1, 2, 3)
    graph.add_edge(1, 3, 2)
    graph.add_edge(1, 4, 2)
    graph.add_edge(3, 2, 5)
    graph.add_edge(3, 1, 1)
    graph.add_edge(4, 3, -3)

    try:
        graph.bellman_ford(0)
    except ValueError as e:
        print(e)