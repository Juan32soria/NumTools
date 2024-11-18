import math
import sympy as sp
from sympy import sympify, lambdify, Symbol

def bisection_method(xi, xs, tol, niter, fun, to_math):
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
        xm = (xi + xs) / 2
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
            xm = (xi + xs) / 2
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

def generate_gx(f_expr, interval):
    x = sp.Symbol('x')  # Variable simbólica

    # Crear varias formas de g(x) reescribiendo f(x) = 0 como x = g(x)
    g_options = [
        x - f_expr,  # g(x) = x - f(x)
        sp.sqrt(f_expr),  # g(x) = sqrt(f(x)), si es posible
        -sp.sqrt(f_expr),  # g(x) = -sqrt(f(x)), si es posible
        1 / f_expr,  # g(x) = 1 / f(x), si es posible
    ]

    valid_g = []
    for g in g_options:
        try:
            g_diff = sp.diff(g, x)  # Derivada de g(x)
            # Evaluar derivada en el intervalo
            g_diff_min = sp.N(sp.Abs(g_diff.subs(x, interval[0])))
            g_diff_max = sp.N(sp.Abs(g_diff.subs(x, interval[1])))

            # Validar criterio de convergencia |g'(x)| < 1
            if g_diff_min < 1 and g_diff_max < 1:
                valid_g.append((g, g_diff))
        except Exception:
            continue

    if not valid_g:
        return {
            "error": "No se pudo encontrar una función g(x) válida en el intervalo dado.",
            "options": []
        }

    # Seleccionar el mejor g(x) con base en el menor |g'(x)|
    best_g = min(valid_g, key=lambda g: sp.N(sp.Abs(g[1].subs(x, (interval[0] + interval[1]) / 2))))

    return {
        "best_g": str(best_g[0]),
        "options": [str(g[0]) for g in valid_g],
    }

def fixed_point_method(gx, xo, tol, niter, precision_value):
    x = Symbol('x')  # Variable simbólica

    # Convertir g(x) en una función evaluable
    gx_expr = sympify(gx)  # Convertir cadena en expresión simbólica
    g = lambdify(x, gx_expr)  # Crear función evaluable de g(x)

    iterations = []  # Lista para almacenar iteraciones
    errors = []  # Lista para almacenar errores

    # Inicializar valores
    c = 0
    error = float('inf')
    xn = xo

    while error > tol and c < niter:
        # Calcular el siguiente valor de x
        xn_next = g(xn)

        # Aplicar precisión si es necesario
        xn_next = round(xn_next, precision_value)

        # Calcular error absoluto
        error = abs(xn_next - xn)

        # Guardar datos de la iteración actual
        iterations.append((c + 1, xn, xn_next, error))
        errors.append(error)

        # Actualizar para la siguiente iteración
        xn = xn_next
        c += 1

    # Verificar resultado final
    if error <= tol:
        status = "Convergencia alcanzada"
    else:
        status = "Número máximo de iteraciones alcanzado"

    return {
        "status": status,
        "iterations": iterations,
        "errors": errors,
        "approximation": xn,
        "iterations_count": c
    }
