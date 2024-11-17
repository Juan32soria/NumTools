import math
import base64
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')  # Backend sin interfaz gráfica

to_math = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'pi': math.pi,
    'e': math.e,
    'log': math.log,
    'log10': math.log10,
    'log2': math.log2,
    'exp': math.exp,
    'sqrt': math.sqrt,
    'abs': abs,
    'asin': math.asin,
    'acos': math.acos,
    'atan': math.atan,
    'atan2': math.atan2,
    'sinh': math.sinh,
    'cosh': math.cosh,
    'tanh': math.tanh,
    'gamma': math.gamma,
    'lgamma': math.lgamma
}

def generate_graph(xi, xs, fun, root=None):
    fig, ax = plt.subplots()

    # Generar valores de x e y para el gráfico
    x_vals = np.linspace(xi, xs, 100)
    y_vals = [eval(fun, {"x": val, "math": math}, to_math) for val in x_vals]

    # Configurar el gráfico
    ax.plot(x_vals, y_vals, color='blue', label='f(x)')
    ax.axhline(0, color='gold', lw=1, linestyle='--', label='y=0')  # Línea horizontal

    # Marcar la raíz si existe
    if root is not None:
        ax.axvline(root, color='#6A0DAD', linestyle='--', label=f'Root: {root}')

    ax.legend()  # Agregar leyenda

    # Convertir el gráfico a base64 para incrustarlo en HTML
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')

    return img_base64

def round_to_significant_figures(value, sig_figs):
    if value == 0:
        return 0
    else:
        return round(value, sig_figs - int(np.floor(np.log10(abs(value)))) - 1)
