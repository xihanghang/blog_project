
from web import models
from django.shortcuts import render,HttpResponse
def latest_essay(request):
    wiki_object=models.Wiki.objects.all()
    print(wiki_object)
    return render(request,'latest_essay.html',{'data':wiki_object})