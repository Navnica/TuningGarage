import flet
from src.database.models import Vehicle, Order


class VehiclePage(flet.SafeArea):
    def get_vehicles_data_rows(self) -> list[flet.DataRow]:
        return [
            flet.DataRow(
                cells=[
                    flet.DataCell(
                        content=flet.Row([flet.Text(vehicle.owner_name)], alignment=flet.MainAxisAlignment.CENTER)
                    ),
                    flet.DataCell(
                        content=flet.Row([flet.Text(vehicle.mark)], alignment=flet.MainAxisAlignment.CENTER)
                    ),
                    flet.DataCell(
                        content=flet.Row([flet.Text(vehicle.model)], alignment=flet.MainAxisAlignment.CENTER)
                    ),
                    flet.DataCell(
                        content=flet.Row([flet.Text(vehicle.year)], alignment=flet.MainAxisAlignment.CENTER)
                    ),
                    flet.DataCell(
                        content=flet.Row([
                            flet.IconButton(
                                icon=flet.icons.EDIT,
                                on_click=self.on_vehicle_edit_click,
                                data=vehicle.id
                            ),
                            flet.IconButton(
                                icon=flet.icons.DELETE,
                                on_click=self.on_vehicle_delete_click,
                                data=vehicle.id
                            )
                        ], alignment=flet.MainAxisAlignment.CENTER)
                    ),
                ]
            ) for vehicle in Vehicle.select()
        ]

    def on_vehicle_edit_click(self, event: flet.ControlEvent):
        vehicle: Vehicle = Vehicle.get(Vehicle.id == event.control.data)

        def on_vehicle_update_click(event: flet.ControlEvent):
            self.on_vehicle_create_click(event, update=True)

        self.page.overlay.clear()
        self.page.overlay.append(
            flet.BottomSheet(
                open=True,
                content=flet.Container(
                    padding=10,
                    content=flet.Column(
                        alignment=flet.MainAxisAlignment.START,
                        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                        controls=[
                            flet.Row(
                                alignment=flet.MainAxisAlignment.CENTER,
                                controls=[
                                    flet.TextField(
                                        label='ФИО Владельца',
                                        value=vehicle.owner_name
                                    ),
                                    flet.TextField(
                                        label='Марка ТС',
                                        value=vehicle.mark
                                    ),
                                ]
                            ),
                            flet.Row(
                                alignment=flet.MainAxisAlignment.CENTER,
                                controls=[
                                    flet.TextField(
                                        label='Модель ТС',
                                        value=vehicle.model
                                    ),
                                    flet.TextField(
                                        label='Год выпуска',
                                        value=vehicle.year
                                    ),
                                ]
                            ),
                            flet.Divider(height=10),
                            flet.FilledButton(
                                text='Сохранить',
                                on_click=on_vehicle_update_click,
                                data=vehicle.id
                            )
                        ]
                    )
                )
            )
        )

        self.page.update()

    def on_vehicle_delete_click(self, event: flet.ControlEvent):
        def on_yes(event: flet.ControlEvent):
            Vehicle.get(Vehicle.id == event.control.data).delete_instance()

            self.update_main_info()
            self.update_data_table()

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

    def update_data_table(self):
        self.content.controls[3].rows = self.get_vehicles_data_rows()
        self.update()

    def update_main_info(self):
        self.content.controls[0].content.controls[0].value = 'На данный момент числится ' + str(
            len(Vehicle.select())) + ' ТС.'
        self.content.controls[0].content.controls[1].value = 'Заказы действуют для ' + str(
            len(Order.select().where(Order.done != True))) + ' из них.'
        self.update()

    def on_vehicle_create_click(self, event: flet.ControlEvent, update=False): # Используется также для обновления
        is_valid = True
        text_fields = {}

        for control in self.page.overlay[-1].content.content.controls:
            if type(control) is flet.Row:
                for text_field in control.controls:
                    text_fields.update({text_field.label: text_field})

                    if text_field.value == '':
                        text_field.error_text = 'Поле пусто'
                        text_field.update()
                        is_valid = False

                    else:
                        text_field.error_text = ''
                        text_field.update()

        if not is_valid:
            return

        if not update:
            new_vehicle = Vehicle.create(
                owner_name=text_fields['ФИО Владельца'].value,
                mark=text_fields['Марка ТС'].value,
                model=text_fields['Модель ТС'].value,
                year=text_fields['Год выпуска'].value
            )
        else:
            vehicle: Vehicle = Vehicle.get(Vehicle.id == event.control.data)
            vehicle.update(
                owner_name=text_fields['ФИО Владельца'].value,
                mark=text_fields['Марка ТС'].value,
                model=text_fields['Модель ТС'].value,
                year=text_fields['Год выпуска'].value
            ).execute()

        self.page.overlay[-1].open = False
        self.page.update()
        self.update_main_info()
        self.update_data_table()

    def on_vehicle_add_click(self, event: flet.ControlEvent):
        self.page.overlay.clear()
        self.page.overlay.append(
            flet.BottomSheet(
                open=True,
                content=flet.Container(
                    padding=10,
                    content=flet.Column(
                        alignment=flet.MainAxisAlignment.START,
                        horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                        controls=[
                            flet.Row(
                                alignment=flet.MainAxisAlignment.CENTER,
                                controls=[
                                    flet.TextField(
                                        label='ФИО Владельца',
                                    ),
                                    flet.TextField(
                                        label='Марка ТС',
                                    ),
                                ]
                            ),
                            flet.Row(
                                alignment=flet.MainAxisAlignment.CENTER,
                                controls=[
                                    flet.TextField(
                                        label='Модель ТС',
                                    ),
                                    flet.TextField(
                                        label='Год выпуска',
                                    ),
                                ]
                            ),
                            flet.Divider(height=10),
                            flet.FilledButton(
                                text='Создать',
                                on_click=self.on_vehicle_create_click
                            )
                        ]
                    )
                )
            )
        )

        self.page.update()

    def build(self):
        self.expand = True
        self.content = flet.Column(
            expand=True,
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            controls=[
                flet.Container(
                    bgcolor=flet.colors.SURFACE_VARIANT,
                    border_radius=15,
                    padding=10,
                    content=flet.Column(
                        controls=[
                            flet.Text(
                                value='На данный момент числится ' + str(len(Vehicle.select())) + ' ТС.'
                            ),
                            flet.Text(
                                value='Заказы действуют для ' + str(
                                    len(Order.select().where(Order.done == True))) + ' из них.'),
                        ]
                    )
                ),
                flet.Divider(height=10),
                flet.FilledButton(
                    icon=flet.icons.ADD,
                    text='Добавить ТС',
                    on_click=self.on_vehicle_add_click
                ),
                flet.DataTable(
                    expand=True,

                    columns=[
                        flet.DataColumn(label=flet.Text('Владелец')),
                        flet.DataColumn(label=flet.Text('Марка')),
                        flet.DataColumn(label=flet.Text('Модель')),
                        flet.DataColumn(label=flet.Text('Год выпуска')),
                        flet.DataColumn(label=flet.Text('Редактирование')),
                    ],
                    rows=self.get_vehicles_data_rows()
                ),
            ],
        )
