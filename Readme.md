<div id="topic">
<h1>Topic:</h1>
<ol>
<li><a href="#intro">Intro</a></li>
<li><a href="#set_up">Set Up Virtual Environment</a></li>
<li><a href="#jsonResponse">Create JSON Response Without Any Framework</a></li>
</ol>
</div>

<div id="intro">
    <a href="#topic">Topic</a>
<h1>Introduction: </h1>
<h3>API + REST Architecture => REST API</h3>
<h3>REST API has 4 parts. These are: (i) End Points, (ii) Headers (Status Code), (iii) Methods (CRUD), (iv) The Data ( JSON )</h3>
</div>

<div id="set_up">
    <a href="#topic">Topic</a>
<h1>Set Up Virtual Environment and Django and Rest Framework installation in environment</h1>

<h3>Create virtual environment:</h3>

```
python -m venv env1
```

<h3>Activate virtual environment</h3>

```
source path/env1/bin/activate
```

<h3>Install django and rest framework</h3>

```
pip install django
pip install djangorestframework
```

<h3>For increase productivity use tabnine and github copilot. You can install these from vs code extensions.Json Viewer pro for chrome extension.</h3>
</div>

<div id="jsonResponse">
    <a href="#topic">Topic</a>
<h1>Create JSONResponse</h1>
<h3>It sends JSON response without REST Framework.</h3>

`views.py`

```py
def movie_list(request):
    movies = Movie.objects.all() # it creates all objects from model
    print (movies.values()) # prints all objects
    data={'movies':list(movies.values())} # converts all objects to json
    return JsonResponse(data) # returns json response

def movie_detail(request, pk):
    try:
        movies = Movie.objects.get(pk=pk) # it fetches a single object by id
        data = {
            'name':movies.name,
            'description':movies.description,
            'active':movies.active, 
        } # converts object to json
    except Movie.DoesNotExist:
        return HttpResponse(status=404) # returns 404 if movie not found
    return JsonResponse(data) # returns json response
```

`urls.py`
```py
from django.shortcuts import render
from django.urls import URLPattern,include,path
from .views import movie_list,movie_detail
urlpatterns=[
    path('list/',movie_list,name='movie_list'),
    path('list/<int:pk>',movie_detail),  # it searches for specific id
]
```
</div>

<div id="">
    <a href="#topic">Topic</a>

``
```py

```
</div>