import requests
import re
# from django.conf import settings


class VINDecoder:
    API_URL = (
        "https://vpic.nhtsa.dot.gov/api/vehicles/"
        "DecodeVINValues/{vin}?format=json"
    )

    @classmethod
    def get_vehicle_info(cls, vin):
        if not cls.is_valid_vin(vin):
            return None

        try:
            response = requests.get(cls.API_URL.format(vin=vin))
            response.raise_for_status()
            data = response.json()

            if data.get('Results'):
                vehicle = data['Results'][0]
                return {
                    'mark': vehicle.get('Make', '').title(),
                    'model': vehicle.get('Model', '').title(),
                    'year': (
                        int(vehicle.get('ModelYear'))
                        if vehicle.get('ModelYear')
                        else None
                    ),
                    'vin': vin
                }
        except (requests.RequestException, ValueError, KeyError) as e:
            print(f"Ошибка при декодировании VIN: {e}")
        return None

    @staticmethod
    def is_valid_vin(vin):
        vin = str(vin).strip().upper()
        return re.match(r'^[A-HJ-NPR-Z0-9]{17}$', vin) is not None
