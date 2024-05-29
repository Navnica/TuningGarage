import flet
from src.database.models import UserAuth
from src.client.manager import ManagerForm
from src.client.mechanic import MechanicForm


class LoginForm(flet.SafeArea):
    def on_login_click(self, event: flet.ControlEvent):
        is_valid = True
        login_field: flet.TextField = self.content.controls[0]
        password_field: flet.TextField = self.content.controls[1]

        for control in self.content.controls[:2]:
            if control.value == '':
                control.error_text = 'Поле пусто'
                is_valid = False

            else:
                control.error_text = ''

        if not is_valid:
            self.update()
            return

        user_auth = UserAuth.get_or_none(login=login_field.value, password=password_field.value)

        if not user_auth:
            login_field.error_text = 'Логин'
        else:
            self.page.session.set('user', user_auth.user)

            if user_auth.user.role == 'Механик':
                self.page.controls[0].controls.append(MechanicForm(visible=False, data='mechanic'))
                self.page.session.get('switch_page')('mechanic')
            else:
                self.page.controls[0].controls.append(ManagerForm(visible=False, data='manager'))
                self.page.session.get('switch_page')('manager')

        self.update()

    def build(self):
        self.expand = True
        self.content = flet.Column(
            alignment=flet.MainAxisAlignment.CENTER,
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            controls=[
                flet.TextField(
                    label='Логин',
                ),
                flet.TextField(
                    label='Пароль',
                    password=True,
                    can_reveal_password=True,
                ),
                flet.FilledButton(
                    text='Войти',
                    on_click=self.on_login_click,
                ),

                flet.FilledButton(
                    text='Регистрация',
                    on_click=lambda _: self.page.session.get('switch_page')('register')
                )
            ]
        )
