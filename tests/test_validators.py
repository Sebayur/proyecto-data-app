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

def test_nombre_con_numeros():
    assert validar_usuario("Sebastian123", 25, "CABA") == \
        "El nombre no puede contener números."


def test_ciudad_con_numeros():
    assert validar_usuario("Sebastian", 25, "CABA123") == \
        "La ciudad no puede contener números."


def test_nombre_no_es_texto():
    assert validar_usuario(123, 25, "Buenos Aires") == \
        "El nombre debe ser un texto."


def test_ciudad_no_es_texto():
    assert validar_usuario("Pedro", 25, 123) == \
        "La ciudad debe ser un texto."


def test_edad_decimal():
    assert validar_usuario("Pedro", 25.5, "Buenos Aires") == \
        "La edad debe ser un número."


def test_edad_boolean():
    assert validar_usuario("Pedro", True, "Buenos Aires") == \
        "La edad debe ser un número entero."


def test_edad_como_texto_entero():
    assert validar_usuario("Pedro", "25", "Buenos Aires") is None


def test_nombre_con_espacios():
    assert validar_usuario("  Pedro  ", 25, "Buenos Aires") is None


def test_ciudad_con_espacios():
    assert validar_usuario("Pedro", 25, "  Buenos Aires  ") is None
