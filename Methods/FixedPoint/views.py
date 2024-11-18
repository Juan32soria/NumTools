from django.shortcuts import render
import Methods.utils.resources as rs
import Methods.utils.numerical_methods as nm
from .forms import FixedPointForm

# Create your views here.
def fixed_point_view(request):
    context = {}
    if request.method == 'POST':
        form = FixedPointForm(request.POST)
        if form.is_valid():
            # Obtener los datos del formulario
            fx = form.cleaned_data['fx'].replace('^', '**').replace(' ', '')
            gx = form.cleaned_data['gx'].replace('^', '**').replace(' ', '')
            xo = form.cleaned_data['xo']
            tol = form.cleaned_data['tol']
            niter = form.cleaned_data['niter']
            precision_type = form.cleaned_data['precision_type']
            precision_value = form.cleaned_data['precision_value']

            try:
                # Si no se proporciona g(x), generarlo automáticamente
                if not gx:
                    interval = (xo - 1, xo + 1)  # Intervalo alrededor de xo
                    gx_data = nm.generate_gx(fx, interval)

                    if "error" in gx_data:
                        # Si no se pudo generar g(x), añadir mensaje de error
                        context = {
                            'form': form,
                            'msg': [gx_data["error"]],
                        }
                        return render(request, 'fixed_point.html', context)

                    # Agregar g(x) y opciones al contexto
                    gx = gx_data["best_g"]
                    context['msg'] = [
                        f'Generated g(x): {gx_data["best_g"]}',
                        f'Other options: {", ".join(gx_data["options"])}',
                    ]

                # Ejecutar el método de punto fijo
                result = nm.fixed_point_method(gx, xo, tol, niter, precision_value)

                # Definir el tipo de error
                error_type = 'Relative Error' if precision_type == 'significant_figures' else 'Absolute Error'

                # Ajustar valores según la precisión
                if result['approximation'] is not None:
                    if precision_type == 'significant_figures':
                        result['approximation'] = rs.round_to_significant_figures(result['approximation'], precision_value)
                        result['errors'] = [rs.round_to_significant_figures(e, precision_value) for e in result['errors']]
                        result['iterations'] = [
                            (i[0], i[1], rs.round_to_significant_figures(i[2], precision_value), rs.round_to_significant_figures(i[3], precision_value))
                            for i in result['iterations']
                        ]
                    elif precision_type == 'decimal_places':
                        result['approximation'] = round(result['approximation'], precision_value)
                        result['errors'] = [round(e, precision_value) for e in result['errors']]
                        result['iterations'] = [
                            (i[0], i[1], round(i[2], precision_value), round(i[3], precision_value))
                            for i in result['iterations']
                        ]

                # Generar gráfico de g(x) para el rango dado
                img_base64 = rs.generate_graph(xo - 2, xo + 2, gx, result['approximation'])

                # Crear el contexto con los resultados
                context = {
                    'form': form,
                    'fx': fx,
                    'gx': gx,
                    'msg': ['Calculation completed successfully'],
                    'graph': img_base64,
                    'table': [{'iteration': i[0], 'x_n': i[1], 'x_next': i[2], 'error': i[3]} for i in result['iterations']],
                    'error_type': error_type,
                    'root': result['approximation'],
                }

            except Exception as e:
                # Manejar excepciones y añadir mensaje de error
                context = {
                    'form': form,
                    'msg': [f"Error: {str(e)}"],
                }
        else:
            context['form'] = form
    else:
        context['form'] = FixedPointForm()
    return render(request, 'fixedpoint.html', context)
