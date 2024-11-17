from django.shortcuts import render

# Create your views here.
def core_view(request):
    context = {'is_content': True}
    return render(request, 'core.html', context)

def about_view(request):
    context = {'is_content': True}
    return render(request, 'about.html', context)