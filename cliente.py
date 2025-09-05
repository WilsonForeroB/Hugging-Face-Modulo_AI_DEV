import requests

BASE_URL = "http://localhost:6000"

def main():
    # 1. Obtener lista de funciones disponibles
    resp = requests.get(BASE_URL + "/")
    if resp.status_code != 200:
        print("Error conectando al servidor:", resp.text)
        return

    data = resp.json()
    functions = data["functions"]

    print("=== CLIENTE API ===")
    print("Funciones disponibles:")
    for i, f in enumerate(functions, start=1):
        print(f"{i}. {f}")

    # 2. El cliente elige función
    choice = int(input("Elige una función (número): ")) - 1
    if choice < 0 or choice >= len(functions):
        print("Opción inválida.")
        return
    function = functions[choice]

    # 3. El cliente escribe el texto
    text = input("Escribe el texto a analizar: ")

    # 4. Llamar al endpoint /run
    resp = requests.post(
        BASE_URL + f"/run?function={function}&text={text}"
    )

    if resp.status_code == 200:
        print("=== RESULTADO ===")
        print(resp.json())
    else:
        print("Error:", resp.text)


if __name__ == "__main__":
    main()
