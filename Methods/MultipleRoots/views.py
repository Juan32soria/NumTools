from django.shortcuts import render
import Methods.utils.resources as rs
import Methods.utils.numerical_methods as nm
from .forms import MultipleRootsForm

def multipleroots_view(request):
    context = {}
    if request.method == 'POST':
        form = MultipleRootsForm(request.POST)
        if form.is_valid():
            # Obtener los datos del formulario
            fun = form.cleaned_data['fun'].replace('^', '**')
            df1 = form.cleaned_data['df1'].replace('^', '**')
            df2 = form.cleaned_data['df2'].replace('^', '**')
            x0 = form.cleaned_data['x0']
            tol = form.cleaned_data['tol']
            n_iter = form.cleaned_data['niter']
            precision_type = form.cleaned_data['precision_type']
            precision_value = form.cleaned_data['precision_value']

            try:
                # Reemplazar '^' con '**' para la sintaxis de potencia en Python
                fun = fun.replace(' ', '')
                df1 = df1.replace(' ', '')
                df2 = df2.replace(' ', '')

                # Ejecutar el método de raíces múltiples
                fm, error, x_values, root, iterations = nm.multipleroots_method(x0, fun, df1, df2, tol, n_iter, rs.to_math)

                # Definir el tipo de error a mostrar en la tabla
                error_type = 'Relative Error' if precision_type == 'significant_figures' else 'Absolute Error'

                # Si se encuentra la raíz, ajustar con la precisión solicitada
                if root is not None:
                    if precision_type == 'significant_figures':
                        fm = [rs.round_to_significant_figures(f, precision_value) for f in fm]
                        root = rs.round_to_significant_figures(root, precision_value)
                        error = [rs.round_to_significant_figures(e, precision_value) for e in error]
                        x_values = [rs.round_to_significant_figures(x, precision_value) for x in x_values]
                    elif precision_type == 'decimal_places':
                        fm = [round(f, precision_value) for f in fm]
                        root = round(root, precision_value)
                        error = [round(e, precision_value) for e in error]
                        x_values = [round(x, precision_value) for x in x_values]

                # Generar gráfico de la función
                img_base64 = rs.generate_graph(x0 - 2, x0 + 2, fun, root)

                # Crear contexto con los resultados
                context = {
                    'form': form,
                    'fx': fun,
                    'df1': df1,
                    'df2': df2,
                    'msg': ['Calculation completed successfully'],
                    'graph': img_base64,
                    'table': [{'iteration': i, 'x_n': x_values[i], 'fx_n': fm[i], 'error': error[i]} for i in range(iterations)],
                    'error_type': error_type,
                    'root': root,
                }
            except Exception as e:
                context['form'] = form
                context['msg'] = [f"Error: {str(e)}"]
        else:
            context['form'] = form
    else:
        context['form'] = MultipleRootsForm()
    return render(request, 'multipleroots.html', context)
