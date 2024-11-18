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

to_maths = {"math": math}

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

def generate_interval_graph(fx, intervals):
    """
    Grafica la función f(x) y resalta los intervalos donde ocurre un cambio de signo.

    Parámetros:
    - fx: Función como cadena (string), e.g., "x**2 - 4".
    - intervals: Lista de intervalos donde ocurre un cambio de signo, e.g., [(1, 2)].
    - to_math: Diccionario con funciones matemáticas seguras.

    Retorna:
    - img_base64: Imagen en formato Base64 lista para incrustar en una página HTML.
    """
    # Crear rango amplio para graficar la función
    for interval in intervals:
        x_start, x_end = interval

    x_vals = np.linspace(x_start-2, x_end+2, 100)  # Rango de -10 a 10 con 500 puntos
    y_vals = [eval(fx, {"x": x, "math": math}, to_math) for x in x_vals]

    # Crear la figura
    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, label=f"f(x): {fx}", color="blue")  # Gráfica de la función

    # Agregar líneas en los intervalos donde ocurre el cambio de signo

    ax.axvline(x_start, color="#6A0DAD", linestyle="--", label=f"Interval Start: {x_start}")
    ax.axvline(x_end, color="#6A0DAD", linestyle="--", label=f"Interval End: {x_end}")

    # Personalizar el gráfico
    ax.axhline(0, color="gold", linewidth=0.8)  # Línea en y = 0
    ax.set_title("Graph of f(x) with Intervals of Sign Change")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend(loc="lower left")

    # Guardar la imagen como Base64
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')

    return img_base64

def generate_solution_graph(solutions, b):
    """
    Genera una gráfica para mostrar cómo las soluciones del método de Jacobi
    convergen a lo largo de las iteraciones.

    Parámetros:
    - solutions: Lista de soluciones en cada iteración (listas o arreglos).
    - b: Vector independiente (términos independientes del sistema Ax = b).
    - tol: Tolerancia utilizada en el método.

    Retorna:
    - img_base64: Imagen en formato Base64 lista para incrustar en una página HTML.
    """
    # Convertir las soluciones a un array de numpy para facilitar la manipulación
    solutions_array = np.array(solutions)

    # Obtener el número de iteraciones
    num_iterations = solutions_array.shape[0]
    indices = np.arange(num_iterations)  # Eje x: número de iteraciones

    # Crear la figura
    fig, ax = plt.subplots(figsize=(10, 6))

    # Graficar cada componente del vector solución
    for i in range(solutions_array.shape[1]):
        ax.plot(indices, solutions_array[:, i], label=f"x[{i}] (Component {i+1})", marker="o")

    # Añadir línea de convergencia teórica (vector b)
    ax.axhline(y=np.linalg.norm(b), color="gold", linestyle="--", label="Expected Convergence")

    # Personalizar el gráfico
    ax.set_title("Convergence of the Method", fontsize=14)
    ax.set_xlabel("Iteration", fontsize=12)
    ax.set_ylabel("Solution Components", fontsize=12)
    ax.legend(loc="best")
    ax.grid(True)

    # Guardar la imagen como Base64
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")

    return img_base64

def plot_gauss_pivoteo(solutions, errors, vector_b):
    """
    Genera gráficos para el método de Gauss con pivoteo parcial.

    Parámetros:
    - solutions: Lista con los estados de la matriz aumentada en cada paso.
    - errors: Lista de errores calculados en cada iteración.
    - vector_b: Vector de términos independientes.

    Retorna:
    - img_base64: Gráfica en formato Base64 para ser usada en la vista.
    """
    fig, axs = plt.subplots(2, 1, figsize=(10, 8))
    plt.tight_layout(pad=5)

    # Subplot 1: Gráfico de errores
    axs[0].plot(range(1, len(errors) + 1), errors, marker='o', linestyle='-')
    axs[0].set_title('Error vs Iteraciones')
    axs[0].set_xlabel('Iteraciones')
    axs[0].set_ylabel('Error')
    axs[0].grid(True)

    # Subplot 2: Estado de las matrices aumentadas
    for idx, sol in enumerate(solutions):
        axs[1].imshow(sol, cmap='viridis', aspect='auto')
        axs[1].set_title('Estado de la matriz aumentada (Última iteración)')
        axs[1].set_xlabel('Columnas (Incluye b)')
        axs[1].set_ylabel('Filas')
        break  # Solo mostrar la última matriz aumentada

    # Guardar la figura como una imagen Base64
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    plt.close(fig)
    return img_base64
