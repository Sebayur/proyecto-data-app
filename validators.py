def validar_usuario(nombre, edad, ciudad):

    if not isinstance(nombre, str):
        return "El nombre debe ser un texto."

    nombre = nombre.strip()

    if len(nombre) < 2:
        return "El nombre debe tener al menos 2 caracteres."

    if any(caracter.isdigit() for caracter in nombre):
        return "El nombre no puede contener números."

    if isinstance(edad, bool):
        return "La edad debe ser un número entero."

    try:
        edad_convertida = int(edad)
    except (ValueError, TypeError):
        return "La edad debe ser un número."

    if isinstance(edad, float) and not edad.is_integer():
        return "La edad debe ser un número."

    if not (0 <= edad_convertida <= 120):
        return "La edad debe estar entre 0 y 120."

    if not isinstance(ciudad, str):
        return "La ciudad debe ser un texto."

    ciudad = ciudad.strip()

    if len(ciudad) < 2:
        return "La ciudad debe tener al menos 2 caracteres."

    if any(caracter.isdigit() for caracter in ciudad):
        return "La ciudad no puede contener números."

    return None