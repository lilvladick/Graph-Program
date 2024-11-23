from flet import (
    Page,
    Text,
    TextField,
    ElevatedButton,
    Dropdown,
    Row,
    Column,
    ListView,
    Container,
    Image,
    SnackBar,
    alignment,
    padding,
    Colors,
    FontWeight,
)
import flet as ft
import matplotlib.pyplot as plt
import io
import base64
from typing import cast
from graph import Graph

def main(page: Page):
    page.title = "Антикризисное финансовое планирование"
    page.theme_mode = "light"

    graph = Graph(0)
    vertices_input = TextField(label="Количество задач (вершин)", width=200)
    edges_list = ListView(expand=1, spacing=5, padding=padding.all(10))
    source_input = TextField(label="Начальная задача (вершина)", width=200)
    result_view = Container(
        content=Text("Результат появится здесь", size=14),
        padding=10,
        bgcolor=Colors.LIGHT_GREEN_100,
    )
    graph_image = Container(
        content=Image(src_base64=None, width=500, height=300, fit=ft.ImageFit.CONTAIN),
        height=300,
        alignment=alignment.center,
    )

    def show_snackbar(message, bgcolor=None):
        snackbar = SnackBar(content=Text(message), bgcolor=bgcolor)
        page.overlay.append(snackbar)
        snackbar.open = True
        page.update()

    def update_dropdowns(num_vertices):
        """Обновляет выпадающие списки для выбора вершин."""
        options = [ft.dropdown.Option(str(i)) for i in range(num_vertices)]
        cast(Dropdown, edges_input.controls[0]).options = options
        cast(Dropdown, edges_input.controls[1]).options = options
        page.update()

    def set_graph(e):
        """Устанавливает новое количество вершин и сбрасывает граф."""
        try:
            num_vertices = int(vertices_input.value)
            if num_vertices < 1:
                raise ValueError
            graph.V = num_vertices
            graph.graph = []
            edges_list.controls.clear()
            update_dropdowns(num_vertices)
            show_snackbar(f"Граф с {num_vertices} задачами создан.")
        except ValueError:
            show_snackbar("Введите корректное число вершин!", bgcolor=Colors.ERROR)

    def add_edge(e):
        """Добавляет ребро в граф."""
        if graph.V == 0:
            show_snackbar("Сначала создайте граф!", bgcolor=Colors.ERROR)
            return
        try:
            u = int(cast(ft.Dropdown, edges_input.controls[0]).value)
            v = int(cast(ft.Dropdown, edges_input.controls[1]).value)
            w = float(cast(ft.TextField, edges_input.controls[2]).value)
            if u < 0 or u >= graph.V or v < 0 or v >= graph.V:
                raise ValueError
            graph.add_edge(u, v, w)
            edges_list.controls.append(Text(f"Ребро: {u} -> {v} (вес: {w})"))
            page.update()
        except ValueError:
            show_snackbar("Введите корректные данные для ребра!", bgcolor=Colors.ERROR)

    def calculate(e):
        """Запускает алгоритм Беллмана-Форда."""
        if graph.V == 0 or not graph.graph:
            show_snackbar("Сначала создайте граф и добавьте рёбра!", bgcolor=Colors.ERROR)
            return
        try:
            src = int(source_input.value)
            result = graph.bellman_ford(src)
            if isinstance(result, str):
                result_view.content = Text(result, color=Colors.RED)
            else:
                result_view.content = Text(
                    "Минимальные расстояния: " + ", ".join(map(str, result))
                )
                draw_graph(result)
            page.update()
        except ValueError:
            show_snackbar(
                "Введите корректный индекс начальной задачи!", bgcolor=Colors.ERROR
            )

    def draw_graph(data):
        """Создаёт график минимальных расстояний."""
        import matplotlib
        matplotlib.use('Agg')

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(range(len(data)), data, marker="o", color="blue")
        ax.set_title("Минимальные расстояния от начальной задачи")
        ax.set_xlabel("Задачи")
        ax.set_ylabel("Затраты")

        with io.BytesIO() as buf:
            plt.savefig(buf, format="png")
            buf.seek(0)
            encoded_image = base64.b64encode(buf.getvalue()).decode("ascii")

        graph_image.content = Image(
            src_base64=encoded_image,
            fit=ft.ImageFit.CONTAIN,
            width=500,
            height=300,
        )
        plt.close(fig)
        page.update()

    edges_input = Row(
        controls=[
            Dropdown(width=100, options=[]),
            Dropdown(width=100, options=[]),
            TextField(label="Вес", width=100),
        ]
    )

    page.add(
        Column(
            controls=[
                Text("Антикризисное планирование", size=20, weight=FontWeight.BOLD),
                Row(
                    controls=[
                        vertices_input,
                        ElevatedButton("Создать граф", on_click=set_graph),
                    ]
                ),
                Row(
                    controls=[
                        edges_input,
                        ElevatedButton("Добавить ребро", on_click=add_edge),
                    ]
                ),
                Text("Список рёбер:"),
                edges_list,
                Row(
                    controls=[
                        source_input,
                        ElevatedButton("Вычислить", on_click=calculate),
                    ]
                ),
                result_view,
                graph_image,
            ],
            spacing=10,
            scroll=ft.ScrollMode.ALWAYS
        )
    )


ft.app(target=main)
