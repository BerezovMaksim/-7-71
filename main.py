import flet as ft
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
def main(page: ft.Page):
    diseases = ["ОРВИ", "Коронавирус", "Грипп", "Корь", "Пневмония", "Коклюш", "Бронхит"]
    user_answers = {
        "cough": None,
        "runny_nose": None,
        "headache": None,
        "weakness": None,
        "breathing_difficulty": None,
        "smell_taste_loss": None,
        "temperature": None
    }
    page.bgcolor = "white"
    color = "black"
    page.title = "Диагностика заболеваний"
    page.update()
    def calculate_probabilities():
        probabilities = {
            "ОРВИ": 30,
            "Коронавирус": 20,
            "Грипп": 25,
            "Корь": 5,
            "Пневмония": 10,
            "Коклюш": 5,
            "Бронхит": 5
        }
        if user_answers["cough"] == "dry":
            probabilities["Коронавирус"] += 15
            probabilities["Грипп"] += 10
            probabilities["ОРВИ"] += 5
        elif user_answers["cough"] == "wet":
            probabilities["Бронхит"] += 15
            probabilities["Пневмония"] += 10
            probabilities["ОРВИ"] += 5
        if user_answers["runny_nose"] == "yes":
            probabilities["ОРВИ"] += 15
            probabilities["Грипп"] += 5
        elif user_answers["runny_nose"] == "congestion":
            probabilities["Коронавирус"] += 10
        if user_answers["headache"] == "yes":
            probabilities["Грипп"] += 10
            probabilities["Коронавирус"] += 5
        if user_answers["weakness"] == "yes":
            probabilities["Грипп"] += 10
            probabilities["Коронавирус"] += 5
            probabilities["Пневмония"] += 5
        if user_answers["breathing_difficulty"] == "yes":
            probabilities["Пневмония"] += 15
            probabilities["Коронавирус"] += 10
            probabilities["Бронхит"] += 5
        if user_answers["smell_taste_loss"] == "yes":
            probabilities["Коронавирус"] += 25
        if user_answers["temperature"] is not None:
            temp = user_answers["temperature"]
            if temp > 37.5:
                probabilities["Грипп"] += 10
                probabilities["Пневмония"] += 5
                probabilities["Коронавирус"] += 5
            if temp > 38.5:
                probabilities["Грипп"] += 5
                probabilities["Пневмония"] += 5
        total = sum(probabilities.values())
        for disease in probabilities:
            probabilities[disease] = round(probabilities[disease] / total * 100)
        diff = 100 - sum(probabilities.values())
        if diff != 0:
            max_disease = max(probabilities, key=probabilities.get)
            probabilities[max_disease] += diff
        return probabilities
    def change_background(color_name):
        page.bgcolor = color_name
        page.update()
    def settings_window(e):
        page.clean()
        color_buttons = ft.Row(
            [
                ft.ElevatedButton(
                    "Синий", on_click=lambda e: change_background("lightblue"),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_100)
                ),
                ft.ElevatedButton(
                    "Зелёный", on_click=lambda e: change_background("lightgreen"),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_100)
                ),
                ft.ElevatedButton(
                    "Белый", on_click=lambda e: change_background("white"),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.WHITE)
                ),
                ft.ElevatedButton(
                    "Жёлтый", on_click=lambda e: change_background("yellow"),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.YELLOW_100)
                ),
                ft.ElevatedButton(
                    "Красный", on_click=lambda e: change_background("#ffcccc"),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.RED_100)
                ),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER
        )
        page.add(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "← Назад",
                                on_click=main_window,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    bgcolor=ft.Colors.BLUE_500,
                                    color="white"
                                )
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START
                    ),
                    ft.Divider(height=20),
                    ft.Text("Выберите цвет фона:", size=20, color="black"),
                    ft.Divider(height=10),
                    color_buttons,
                    ft.Divider(height=30),
                    ft.ElevatedButton(
                        "Вернуться в главное меню",
                        on_click=main_window,
                        width=300,
                        height=50,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            bgcolor=ft.Colors.BLUE_500,
                            color="white"
                        )
                    )
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        )
        page.update()
    def one_window(e):
        page.clean()
        cough_group = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="dry", label="Да, сухой кашель", fill_color="blue"),
                ft.Radio(value="wet", label="Да, влажный кашель", fill_color="blue"),
                ft.Radio(value="none", label="Нет", fill_color="blue")
            ]),
            on_change=lambda e: user_answers.update({"cough": e.control.value})
        )
        runny_nose_group = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="yes", label="Да", fill_color="blue"),
                ft.Radio(value="congestion", label="Нет, но есть заложенность носа", fill_color="blue"),
                ft.Radio(value="none", label="Нет", fill_color="blue"),
            ]),
            on_change=lambda e: user_answers.update({"runny_nose": e.control.value})
        )
        headache_group = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="yes", label="Да", fill_color="blue"),
                ft.Radio(value="no", label="Нет", fill_color="blue"),
            ]),
            on_change=lambda e: user_answers.update({"headache": e.control.value})
        )
        weakness_group = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="yes", label="Да", fill_color="blue"),
                ft.Radio(value="no", label="Нет", fill_color="blue"),
            ]),
            on_change=lambda e: user_answers.update({"weakness": e.control.value})
        )
        breathing_group = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="yes", label="Да", fill_color="blue"),
                ft.Radio(value="no", label="Нет", fill_color="blue"),
            ]),
            on_change=lambda e: user_answers.update({"breathing_difficulty": e.control.value})
        )
        smell_group = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="yes", label="Да", fill_color="blue"),
                ft.Radio(value="no", label="Нет", fill_color="blue"),
            ]),
            on_change=lambda e: user_answers.update({"smell_taste_loss": e.control.value})
        )
        def create_question_card(title, control):
            return ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(title, size=16, weight="bold", color="black"),
                        control
                    ], spacing=10),
                    padding=15
                ),
                elevation=5,
                width=300
            )
        # Строки, отвечающие за прокрутку:
        # scroll=ft.ScrollMode.AUTO - включает автоматическую прокрутку
        # expand=True - позволяет контейнеру расширяться
        content_column = ft.Column(
            [
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "← Назад",
                            on_click=main_window,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                bgcolor=ft.Colors.BLUE_500,
                                color="white"
                            )
                        ),
                        ft.ElevatedButton(
                            "Далее →",
                            on_click=two_window,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                bgcolor=ft.Colors.BLUE_500,
                                color="white"
                            )
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Divider(height=20),
                ft.Row(
                    [
                        create_question_card("1. У вас есть кашель?", cough_group),
                        create_question_card("2. У вас есть насморк?", runny_nose_group)
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    [
                        create_question_card("3. У вас есть головная боль?", headache_group),
                        create_question_card("4. У вас есть слабость?", weakness_group)
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    [
                        create_question_card("5. У вас есть затруднения дыхания?", breathing_group),
                        create_question_card("6. У вас есть потери обоняния и вкуса?", smell_group)
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Divider(height=20),
                ft.ElevatedButton(
                    "Продолжить",
                    on_click=two_window,
                    width=300,
                    height=50,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        bgcolor=ft.Colors.BLUE_500,
                        color="white"
                    )
                )
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,  # Это строка включает прокрутку
            expand=True  # Это позволяет колонке расширяться и занимать доступное пространство
        )
        page.add(content_column)
        page.update()
    def two_window(e):
        error_text = ft.Text("", color="red")
        next_button = ft.ElevatedButton("Показать результаты", on_click=chart_window, visible=False)
        def save_temperature(e):
            try:
                temp = float(temperature_field.value)
                if 35 <= temp <= 43:
                    user_answers["temperature"] = temp
                    error_text.value = ""
                    next_button.visible = True
                else:
                    error_text.value = "Такой температуры у человека не может быть."
                    next_button.visible = False
            except ValueError:
                error_text.value = "Пожалуйста, введите число"
                next_button.visible = False
            page.update()
        temperature_field = ft.TextField(
            label="Введите температуру (например: 36.6)",
            icon=ft.Icons.THERMOSTAT,
            width=300,
            on_change=save_temperature
        )
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "← Назад",
                                on_click=one_window,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    bgcolor=ft.Colors.BLUE_500,
                                    color="white"
                                )
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START
                    ),
                    ft.Divider(height=30),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("7. Какая у вас температура?", size=18, weight="bold", color="black"),
                                ft.Divider(height=10),
                                temperature_field,
                                error_text,
                                ft.Divider(height=20),
                                ft.ElevatedButton(
                                    "Сохранить температуру",
                                    on_click=save_temperature,
                                    width=300,
                                    height=50,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                        bgcolor=ft.Colors.BLUE_500,
                                        color="white"
                                    )
                                ),
                                ft.Divider(height=20),
                                next_button
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10
                        ),
                        alignment=ft.alignment.center,
                        width=400
                    )
                ],
                spacing=20,
                expand=True
            )
        )
    def chart_window(e):
        probabilities = calculate_probabilities()
        diseases = list(probabilities.keys())
        data = list(probabilities.values())
        fig = plt.figure(figsize=(10, 7))
        plt.pie(
            data,
            labels=diseases,
            autopct='%1.1f%%',
            startangle=90,
            shadow=True,
            explode=[0.1 if d == max(data) else 0 for d in data],
            colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6', '#ff6666']
        )
        plt.title('Вероятность заболеваний', pad=20)
        plt.axis('equal')
        plt.tight_layout()
        plt.show()
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "← Назад",
                                on_click=main_window,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    bgcolor=ft.Colors.BLUE_500,
                                    color="white"
                                )
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START
                    ),
                    ft.Divider(height=30),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Диаграмма отображается в отдельном окне", size=18, color="black"),
                                ft.Divider(height=30),
                                ft.ElevatedButton(
                                    "Вернуться в главное меню",
                                    on_click=main_window,
                                    width=300,
                                    height=50,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                        bgcolor=ft.Colors.BLUE_500,
                                        color="white"
                                    )
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        alignment=ft.alignment.center
                    )
                ],
                expand=True
            )
        )
    def main_window(e):
        page.clean()
        for key in user_answers:
            user_answers[key] = None
        page.add(
            ft.Column(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Диагностика болезни",
                                    style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD),
                                    text_align=ft.TextAlign.CENTER,
                                    color=ft.Colors.BLUE_800
                                ),
                                ft.Divider(height=30),
                                ft.Image(
                                    src="https://cdn-icons-png.flaticon.com/512/2964/2964488.png",
                                    width=150,
                                    height=150,
                                    fit=ft.ImageFit.CONTAIN
                                ),
                                ft.Divider(height=30),
                                ft.ElevatedButton(
                                    "Начать диагностику",
                                    on_click=one_window,
                                    width=250,
                                    height=50,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                        bgcolor=ft.Colors.BLUE_700,
                                        color="white",
                                        padding=15,
                                        elevation=5
                                    )
                                ),
                                ft.Divider(height=10),
                                ft.ElevatedButton(
                                    "Настройки",
                                    on_click=settings_window,
                                    width=250,
                                    height=50,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                        bgcolor=ft.Colors.BLUE_500,
                                        color="white",
                                        padding=15,
                                        elevation=5
                                    )
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        alignment=ft.alignment.center,
                        expand=True
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            )
        )
        page.update()
    main_window(None)
ft.app(target=main)
