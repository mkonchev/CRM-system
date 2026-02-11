from typing import Optional, Dict, Any
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from apps.car.models.CarModel import Car
from apps.api.serializers.CarSerializer import CarSerializer


class CarService:

    @staticmethod
    def get_cars(filters: Optional[dict] = None) -> list[Car]:
        """Get car list with 'mark' and 'year' filters"""
        queryset = Car.objects.all()

        if filters:
            if mark := filters.get('mark'):
                queryset = queryset.filter(mark__icontains=mark)
            if year := filters.get('year'):
                queryset = queryset.filter(year=year)

        return queryset

    @staticmethod
    def get_car(pk: int):
        """Get car by id"""
        return get_object_or_404(Car, pk=pk)

    @staticmethod
    def create_car(data: Dict[str, Any]) -> Car:
        """Create new car"""
        serializer = CarSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @staticmethod
    def update_car(pk: int, data: Dict[str, Any], partial: bool = False) -> Car:
        """Update the car"""
        car = get_object_or_404(Car, pk=pk)
        serializer = CarSerializer(car, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @staticmethod
    def delete_car(pk: int) -> None:
        """Delete the car"""
        car = get_object_or_404(Car, pk=pk)
        car.delete()
