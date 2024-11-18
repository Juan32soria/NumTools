import numpy as np
from django.shortcuts import render
import Methods.utils.numerical_methods as nm
import Methods.utils.resources as rs
from .forms import PartialPivotForm

def partialpivot_view(request):
    context = {}
    matrix_size = 3  # Tamaño de la matriz predeterminado

    if request.method == 'POST':
        # Intentar obtener el tamaño de la matriz desde el formulario
        try:
            matrix_size = int(request.POST.get('matrix_size', 3))
        except ValueError:
            matrix_size = 3  # Valor predeterminado en caso de error

        form = PartialPivotForm(request.POST, matrix_size=matrix_size)

        if form.is_valid():
            try:
                # Obtener parámetros básicos del formulario
                tol = form.cleaned_data['tol']
                niter = form.cleaned_data['niter']
                matrix_size = int(form.cleaned_data['matrix_size'])  # Asegurar conversión a entero
                # Crear las matrices dinámicamente a partir de los datos del formulario
                a = []
                b = []
                for i in range(matrix_size):
                    b.append(float(form.cleaned_data[f'b_{i}']))
                    row = []
                    for j in range(matrix_size):
                        row.append(float(form.cleaned_data[f'A_{i}_{j}']))
                    a.append(row)

                # Ejecutar el método Gauss con pivoteo parcial
                solutions, errors, approximation, iterations = nm.pivoteo_parcial(
                    np.array(a), np.array(b), tol=tol, niter=niter
                )
                
                # Generar gráfico de convergencia
                img_base64 = rs.plot_gauss_pivoteo(solutions, errors, b)

                # Agregar resultados al contexto
                context.update({
                    'table': [
                        {'iteration': idx + 1, 'matrix': sol.tolist()} for idx, sol in enumerate(solutions)
                    ],
                    'approximation': approximation,
                    'matrix': a,
                    'solutions': solutions,
                    'graph': img_base64,
                    'vector_b': b,
                    'iterations': iterations,
                    'errors': errors,
                    'msg': ['Partial pivoting completed successfully.'] if approximation is not None else [
                        'The method did not converge within the iteration limit.'],
                })

            except Exception as e:
                # Manejo de errores durante el cálculo
                context['msg'] = [f"Error occurred: {e}"]
        else:
            # Manejo de errores de formulario
            context['msg'] = [f"Error occurred: {form.errors}"]
    else:
        # Solicitud GET, crear formulario inicial
        form = PartialPivotForm(matrix_size=matrix_size)

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
    return render(request, 'gpartialpivot.html', context)
