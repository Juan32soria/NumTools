import math
import numpy as np
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
    xm_values = [xi]  # Lista para almacenar los valores de x_m.

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
        xm_values.append(xm)  # Guardar el valor de x_m.
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
            xm_values.append(xm)  # Guardar el nuevo valor de x_m.
            # Calcular el error absoluto entre los puntos medios consecutivos.
            abs_error = abs(xm - xa)
            error.append(abs_error)  # Guardar el error en la lista.
            c += 1  # Incrementar el contador de iteraciones.

        # Verificar las condiciones de parada.
        if fe == 0 or abs_error < tol:
            # Si f(xm) = 0 o el error es menor que la tolerancia, se encontró la raíz.
            return fm, error,xm_values, xm, c
        else:
            # Si se alcanzó el máximo de iteraciones sin convergencia, devolver los resultados obtenidos.
            return fm, error,xm_values, xm, niter
    else:
        # Si no hay un cambio de signo en el intervalo, no hay garantía de raíz.
        return [], [], [], None, None

def falseposition_method(xi, xs, tol, niter, fun, to_math):
    fm = []
    error = []
    xm_values = [xi]
    
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
        xm_values.append(xm)
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
            xm_values.append(xm)
            abs_error = abs(xm - xa)
            error.append(abs_error)
            c += 1

        if fe == 0 or abs_error < tol:
            return fm, error,xm_values, xm, c
        else:
            return fm, error,xm_values, xm, niter
    else:
        return [], [],[], None, None

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

def secant_method(x0, x1, tol, niter, fun, to_math):
    """
    Método de la Secante para encontrar la raíz de una función.
    
    Parámetros:
    - x0: Primer valor inicial.
    - x1: Segundo valor inicial.
    - tol: Tolerancia para el error absoluto.
    - niter: Número máximo de iteraciones permitidas.
    - fun: Función a evaluar como cadena (string).
    - to_math: Diccionario con funciones matemáticas seguras.

    Retorna:
    - fm: Lista con los valores de la función en cada iteración.
    - error: Lista con los errores absolutos en cada iteración.
    - x1: Valor aproximado de la raíz.
    - c: Número de iteraciones realizadas.
    """
    # Inicializar las listas para almacenar los valores de la función y los errores.
    fm = []  # Lista para valores de f(x) en cada iteración.
    error = []  # Lista para errores absolutos en cada iteración.
    xn_values = [x0, x1]  # Lista para almacenar los valores de x_n.

    # Evaluar la función en los puntos iniciales x0 y x1.
    f0 = eval(fun, {"x": x0, "math": math}, to_math)  # f(x0)
    f1 = eval(fun, {"x": x1, "math": math}, to_math)  # f(x1)

    # Comprobar si alguno de los puntos iniciales es una raíz.
    if f0 == 0:
        return [], [], [x0], x0, 0  # x0 es la raíz exacta.
    elif f1 == 0:
        return [], [],[x0], x1, 0  # x1 es la raíz exacta.

    # Inicializar variables para el proceso iterativo.
    c = 0  # Contador de iteraciones.
    error.append(100)  # Inicializar el error con un valor alto.

    # Iterar mientras el error sea mayor que la tolerancia, no se alcance una raíz exacta,
    # y no se supere el número máximo de iteraciones.
    while error[c] > tol and f1 != 0 and (f1 - f0) != 0 and c < niter:
        # Calcular el siguiente valor de x usando la fórmula de la secante.
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        xn_values.append(x2)

        # Calcular el error absoluto.
        abs_error = abs(x2 - x1)
        error.append(abs_error)  # Guardar el error en la lista.

        # Evaluar la función en el nuevo valor x2.
        f2 = eval(fun, {"x": x2, "math": math}, to_math)  # f(x2)
        fm.append(f2)  # Guardar el valor de f(x2) en la lista.

        # Actualizar los valores para la siguiente iteración.
        x0, f0 = x1, f1  # Desplazar x1 a x0.
        x1, f1 = x2, f2  # Actualizar x1 con el nuevo x2.
        c += 1  # Incrementar el contador de iteraciones.

    # Verificar las condiciones de parada.
    if f1 == 0:
        # Si f(x1) = 0, x1 es una raíz exacta.
        return fm, error, xn_values, x1, c
    elif error[-1] < tol:
        # Si el error es menor que la tolerancia, x1 es una aproximación de la raíz.
        return fm, error, xn_values, x1, c
    elif (f1 - f0) == 0:
        # Si el denominador es cero, puede haber una raíz múltiple.
        return fm, error, xn_values, None, c
    else:
        # Si se alcanzó el máximo de iteraciones sin convergencia, devolver los resultados obtenidos.
        return fm, error, xn_values, x1, niter

def newton_method(f, df, x0, tol, niter, to_math):
    """
    Método de Newton para encontrar la raíz de una función.

    Parámetros:
    - f: Función a evaluar como cadena (string).
    - df: Derivada de la función como cadena (string).
    - x0: Valor inicial.
    - tol: Tolerancia para el error absoluto.
    - niter: Número máximo de iteraciones permitidas.
    - to_math: Diccionario con funciones matemáticas seguras.

    Retorna:
    - fx_values: Lista con los valores de f(x) en cada iteración.
    - error: Lista con los errores absolutos en cada iteración.
    - x_values: Lista con los valores de x en cada iteración.
    - x0: Valor aproximado de la raíz.
    - c: Número de iteraciones realizadas.
    """
    # Inicializar listas para almacenar resultados de cada iteración
    fx_values = []  # Lista para valores de f(x) en cada iteración.
    error = []  # Lista para errores absolutos en cada iteración.
    x_values = [x0]  # Lista para almacenar los valores de x en cada iteración.

    # Evaluar la función y su derivada en el punto inicial
    fx = eval(f, {"x": x0, "math": math}, to_math)  # f(x0)
    dfx = eval(df, {"x": x0, "math": math}, to_math)  # f'(x0)

    # Comprobar si el punto inicial ya es una raíz
    if fx == 0:
        return [], [], [x0], x0, 0  # x0 es la raíz exacta.

    c = 0  # Contador de iteraciones
    error.append(100)  # Inicializar el error con un valor alto.

    # Iterar mientras el error sea mayor que la tolerancia, no se alcance una raíz exacta,
    # y no se supere el número máximo de iteraciones.
    while error[c] > tol and fx != 0 and dfx != 0 and c < niter:
        # Calcular el siguiente valor de x
        x1 = x0 - (fx / dfx)

        # Calcular el error absoluto
        abs_error = abs(x1 - x0)
        error.append(abs_error)  # Guardar el error en la lista.

        # Evaluar la función y su derivada en el nuevo valor x1
        fx = eval(f, {"x": x1, "math": math}, to_math)  # f(x1)
        dfx = eval(df, {"x": x1, "math": math}, to_math)  # f'(x1)

        # Guardar los valores en las listas correspondientes
        fx_values.append(fx)  # Guardar el valor de f(x1).
        x_values.append(x1)  # Guardar el nuevo valor de x1.

        # Actualizar x0 para la siguiente iteración
        x0 = x1
        c += 1  # Incrementar el contador de iteraciones.

    # Verificar las condiciones de parada.
    if fx == 0:
        # Si f(x) = 0, x es una raíz exacta.
        return fx_values, error, x_values, x0, c
    elif error[-1] < tol:
        # Si el error es menor que la tolerancia, x es una aproximación de la raíz.
        return fx_values, error, x_values, x0, c
    elif dfx == 0:
        # Si la derivada es cero, puede haber una raíz múltiple.
        return fx_values, error, x_values, None, c
    else:
        # Si se alcanzó el máximo de iteraciones sin convergencia, devolver los resultados obtenidos.
        return fx_values, error, x_values, x0, niter

def multipleroots_method(x0, fun, df1, df2, tol, niter, to_math):
    """
    Método de raíces múltiples para encontrar la raíz de una función.
    
    Parámetros:
    - x0: Valor inicial.
    - fun: Función a evaluar como cadena (string).
    - df1: Primera derivada de la función como cadena (string).
    - df2: Segunda derivada de la función como cadena (string).
    - tol: Tolerancia para el error absoluto.
    - niter: Número máximo de iteraciones permitidas.
    - to_math: Diccionario con funciones matemáticas seguras.

    Retorna:
    - fm: Lista con los valores de la función en cada iteración.
    - error: Lista con los errores absolutos en cada iteración.
    - x_values: Lista con los valores de x en cada iteración.
    - x: Valor aproximado de la raíz.
    - c: Número de iteraciones realizadas.
    """
    # Inicializar listas para almacenar los valores de la función, errores y x.
    fm = []  # Lista para valores de f(x) en cada iteración.
    error = []  # Lista para errores absolutos en cada iteración.
    x_values = [x0]  # Lista para almacenar los valores de x.

    # Evaluar las funciones en el valor inicial x0.
    f = eval(fun, {"x": x0, "math": math}, to_math)  # f(x0)
    df1_val = eval(df1, {"x": x0, "math": math}, to_math)  # f'(x0)
    df2_val = eval(df2, {"x": x0, "math": math}, to_math)  # f''(x0)

    # Comprobar si el valor inicial es una raíz.
    if f == 0:
        return [], [], [x0], x0, 0  # x0 es la raíz exacta.

    # Inicializar el contador de iteraciones y el error inicial.
    c = 0  # Contador de iteraciones.
    error.append(100)  # Inicializar el error con un valor alto.

    # Iterar mientras el error sea mayor que la tolerancia, no se alcance una raíz exacta,
    # y no se supere el número máximo de iteraciones.
    while error[c] > tol and f != 0 and df1_val != 0 and c < niter:
        # Calcular el denominador: f'(x)^2 - f(x) * f''(x).
        denominator = df1_val ** 2 - f * df2_val
        if denominator == 0:
            # Si el denominador es 0, la raíz es múltiple o el método falla.
            return fm, error, x_values, None, c

        # Calcular el siguiente valor de x.
        x1 = x0 - (f * df1_val) / denominator

        # Calcular el error absoluto.
        abs_error = abs(x1 - x0)
        error.append(abs_error)  # Guardar el error en la lista.

        # Evaluar las funciones en el nuevo valor x1.
        f = eval(fun, {"x": x1, "math": math}, to_math)  # f(x1)
        df1_val = eval(df1, {"x": x1, "math": math}, to_math)  # f'(x1)
        df2_val = eval(df2, {"x": x1, "math": math}, to_math)  # f''(x1)

        # Guardar los valores de la función y x en las listas.
        fm.append(f)  # Guardar el valor de f(x1).
        x_values.append(x1)  # Guardar el nuevo valor de x.

        # Actualizar x0 para la siguiente iteración.
        x0 = x1
        c += 1  # Incrementar el contador de iteraciones.

    # Verificar las condiciones de parada.
    if f == 0:
        # Si f(x) = 0, x es una raíz exacta.
        return fm, error, x_values, x1, c
    elif error[-1] < tol:
        # Si el error es menor que la tolerancia, x1 es una aproximación de la raíz.
        return fm, error, x_values, x1, c
    else:
        # Si se alcanzó el máximo de iteraciones sin convergencia, devolver los resultados obtenidos.
        return fm, error, x_values, None, c

def jacobi_method(a, b, xo, tol, niter, err_type):
    """
    Método de Jacobi para resolver sistemas de ecuaciones lineales.

    Parámetros:
    - a : Matriz de coeficientes (numpy array).
    - b: Vector de términos independientes (numpy array).
    - xo: Vector inicial (numpy array).
    - tol: Tolerancia para el criterio de parada.
    - niter: Número máximo de iteraciones.
    - err_type: Tipo de error ("abs" para absoluto, "rel" para relativo).

    Retorna:
    - solutions: Lista con los vectores solución en cada iteración.
    - errors: Lista con los errores calculados en cada iteración.
    - approximation: Vector solución aproximado o None si no converge.
    - iterations: Número de iteraciones realizadas.
    """
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    xo = np.array(xo, dtype=float)

    # Verificar que la diagonal no tenga ceros
    if np.any(np.diag(a) == 0):
        raise ValueError("La matriz tiene ceros en la diagonal principal, Jacobi no es aplicable.")
    
    # Verificar si la matriz es diagonal dominante (recomendado pero opcional)
    for i in range(len(b)):
        if 2 * abs(a[i, i]) <= np.sum(np.abs(a[i, :])):
            print("Advertencia: La matriz puede no ser diagonal dominante, el método podría no converger.")
            break

    solutions = [xo]
    errors = []
    x_prev = xo.copy()
    iteration = 0
    dispersion = float("inf")

    while dispersion > tol and iteration < niter:
        x_new = np.zeros_like(x_prev)
        for i, _ in enumerate(b):
            suma = np.dot(a[i, :], x_prev) - a[i, i] * x_prev[i]
            x_new[i] = (b[i] - suma) / a[i, i]

        abs_error = np.max(np.abs(x_new - x_prev))
        rel_error = np.max(np.abs((x_new - x_prev) / (x_new + np.finfo(float).eps)))  # Evitar división por cero
        errors.append(abs_error if err_type == "abs" else rel_error)
        
        dispersion = errors[-1]
        solutions.append(x_new.copy())
        x_prev = x_new
        iteration += 1

    if dispersion <= tol:
        return solutions, errors, x_new, iteration
    else:
        return solutions, errors, None, iteration

def simple_gauss(a, b, tol, niter, err_type="abs"):
    """
    Método de eliminación de Gauss para resolver sistemas de ecuaciones lineales.

    Parámetros:
    - a : Matriz de coeficientes (numpy array).
    - b: Vector de términos independientes (numpy array).
    - tol: Tolerancia para el criterio de parada.
    - niter: Número máximo de iteraciones.
    - err_type: Tipo de error ("abs" para absoluto, "rel" para relativo).

    Retorna:
    - solutions: Lista con los vectores solución en cada iteración.
    - errors: Lista con los errores calculados en cada iteración.
    - approximation: Vector solución aproximado o None si no converge.
    - iterations: Número de iteraciones realizadas.
    """
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    ab = np.column_stack((a, b))  # Crear la matriz aumentada
    solutions = []
    errors = []
    iteration = 0

    # Eliminación de Gauss
    for k in range(n - 1):
        for i in range(k + 1, n):
            if ab[k][k] == 0:
                raise ValueError("Cero en la diagonal, la matriz no puede resolverse con Gauss.")
            multiplicador = ab[i][k] / ab[k][k]
            for j in range(k, n + 1):
                ab[i][j] -= multiplicador * ab[k][j]
        solutions.append(ab.copy())  # Almacenar cada etapa de la matriz

    # Sustitución regresiva
    x = np.zeros(n)
    x[-1] = ab[-1][-1] / ab[-1][-2]
    for i in range(n - 2, -1, -1):
        suma = sum(ab[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (ab[i][-1] - suma) / ab[i][i]

    # Calcular errores (opcional)
    for _ in range(niter):
        iteration += 1
        if err_type == "abs":
            error = np.max(np.abs(b - np.dot(a, x)))
        elif err_type == "rel":
            error = np.max(np.abs((b - np.dot(a, x)) / (b + np.finfo(float).eps)))
        else:
            raise ValueError("Tipo de error no válido. Use 'abs' o 'rel'.")
        errors.append(error)

        # Verificar tolerancia
        if error <= tol:
            return solutions, errors, x, iteration

    return solutions, errors, None, iteration  # Si no converge
