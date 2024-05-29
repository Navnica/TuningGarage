import flet
from src.client.forms import *


def main(page: flet.Page):
    def switch_page(page_name: str):
        for control in page.controls[0].controls:
            control.visible = control.data == page_name

        page.update()

    page.session.set('switch_page', switch_page)

    page.title = 'Тюнинг гараж'
    page.window_center()
    page.padding = 20
    page.expand = True

    page.add(
        flet.Column(
            expand=True,
            controls=[
                LoginForm(data='login'),
                RegisterForm(visible=False, data='register'),
            ]
        )
    )


if __name__ == '__main__':
    flet.app(main)
