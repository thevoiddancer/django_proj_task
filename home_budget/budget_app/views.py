from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, Django!")




# from rest_framework import viewsets, permissions
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.decorators import action
# from .models import Expense, Income, Category
# from .serializers import ExpenseSerializer, IncomeSerializer, CategorySerializer
# from django.db.models import Sum

# class ExpenseViewSet(viewsets.ModelViewSet):
#     serializer_class = ExpenseSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Expense.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# class IncomeViewSet(viewsets.ModelViewSet):
#     serializer_class = IncomeSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Income.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [permissions.IsAuthenticated]

# class CurrentStateView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         total_income = Income.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
#         total_expense = Expense.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
#         return Response({
#             'total_income': total_income,
#             'total_expense': total_expense,
#             'current_balance': total_income - total_expense
#         })

# class ExpenseByCategoryView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         data = (
#             Expense.objects.filter(user=request.user)
#             .values('category__name')
#             .annotate(total=Sum('amount'))
#         )
#         return Response(data)
