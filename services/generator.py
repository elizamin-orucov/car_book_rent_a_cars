import string
import random

chars = string.digits + string.ascii_letters

class CodeGenerator:
    @staticmethod
    def code_slug_generator(size, chars=chars):
        return "".join(random.choice(chars) for _ in range(size))

    @staticmethod
    def cars_code_generator(size, chars=string.digits):
        return "".join(random.choice(chars) for _ in range(size))

    @classmethod
    def create_slug_shortcode(cls, size, model_):
        new_code = cls.code_slug_generator(size=size)
        qs_exists = model_.objects.filter(code=new_code).exists()
        return cls.create_slug_shortcode(size, model_) if qs_exists else new_code

    @classmethod
    def create_user_activate_shortcode(cls, size, model_):
        new_code = cls.code_slug_generator(size=size)
        qs_exists = model_.objects.filter(activation_code=new_code).exists()
        return cls.create_user_activate_shortcode(size, model_) if qs_exists else new_code


    @classmethod
    def create_customer_shortcode(cls, size, model_):
        new_code = cls.code_slug_generator(size=size)
        qs_exists = model_.objects.filter(customer_code=new_code).exists()
        return cls.create_customer_shortcode(size, model_) if qs_exists else new_code

    @classmethod
    def create_slug_shortcode_profile(cls, size, model_):
        new_code = cls.code_slug_generator(size=size)
        qs_exists = model_.objects.filter(slug=new_code).exists()
        return cls.create_slug_shortcode(size, model_) if qs_exists else new_code

    @classmethod
    def create_activation_link_code(cls, size, model_):
        new_code = cls.code_slug_generator(size=size)
        qs_exists = model_.objects.filter(activation_code=new_code).exists()
        return cls.create_user_activate_shortcode(size, model_) if qs_exists else new_code

    @classmethod
    def cars_code_create(cls, size, model_):
        code1 = cls.cars_code_generator(size=size)
        qs_exists = model_.objects.filter(code=code1).exists()
        return cls.cars_code_create(size, model_) if qs_exists else code1