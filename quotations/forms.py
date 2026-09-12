from django import forms

from .models import (
    Customer,
    QuoteRequest,
    Service,
)


class QuoteRequestForm(forms.ModelForm):

    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select Services",
    )

    class Meta:
        model = QuoteRequest

        fields = [
            "customer",
            "services",
            "requirements",
        ]

        widgets = {
            "customer": forms.Select(
                attrs={
                    "class": "form-select form-select-lg",
                }
            ),

            "requirements": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": (
                        "Tell us about your project or requirements..."
                    ),
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["customer"].queryset = (
            Customer.objects.select_related("business")
        )

        self.fields["services"].queryset = (
            Service.objects.filter(is_active=True)
            .select_related("business")
        )