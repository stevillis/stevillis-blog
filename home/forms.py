import re

from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Seu nome",
                "class": "p-3 w-full my-2 bg-gray-900 border-slate-700 rounded-lg",
                "minlength": "2",
            }
        ),
        required=True,
        min_length=2,
        error_messages={
            "required": "Nome é obrigatório",
            "min_length": "Nome deve ter pelo menos 2 caracteres",
        },
    )

    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Seu email",
                "class": "p-3 w-full my-2 bg-gray-900 border-slate-700 rounded-lg",
            }
        ),
        required=True,
        error_messages={
            "required": "Email é obrigatório",
            "invalid": "Formato de email inválido",
        },
    )

    def validate_phone(value):
        if value:
            # Brazilian phone number pattern
            pattern = r"^\(?([1-9]{2})\)?[-.\s]?([2-9]{1}[0-9]{3,4})[-.\s]?([0-9]{4})$"
            if not re.match(pattern, value):
                raise forms.ValidationError(
                    "Formato de telefone inválido. Use: (XX) XXXXX-XXXX ou XX XXXXX XXXX"
                )

    phone = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Seu telefone",
                "class": "p-3 w-full my-2 bg-gray-900 border-slate-700 rounded-lg",
            }
        ),
        required=False,
        validators=[validate_phone],
        error_messages={
            "invalid": "Formato de telefone inválido. Use: (XX) XXXXX-XXXX ou XX XXXXX XXXX",
        },
    )

    message = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Sua mensagem",
                "class": "p-3 resize-none w-full h-72 my-2 bg-gray-900 border-slate-700 rounded-lg",
                "minlength": "10",
            }
        ),
        required=True,
        min_length=10,
        error_messages={
            "required": "Mensagem é obrigatória",
            "min_length": "Mensagem deve ter pelo menos 10 caracteres",
        },
    )
