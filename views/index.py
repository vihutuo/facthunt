import flet as ft

def IndexView(page:ft.Page, params):
    def CreateAppBar():
        app_bar = ft.AppBar(
            leading=ft.Image("images/csc_logo_100.png"),
            leading_width=40,
            title=ft.Text("Fact Hunt"),
            #center_title=False,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            actions=[
                ft.IconButton(ft.Icons.RESTART_ALT, on_click=restart_clicked),
                ft.IconButton(ft.Icons.FILTER_3),

            ],
        )
        return app_bar

    def restart_clicked(e):
         dlg = ft.AlertDialog(title=ft.Text("You clicked restart"))
         page.open(dlg)


    def submit_clicked(e):
        user_answer = user_input_box.value
        if user_answer in question_data["answers"]:
            i = question_data["answers"].index(user_answer)
            answer_textboxes[i].opacity = 1
        page.update()
    def new_question():
        question_data["question"] = "Name the 5 largest countries"
        question_data["answers"] = ["Russia", "Canada", "China", "USA", "Brazil"]
        nonlocal  answers_count
        answers_count = len(question_data["answers"])
        question_txt.value = question_data["question"]
        answer_textboxes.clear()

        for i in range(answers_count):
            answer = question_data["answers"][i]
            a = ft.Text(answer, size=22, opacity=0, animate_opacity=700)
            number_circle = ft.Container(
                content=ft.Text(i + 1, size=18, weight="bold", text_align=ft.TextAlign.CENTER),
                width=32,
                height=32,
                bgcolor=ft.Colors.SECONDARY_CONTAINER,
                border_radius=16,  # Half of width/height for perfect circle
                alignment=ft.alignment.center,
            )
            r = ft.Row(controls=[number_circle, a])
            answer_column.controls.append(r)
            answer_textboxes.append(a)


    question_data = {"question" : "",
                     "answers" : []
                     }
    answers_count= 0
    question_txt = ft.Text(size=28)
    user_input_box = ft.TextField(label="Type here",on_submit=submit_clicked)
    answer_column = ft.Column()
    answer_textboxes = []
    new_question()

    appbar = CreateAppBar()
    div = ft.Divider(height=20)

    content_column = ft.Column(controls=[question_txt,answer_column,div,user_input_box],
                               width= min([page.width,600]))
    page.views.append(ft.View(
        "/",
        [appbar, content_column],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    )
    page.update()
