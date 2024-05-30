import flet
import datetime
from src.database.models import Report


class NewReportForm(flet.SafeArea):
    def on_send_click(self, event: flet.ControlEvent):
        def on_ok_click(event: flet.ControlEvent):
            self.page.dialog.open = False
            self.page.update()

        Report.create(
            from_user=self.page.session.get('user'),
            title=self.content.controls[2].value,
            text=self.content.controls[-1].value,
        )

        self.page.dialog = flet.AlertDialog(
            open=True,
            content=flet.Text('Отчёт отправлен'),
            actions=[
                flet.FilledButton(
                    text='Ок',
                    on_click=on_ok_click
                )
            ]
        )
        self.page.update()

    def build(self):
        self.expand = True
        self.content = flet.Column(
            expand=True,
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            controls=[
                flet.TextButton(
                    text='Отправить',
                    icon=flet.icons.SEND,
                    on_click=self.on_send_click
                ),
                flet.Divider(height=20),
                flet.TextField(
                    value='Отчёт о проделанной работе от ' + self.page.session.get('user').fullname,
                    read_only=True
                ),
                flet.TextField(
                    value=str(datetime.datetime.now().replace(second=0, microsecond=0)),
                    read_only=True
                ),
                flet.Divider(height=20),
                flet.Text('Текст отчёта'),
                flet.TextField(
                    multiline=True,
                    expand=True,
                    min_lines=40
                )
            ]
        )
