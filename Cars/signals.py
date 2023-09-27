from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cars, VacancyMuraciet, CarsOrder, FastOrder, OrderCancel, ContactUs
from services.generator import CodeGenerator
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=Cars)
def cars_code_signals(sender, instance, created, **kwargs):
    if created:
        instance.code = CodeGenerator.cars_code_create(size=8, model_=Cars)
        instance.save()


@receiver(post_save, sender=CarsOrder)
def cars_order_code_signals(sender, instance, created, **kwargs):
    if created:
        instance.code = CodeGenerator.cars_code_create(size=10, model_=CarsOrder)
        instance.save()
        send_mail(
            'Yeni sifariş',  # subject
            f"{instance.created_at.strftime('%d.%m.%Y')} tarixi üzrə yeni sifariş var.Müştəri ilə əlaqəyə keçin.\nSifariş kodu {instance.code} elan kodu {instance.car.code}",  # message
            settings.EMAIL_HOST_USER,  # from email
            ["elizaminoruc599@gmail.com"],  # to mail list
            fail_silently=False,
        )


@receiver(post_save, sender=OrderCancel)
def order_cancel_signals(sender, instance, created, **kwargs):
    if created:
        message = f"{instance.created_at.strftime('%d.%m.%Y')} tarixi üzrə sifarişin ləğv edilməsi müraciəti.\nSifarişin kodu: {instance.order_code}"
        send_mail(
            "Sifariş İmtina",
            message,
            settings.EMAIL_HOST_USER,
            ["elizaminoruc599@gmail.com"],
            fail_silently=False
            )


@receiver(post_save, sender=FastOrder)
def fast_order_code_signals(sender, instance, created, **kwargs):
    if created:
        instance.code = CodeGenerator.cars_code_create(size=10,model_=FastOrder)
        instance.save()
        message = f"{instance.created_at.strftime('%d.%m.%Y')} tarixi üzrə yeni sürətli sifariş müraciəti var.Müştəri ilə əlaqəyə keçin.\nMüştəri məlumatları:\nmobile:{instance.mobile} - Ad: {instance.full_name}\nSifariş kodu {instance.code}\nTəhfil tarixi: {instance.pickup_date}"
        send_mail(
            'Sürətli sifariş var!',  # subject
            message,
            settings.EMAIL_HOST_USER,  # from email
            ["elizaminoruc599@gmail.com"],  # to mail list
            fail_silently=False,
        )


@receiver(post_save, sender=VacancyMuraciet)
def new_vacancy_signals(sender, instance, created, **kwargs):
    if created:
        message = f"{instance.vacancy.name} vakansiyasına {instance.created_at.strftime('%d,%b,%Y')}-tarixi üzrə yeni müraciət var."
        send_mail(
            "Vakansiya müraciəti",
            message,
            settings.EMAIL_HOST_USER,
            ["elizaminoruc599@gmail.com"],
            fail_silently=False
            )


@receiver(post_save, sender=ContactUs)
def contact_us_signals(sender, instance, created, **kwargs):
    if created:
        message = f"{instance.created_at.strftime('%d.%m.%Y')} tarixi üzrə müraciət."
        send_mail(
            "Yeni müraciət var.",
            message,
            settings.EMAIL_HOST_USER,
            ["elizaminoruc599@gmail.com"],
            fail_silently=False
            )