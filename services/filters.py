from django.db.models import Q


class CarsFilter:

    FILTER_PART = {
        "year": lambda x: Q(year__gte=int(x)),
        "day-price": lambda x: Q(price_to_day__lte=float(x)),
        "week-price": lambda x: Q(price_to_week__lte=float(x)),
        "month-price": lambda x: Q(price_to_month__lte=float(x)),
        "gearbox": lambda x: Q(gearbox_id=int(x)),
        "bantype": lambda x: Q(bantype_id=int(x)),
        "color": lambda x: Q(color_id=int(x)),
        "fuel": lambda x: Q(fuel_id=int(x)),
        "gear": lambda x: Q(transmitter=x),
        "driver": lambda x: Q(with_driver=x),
        "addtional": lambda x: Q(additional__in=x),
    }

    GET_DATA = {
        "year": lambda data, key: data.get(key),
        "day-price": lambda data, key: data.get(key),
        "week-price": lambda data, key: data.get(key),
        "month-price": lambda data, key: data.get(key),
        "gearbox": lambda data, key: data.get(key),
        "bantype": lambda data, key: data.get(key),
        "color": lambda data, key: data.get(key),
        "fuel": lambda data, key: data.get(key),
        "gear": lambda data, key: data.get(key),
        "driver": lambda data, key: data.get(key),
        "addtional": lambda data, key: data.getlist(key),
    }

    def get_filtered_cars(self, queryset, data):
        filter_, filter_dict, = Q(), {}

        for key in data:
            if data[key] and key in self.FILTER_PART.keys():
                filter_.add(
                    self.FILTER_PART[key](
                        self.GET_DATA[key](data, key)
                    ), Q.AND
                )
                filter_dict[key] = f"{key}={self.GET_DATA[key](data, key)}&"

        return queryset.filter(filter_).distinct(), filter_dict.values()
