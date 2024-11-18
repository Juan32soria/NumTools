from django.shortcuts import render
import Methods.utils.resources as rs
import Methods.utils.numerical_methods as nm
from .forms import JacobiForm

def jacobi_view(request):
    context = {}
    matrix_size = 3  # Tamaño de matriz predeterminado

    if request.method == 'POST':
        # Obtener el tamaño de la matriz enviado en el formulario
        try:
            matrix_size = int(request.POST.get('matrix_size', 3))
        except ValueError:
            matrix_size = 3  # Si el valor no es válido, usar predeterminado

        form = JacobiForm(request.POST, matrix_size=matrix_size)

        if form.is_valid():
            try:
                # Obtener valores básicos del formulario
                tol = form.cleaned_data['tol']
                niter = form.cleaned_data['niter']
                error_type = form.cleaned_data['error_type']
                matrix_size = form.cleaned_data['matrix_size']
                matrix_size = int(matrix_size)  # Convertir a entero
                # Construir matrices dinámicamente
                matrix, b, x0 = [], [], []
                for i in range(matrix_size):
                    tmp = form.cleaned_data[f'b_{i}']
                    b.append(tmp)
                    tmp = form.cleaned_data[f'x0_{i}']
                    x0.append(tmp)
                    row = []
                    for j in range(matrix_size):
                        tmp = form.cleaned_data[f'A_{i}_{j}']
                        row.append(tmp)
                    matrix.append(row)

                # Ejecutar el método de Jacobi
                solutions, errors, _, iterations = nm.jacobi_method(
                    matrix, b, x0, tol, niter, error_type)

                # Generar gráfico de convergencia
                img_base64 = rs.generate_jacobi_solution_graph(solutions, b)

                # Agregar resultados al contexto
                context.update({
                    'table': [
                        {'iteration': idx + 1, 'x': sol, 'error': err}
                        for idx, (sol, err) in enumerate(zip(solutions, errors))
                    ],
                    'solutions': solutions[-1],
                    'matrix': matrix,
                    'vector_b': b,
                    'vector_x0': x0,
                    'iterations': iterations,
                    'graph': img_base64,
                    'msg': ['Jacobi method completed successfully.'],
                    'error_type': error_type,
                })

            except Exception as e:
                # Manejar errores en el cálculo
                context['msg'] = [f"Unexpected error: {e}"]
    else:
        # Solicitud GET, crear formulario inicial
        form = JacobiForm(matrix_size=matrix_size)

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
    return render(request, 'jacobi.html', context)
