import base64
from streamlit_card import card


def nav_card(image: str, title: str, subtitle: str, on_click):
    with open(image, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data)
    data = "data:image/png;base64," + encoded.decode("utf-8")

    card(
        title=title,
        text=subtitle,
        image=data,
        on_click=on_click,
    )
