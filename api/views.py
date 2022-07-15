import logging

from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle

from .serializers import SignUpSerializer, StockPriceSerializer
from .stocks import StocksClient
from .exceptions import InvalidSymbolError, AlphaVantageApiError

logger = logging.getLogger(__name__)


@api_view(['POST'])
def signup_view(request):
    logger.info("Signup request")
    signup_serializer = SignUpSerializer(data=request.data)
    if signup_serializer.is_valid():
        signup_data = signup_serializer.validated_data
        logger.info("Valid signup data: %s", request.data)
        email = signup_data.get('email')
        if not User.objects.filter(username=email).exists():
            logger.info("User %s dont exists, creating it", email)
            user_extra_data = {'first_name': signup_data.get('name', ''), 'last_name': signup_data.get('lastname', '')}
            user_random_password = User.objects.make_random_password()
            user = User.objects.create_user(username=email, email=email,
                                            password=user_random_password, **user_extra_data)
            user.save()
        else:
            logger.info("User %s exists", email)
            user = User.objects.get(username=email)
        token, created = Token.objects.get_or_create(user=user)
        logger.info("Token %s for user %s", token.key, user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)
    else:
        logger.error("Invalid signup data: %s", signup_serializer.errors)
        return Response({"message": signup_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def get_stocks_view(request, symbol):
    logger.info("Get stocks for: %s", symbol)
    stocks_client = StocksClient(settings.ALPHA_VANTAGE_API_KEY)
    try:
        stock_price = stocks_client.get_stocks_price(symbol)
        stock_price_json = StockPriceSerializer(stock_price.get_data())
        logger.info("%s requested: %s", request.user, stock_price_json.data)
    except InvalidSymbolError as e:
        return Response({"error": e.message}, status=status.HTTP_400_BAD_REQUEST)
    except AlphaVantageApiError:
        return Response({"error": f"Problems with the api"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except Exception as e:
        logger.error("Unknown error: %s", e)
        return Response({"error": f"Problems with the api"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    else:
        return Response(stock_price_json.data, status=status.HTTP_200_OK)

