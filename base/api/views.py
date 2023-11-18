from .serializers import *
from ..models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_routes(request):
    routes=[
        'GET /api',
        'GET /api/rooms',
        'GET /api/room/:id',
    ]
    return Response(routes)

@api_view(['GET','POST'])
def get_rooms(request):
    if request.method=='GET':
        room = Room.objects.all()
        serializer = RoomSerializer(room,many=True)
        return Response(serializer.data)
    if request.method=='POST':
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

@api_view(['GET'])
def get_room(request,pk):
    try:
        room = Room.objects.get(id=pk)
    except Room.DoesNotExist:
        raise Room.DoesNotExist
    if request.method=='GET':
        serializer = RoomSerializer(room)
        return Response(serializer.data)
    
