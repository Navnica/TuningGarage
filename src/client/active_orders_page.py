import flet
from src.database.models import Order


class ActiveOrdersPage(flet.SafeArea):
    def get_orders_list(self) -> list[flet.ExpansionPanel]:
        def mark_done(event: flet.ControlEvent):
            order = Order.get(Order.id == event.control.data)
            order.done = True
            order.save()

            self.on_update_click(event)

        return [
            flet.ExpansionPanel(
                header=flet.ListTile(
                    title=flet.Text(
                        value='Заказ на ТС ' + str(order.vehicle.license_plate)
                    ),
                    trailing=flet.TextButton(
                        text='Пометить выполненным',
                        icon=flet.icons.CHECK,
                        on_click=mark_done,
                        data=order.id
                    )
                ),
                content=flet.Container(
                    padding=20,
                    content=flet.Column(
                        controls=[
                            flet.Row(
                                alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    flet.Text(value='Перечень услуг'),
                                ]
                            ),
                            flet.Divider(height=10),
                            flet.Column(
                                controls=[
                                    flet.Row(
                                        alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            flet.Text(value=service.service.name)
                                        ]
                                    )

                                    for service in order.service_orders
                                ]
                            )
                        ]
                    )
                )
            )
            for order in Order.select().where(Order.done == False)
        ]

    def on_update_click(self, event: flet.ControlEvent):
        self.content.controls[3].controls = self.get_orders_list()
        self.update()

    def build(self):
        self.expand = True
        self.content = flet.Column(
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            controls=[
                flet.Text(
                    value='Действующие заказы'
                ),
                flet.Divider(height=20),
                flet.Row(
                    alignment=flet.MainAxisAlignment.CENTER,
                    controls=[
                        flet.TextButton(
                            icon=flet.icons.AUTORENEW,
                            text='Обновить',
                            on_click=self.on_update_click
                        )
                    ]
                ),
                flet.ExpansionPanelList(
                    controls=self.get_orders_list()
                )
            ]
        )



