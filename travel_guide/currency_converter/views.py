# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import CurrencyConverter,SafetyService,get_coordinates,get_emergency_services,Countrycode_Service
from .serializers import CurrencyConversionSerializer,EmergencyServiceSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny

class CurrencyConversionView(APIView):
    serializer_class=CurrencyConversionSerializer
    # permission_classes = [IsAuthenticated]
    def get(self,request):
        currency_converter = CurrencyConverter()
        currency_codes = currency_converter.get_currency_codes()
        if currency_codes is not None:
            response_data = {'currency_codes': currency_codes}
            return Response(response_data)
        else:
            return Response({'error': 'Unable to fetch information'}, status=500)

    def post(self, request):
        serializer = CurrencyConversionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']
        from_currency = serializer.validated_data['from_currency']
        to_currency = serializer.validated_data['to_currency']

        # Make sure to replace 'your_api_key' with your actual API key  f6e9d49461055b64ddbf1f7d
        currency_converter = CurrencyConverter()

        converted_amount = currency_converter.convert_currency(amount, from_currency, to_currency)
         
        if converted_amount is not None:
            response_data = {'converted_amount': converted_amount}
            return Response(response_data)
        else:
            return Response({'error': 'Unable to fetch exchange rates'}, status=500)


class SafetyInfoView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        country_code = self.request.query_params.get('country_code')

        # Replace 'https://api.safetyprovider.com/' with the actual base URL
        safety_service = SafetyService()

        country_safety_info = safety_service.get_safety_information(country_code)
        if country_safety_info is not None:
            response_data = {'country_safety_info': country_safety_info}
            return Response(response_data)
        else:
            return Response({'error': 'Unable to fetch safety information'}, status=500)

class Country_codeView(APIView):
    def get(self,request):

        # Replace 'https://api.safetyprovider.com/' with the actual base URL
        safety_service = Countrycode_Service()

        country_codes = safety_service.iso_countrycode()
        if country_codes is not None:
            response_data = {'country_codes': country_codes}
            return Response(response_data)
        else:
            return Response({'error': 'Unable to fetch safety information'}, status=500)


class EmergencyServicesView(APIView):
    def post(self, request, *args, **kwargs):
        place_name = request.data.get('place_name')

        if not place_name:
            return Response({'error': 'Place name is required'}, status=status.HTTP_400_BAD_REQUEST)

        coordinates = get_coordinates(place_name)

        if not coordinates:
            return Response({'error': 'Failed to obtain coordinates'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        lat, lng = coordinates
        print('ggg',lat,'ggg',lng,'ggg')
        emergency_services = get_emergency_services(lat, lng)

        if not emergency_services:
            return Response({'error': 'Failed to obtain emergency services'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'emergency_services': emergency_services})