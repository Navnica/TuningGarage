import flet
from src.client.veihcle_page import VehiclePage


class MechanicForm(flet.SafeArea):
    def switch_page(self, event: flet.ControlEvent):
        pages = [
            'vehicle_page',
            'report_page',
        ]
        page_name = pages[int(event.data)]

        for page in self.content.controls:
            if not str(page.data).endswith('_page'):
                continue

            page.visible = page.data == page_name

        self.update()

    def build(self):
        self.expand = True
        self.content = flet.Row(
            vertical_alignment=flet.CrossAxisAlignment.START,
            controls=[
                flet.Container(
                    margin=-20,
                    content=flet.NavigationRail(
                        selected_index=0,
                        bgcolor=flet.colors.SURFACE_VARIANT,
                        height=3000,
                        on_change=self.switch_page,
                        destinations=[
                            flet.NavigationRailDestination(
                                label="Менеджер ТС",
                                icon=flet.icons.DIRECTIONS_CAR,
                            ),
                            flet.NavigationRailDestination(
                                label="Создание отчётов",
                                icon=flet.icons.ASSIGNMENT,
                            ),
                        ]
                    ),
                ),

                flet.VerticalDivider(width=20),
                VehiclePage(visible=True, data='vehicle_page'),
            ]
        )
