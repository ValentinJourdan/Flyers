from django.shortcuts import render
import json
from django import template
from django.utils.timesince import timesince

from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from .models import Room
from Flow.models import Utilisateur
from django.contrib.auth.models import User

from Flow.models import Event
register = template.Library()

# Create your views here.


@register.filter(user_name='initials')
def initials(value):
    initials = ''

    for name in value.split(' '):
        if name and len(initials) < 3:
            initials += name[0].upper()

    return initials


@login_required
@require_POST
def create_room(request, eId):
    event = Event.objects.get(id=eId)
    name = f"groupe de : {event.title}"
    # url = request.POST.get('url', '') IMPORTANT ????
    Room.objects.create(name=name, event=event, eId=eId)
    return JsonResponse({'message': f"un groupe a été créé pour l'évènement {event.title}"})


# UUID = Event_id !!!!
# On créé une Room dès que l'on poste un évènement, l'id de l'évènement est alors intrinsèquement lié à la room
# On identifie alors la room avec event_id
# Chaque fois que qqn rejoint un évènement, on lui donne la permission de voir, dans son onglet "groupPage", et d'accéder, au chat du groupe correspondant.

# On récupère les rooms pour lesquelles l'utilisateur est membre de l'event associé à la room
# ATTENTION CE FILTRE NE SUFFIT PAS : il faut aussi créer une permission pour chaque groupe que l'utilisateur obtient : soit s'il créé l'évènement assocéi, soit s'il rejoint un évènement


@login_required
def GroupPage(request):
    eIds = Event.objects.filter(
        members=request.user).values_list('id', flat=True)
    rooms = Room.objects.filter(eId__in=eIds)
    users = User.objects.all()
    return render(request, 'Chat/GroupPage.html', {
        'rooms': rooms,
        'users': users
    })
# ATTENTION CE FILTRE NE SUFFIT PAS : il faut aussi créer une permission pour chaque groupe que l'utilisateur obtient : soit s'il créé l'évènement assocéi, soit s'il rejoint un évènement


@login_required
def Room_chat(request, eId):
    def Time(a):
        return timesince(a)
    event = Event.objects.get(id=eId)
    room = Room.objects.get(eId=eId)
    user = request.user
    return render(request, 'Chat/Room_chat.html', {
        'room': room,
        'user': user,
        'event': event,
        'eId': eId,
        'Time': Time,
    })


def member_profile(request, id):
    other = Utilisateur.objects.get(id=id)
    s = request.user
    self = Utilisateur.objects.get(id=s.id)
    print(self.email)
    print(other.email)
    return render(request, 'Chat/member_profile.html', {'other': other, 'self': self})


@login_required
def Roadmap(request, eId):
    event = Event.objects.get(id=eId)
    return render(request, 'Chat/Roadmap.html', {'event': event, 'eId': eId})
