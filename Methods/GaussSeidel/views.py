from django.shortcuts import render
import Methods.utils.numerical_methods as nm
import Methods.utils.resources as rs
from .forms import GaussSeidelForm  # Formulario específico para Gauss-Seidel

def gaussseidel_view(request):
    context = {}
    matrix_size = 3  # Tamaño de matriz predeterminado

    if request.method == 'POST':
        # Obtener el tamaño de la matriz enviado en el formulario
        try:
            matrix_size = int(request.POST.get('matrix_size', 3))
        except ValueError:
            matrix_size = 3  # Si el valor no es válido, usar predeterminado

        form = GaussSeidelForm(request.POST, matrix_size=matrix_size)

        if form.is_valid():
            try:
                # Obtener valores básicos del formulario
                tol = form.cleaned_data['tol']
                niter = form.cleaned_data['niter']
                matrix_size = int(form.cleaned_data['matrix_size'])

                # Construir matrices dinámicamente
                matrix, b, x0 = [], [], []
                for i in range(matrix_size):
                    b.append(form.cleaned_data[f'b_{i}'])
                    x0.append(form.cleaned_data[f'x0_{i}'])  # Vector inicial
                    row = [form.cleaned_data[f'A_{i}_{j}'] for j in range(matrix_size)]
                    matrix.append(row)

                # Ejecutar el método de Gauss-Seidel
                solutions, errors, final_approximation, iterations = nm.gauss_seidel(
                    matrix, b, tol, niter
                )
                
                # Generar gráfico de convergencia
                img_base64 = rs.generate_solution_graph(solutions, b)

                # Agregar resultados al contexto
                context.update({
                    'table': [
                        {'iteration': idx + 1, 'solution': solutions[idx], 'error': errors[idx]} for idx in range(min(len(solutions), len(errors)))
                    ],
                    'solutions': final_approximation,
                    'matrix': matrix,
                    'vector_b': b,
                    'vector_x0': x0,
                    'iterations': iterations,
                    'graph': img_base64,
                    'errors': errors,
                    'msg': ['Gauss-Seidel method completed successfully.'],
                })

            except Exception as e:
                # Manejar errores en el cálculo
                context['msg'] = [f"Unexpected error: {e}"]
    else:
        # Solicitud GET, crear formulario inicial
        form = GaussSeidelForm(matrix_size=matrix_size)

    # Crear listas de campos para renderizar en el template
    matrix_fields = [
        [form[f'A_{i}_{j}'] for j in range(matrix_size)]
        for i in range(matrix_size)
    ]
    vector_b_fields = [form[f'b_{i}'] for i in range(matrix_size)]
    initial_guess_fields = [form[f'x0_{i}'] for i in range(matrix_size)]

    # Actualizar el contexto
    context.update({
        'form': form,
        'matrix_fields': matrix_fields,
        'vector_b_fields': vector_b_fields,
        'initial_guess_fields': initial_guess_fields,
        'range': range(matrix_size),
    })

    # Renderizar la plantilla
    return render(request, 'gaussseidel.html', context)
