from django import forms

class GaussSeidelForm(forms.Form):
    matrix_size = forms.ChoiceField(
        choices=[(i, f"{i}x{i}") for i in range(2, 6)],
        label="Matrix Size (n x n)",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    tol = forms.FloatField(
        label="Tolerance",
        widget=forms.NumberInput(attrs={"placeholder": "0.0001", "class": "form-control"}),
    )
    niter = forms.IntegerField(
        label="Maximum Iterations",
        widget=forms.NumberInput(attrs={"placeholder": "100", "class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        # Manejar el tamaño de la matriz dinámicamente
        matrix_size = int(kwargs.pop("matrix_size", 3))  # Default size is 3x3
        super().__init__(*args, **kwargs)

        # Crear campos dinámicamente
        for i in range(matrix_size):
            # Campos para la matriz A
            for j in range(matrix_size):
                field_name = f"A_{i}_{j}"
                self.fields[field_name] = forms.FloatField(
                    label=f"A[{i+1}][{j+1}]",
                    widget=forms.NumberInput(attrs={"placeholder": "0", "class": "form-control"}),
                )

            # Campos para el vector b
            field_b_name = f"b_{i}"
            self.fields[field_b_name] = forms.FloatField(
                label=f"b[{i+1}]",
                widget=forms.NumberInput(attrs={"placeholder": "0", "class": "form-control"}),
            )

            # Campos para el vector inicial x₀
            field_x0_name = f"x0_{i}"
            self.fields[field_x0_name] = forms.FloatField(
                label=f"x₀[{i+1}]",
                widget=forms.NumberInput(attrs={"placeholder": "0", "class": "form-control"}),
            )
