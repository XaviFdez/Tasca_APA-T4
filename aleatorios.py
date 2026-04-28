"""
Generación de números aleatorios usando el algoritmo LGC (Linear Congruential Generator).
 
Este módulo implementa el generador pseudoaleatorio LGC tanto como clase iterable (Aleat)
como función generadora (aleat()). El algoritmo aplica iterativamente la fórmula:
 
    x_{n+1} = (a * x_n + c) mod m
 
Los valores por defecto de m, a y c corresponden al estándar POSIX.
 
Autor: Xavi Fernández Rodríguez
"""
 
# Valores POSIX por defecto
_M_POSIX = 2 ** 48
_A_POSIX = 25214903917
_C_POSIX = 11
_X0_DEFAULT = 1212121
 
 
class Aleat:
    """
    Generador de números pseudoaleatorios basado en el algoritmo LGC.
 
    Implementa el protocolo iterador mediante __next__(), generando valores
    en el rango 0 <= x_n < m usando la recurrencia:
 
        x_{n+1} = (a * x_n + c) mod m
 
    Atributos:
        _m  (int): Módulo de la secuencia (> 0).
        _a  (int): Multiplicador (0 < a < m).
        _c  (int): Incremento (0 <= c < m).
        _xn (int): Estado actual de la secuencia (semilla o valor previo).
 
    Métodos:
        __next__(): Devuelve el siguiente número pseudoaleatorio.
        __call__(x0): Reinicia la secuencia con la semilla x0.
        __iter__(): Devuelve el propio objeto (es un iterador).
 
    Pruebas unitarias:
 
    Comprobación del funcionamiento de Aleat:
    >>> rand = Aleat(m=32, a=9, c=13, x0=11)
    >>> for _ in range(4):
    ...     print(next(rand))
    ...
    16
    29
    18
    15
 
    Comprobación del reinicio de Aleat:
    >>> rand(29)
    >>> for _ in range(4):
    ...     print(next(rand))
    ...
    18
    15
    20
    1
    """
 
    def __init__(self, *, m=_M_POSIX, a=_A_POSIX, c=_C_POSIX, x0=_X0_DEFAULT):
        self._m = m
        self._a = a
        self._c = c
        self._xn = x0
 
    def __iter__(self):
        return self
 
    def __next__(self):
        self._xn = (self._a * self._xn + self._c) % self._m
        return self._xn
 
    def __call__(self, x0):
        self._xn = x0
 
 
def aleat(*, m=_M_POSIX, a=_A_POSIX, c=_C_POSIX, x0=_X0_DEFAULT):
    """
    Función generadora de números pseudoaleatorios basada en el algoritmo LGC.
 
    Genera valores en el rango 0 <= x_n < m usando la recurrencia:
 
        x_{n+1} = (a * x_n + c) mod m
 
    Si se envía un valor al generador mediante send(), la secuencia se reinicia
    usando ese valor como nueva semilla.
 
    Argumentos (solo por clave):
        m  (int): Módulo. Por defecto 2**48 (POSIX).
        a  (int): Multiplicador. Por defecto 25214903917 (POSIX).
        c  (int): Incremento. Por defecto 11 (POSIX).
        x0 (int): Semilla inicial. Por defecto 1212121.
 
    Salida:
        Genera enteros pseudoaleatorios en [0, m).
 
    Pruebas unitarias:
 
    Comprobación del funcionamiento de aleat():
    >>> rand = aleat(m=64, a=5, c=46, x0=36)
    >>> for _ in range(4):
    ...     print(next(rand))
    ...
    34
    24
    38
    44
 
    Comprobación del reinicio de aleat():
    >>> rand.send(24)
    38
    >>> for _ in range(4):
    ...     print(next(rand))
    ...
    44
    10
    32
    14
    """
    xn = x0
    semilla = None
    while True:
        xn = (a * xn + c) % m
        semilla = yield xn
        if semilla is not None:
            xn = semilla
 
 
if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)