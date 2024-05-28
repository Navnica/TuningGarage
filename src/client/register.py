import flet
from src.database.models import User, UserAuth


class RegisterForm(flet.SafeArea):
    def on_register_click(self, event: flet.ControlEvent):
        login_field: flet.TextField = self.content.controls[1]
        password_field: flet.TextField = self.content.controls[2]
        password_field_confirm: flet.TextField = self.content.controls[3]

        is_valid = True

        for control in self.content.controls[1:-2]:
            if control.value == '':
                control.error_text = 'Поле пусто'
                is_valid = False

            else:
                control.error_text = ''

        if User.get_or_none(fullname=login_field.value):
            login_field.error_text = 'Имя занято'
            is_valid = False

        if password_field.value != password_field_confirm.value:
            password_field_confirm.error_text = 'Не совпадает с паролем'
            is_valid = False

        else:
            password_field_confirm.error_text = ''

        if not is_valid:
            self.update()
            return

        new_user = User.create(fullname=login_field.value, role=self.content.controls[4].value)
        UserAuth.create(user=new_user, login=login_field.value, password=password_field.value)

        self.update()
        self.page.session.get('switch_page')('login')

    def build(self):
        self.expand = True
        self.content = flet.Column(
            alignment=flet.MainAxisAlignment.CENTER,
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            controls=[
                flet.Row(
                    alignment=flet.MainAxisAlignment.START,
                    controls=[
                        flet.IconButton(
                            icon=flet.icons.ARROW_BACK,
                            on_click=lambda _: self.page.session.get('switch_page')('login')
                        )
                    ]
                ),
                flet.TextField(
                    label='Логин',
                ),
                flet.TextField(
                    label='Пароль',
                    password=True,
                    can_reveal_password=True,
                ),
                flet.TextField(
                    label='Подтверждение',
                    password=True,
                    can_reveal_password=True,
                ),

                flet.RadioGroup(
                    value='Механик',
                    content=flet.Column(
                        controls=[
                            flet.Radio(label='Механик', value='Механик'),
                            flet.Radio(label='Менеджер', value='Менеджер'),
                            flet.Radio(label='Директор', value='Директор')
                        ]
                    )
                ),
                flet.FilledButton(
                    text='Регистрация',
                    on_click=self.on_register_click
                ),
            ]
        )
