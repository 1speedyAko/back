from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import SubscriptionPlan, UserSubscription
from .serializers import SubscriptionPlanSerializer, UserSubscriptionSerializer
from .utils import process_crypto_payment

class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer

class UserSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk=None):
        plan = self.get_object()
        user = request.user
        # Call the function to process the payment
        success = process_crypto_payment(user, plan)
        if success:
            UserSubscription.objects.create(user=user, plan=plan)
            return Response({'status': 'subscription successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'subscription failed'}, status=status.HTTP_400_BAD_REQUEST)

def process_payment(request):
    # Your payment processing logic here
    pass
