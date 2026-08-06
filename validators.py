def validar_usuario(nombre, edad, ciudad):

    if len(nombre.strip()) < 2:
        return "El nombre debe tener al menos 2 caracteres."

    try:
        edad = int(edad)
    except ValueError:
        return "La edad debe ser un número."

    if not (0 <= edad <= 120):
        return "La edad debe estar entre 0 y 120."

    if len(ciudad.strip()) < 2:
        return "La ciudad debe tener al menos 2 caracteres."

    return None