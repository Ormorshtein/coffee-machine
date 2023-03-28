from enum import Enum


class MeasurementUnit(Enum):
    GRAM = 'g'
    MILLILITER = 'ml'


class Resource(Enum):
    MILK = ('milk', MeasurementUnit.MILLILITER)
    WATER = ('water', MeasurementUnit.MILLILITER)
    COFFEE = ('coffee', MeasurementUnit.GRAM)

    def __new__(cls, resource_type: str, measurement_unit: MeasurementUnit):
        new_resource = object.__new__(cls)
        new_resource._value_ = resource_type
        new_resource.measurement_unit = measurement_unit
        return new_resource
