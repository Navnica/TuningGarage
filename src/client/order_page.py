import flet
from src.database.models import Order, ServiceOrder, Service
from src.client.new_order_form import NewOrderForm
from peewee import fn
import openpyxl


class OrderPage(flet.SafeArea):
    main_content = None
    new_order_page = None

    def on_create_invoice_click(self, event: flet.ControlEvent):
        def on_result(file_picker_event: flet.FilePickerResultEvent):
            filepath = file_picker_event.path + '.xlsx'
            current_order = Order.get(Order.id == event.control.data)

            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = 'Счёт для ' + current_order.vehicle.license_plate

            ws.append([ws.title])
            ws.append(["Название услуги", "Цена (₽)"])

            services = (ServiceOrder
                        .select(Service.name, Service.price)
                        .join(Service)
                        .where(ServiceOrder.order == current_order))

            for service in services:
                ws.append([service.service.name, service.service.price])

            total_cost = (ServiceOrder
                          .select(fn.SUM(Service.price))
                          .join(Service)
                          .where(ServiceOrder.order == current_order)
                          .scalar() or 0)

            ws.append([])
            ws.append(["Итоговая стоимость", f"{total_cost}₽"])

            wb.save(filepath)

        current_order = Order.get(Order.id == event.control.data)

        self.page.overlay.clear()
        self.page.overlay.append(
            flet.FilePicker(
                on_result=on_result
            )
        )


        self.page.update()

        self.page.overlay[-1].save_file(
            file_name='Счёт для ' + current_order.vehicle.license_plate,
            file_type='xlsx'
        )

    def get_orders_list(self) -> list[flet.ExpansionPanel]:
        return [
            flet.ExpansionPanel(
                header=flet.ListTile(
                    title=flet.Text(
                        value='Заказ на ТС ' + str(order.vehicle.license_plate)
                    ),
                    leading=flet.Container(
                        padding=3,
                        border_radius=5,
                        bgcolor=flet.colors.SURFACE_TINT if order.done else flet.colors.GREEN,
                        content=flet.Text(
                            value='Выполнен' if order.done else 'Активен',
                            color=flet.colors.WHITE,
                            size=12,
                            width=80,
                            text_align=flet.TextAlign.CENTER
                        ),
                    ),
                    trailing=flet.TextButton(
                        text='Сформировать счёт',
                        icon=flet.icons.PRICE_CHANGE,
                        on_click=self.on_create_invoice_click,
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
                                    flet.Text(value=f"{(ServiceOrder.select(fn.SUM(Service.price))
                                                        .join(Service)
                                                        .where(ServiceOrder.order == order)
                                                        .scalar() or 0)}₽")
                                ]
                            ),
                            flet.Divider(height=10),
                            flet.Column(
                                controls=[
                                    flet.Row(
                                        alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            flet.Text(value=service.service.name),
                                            flet.Text(value=service.service.price + '₽')
                                        ]
                                    )

                                    for service in order.service_orders
                                ]
                            )
                        ]
                    )
                )
            )
            for order in Order.select()
        ]

    def go_to_main_content(self):
        self.new_order_page = None
        self.content = self.main_content
        self.main_content.controls[3].controls = self.get_orders_list()
        self.update()

    def on_new_order_click(self):
        self.new_order_page = NewOrderForm()
        self.content = self.new_order_page
        self.update()

    def build(self):
        self.main_content = flet.Column(
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            controls=[
                flet.Text(
                    value='Действующие заказы'
                ),
                flet.Divider(height=20),
                flet.Row(
                    alignment=flet.MainAxisAlignment.CENTER,
                    controls=[
                        flet.FilledButton(
                            text='Новый заказ',
                            icon=flet.icons.ADD,
                            on_click=lambda _: self.on_new_order_click()
                        ),
                        flet.TextButton(
                            icon=flet.icons.AUTORENEW,
                            text='Обновить',
                            on_click=lambda _: self.go_to_main_content()
                        )
                    ]
                ),
                flet.ExpansionPanelList(
                    controls=self.get_orders_list()
                )
            ]
        )

        self.expand = True
        self.content = self.main_content
