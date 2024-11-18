from django.shortcuts import render
import Methods.utils.resources as rs
import Methods.utils.numerical_methods as nm
from .forms import IncrementalSearchForm

def incrementalsearch_view(request):
    context = {}
    if request.method == 'POST':
        form = IncrementalSearchForm(request.POST)
        if form.is_valid():
            # Obtener los datos del formulario
            fx = form.cleaned_data['fx'].replace('^', '**')
            x0 = form.cleaned_data['x0']
            delta_x = form.cleaned_data['delta_x']
            niter = form.cleaned_data['niter']

            # Ejecutar el método de Búsquedas Incrementales
            intervals, evaluations, steps = nm.incremental_search_method(fx, x0, delta_x, niter, rs.to_math)

            # Crear gráfico de la función
            img_base64 = rs.generate_interval_graph(fx, intervals)

            # Crear contexto con los resultados
            context = {
                'form': form,
                'intervals': intervals,
                'table': [{'steps': idx + 1, 'x': eval[0], 'fx_n': eval[1]} for idx, eval in enumerate(evaluations)],
                'evaluations': evaluations,
                'fx': fx,
                'graph': img_base64,
                'msg': ['Completed successfully.'],
            }
        else:
            context['form'] = form
    else:
        context['form'] = IncrementalSearchForm()
    return render(request, 'incrementalsearch.html', context)
