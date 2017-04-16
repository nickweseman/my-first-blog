from django.shortcuts import render

def post_list(request, header):
    print(header)
    print(request)
    print(type(header))
    return render(request, 'blog/post_list.html', {})

