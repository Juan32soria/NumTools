from django import forms

class FixedPointForm(forms.Form):
    fx = forms.CharField(
        label="Function f(x)",
        max_length=200,
        widget=forms.TextInput(
            attrs={"placeholder": "cos(x)-x", "class": "form-control"}
        ),
	)

    gx = forms.CharField(
        label="Function g(x)",
        max_length=200,
        widget=forms.TextInput(
            attrs={"placeholder": "cos(x)", "class":"form-control"}
        ),
	)

    xo = forms.FloatField(
        label="Initial value (xo)",
        widget=forms.NumberInput(attrs={"placeholder": "-2", "class": "form-control"}),
    )

    tol = forms.FloatField(
        label="Tolerance",
        widget=forms.NumberInput(
            attrs={"placeholder": "0.5e-5", "class": "form-control"}
        ),
    )

    niter = forms.IntegerField(
        label="Maximum number of iterations",
        widget=forms.NumberInput(attrs={"placeholder": "100", "class": "form-control"}),
    )

    precision_type = forms.ChoiceField(
        label="Precision type",
        choices=[
            ("significant_figures", "Significant figures"),
            ("decimal_places", "Decimal places"),
        ],
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    precision_value = forms.IntegerField(
        label="Precision value",
        widget=forms.NumberInput(attrs={"placeholder": "5", "class": "form-control"}),
    )
