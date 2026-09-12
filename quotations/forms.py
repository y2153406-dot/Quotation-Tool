from django import forms

from .models import QuoteRequest


class QuoteRequestForm(forms.ModelForm):

    class Meta:
        model = QuoteRequest

        fields = [
            "customer",
            "requirements",
            "quantity",
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
                    "placeholder": "Tell us about your project or requirements...",
                }
            ),

            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-lg",
                    "min": 1,
                }
            ),
        }