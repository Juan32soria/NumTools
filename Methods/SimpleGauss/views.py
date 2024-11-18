from django.shortcuts import render
import Methods.utils.numerical_methods as nm
import Methods.utils.resources as rs
from .forms import SimpleGaussForm  # Si deseas, puedes renombrar el formulario

def simplegauss_view(request):
    context = {}
    matrix_size = 3  # Tamaño de matriz predeterminado

    if request.method == 'POST':
        # Obtener el tamaño de la matriz enviado en el formulario
        try:
            matrix_size = int(request.POST.get('matrix_size', 3))
        except ValueError:
            matrix_size = 3  # Si el valor no es válido, usar predeterminado

        form = SimpleGaussForm(request.POST, matrix_size=matrix_size)  # Reutilizando el formulario de Jacobi

        if form.is_valid():
            try:
                # Obtener valores básicos del formulario
                tol = form.cleaned_data['tol']
                niter = form.cleaned_data['niter']
                matrix_size = form.cleaned_data['matrix_size']
                matrix_size = int(matrix_size)  # Convertir a entero

                # Construir matrices dinámicamente
                matrix, b = [], []
                for i in range(matrix_size):
                    tmp = form.cleaned_data[f'b_{i}']
                    b.append(tmp)
                    row = []
                    for j in range(matrix_size):
                        tmp = form.cleaned_data[f'A_{i}_{j}']
                        row.append(tmp)
                    matrix.append(row)

                # Ejecutar el método de Gauss
                solutions, errors, final_approximation, iterations = nm.simple_gauss(
                    matrix, b, tol, niter
                )
                
                # Generar gráfico de convergencia
                img_base64 = rs.generate_solution_graph(solutions, b)

                # Agregar resultados al contexto
                context.update({
                    'table': [
                        {'iteration': idx + 1, 'matrix': sol} for idx, sol in enumerate(solutions)
                    ],
                    'solutions': final_approximation,
                    'matrix': matrix,
                    'vector_b': b,
                    'iterations': iterations,
                    'graph': img_base64,
                    'errors': errors,
                    'msg': ['Gauss method completed successfully.'],
                })

            except Exception as e:
                # Manejar errores en el cálculo
                context['msg'] = [f"Unexpected error: {e}"]
    else:
        # Solicitud GET, crear formulario inicial
        form = SimpleGaussForm(matrix_size=matrix_size)

    # Crear listas de campos para renderizar en el template
    matrix_fields = [
        [form[f'A_{i}_{j}'] for j in range(matrix_size)]
        for i in range(matrix_size)
    ]
    vector_b_fields = [form[f'b_{i}'] for i in range(matrix_size)]

    # Actualizar el contexto
    context.update({
        'form': form,
        'matrix_fields': matrix_fields,
        'vector_b_fields': vector_b_fields,
        'range': range(matrix_size),
    })

    # Renderizar la plantilla
    return render(request, 'simplegauss.html', context)
