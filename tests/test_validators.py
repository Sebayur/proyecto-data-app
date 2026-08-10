from validators import validar_usuario

def test_usuario_valido():
    assert validar_usuario("Pedro", 25, "Buenos Aires") is None


def test_nombre_muy_corto():
    assert validar_usuario("A", 25, "Buenos Aires") == \
        "El nombre debe tener al menos 2 caracteres."


def test_nombre_vacio():
    assert validar_usuario("", 25, "Buenos Aires") == \
        "El nombre debe tener al menos 2 caracteres."


def test_edad_no_numerica():
    assert validar_usuario("Pedro", "abc", "Buenos Aires") == \
        "La edad debe ser un número."


def test_edad_menor_a_cero():
    assert validar_usuario("Pedro", -1, "Buenos Aires") == \
        "La edad debe estar entre 0 y 120."


def test_edad_mayor_a_120():
    assert validar_usuario("Pedro", 121, "Buenos Aires") == \
        "La edad debe estar entre 0 y 120."


def test_ciudad_muy_corta():
    assert validar_usuario("Pedro", 25, "A") == \
        "La ciudad debe tener al menos 2 caracteres."


def test_ciudad_vacia():
    assert validar_usuario("Pedro", 25, "") == \
        "La ciudad debe tener al menos 2 caracteres."