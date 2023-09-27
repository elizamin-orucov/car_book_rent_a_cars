from django.shortcuts import render, get_object_or_404
from services.choices import YEAR
from services.filters import CarsFilter
from .forms import (
    ContactUsForms, VacanciesForms, CarsOrderForms, FastOrderForms, OrderCancelForms
)
from django.http.response import JsonResponse
from .models import (
    Colors, Cars, Additional, GearBoxs,
    BanType, Fuel, Vacancies, Faq, CarsOrder
)
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings


def index_view(request):
    cars = Cars.objects.filter(status="Active").order_by("?")[:12]
    form = FastOrderForms()
    if request.method == "POST":
        form_ = FastOrderForms(request.POST or None)
        date = request.POST.get("pickup-date")
        pickup_location = request.POST.get("location")
        if form_.is_valid():
            new_order = form_.save(commit=False)
            new_order.pickup_location = pickup_location
            new_order.pickup_date = date
            new_order.save()
    context = {"cars": cars, "form": form}
    return render(request,"projects/index.html", context)


def cars_list_view(request):
    gearbox = GearBoxs.objects.order_by("created_at")
    colors = Colors.objects.order_by("created_at")
    bantype = BanType.objects.order_by("created_at")
    additional = Additional.objects.order_by("created_at")
    fuel = Fuel.objects.order_by("created_at")
    cars = Cars.objects.filter(status="Active").order_by("-created_at")

    filtered_cars = CarsFilter().get_filtered_cars(cars, request.GET)

    cars_ = filtered_cars[0]
    filter_dict = filtered_cars[1]

    paginator = Paginator(cars_, 9)
    page = request.GET.get("page", 1)
    car_list = paginator.get_page(page)

    context = {
               "gearbox": gearbox,
               "years": YEAR[::-1],
               "colors": colors,
               "bantype": bantype,
               "additional": additional,
               "fuels": fuel,
               "cars_list": car_list,
               "paginator": paginator,
               "filter_dict": filter_dict
               }

    return render(request, "cars/car.html", context)


def car_detail(request,id):
    car = get_object_or_404(Cars, id=id)
    cars_list = Cars.objects.order_by('?').exclude(id=id)[:6]
    addtional = Additional.objects.order_by("created_at")
    context = {"car": car, "addtionals": addtional, "cars_list": cars_list}
    return render(request,"cars/detail.html",context)


@login_required(login_url="users:login")
def wish_list_view(request):
    cars = Cars.objects.filter(wishlist__in=[request.user]).order_by("-created_at")
    paginator = Paginator(cars, 8)
    page = request.GET.get("page",1)
    cars_list = paginator.get_page(page)
    context = {"cars_list": cars_list, "paginator": paginator}
    return render(request, "projects/wishlist.html", context)


def contact_us(request):
    form = ContactUsForms()
    if request.method == "POST":
        form = ContactUsForms(request.POST)
        if form.is_valid():
            form.save()
    context = {"form":form}
    return render(request, "projects/contact_us.html", context)


@login_required(login_url="users:login")
def pricing_list_view(request):
    cars = Cars.objects.filter(pricing_list__in=[request.user])
    context = {"cars": cars}
    return render(request, "cars/pricing.html", context)


def about_view(request):
    return render(request, "projects/services.html", {})


def privacy_view(request):
    return render(request,"projects/privacy.html", {})


def wish_view(request):
    data = {}
    car = get_object_or_404(Cars,id=request.POST.get("id"))
    if request.user.is_authenticated:
        data["logg"] = True
        if request.user in car.wishlist.all():
            car.wishlist.remove(request.user)
            data["success"] = False
        else:
            car.wishlist.add(request.user)
            data["success"] = True
    else:
        data["logg"] = False

    return JsonResponse(data)


def pricing_view(request):
    data = {}
    car = get_object_or_404(Cars,id=request.POST.get("id"))
    if request.user.is_authenticated:
        data["logg"] = True
        if request.user in car.pricing_list.all():
            car.pricing_list.remove(request.user)
            data["success"] = False
        else:
            car.pricing_list.add(request.user)
            data["success"] = True
    else:
        data["logg"] = False

    return JsonResponse(data)


def vacancies_view(request):
    vacancy = Vacancies.objects.filter(status="Active")
    context = {"vacancy":vacancy}
    return render(request,"projects/vacancies.html", context)


def vacancy_detail(request, id):

    vacancy = Vacancies.objects.get(id=id)
    vacancies = Vacancies.objects.filter(status="Active").exclude(id=id)
    form = VacanciesForms()

    if request.method == "POST":
        form = VacanciesForms(request.POST, request.FILES or None)
        if form.is_valid():
            form_ = form.save(commit=False)
            form_.vacancy = vacancy
            form_.save()

    context = {"vacancy": vacancy, "vacancies": vacancies, "form": form}

    return render(request, "projects/vacancies-detail.html", context)


def vacancy_appleal(request,id):
    form = VacanciesForms()
    vacancy = Vacancies.objects.get(id=id)

    if request.method == "POST":
        form = VacanciesForms(request.POST, request.FILES or None)
        if form.is_valid():
            form_ = form.save(commit=False)
            form_.vacancy = vacancy
            form_.save()
    context = {"form": form, "vacancy": vacancy}
    return render(request, "projects/vacancy_appleal.html", context)


def faq_view(request):
    questions = Faq.objects.order_by("created_at")
    context = {"questions": questions}
    return render(request, "projects/faq.html", context)


def car_order_view(request,id):
    form = CarsOrderForms()
    car = get_object_or_404(Cars,id=int(id))
    if request.method == "POST":
        pickup_date = request.POST.get("pickup-date")
        drop_date = request.POST.get("drop-date")
        with_driver = request.POST.get("driver")

        form = CarsOrderForms(request.POST or None)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.car = car
            new_order.pickup_date = pickup_date
            new_order.drop_date = drop_date
            if with_driver:
                new_order.with_driver = "True"
            new_order.save()
            message = f"Sizin {new_order.car.model.parent} {new_order.car.model} sifarişiniz qeyde alınmışdır. Sifarişinizin kodu {new_order.code}\nTezliklə əməkdaşımız sizinlə əlaqə saxlayacaqdır."
            send_mail(
                'CarBook',  # subject
                message,  # message
                settings.EMAIL_HOST_USER,  # from email
                [new_order.email],  # to mail list
                fail_silently=False,
            )

    context = {
        "form": form
    }
    return render(request, "projects/car-order.html", context)


def order_cancel_view(request):
    form = OrderCancelForms()

    if request.method == "POST":
        form = OrderCancelForms(request.POST or None)
        if form.is_valid():
            form.save()

            code = form.cleaned_data.get("order_code")
            order = CarsOrder.objects.get(code=code)


            send_mail(
                "CarBook",
                f"Sizin {order.car.model.name} sifarişinin ləğvi istəyiniz qeydiyata alınmışdır.\nƏməkdaşımız sizinlə əlaqəyə keçəcək.",
                settings.EMAIL_HOST_USER,  # from email
                [order.email],  # to mail list
                fail_silently=False,
            )
    context = {"form": form}
    return render(request, "projects/order_cancel.html", context)