from django import forms

class MultipleRootsForm(forms.Form):
    fun = forms.CharField(
        label="Function f(x)",
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'x**3 - x - 2', 'class': 'form-control'})
    )
    df1 = forms.CharField(
        label="First Derivative f'(x)",
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': '3*x**2 - 1', 'class': 'form-control'})
    )
    df2 = forms.CharField(
        label="Second Derivative f''(x)",
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': '6*x', 'class': 'form-control'})
    )
    x0 = forms.FloatField(
        label="Initial value (x0)",
        widget=forms.NumberInput(attrs={'placeholder': '1.0', 'class': 'form-control'})
    )
    tol = forms.FloatField(
        label="Tolerance",
        widget=forms.NumberInput(attrs={'placeholder': '0.5e-5', 'class': 'form-control'})
    )
    niter = forms.IntegerField(
        label="Maximum number of iterations",
        widget=forms.NumberInput(attrs={'placeholder': '100', 'class': 'form-control'})
    )
    precision_type = forms.ChoiceField(
        label="Precision type",
        choices=[
            ('significant_figures', 'Significant figures'),
            ('decimal_places', 'Decimal places')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    precision_value = forms.IntegerField(
        label="Precision value",
        widget=forms.NumberInput(attrs={'placeholder': '5', 'class': 'form-control'})
    )
