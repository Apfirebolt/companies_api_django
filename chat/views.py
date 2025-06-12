from django.shortcuts import render
import json

def room(request, room_name):
    print(f"Room name: {room_name}")
    return render(request, 'lobby.html', {
        'room_name_json': json.dumps(room_name)
    })