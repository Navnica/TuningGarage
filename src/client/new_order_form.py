import flet
from src.database.models import Order, Vehicle, Service, ServiceOrder


class NewOrderForm(flet.SafeArea):
    def on_save_click(self):
        is_valid = True

        vehicle_dropdown: flet.Dropdown = self.content.controls[3].controls[0].controls[1]

        if not vehicle_dropdown.value:
            vehicle_dropdown.error_text = 'Поле пусто'
            is_valid = False

        else:
            vehicle_dropdown.error_text = ''

        vehicle_dropdown.update()

        for service in self.content.controls[3].controls[1].controls:
            service_dropdown: flet.Dropdown = service.controls[1]

            if not service_dropdown.value:
                service_dropdown.error_text = 'Поле пусто'
                is_valid = False

            else:
                service_dropdown.error_text = ''

            service_dropdown.update()

        if is_valid:
            new_order = Order.create(
                vehicle=Vehicle.get(Vehicle.id == vehicle_dropdown.value)
            )

            for service in self.content.controls[3].controls[1].controls:
                service_dropdown: flet.Dropdown = service.controls[1]

                ServiceOrder.create(
                    order=new_order,
                    service=Service.get(Service.id == service_dropdown.value)
                )

            self.parent.go_to_main_content()

    def on_add_service_click(self):
        self.content.controls[3].controls[1].controls.append(
            flet.Row(
                alignment=flet.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    flet.Text(
                        width=100,
                        value='Выбор услуги'
                    ),
                    flet.Dropdown(
                        options=[
                            flet.dropdown.Option(
                                text=service.name,
                                key=service.id
                            )
                            for service in Service.select()
                        ]
                    )
                ]
            ),
        )
        self.update()

    def build(self):
        self.expand = True
        self.content = flet.Column(
            scroll=flet.ScrollMode.AUTO,
            alignment=flet.MainAxisAlignment.START,
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            controls=[
                flet.Row(
                    controls=[
                        flet.IconButton(
                            icon=flet.icons.ARROW_BACK,
                            on_click=lambda _: self.parent.go_to_main_content()
                        ),
                        flet.TextButton(
                            text='Сформировать',
                            icon=flet.icons.SAVE,
                            on_click=lambda _: self.on_save_click()
                        )

                    ]
                ),
                flet.Text('Форма создания заказа'),
                flet.Divider(height=20),
                flet.Column(
                    controls=[
                        flet.Row(
                            alignment=flet.MainAxisAlignment.SPACE_AROUND,
                            controls=[
                                flet.Text(
                                    width=100,
                                    value='Выбор ТС'
                                ),
                                flet.Dropdown(
                                    options=[
                                        flet.dropdown.Option(
                                            text=vehicle.license_plate,
                                            key=vehicle.id
                                        )
                                        for vehicle in Vehicle.select()
                                    ]
                                )
                            ]
                        ),
                        flet.Column(
                            controls=[
                                flet.Row(
                                    alignment=flet.MainAxisAlignment.SPACE_AROUND,
                                    controls=[
                                        flet.Text(
                                            width=100,
                                            value='Выбор услуги'
                                        ),
                                        flet.Dropdown(
                                            options=[
                                                flet.dropdown.Option(
                                                    text=service.name,
                                                    key=service.id
                                                )
                                                for service in Service.select()
                                            ]
                                        )
                                    ]
                                ),
                            ]
                        ),
                        flet.Divider(height=20),
                        flet.Row(
                            alignment=flet.MainAxisAlignment.CENTER,
                            controls=[
                                flet.FilledButton(
                                    text='Добавить',
                                    icon=flet.icons.ADD,
                                    on_click=lambda _: self.on_add_service_click()
                                )
                            ]
                        )
                    ]
                )
            ]
        )
