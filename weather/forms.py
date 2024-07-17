from django import forms


class CityForm(forms.Form):
    """
    Форма для ввода названия города.

    Attributes:
        city (CharField): Название города.
    """

    city = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"autocomplete": "off"})
    )
