from django.shortcuts import render
import Methods.utils.resources as rs
import Methods.utils.numerical_methods as nm
from .forms import SecantForm

def secant_views(request):
    context = {}
    if request.method == 'POST':
        form = SecantForm(request.POST)
        if form.is_valid():
            # Obtener los datos del formulario
            fun = form.cleaned_data['fun'].replace('^', '**')  # Reemplazar '^' por '**' para Python
            x0 = form.cleaned_data['x0']  # Primer punto inicial
            x1 = form.cleaned_data['x1']  # Segundo punto inicial
            tol = form.cleaned_data['tol']  # Tolerancia
            n_iter = form.cleaned_data['niter']  # Número máximo de iteraciones
            precision_type = form.cleaned_data['precision_type']  # Tipo de precisión
            precision_value = form.cleaned_data['precision_value']  # Valor de precisión

            try:
                # Limpiar espacios en blanco en la función
                fun = fun.replace(' ', '')

                # Ejecutar el método de la secante
                fm, error, xn_values, root, iterations = nm.secant_method(x0, x1, tol, n_iter, fun, rs.to_math)

                # Definir el tipo de error a mostrar en la tabla
                error_type = 'Relative Error' if precision_type == 'significant_figures' else 'Absolute Error'

                # Si se encuentra la raíz, ajustar con la precisión solicitada
                if root is not None:
                    if precision_type == 'significant_figures':
                        fm = [rs.round_to_significant_figures(f, precision_value) for f in fm]
                        root = rs.round_to_significant_figures(root, precision_value)
                        error = [rs.round_to_significant_figures(e, precision_value) for e in error]
                    elif precision_type == 'decimal_places':
                        fm = [round(f, precision_value) for f in fm]
                        root = round(root, precision_value)
                        error = [round(e, precision_value) for e in error]

                # Generar el gráfico de la función en el intervalo
                img_base64 = rs.generate_graph(x0-2, x1+20, fun, root)

                # Crear contexto con los resultados
                context = {
                    'form': form,
                    'fx': fun,
                    'msg': ['Calculation completed successfully'],
                    'graph': img_base64,
                    'table': [{'iteration': i, 'x_n': xn_values[i], 'fx_n': fm[i], 'error': error[i]} for i in range(iterations)],
                    'error_type': error_type,
                    'root': root,
                }
            except Exception as e:
                # Manejar excepciones y añadir mensaje de error
                context['form'] = form
                context['msg'] = [f"Error: {str(e)}"]
        else:
            # Si el formulario no es válido, devolverlo con errores
            context['form'] = form
    else:
        # Si no hay datos enviados, inicializar el formulario vacío
        context['form'] = SecantForm()

    return render(request, 'secant.html', context)
