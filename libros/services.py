import requests


def obtener_datos_libro_por_isbn(isbn: str) -> dict:
    url = (
        f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        key = f"ISBN:{isbn}"
        if key not in data:
            return {}

        libro_data = data[key]

        portada = None
        if "cover" in libro_data:
            portada = (
                libro_data["cover"].get("large")
                or libro_data["cover"].get("medium")
                or libro_data["cover"].get("small")
            )

        editorial = None
        if libro_data.get("publishers"):
            editorial = libro_data["publishers"][0].get("name")

        return {
            "titulo_api": libro_data.get("title"),
            "editorial_api": editorial,
            "portada_url": portada,
        }

    except requests.RequestException:
        return {}
