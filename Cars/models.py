from django.db import models
from services.mixin import DateMixin, BaseModel
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from services.choices import (
    YEAR, MOTOR, STATUS, TRANSMİTTER, VACANCY,
    DRIVING_LICENSE_CHOICES, PICKUP_LOCATION_CHOICES,
    DRIVER_CHOICES, CARS_STATUS_CHOICES
)
from services.uploader import Uploader
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone


User = get_user_model()


class Category(BaseModel, DateMixin, MPTTModel):
    parent = TreeForeignKey("self",on_delete=models.CASCADE,blank=True,null=True,related_name='children')
    icon = models.ImageField(upload_to=Uploader.upload_logo_category,blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Kateqoriyalar"
        verbose_name = "Kateqoriya"


class GearBoxs(BaseModel, DateMixin):

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Sürətlər qutusu"
        verbose_name = "Sürətlər qutusu"


class Colors(BaseModel, DateMixin):

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Rənglər"
        verbose_name = "Rəng"


class BanType(BaseModel, DateMixin):

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Ban növləri"
        verbose_name = "Ban növü"


class Additional(BaseModel, DateMixin):

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Əlavə təchizatlar"
        verbose_name = "Təchizat"


class Fuel(BaseModel, DateMixin):

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Yanacaq növləri"
        verbose_name = "Yanacaq"


class Cars(DateMixin):
    model = models.ForeignKey(Category,on_delete=models.CASCADE)
    year = models.IntegerField(choices=YEAR)
    color = models.ForeignKey(Colors,on_delete=models.CASCADE)
    gearbox = models.ForeignKey(GearBoxs,on_delete=models.CASCADE)
    bantype = models.ForeignKey(BanType,on_delete=models.CASCADE)
    description = RichTextField(blank=True,null=True)
    engine = models.FloatField(choices=MOTOR)
    fuel = models.ForeignKey(Fuel,on_delete=models.CASCADE)
    additional = models.ManyToManyField(Additional,blank=True)
    transmitter = models.CharField(max_length=30,choices=TRANSMİTTER)

    seats_count = models.PositiveIntegerField()
    with_driver = models.BooleanField(default=False)
    wishlist = models.ManyToManyField(User,blank=True,editable=False)
    pricing_list = models.ManyToManyField(User,blank=True,related_name="pricing",editable=False)
    status = models.CharField(max_length=30,choices=STATUS,default="Active")
    code = models.SlugField(unique=True, editable=False, blank=True, null=True)

    price_to_day = models.FloatField()
    price_to_week = models.FloatField()
    price_to_month = models.FloatField()
    discount_price = models.FloatField(blank=True,null=True)

    def __str__(self):
        return self.model.name

    class Meta:
        verbose_name_plural = "Maşınlar"
        verbose_name = "Maşın"


class CarsImages(DateMixin):
    car = models.ForeignKey(Cars,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=Uploader.upload_image_cars)

    def __str__(self):
        return self.car.model.name

    class Meta:
        verbose_name_plural = "Maşınlar şəkil"
        verbose_name = "Şəkil"


class OrderItems(DateMixin):
    cars = models.ForeignKey(Cars,on_delete=models.CASCADE)

    month_count = models.PositiveIntegerField()

    def __str__(self):
        return f" sifaris {self.cars.model}  ay sayi {self.month_count}"


class Orders(DateMixin):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    cars_item = models.ManyToManyField(OrderItems,blank=True)


class ContactUs(BaseModel, DateMixin):
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()

    def __str__(self):
        return f"İstifadəçi: {self.name} --- {self.email} Başlıq: {self.subject}"

    class Meta:
        verbose_name_plural = "Muracietler"
        verbose_name = "Muraciet"


class Vacancies(BaseModel, DateMixin):
    salary = models.FloatField(blank=True, null=True)
    type = models.CharField(max_length=30,choices=VACANCY, blank=True, null=True)
    image = models.ImageField(upload_to="vacancies/", blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS, default="Active")
    obligations = RichTextField()
    requirments = RichTextField()
    working_conditions = models.CharField(max_length=100)
    view_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Vakansiyalar"
        verbose_name = "Vakansiya"


class VacancyMuraciet(DateMixin):
    vacancy = models.ForeignKey(Vacancies,on_delete=models.CASCADE,blank=True,null=True)
    fullname = models.CharField(max_length=200)
    email = models.EmailField()
    mobile = PhoneNumberField(region="AZ")
    description = models.TextField(blank=True, null=True)
    cv = models.FileField(upload_to="vakansiyalar/",blank=True,null=True)

    class Meta:
        verbose_name_plural = "Vakansiya müraciətləri"
        verbose_name = "Müraciət"

    def __str__(self):
        return f"Müraciət olunan vakansiya: {self.vacancy.name}"


class Faq(DateMixin):
    question = models.CharField(max_length=200)
    answer = RichTextField()

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = "Tez-tez verilən suallar"
        verbose_name = "Sual"


class CarsOrder(DateMixin):
    car = models.ForeignKey(Cars, on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=200)
    mobile = PhoneNumberField(region="AZ")
    email = models.EmailField()
    pickup_location = models.CharField(max_length=100, choices=PICKUP_LOCATION_CHOICES,default="İcarə məntəqəsi")
    passport_series = models.CharField(max_length=50)
    driving_license_category = models.CharField(max_length=30, choices=DRIVING_LICENSE_CHOICES, blank=True, null=True)
    pickup_date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    drop_date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    code = models.SlugField(unique=True, editable=False, blank=True, null=True)
    with_driver = models.CharField(max_length=30,choices=DRIVER_CHOICES,default="False")
    status = models.CharField(max_length=50,choices=CARS_STATUS_CHOICES,default="Gözləmədə")

    def __str__(self):
        return f"Sifariş:{self.car.model.name}"

    class Meta:
        verbose_name_plural = "Sifarişlər"
        verbose_name = "Sifariş"


class FastOrder(DateMixin):
    full_name = models.CharField(max_length=100)
    mobile = PhoneNumberField(region="AZ")
    pickup_location = models.CharField(max_length=100, choices=PICKUP_LOCATION_CHOICES, default="İcarə məntəqəsi", blank=True, null=True)
    pickup_date = models.CharField(max_length=100)
    driver_license = models.CharField(max_length=30)
    code = models.SlugField(unique=True, editable=False)

    def __str__(self):
        return f"{self.full_name}: {self.pickup_date}"

    class Meta:
        verbose_name_plural = "Sürətli sifarişlər"
        verbose_name = "Sifariş"


class OrderCancel(DateMixin):
    full_name = models.CharField(max_length=100)
    order_code = models.CharField(max_length=30)
    reason = models.TextField()
    status = models.CharField(max_length=70, choices=CARS_STATUS_CHOICES, default="Gözləmədə")

    def __str__(self):
        return f"Sifariş: {self.order_code} --- {self.created_at.strftime('%d.%m.%Y')}"

    class Meta:
        verbose_name_plural = "Ləğv ediləcək sifarişlər"
        verbose_name = "Sifariş"