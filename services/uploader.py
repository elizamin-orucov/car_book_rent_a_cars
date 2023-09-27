class Uploader:

    @staticmethod
    def upload_logo_category(instance, filename):
        return f"categories/{instance.name}/{filename}"

    @staticmethod
    def upload_image_cars(instance, filename):
        return f"cars/{instance.car.model.name}/{filename}"