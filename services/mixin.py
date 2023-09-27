from django.db import models


class DateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SlugMixin(models.Model):
    slug = models.SlugField(unique=True, editable=False)
    code = models.SlugField(unique=True, editable=False)

    class Meta:
        abstract = True


class BaseModel(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True
