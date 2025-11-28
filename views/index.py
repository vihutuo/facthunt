import random

import flet as ft
from modules import users_manager as um
from modules import log
from modules import player_name_ctrl
from modules import mytimer
from modules import question_manager

ROUND_TIME = 30
QM = question_manager.QuestionManager(ROUND_TIME)


def IndexView(page:ft.Page, params):
    def page_on_connect(e):
        log.info("Session connect")
        UM.add_user(page.session_id,player_name)
        if not main_timer.running:
            log.info("On connect new round started")
            new_round()


    def page_on_disconnect(e):
        print("Session disconnect")
        UM.remove_user(page.session_id)


    def on_pubsub(msg):
        log.info("Pubsub msg received" + msg)
        msg_list = msg.split("|")
        if msg_list[0] == "UM":

            user_count_txt.value = UM.get_user_count()
            page.update()
        elif msg_list[0] == "Answer Found":
            show_answers()


    page.pubsub.subscribe(on_pubsub)
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
                ft.Text("Online : "),
                ft.Container(
                    content=user_count_txt,
                    margin=ft.margin.only(right=20)  # ✅ Right margin
                )


            ],
        )
        return app_bar

    def restart_clicked(e):
         dlg = ft.AlertDialog(title=ft.Text("You clicked restart"))
         page.open(dlg)
    def show_high_scores(e=None):
        main_timer.start(6, new_round)
        scores_dialog.content = get_high_score_table()
        page.open(scores_dialog)



    def get_high_score_table():
        # print("Drawinh HS table")

        # print(data)
        tbl = ft.DataTable(columns=[

            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Score"), numeric=True),
        ],
            heading_row_height=0,
            column_spacing=50,
            rows=[]
        )

        high_scores = []
        print(set(QM.question.first_correct))
        for user_name in set(QM.question.first_correct):
                print(f"{user_name=}")
                if user_name is None:
                    continue
               # score = UM.get_score_by_username(user_name)
                try:
                    score = UM.get_score_by_username(user_name)
                    print(f"{score=}")

                except Exception as e:
                       log.warn("username not found " + user_name)
                else:
                       high_scores.append([user_name,score])

        print(f"{high_scores=}")
        high_scores.sort(reverse=True, key=lambda e : e[1])


        for  name, score in high_scores:
               tbl.rows.append( ft.DataRow(
                                           cells=[

                                               ft.DataCell(ft.Text(name)),
                                               ft.DataCell(ft.Text(score)),
                                           ]))



        return tbl

    def player_name_changed(new_name):
       UM.update_user(page.session_id, username=new_name)
       print("Playername updated", player_name_control.player_name)

    def show_answers():
        all_answers_done = True
        for i in range(len(QM.question.first_correct)):
            if QM.question.first_correct[i] is not None:
                print("i=", i)
                print("LEn =", len(answer_textboxes))
                answer_textboxes[i].opacity = 1
                answer_msg_boxes[i].value = QM.question.first_correct[i]
            else:
                all_answers_done = False
        if all_answers_done:
            main_timer.set_time_remaining(3)
            #show_high_scores()


        page.update()
    def update_score_ui(score):
          score_text.value = f"Score : {score}"
    def submit_clicked(e):
        if not QM.question:
            return
        user_answer = user_input_box.value
        idx = QM.submit_answer(player_name_control.player_name,user_answer)

        if idx >= 0:
            #answer correct
            user_input_box.value = ""
            user_input_box.focus()
            if idx == 0:
                UM.add_score(page.session_id, 15)
            else:
                UM.add_score(page.session_id, 10)
            score = UM.get_user(page.session_id).score
            update_score_ui(score)
            page.pubsub.send_all(f"Answer Found|{idx}")
            show_answers()
        print(QM.question)
        page.update()

    def round_end(e):
        log.info("Round end")
        new_round()
    def new_round(e=None):
        log.info("In new round")
        q = QM.get_question()
        scores_dialog.open = False
        UM.get_user(page.session_id).score = 0

        question_txt.value = q.question
        answer_textboxes.clear()
        answer_msg_boxes.clear()
        answer_column.controls.clear()
        time_remaining = QM.get_time_remaining()
        print(f"{time_remaining=}")
        main_timer.start(time_remaining, show_high_scores)

        for i, answer  in enumerate(q.answers):
            a = ft.Text(answer, size=22, opacity=0, animate_opacity=700)
            msg  = ft.Text("", size=16, opacity=1, animate_opacity=700, font_family="smoochsans", color="#00C8FF"  )
            number_circle = ft.Container(
                content=ft.Text(i + 1, size=18, weight="bold", text_align=ft.TextAlign.CENTER),
                width=32,
                height=32,
                bgcolor=ft.Colors.SECONDARY_CONTAINER,
                border_radius=16,  # Half of width/height for perfect circle
                alignment=ft.alignment.center,
            )
            r = ft.Row(controls=[number_circle, a,msg])
            answer_column.controls.append(r)
            answer_textboxes.append(a)
            answer_msg_boxes.append(msg)

        update_score_ui(0)
        show_answers()
        page.update()


    #main start
    question_data = { }

    question_txt = ft.Text(size=28)
    user_input_box = ft.TextField(label="Type here", on_submit=submit_clicked)
    answer_column = ft.Column()
    answer_textboxes = []
    answer_msg_boxes = []
    user_count_txt = ft.Text(value="0", style=ft.TextThemeStyle.LABEL_LARGE)  # used in AppBar

    appbar = CreateAppBar()
    div = ft.Divider(height=20)
    player_name = "Player" + str(random.randrange(1, 1000))
    UM = um.UserManager(page)
    UM.add_user(page.session_id, player_name)



    player_name_control = player_name_ctrl.PlayerNameControl(player_name,player_name_changed)
    score_text=ft.Text("0",style=ft.TextStyle(size=20), )
    update_score_ui(0)
    main_timer = mytimer.Countdown()
    icon_timer = ft.Icon(name=ft.Icons.SCHEDULE, color=ft.Colors.SECONDARY)
    line_1 = ft.Divider(height=1, color=ft.Colors.SECONDARY_CONTAINER)

    scores_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Scores"),
        content=ft.Text(""),
        actions_alignment=ft.MainAxisAlignment.END
    )


    score_row=ft.Row(controls=[player_name_control,    score_text,  ft.Row(controls=[icon_timer,main_timer], width = 80)],
                     alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    content_column = ft.Column(controls=[score_row,question_txt,answer_column,div,user_input_box],
                               width= min([page.width,600]))

    page.views.append(ft.View(
        "/",
        [appbar,  content_column],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO
    )
    )
    page.update()
    page.on_disconnect = page_on_disconnect
    page.on_connect = page_on_connect
    new_round()
