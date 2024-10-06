import flet as ft
import json
import random

def pick_random(products: list, current_product: {}) -> {}:
    selected = random.choice(products)
    while selected == current_product:
        selected = random.choice(products)
    return selected

def main(page: ft.Page):
    page.add(ft.Row([ft.Text("Combien coûte l'objet suivant ?", size=36)], alignment=ft.MainAxisAlignment.CENTER))
    image = ft.Image(random_product["src"], border_radius=30, scale=0.8)

    def button_click(e: ft.ControlEvent):
        if int(value.value) != random_product["price"]:
            dialog = ft.AlertDialog(True, ft.Text("Mauvais prix !", size=24), ft.Text("Souhaitez vous réessayer avec le même objet ?"), [ ft.TextButton("Oui", on_click=lambda _: close_alert_ok(dialog)), ft.TextButton("Je passe", on_click=lambda _: close_alert_pass(dialog))])
            page.dialog = dialog
            dialog.open = True
            page.update()
        else:
            dialog = ft.AlertDialog(True, ft.Text("Bravo !", size=24), ft.Text("Pour rejouer appuyez sur \"Rejouer\" ?"), [ ft.TextButton("Rejouer", on_click=lambda _: replay(dialog))])
            page.dialog = dialog
            dialog.open = True
            page.update()

    value = ft.TextField(value=0, border_radius=10, border_color="blue", keyboard_type=ft.KeyboardType.NUMBER, input_filter=ft.InputFilter(regex_string=r"^\d*$", allow=True, replacement_string=""), hint_text="Prix", on_submit=button_click)
    

    def replay(dialog: ft.AlertDialog):
        global random_product
        random_product = pick_random(data, random_product)
        image.src = random_product["src"]
        image.update()
        value.value = 0
        dialog.open = False
        page.update()

    def close_alert_ok(dialog: ft.AlertDialog):
        dialog.open = False
        page.update()

    def close_alert_pass(dialog: ft.AlertDialog):
        global random_product
        random_product = pick_random(data, random_product)
        image.src = random_product["src"]
        image.update()
        value.value = 0
        dialog.open = False
        page.update()

    def input_change(e: ft.ControlEvent):
        value.value = e.data
        page.update()
    
    def decrease(_):
        if int(value.value) > 0:
            value.value = int(value.value) - 1
            value.update()
    
    def increase(_):
        value.value = int(value.value) + 1
        value.update()

    value.on_change=input_change

    page.add(
        ft.Row(
            [
                image,
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.IconButton(ft.icons.REMOVE, on_click=decrease),
                                value,
                                ft.IconButton(ft.icons.ADD, on_click=increase),
                            ],
                        ),
                        ft.TextButton("J'achète", scale=1.2, style=ft.ButtonStyle(side=ft.BorderSide(color="blue", width=1), shape=ft.RoundedRectangleBorder(radius=5)), on_click=button_click)
                    ],
                    
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            ))
    

if __name__ == "__main__":
    with open("products.json") as f:
        data = json.load(f)
    random_product = pick_random(data, {})
    ft.app(main)
