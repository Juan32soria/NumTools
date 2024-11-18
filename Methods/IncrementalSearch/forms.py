import math
from django import forms

class IncrementalSearchForm(forms.Form):
    fx = forms.CharField(
        label="Function f(x)",
        max_length=200,
        widget=forms.TextInput(
            attrs={"placeholder": "x**3 - x - 2", "class": "form-control"}
        ),
    )
    x0 = forms.FloatField(
        label="Initial value (x₀)",
        widget=forms.NumberInput(attrs={"placeholder": "1", "class": "form-control"}),
    )
    delta_x = forms.FloatField(
        label="Increment (Δx)",
        widget=forms.NumberInput(attrs={"placeholder": "0.1", "class": "form-control"}),
    )
    niter = forms.IntegerField(
        label="Maximum iterations",
        widget=forms.NumberInput(attrs={"placeholder": "100", "class": "form-control"}),
    )

    def clean_fx(self):
        fx = self.cleaned_data.get("fx").replace("^", "**").replace(' ', '') # Reemplazar '^' con '**' para la sintaxis de potencia en Python
        try:
            eval(fx, {"x": 1, "math": math}, {"sin": math.sin, "cos": math.cos})  # Verificar que la función sea válida
        except Exception:
            raise forms.ValidationError("Invalid function. Ensure the syntax is correct (e.g., 'x**2 - 4').")
        return fx

    def clean_delta_x(self):
        delta_x = self.cleaned_data.get("delta_x")
        if delta_x <= 0:
            raise forms.ValidationError("Increment (Δx) must be greater than 0.")
        return delta_x

    def clean_niter(self):
        niter = self.cleaned_data.get("niter")
        if niter <= 0:
            raise forms.ValidationError("Maximum iterations must be greater than 0.")
        return niter
