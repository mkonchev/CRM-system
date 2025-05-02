from django import forms
from apps.car.models.CarModel import Car
from apps.car.services.VINDecoder import VINDecoder


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['vin', 'number', 'owner']

    def clean_vin(self):
        vin = self.cleaned_data['vin'].upper()
        if not VINDecoder.is_valid_vin(vin):
            raise forms.ValidationError(
                "Неверный формат VIN номера. "
                "Должно быть 17 символов "
                "(цифры и заглавные буквы кроме I, O, Q)"
            )
        return vin
