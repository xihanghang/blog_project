
from django.shortcuts import render
def project_list(request):
    print(request.blog.user)
    print(request.blog.price_policy)
    return render(request,'project_list.html')