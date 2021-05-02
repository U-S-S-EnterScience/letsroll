from django.shortcuts import render
import requests
import json


def index(request):
    url = 'https://www.dnd5eapi.co/api/classes/barbarian/'
    r = requests.get(url)
    js = json.loads(r.text)
    classe = js["index"]
    return render(request, 'cria_ficha.html', classe)
