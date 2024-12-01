import sys
from PyQt5.QtWidgets import QApplication,QMessageBox , QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsLineItem
from PyQt5.QtGui import QBrush, QColor
from graph import Graph

class GraphGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Кратчайшие пути в графе")
        self.setGeometry(100, 100, 800, 600)

        self.vertices = []
        self.edges = []
        self.graph = None

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.graphics_view = QGraphicsView(self)
        self.graphics_scene = QGraphicsScene()
        self.graphics_view.setScene(self.graphics_scene)

        layout.addWidget(self.graphics_view)

        self.form_layout = QFormLayout()

        self.vertex_x_input = QLineEdit()
        self.vertex_y_input = QLineEdit()
        self.form_layout.addRow("X координата вершины:", self.vertex_x_input)
        self.form_layout.addRow("Y координата вершины:", self.vertex_y_input)

        self.add_vertex_button = QPushButton("Добавить вершину", self)
        self.add_vertex_button.clicked.connect(self.add_vertex)

        self.form_layout.addRow(self.add_vertex_button)

        self.edge_u_input = QLineEdit()
        self.edge_v_input = QLineEdit()
        self.edge_weight_input = QLineEdit()
        self.form_layout.addRow("Начальная вершина:", self.edge_u_input)
        self.form_layout.addRow("Конечная вершина:", self.edge_v_input)
        self.form_layout.addRow("Вес ребра:", self.edge_weight_input)

        self.add_edge_button = QPushButton("Добавить ребро", self)
        self.add_edge_button.clicked.connect(self.add_edge)

        self.form_layout.addRow(self.add_edge_button)

        self.src_input = QLineEdit()
        self.form_layout.addRow("Начальная вершина для алгоритма:", self.src_input)

        self.run_algorithm_button = QPushButton("Запустить алгоритм", self)
        self.run_algorithm_button.clicked.connect(self.run_algorithm)
        self.form_layout.addRow(self.run_algorithm_button)

        layout.addLayout(self.form_layout)

        self.setLayout(layout)

    def add_vertex(self):
        """Добавляет вершину на холст."""
        try:
            x = int(self.vertex_x_input.text())
            y = int(self.vertex_y_input.text())

            self.vertices.append((x, y))
            self.graph = Graph(len(self.vertices))

            ellipse = QGraphicsEllipseItem(x - 10, y - 10, 20, 20)
            ellipse.setBrush(QBrush(QColor(0, 0, 255)))
            self.graphics_scene.addItem(ellipse)
            self.graphics_scene.addText(str(len(self.vertices) - 1)).setPos(x - 5, y - 5)

            self.vertex_x_input.clear()
            self.vertex_y_input.clear()

        except ValueError:
            self.show_error("Ошибка", "Введите корректные числа для координат.")

    def add_edge(self):
        """Добавляет ребро между двумя вершинами."""
        try:
            u = int(self.edge_u_input.text())
            v = int(self.edge_v_input.text())
            weight = int(self.edge_weight_input.text())

            if u >= len(self.vertices) or v >= len(self.vertices):
                raise ValueError("Неверные номера вершин.")

            self.graph.add_edge(u, v, weight)

            x1, y1 = self.vertices[u]
            x2, y2 = self.vertices[v]
            line = QGraphicsLineItem(x1, y1, x2, y2)
            self.graphics_scene.addItem(line)
            self.graphics_scene.addText(str(weight)).setPos((x1 + x2) / 2, (y1 + y2) / 2)

            self.edge_u_input.clear()
            self.edge_v_input.clear()
            self.edge_weight_input.clear()

        except ValueError:
            self.show_error("Ошибка", "Введите корректные данные для ребра.")

    def run_algorithm(self):
        """Запускает алгоритм Беллмана-Форда."""
        try:
            src = int(self.src_input.text())

            if src >= len(self.vertices):
                raise ValueError("Неверный номер начальной вершины.")

            dist = self.graph.bellman_ford(src)
            if isinstance(dist, str):
                self.show_error("Ошибка", dist)
            else:
                result = "\n".join([f"Вершина {i}: расстояние {dist[i]}" for i in range(len(dist))])
                self.show_info("Результаты алгоритма", result)

            self.src_input.clear()

        except ValueError:
            self.show_error("Ошибка", "Введите корректный номер начальной вершины.")

    def show_error(self, title, message):
        """Показывает сообщение об ошибке."""
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle(title)
        error_dialog.setText(message)
        error_dialog.exec_()

    def show_info(self, title, message):
        """Показывает информационное сообщение."""
        info_dialog = QMessageBox(self)
        info_dialog.setIcon(QMessageBox.Information)
        info_dialog.setWindowTitle(title)
        info_dialog.setText(message)
        info_dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = GraphGUI()
    ex.show()
    sys.exit(app.exec_())
