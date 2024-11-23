import unittest
from graph import Graph

class TestGraph(unittest.TestCase):

    def test_add_edge(self):
        graph = Graph(5)

        graph.add_edge(0, 1, 10)
        self.assertEqual(graph.graph, [[0, 1, 10]])

        with self.assertRaises(ValueError):
            graph.add_edge(0, 1, 10)

    def test_bellman_ford(self):
        graph = Graph(5)
        graph.add_edge(0, 1, -1)
        graph.add_edge(0, 2, 4)
        graph.add_edge(1, 2, 3)
        graph.add_edge(1, 3, 2)
        graph.add_edge(1, 4, 2)
        graph.add_edge(3, 2, 5)
        graph.add_edge(3, 1, 1)
        graph.add_edge(4, 3, -3)

        dist = graph.bellman_ford(0)
        self.assertEqual(dist, [0, -1, 2, -2, 1])

        graph.add_edge(2, 0, -10)
        dist = graph.bellman_ford(0)
        self.assertEqual(dist, "Обнаружен отрицательный цикл!")

    def test_invalid_source(self):
        graph = Graph(5)

        with self.assertRaises(ValueError):
            graph.bellman_ford(-1)
        with self.assertRaises(ValueError):
            graph.bellman_ford(5)

    def test_print_arr(self):
        graph = Graph(5)
        dist = [0, 1, 2, 3, 4]

        result = graph.print_arr(dist)
        expected = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
