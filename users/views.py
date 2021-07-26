from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserSerializer


class UserView(APIView):

    def get(self, request):
        if request.GET:
            try:
                user = User.objects.get(Q(username=request.GET.get('login')) | Q(pk=request.GET.get('id')))
                serializer = UserSerializer(user)
                return Response({'user': serializer.data})
            except ObjectDoesNotExist:
                return Response('User not found')
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({'users': serializer.data})

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({'success': f'User created successfully'})

    def put(self, request):
        if request.GET:
            user = get_object_or_404(User.objects.all(),
                                     Q(username=request.GET.get('login')) | Q(pk=request.GET.get('id')))
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({'success': f'User updated successfully'})

    def delete(self, request):
        user = get_object_or_404(User.objects.all(),
                                 Q(username=request.GET.get('login')) | Q(pk=request.GET.get('id')))
        user.delete()
        return Response({
            'message': f'User has been deleted.'
        }, status=204)
