from django import forms
from .models import ContactUs, VacancyMuraciet, CarsOrder, FastOrder, OrderCancel
import pathlib


class ContactUsForms(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for filed in self.fields:
            placeholders={"name":"Adınız","email":"Mailiniz","subject":"Başlıq","message":"Müraciətiniz"}
            self.fields[filed].widget.attrs.update({"class":"form-control","placeholder":f"{placeholders[filed]}"})


class VacanciesForms(forms.ModelForm):
    class Meta:
        model = VacancyMuraciet
        exclude = ("vacancy",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {"fullname":"* Ad, soyad, ata adı","email":"* Mail ünvanı","mobile":"* Mobil nömrə","description":"Motivasiya məktubu"}
        for field in placeholders:
            self.fields[field].widget.attrs.update({"class":"form-control","placeholder":f"{placeholders[field]}"})

    def clean(self):
        file = self.cleaned_data.get("cv")
        # full_name = self.cleaned_data.get("fullname")
        # name = full_name.split(" ")
        if file:
            if file is not None and file is not False:
                file_path = pathlib.Path(str(file)).suffix
                if file_path not in ['.pdf', '.pdfa', '.pdfx','.pdfvt','.pdfua']:
                    self.add_error("cv", "CV sadəcə .pdf, .pdfa, .pdfx, .pdfvt və .pdfua formatında yüklənə bilər.")
            # if len(name) <= 2:
            #     self.add_error("full_name","Ad, soyad və ata adını düzgün qeyd edin.")
        return self.cleaned_data



class CarsOrderForms(forms.ModelForm):
    class Meta:
        model = CarsOrder
        fields = ("full_name", "mobile", "email", "pickup_location", "passport_series", "driving_license_category")

    def clean(self):
        fullname = self.cleaned_data.get("full_name")
        name = fullname.split(" ")
        if len(name) <= 2:
            self.add_error("full_name","Xahiş edirik ad, soyad və ata adınızı düzgün qeyd edəsiniz.")
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        placeholders = {
            "full_name": "*Ad, soyad və ata adı.",
            "mobile": "*Əlaqə saxlamağımız üçün mobil nömrə.",
            "email": "*Əlaqə saxlamağımız üçün mail ünvanı.",
            "pickup_location": "Götürmə yeri.",
            "passport_series": "*Şəxsiyyət vəsiqəsinin seriya nömrəsi.",
            "driving_license_category": "Sürücülük vəsiqəsinin kateqoriyası."
        }
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class":"form-control","placeholder":f"{placeholders[field]}"})


class FastOrderForms(forms.ModelForm):
    class Meta:
        model = FastOrder
        fields = ("full_name", "mobile", "driver_license")

    def __init__(self, *args, **kwargs):
        placeholders = {"full_name": "Ad, soyad və ata adı", "mobile": "Telefon nömrəsi", "driver_license":"Kategoriya?-A,B.."}
        super().__init__(*args, **kwargs)
        for filed in self.fields:
            self.fields[filed].widget.attrs.update({"class": "form-control", "style": "color:black;", "placeholder": f"{placeholders[filed]}"})




class CarsSOrderForms(forms.ModelForm):
    class Meta:
        model = CarsOrder
        fields = ("car","full_name", "mobile", "email", "pickup_location", "passport_series", "driving_license_category")


    def clean(self):
        fullname = self.cleaned_data.get("full_name")
        name = fullname.split(" ")
        if len(name) <= 2:
            self.add_error("full_name","Xahiş edirik ad, soyad və ata adını düzgün qeyd edəsiniz.")
        return self.cleaned_data


    def __init__(self, *args, **kwargs):
        placeholders = {
            "full_name": "*Ad, soyad və ata adı.",
            "mobile": "*Əlaqə saxlamağımız üçün mobil nömrə.",
            "email": "*Əlaqə saxlamağımız üçün mail ünvanı.",
            "pickup_location": "Götürmə yeri.",
            "passport_series": "*Şəxsiyyət vəsiqəsinin seriya nömrəsi.",
            "driving_license_category": "Sürücülük vəsiqəsinin kateqoriyası."
        }
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class":"form-control","placeholder":f"{placeholders[field]}"})


class OrderCancelForms(forms.ModelForm):
    class Meta:
        model = OrderCancel
        fields = ("full_name", "order_code", "reason")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {"full_name": "Ad, soyad və ata adı", "order_code":"Sifariş kodu", "reason":"İmtina səbəbi"}
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class":"form-control", "placeholder":f"{placeholders[field]}"})

    def clean(self):
        code = self.cleaned_data.get("order_code")
        full_name = self.cleaned_data.get("full_name")
        name = full_name.split(" ")
        if len(name) <= 2:
            self.add_error("full_name","Ad, soyad və ata adını düzgün qeyd edin.")
        if not CarsOrder.objects.filter(code=code).exists():
            self.add_error("order_code","Sifariş tapilmadı. Sifariş kodu yanlışdır")
        return self.cleaned_data


