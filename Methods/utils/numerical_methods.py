import math
import sympy as sp
from sympy import sympify, lambdify, Symbol
import Methods.utils.resources as rs

def bisection_method(xi, xs, tol, niter, fun, to_math):
    """
    Método de bisección para encontrar la raíz de una función en un intervalo dado.
    
    Parámetros:
    - xi: Límite inferior del intervalo.
    - xs: Límite superior del intervalo.
    - tol: Tolerancia para el error absoluto.
    - niter: Número máximo de iteraciones permitidas.
    - fun: Función a evaluar como cadena (string).
    - to_math: Diccionario con funciones matemáticas seguras.

    Retorna:
    - fm: Lista con los valores de la función en cada iteración.
    - error: Lista con los errores absolutos en cada iteración.
    - xm: Valor aproximado de la raíz.
    - c: Número de iteraciones realizadas.
    """
    # Inicializar las listas para almacenar los valores de la función y los errores.
    fm = []  # Lista para valores de f(x) en cada iteración.
    error = []  # Lista para errores absolutos en cada iteración.

    # Evaluar la función en los extremos del intervalo inicial.
    fi = eval(fun, {"x": xi, "math": math}, to_math)  # f(xi)
    fs = eval(fun, {"x": xs, "math": math}, to_math)  # f(xs)

    # Comprobar si alguno de los extremos del intervalo es una raíz.
    if fi == 0:
        return [], [], xi, 0  # xi es la raíz exacta.
    elif fs == 0:
        return [], [], xs, 0  # xs es la raíz exacta.

    # Comprobar si el intervalo contiene una raíz (signos opuestos en los extremos).
    elif fs * fi < 0:
        c = 0  # Contador de iteraciones.
        # Calcular el primer punto medio.
        xm = (xi + xs) / 2  # Punto medio inicial.
        fe = eval(fun, {"x": xm, "math": math}, to_math)  # f(xm)
        fm.append(fe)  # Guardar el valor de f(xm).
        error.append(100)  # Inicializar el error con un valor alto.

        # Iterar mientras el error sea mayor que la tolerancia, no se alcance una raíz exacta,
        # y no se supere el número máximo de iteraciones.
        while error[c] > tol and fe != 0 and c < niter:
            if fi * fe < 0:
                # Si el signo de f(xi) y f(xm) es opuesto, la raíz está en [xi, xm].
                xs = xm  # Actualizar el extremo superior.
                fs = eval(fun, {"x": xs, "math": math}, to_math)  # Recalcular f(xs).
            else:
                # Si el signo de f(xm) y f(xs) es opuesto, la raíz está en [xm, xs].
                xi = xm  # Actualizar el extremo inferior.
                fs = eval(fun, {"x": xi, "math": math}, to_math)  # Recalcular f(xi).

            # Guardar el valor anterior del punto medio.
            xa = xm
            # Calcular el nuevo punto medio.
            xm = (xi + xs) / 2  # Nuevo punto medio.
            fe = eval(fun, {"x": xm, "math": math}, to_math)  # Recalcular f(xm).
            fm.append(fe)  # Guardar el nuevo valor de f(xm).
            # Calcular el error absoluto entre los puntos medios consecutivos.
            abs_error = abs(xm - xa)
            error.append(abs_error)  # Guardar el error en la lista.
            c += 1  # Incrementar el contador de iteraciones.

        # Verificar las condiciones de parada.
        if fe == 0 or abs_error < tol:
            # Si f(xm) = 0 o el error es menor que la tolerancia, se encontró la raíz.
            return fm, error, xm, c
        else:
            # Si se alcanzó el máximo de iteraciones sin convergencia, devolver los resultados obtenidos.
            return fm, error, xm, niter
    else:
        # Si no hay un cambio de signo en el intervalo, no hay garantía de raíz.
        return [], [], None, None

def falseposition_method(xi, xs, tol, niter, fun, to_math):
    fm = []
    error = []
    fi = eval(fun, {"x": xi, "math": math}, to_math)
    fs = eval(fun, {"x": xs, "math": math}, to_math)

    if fi == 0:
        return [], [], xi, 0
    elif fs == 0:
        return [], [], xs, 0
    elif fs * fi < 0:
        c = 0
        xm = xs - (fs * (xi - xs)) / (fi - fs)
        fe = eval(fun, {"x": xm, "math": math}, to_math)
        fm.append(fe)
        error.append(100)

        while error[c] > tol and fe != 0 and c < niter:
            if fi * fe < 0:
                xs = xm
                fs = eval(fun, {"x": xs, "math": math}, to_math)
            else:
                xi = xm
                fs = eval(fun, {"x": xi, "math": math}, to_math)

            xa = xm
            xm = xs - (fs * (xi - xs)) / (fi - fs)
            fe = eval(fun, {"x": xm, "math": math}, to_math)
            fm.append(fe)
            abs_error = abs(xm - xa)
            error.append(abs_error)
            c += 1

        if fe == 0 or abs_error < tol:
            return fm, error, xm, c
        else:
            return fm, error, xm, niter
    else:
        return [], [], None, None

def fixed_point_method(gx, xo, tol, niter, precision_value, precision_type, to_math):
    # Crear una función evaluable a partir de gx usando eval y to_math
    def g(x_value):
        # Evaluar la función g(x) con el valor actual de x
        return eval(gx, {"x": x_value, "math": math}, to_math)
    
    iterations = []  # Lista para almacenar iteraciones
    errors = []  # Lista para almacenar errores

    # Inicializar valores
    c = 0
    error = 100
    xn = xo

    while error > tol and c < niter:
        # Calcular el siguiente valor de x
        xn_next = g(xn)

        # Aplicar precisión según el tipo solicitado
        if precision_type == "significant_figures":
            xn_next = rs.round_to_significant_figures(xn_next, precision_value)
        elif precision_type == "decimal_places":
            xn_next = round(xn_next, precision_value)

        # Calcular error absoluto
        abs_error = abs(xn_next - xn)

        # Guardar datos de la iteración actual
        iterations.append((c + 1, xn, xn_next, abs_error))
        errors.append(abs_error)

        # Verificar si se cumple el criterio de tolerancia
        if abs_error <= tol:
            break  # Detener el bucle si se cumple la tolerancia

        # Actualizar para la siguiente iteración
        xn = xn_next
        c += 1

    return {
        "iterations": iterations,
        "errors": errors,
        "approximation": xn,
        "iterations_count": c
    }

def incremental_search_method(fx, x0, delta_x, niter, to_math):
    """
    Método de Búsquedas Incrementales para encontrar un intervalo que contenga una raíz.

    Parámetros:
    - fx: Función como cadena (string) a evaluar, e.g., "x**3 - x - 2".
    - x0: Valor inicial de partida.
    - delta_x: Tamaño del incremento en x.
    - niter: Número máximo de iteraciones.
    - to_math: Diccionario con funciones matemáticas seguras.

    Retorna:
    - intervals: Lista de tuplas con los intervalos donde hay cambio de signo.
    - evaluations: Lista de evaluaciones de la función en los puntos x_n.
    - steps: Número de iteraciones realizadas.
    """
    # Inicializar listas para almacenar intervalos y evaluaciones
    intervals = []
    evaluations = []

    # Evaluar f(x0)
    x_n = x0
    f_xn = eval(fx, {"x": x_n, "math": math}, to_math)

    # Verificar si el punto inicial ya es una raíz
    if f_xn == 0:
        return [(x_n, x_n)], [f_xn], 0  # Intervalo único, raíz exacta encontrada

    # Comenzar el ciclo de iteraciones
    for i in range(niter):
        # Calcular el siguiente punto
        x_next = x_n + delta_x

        # Evaluar f(x_next)
        f_xnext = eval(fx, {"x": x_next, "math": math}, to_math)

        # Guardar la evaluación actual
        evaluations.append((x_n, f_xn))

        # Verificar cambio de signo entre f(x_n) y f(x_next)
        if f_xn * f_xnext < 0:
            intervals.append((x_n, x_next))  # Guardar el intervalo donde ocurre el cambio de signo
            evaluations.append((x_next, f_xnext))
            break  # Detener el proceso, ya que se encontró un cambio de signo

        # Preparar para la siguiente iteración
        x_n = x_next
        f_xn = f_xnext

    # Retornar los resultados
    return intervals, evaluations, i + 1
