import flet
from src.database.models import Service


class ServicePage(flet.SafeArea):
    def on_service_add_click(self, event: flet.ControlEvent):
        def on_save_click(event: flet.ControlEvent):
            if name_text_field.value == '' or price_text_field.value == '':
                if name_text_field.value == '':
                    name_text_field.error_text = 'Поле пусто'
                    name_text_field.update()
                else:
                    price_text_field.error_text = 'Поле пусто'
                    price_text_field.update()
            else:
                name_text_field.error_text = ''
                price_text_field.error_text = ''
                name_text_field.update()
                price_text_field.update()

                Service.create(
                    name=name_text_field.value,
                    price=price_text_field.value
                )

                self.page.overlay[-1].open = False
                self.update_service_list()
                self.page.update()

        name_text_field = flet.TextField(label='Название')
        price_text_field = flet.TextField(label='Цена')

        self.page.overlay.clear()
        self.page.overlay.append(
            flet.BottomSheet(
                open=True,
                content=flet.Container(
                    padding=20,
                    content=flet.Column(
                        alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
                        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                        controls=[
                            flet.Column(
                                controls=[
                                    name_text_field,
                                    price_text_field
                                ],
                                spacing=10
                            ),
                            flet.FilledButton(
                                text='Сохранить',
                                on_click=on_save_click
                            )
                        ]
                    )
                )
            )
        )

        self.page.update()

    def on_service_delete_click(self, event: flet.ControlEvent):
        def on_yes(event: flet.ControlEvent):
            Service.get(Service.id == event.control.data).delete_instance()
            self.update_service_list()
            self.page.dialog.open = False
            self.page.update()

        def on_no(event: flet.ControlEvent):
            self.page.dialog.open = False
            self.page.update()

        self.page.dialog = flet.AlertDialog(
            open=True,
            content=flet.Text('Вы уверены?'),
            actions=[
                flet.TextButton(text='Да', on_click=on_yes, data=event.control.data),
                flet.TextButton(text='Нет', on_click=on_no)
            ]
        )
        self.page.update()

    def update_service_list(self):
        self.service_list.controls = self.get_service_cards()
        self.service_list.update()

    def get_service_cards(self) -> list[flet.Control]:
        return [
            flet.Card(
                content=flet.Container(
                    padding=15,
                    content=flet.Row(
                        controls=[
                            flet.Column(
                                expand=True,
                                controls=[
                                    flet.Text(value='Услуга: ' + service.name),
                                    flet.Text(value=f'Цена: {service.price}₽'),
                                ]
                            ),

                            flet.Column(
                                alignment=flet.MainAxisAlignment.CENTER,
                                controls=[
                                    flet.IconButton(
                                        icon=flet.icons.DELETE,
                                        on_click=self.on_service_delete_click,
                                        data=service.id
                                    )
                                ]
                            )
                        ]
                    )
                ),
            ) for service in Service.select()
        ]

    def build(self):
        self.expand = True
        self.service_list = flet.Column(
            spacing=10,
            expand=True,
            controls=self.get_service_cards()
        )
        self.content = flet.Column(
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            controls=[
                flet.Text(value='Доступные услуги'),
                flet.Divider(height=20),
                flet.FilledButton(
                    text='Новая',
                    icon=flet.icons.ADD,
                    on_click=self.on_service_add_click
                ),
                self.service_list
            ],
        )

