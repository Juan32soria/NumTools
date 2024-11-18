from django.shortcuts import render
import Methods.utils.resources as rs
import Methods.utils.numerical_methods as nm
from .forms import NewtonForm

def newton_view(request):
    context = {}
    if request.method == 'POST':
        form = NewtonForm(request.POST)
        if form.is_valid():
            # Obtener los datos del formulario
            fun = form.cleaned_data['fun'].replace('^', '**')
            dfun = form.cleaned_data['dfun'].replace('^', '**')
            x0 = form.cleaned_data['x0']
            tol = form.cleaned_data['tol']
            n_iter = form.cleaned_data['niter']
            precision_type = form.cleaned_data['precision_type']
            precision_value = form.cleaned_data['precision_value']

            try:
                # Reemplazar '^' con '**' para la sintaxis de potencia en Python
                fun = fun.replace(' ', '')
                dfun = dfun.replace(' ', '')

                # Ejecutar el método de Newton
                fx_values, error, x_values, root, iterations = nm.newton_method(fun, dfun, x0, tol, n_iter, rs.to_math)

                # Definir el tipo de error a mostrar en la tabla
                error_type = 'Relative Error' if precision_type == 'significant_figures' else 'Absolute Error'

                # Si se encuentra la raíz, ajustar con la precisión solicitada
                if root is not None:
                    if precision_type == 'significant_figures':
                        fx_values = [rs.round_to_significant_figures(f, precision_value) for f in fx_values]
                        root = rs.round_to_significant_figures(root, precision_value)
                        error = [rs.round_to_significant_figures(e, precision_value) for e in error]
                        x_values = [rs.round_to_significant_figures(x, precision_value) for x in x_values]
                    elif precision_type == 'decimal_places':
                        fx_values = [round(f, precision_value) for f in fx_values]
                        root = round(root, precision_value)
                        error = [round(e, precision_value) for e in error]
                        x_values = [round(x, precision_value) for x in x_values]

                # Generar gráfico de la función
                img_base64 = rs.generate_graph(x0 - 20, x0 + 20, fun, root)

                # Crear contexto con los resultados
                context = {
                    'form': form,
                    'fx': fun,
                    'dfx': dfun,
                    'msg': ['Calculation completed successfully'],
                    'graph': img_base64,
                    'table': [{'iteration': i, 'x_n': x_values[i], 'fx_n': fx_values[i], 'error': error[i]} for i in range(iterations)],
                    'error_type': error_type,
                    'root': root,
                }
            except Exception as e:
                context['form'] = form
                context['msg'] = [f"Error: {str(e)}"]
        else:
            context['form'] = form
    else:
        context['form'] = NewtonForm()
    return render(request, 'newton.html', context)
