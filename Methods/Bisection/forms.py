from django import forms

class BisectionForm(forms.Form):
    fun = forms.CharField(
        label="Función f(x)",
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'x**3 - x - 2', 'class': 'form-control'})
    )
    xi = forms.FloatField(
        label="Extremo inferior (xi)",
        widget=forms.NumberInput(attrs={'placeholder': '-2','class': 'form-control'})
    )
    xs = forms.FloatField(
        label="Extremo superior (xs)",
        widget=forms.NumberInput(attrs={'placeholder': '2','class': 'form-control'})
    )
    tol = forms.FloatField(
        label="Tolerancia",
        widget=forms.NumberInput(attrs={'placeholder': '0.5e-5','class': 'form-control'})
    )
    niter = forms.IntegerField(
        label="Número máximo de iteraciones",
        widget=forms.NumberInput(attrs={'placeholder': '100','class': 'form-control'})
    )
    precision_type = forms.ChoiceField(
        label="Tipo de precisión",
        choices=[
            ('significant_figures', 'Cifras significativas'),
            ('decimal_places', 'Decimales')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    precision_value = forms.IntegerField(
        label="Cantidad de precisión",
        widget=forms.NumberInput(attrs={'placeholder': '5','class': 'form-control'})
    )
