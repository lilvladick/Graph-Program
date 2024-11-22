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
    border,
    Colors,
    FontWeight,
)
import flet as ft
import matplotlib.pyplot as plt
import io
import base64
from typing import cast
from graph import Graph  # Убедитесь, что модуль `graph` доступен

def main(page: Page):
    page.title = "Антикризисное финансовое планирование"
    page.theme_mode = "light"

    graph = Graph(0)  # Изначально пустой граф
    vertices_input = TextField(label="Количество задач (вершин)", width=200)
    edges_list = ListView(expand=1, spacing=5, padding=padding.all(10))
    source_input = TextField(label="Начальная задача (вершина)", width=200)
    result_view = Container(
        content=Text("Результат появится здесь", size=14),
        padding=10,
        bgcolor=Colors.LIGHT_GREEN_100,
    )
    graph_image = Container(
        content=Text("График появится здесь"),
        height=300,
        alignment=alignment.center,
    )

    def show_snackbar(message, bgcolor=None):
        snackbar = SnackBar(content=Text(message), bgcolor=bgcolor)
        page.overlay.append(snackbar)
        snackbar.open = True
        page.update()

    def set_graph(e):
        try:
            num_vertices = int(vertices_input.value)
            if num_vertices < 1:
                raise ValueError
            graph.V = num_vertices
            show_snackbar(f"Граф с {num_vertices} задачами создан.")
        except ValueError:
            show_snackbar("Введите корректное число вершин!", bgcolor=Colors.ERROR)

    def add_edge(e):
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
        try:
            src = int(source_input.value)
            result = graph.bellman_ford(src)
            if isinstance(result, str):
                result_view.content = Text(result, color=Colors.RED)
            else:
                result_view.content = Text(
                    "Минимальные расстояния: " + ", ".join(map(str, result))
                )
                draw_graph(result)  # Рисуем график
            page.update()
        except ValueError:
            show_snackbar(
                "Введите корректный индекс начальной задачи!", bgcolor=Colors.ERROR
            )

    def draw_graph(data):
        fig, ax = plt.subplots()
        ax.plot(range(len(data)), data, marker="o", color="blue")
        ax.set_title("Минимальные расстояния от начальной задачи")
        ax.set_xlabel("Задачи")
        ax.set_ylabel("Затраты")
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        encoded_image = base64.b64encode(buf.getvalue()).decode("ascii")
        graph_image.content = Image(
            src_base64=encoded_image,
            fit=ft.ImageFit.CONTAIN,
        )
        buf.close()
        page.update()

    edges_input = Row(
        controls=[
            Dropdown(width=100, options=[ft.dropdown.Option(str(i)) for i in range(10)]),
            Dropdown(width=100, options=[ft.dropdown.Option(str(i)) for i in range(10)]),
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
        )
    )


ft.app(target=main)
