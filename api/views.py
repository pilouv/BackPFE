from django.shortcuts import render, HttpResponse
from api.models import Article
#from api.serializers import ArticleSerializer
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework import viewsets
from django.core import serializers
import json
from django.views.generic import View
from django.http import JsonResponse
from api import pfexpert_clean

# Create your views here.
path = "videos/atkdltyyen.mp4"

class ArticleView(View):
    def get(self, *args, **kwargs):
        #queryset = Article.objects.all()
        #test = pfexpert_clean.main(path)
        #print("LET'S GO :",test)
        context = {
            #'articles' : json.loads(serializers.serialize('json', queryset))
            #"res" : [{"id": "1", "res" : "12"},{"id" :"2","res":"8"}] 
            #"score" : [{"score": float(test)}]
            "score" : [{"score": "0.98"}]
        }
        return JsonResponse(context)

"""
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    print(queryset)
    serializer_class = ArticleSerializer
"""
"""
class ArticleList(APIView):

    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def article_list(request):

    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.erros, status=400)
"""