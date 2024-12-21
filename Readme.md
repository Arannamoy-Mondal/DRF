<div id="topic">
<h1>Topic:</h1>
<ol>
<li><a href="#intro">Intro</a></li>
<li><a href="#set_up">Set Up Virtual Environment</a></li>
<li><a href="#jsonResponse">Create JSON Response Without Any Framework</a></li>
<li><a href="#serialization">Serialization</a></li>
<li><a href="#view">View</a></li>
<li><a href="#functionbasedview">Functionbasedview</a></li>
<li><a href="#validation">Validation</a></li>
<li><a href="#customSerializerField">Custom Serializer Field</a></li>
<li><a href="#updatingModel">Update Model</a></li>
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

<div id="serialization">
<a href="#topic">Topic</a>
<h1>Serialization:</h1>
<h3>Most used these two serializer (i) Serializer (ii) ModelSerializer</h3>

<strong>Serializer</strong>

`serializers.py`

```py
from rest_framework import serializers
from .models import Movie
class MovieSerializer(serializers.Serializer): # General Serializer
class Meta:
model=Movie # Select Model
fields='__all__' # List of fields


class MovieModelSerializer(serializers.ModelSerializer): # Model serializer
class Meta:
model=Movie # select Model
fields='__all__' # select fields

```

<strong>ModelSerializer</strong>

`serializers.py`

```py
class MovieModelSerializer(serializers.ModelSerializer): # Model serializer . Don not need crud method. This is the benefit of model serializers.
class Meta:
model=Movie # select Model
fields='__all__' # select fields
exclude=['name','description']

```
</div>


<div id="view">
<a href="#topic">Topic</a>

<h1>View:</h1>
<h3>Two types of views classbased and function based view. classbased view used four type of views (Generic views, Mixins, Concrete class views, Viewsets).
But function based views use decorator for view ( @api_view ).
</h3>

`views.py`
```py
@api_view() # need to use decorator for api views
def post(self): # function based
return JsonResponse(self)

class MovieViewSet(viewsets.ModelViewSet):
queryset = Movie.objects.all()
serializer_class = MovieModelSerializer # using serializer from serializers.py
```


</div>

<div id="functionbasedview">
<a href="#topic">Topic</a>
<h1>Functionbasedview:</h1>
<h3>Function based api view</h3>

`serializers.py`
```py
from rest_framework import serializers
from .models import Movie
class MovieSerializer(serializers.Serializer): # General Serializer
id=serializers.IntegerField(read_only=True)
name=serializers.CharField()
description=serializers.CharField()
active=serializers.BooleanField()
# class Meta:
# model=Movie # Select Model
# fields='__all__' # List of fields
```

`views.py`

```py
@decorators.api_view(['GET']) # from rest_framework import decorators
def movie_list(request):
movie=Movie.objects.all()
serializer=MovieSerializer(movie,many=True) # many=true means it check all object of serializer individually.
return response.Response(serializer.data)
```

<strong>Sample CRUD operation</strong>
<h3>For function based view</h3>

`views.py`

```py   
@decorators.api_view(['GET','POST','DELETE','PUT'])
def movie_detail(request, pk):
if request.method=='GET':
try:
movies = Movie.objects.get(pk=pk) # it fetches a single object by id
serializer=MovieSerializer(movies)
except Movie.DoesNotExist:
return HttpResponse(status=404) # returns 404 if movie not found
return response.Response(serializer.data) # returns json response
if request.method=='POST':
serializer=MovieSerializer(data=request.data)
if serializer.is_valid():
serializer.save()
return redirect('movie_list')
return HttpResponse('Something went wrong')
if request.method == 'PUT':
movie = Movie.objects.get(pk=pk)
serializer = MovieSerializer(movie, data=request.data)
if serializer.is_valid():
serializer.save()
return response.Response(serializer.data)
else:
return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
if request.method == 'DELETE':
movie = Movie.objects.get(pk=pk)
movie.delete()
return response.Response(status=status.HTTP_204_NO_CONTENT)
```

<h3>For class based view</h3>

`serializer.py`

```py
from rest_framework import serializers
from .models import Movie
class MovieSerializer(serializers.Serializer): # General Serializer
id=serializers.IntegerField(read_only=True)
name=serializers.CharField()
description=serializers.CharField()
active=serializers.BooleanField(read_only=True)


def create(self,validated_data):  # create method
movie = Movie.objects.create(**validated_data)
return movie   

def update(self, instance, validated_data): # update method
instance.name = validated_data.get('name', instance.name)
instance.description = validated_data.get('description', instance.description)
instance.active = validated_data.get('active', instance.active)
instance.save()
return instance 


class MovieModelSerializer(serializers.ModelSerializer): # Model serializer
class Meta:
model=Movie # select Model
fields='__all__' # select fields
```


`views.py`

```py
class movie_list(views.APIView):

def get(self,request): # instead of get condition and can not use if serializer.is_valid() in get method
movies=Movie.objects.all()
serializer=MovieSerializer(movies,many=True)
return response.Response(serializer.data)

def post(self,request): 
serializer=MovieSerializer(data=request.data)
if serializer.is_valid():
serializer.save()
return response.Response(serializer.data)
else:
return response.Response(serializer.errors)


class movie_detail(views.APIView):
def get(self,request,pk): # r = read operation
movie=Movie.objects.get(pk=pk)
serializer=MovieSerializer(movie)
return response.Response(serializer.data)

def post(self,request): # c = create operation
serializer=MovieSerializer(data=request.data)
if serializer.is_valid():
serializer.save()
return response.Response(serializer.data)
else:
return response.Response(serializer.errors)

def put(self,request,pk): # u = update operation
movie=Movie.objects.get(pk=pk)
serializer=MovieSerializer(movie,data=request.data)
if serializer.is_valid():
serializer.save()
return response.Response(serializer.data)
# return redirect('movie_list')
else:
return response.Response(serializer.errors)
# return redirect('movie_detail')

def delete(self,request,pk): # d = delete operation
movie=Movie.objects.get(pk=pk)
movie.delete()
return redirect('movie_list')
```
</div>

<div id="validation">
<a href="#topic">Topic</a>

<h1>Validation</h1>
<h3>It will update within 27 December, 2024</h3>

``
```py

```
</div>

<div id="customSerializerField">
<a href="#topic">Topic</a>

<h1>Custom Serializer Field</h1>

`serializer.py`

```py
class MovieModelSerializer(serializers.ModelSerializer): # Model serializer . Don not need crud method. This is the benefit of model serializers.
length_name = serializers.SerializerMethodField() # get the length
class Meta:
model=Movie # select Model
# fields=['name','description'] # select fields
exclude=['name','description']

def get_length_name(self,obj): # Custom method . this works like getter method
return len(obj.name)   
```
</div>


<div id="updatingModel">
<a href="#topic">Topic</a>
<h1>Updating model</h1>

``
```py

```
</div>