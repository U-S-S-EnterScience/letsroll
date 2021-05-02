from django.views.generic import TemplateView

from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

import requests
import json


def call(url):
    r = requests.get(url)
    return json.loads(r.text)


def ficha(request):
    ficha = dict(character_name="Drezon Tizar", race={"index": "elf", "name": "Elf", "url": "/api/races/elf"},
                 subrace={"index": "high-elf", "name": "High Elf", "url": "/api/subraces/high-elf"}, ability=[
            {"ability_score": {"index": "str", "name": "Strength", "url": "/api/ability-scores/str"}, "value": 13,
             "bonus": 1},
            {"ability_score": {"index": "dex", "name": "Dexterity", "url": "/api/ability-scores/dex"}, "value": 17,
             "bonus": 3},
            {"ability_score": {"index": "con", "name": "Constitution", "url": "/api/ability-scores/con"}, "value": 12,
             "bonus": 1},
            {"ability_score": {"index": "int", "name": "Intelligence", "url": "/api/ability-scores/int"}, "value": 12,
             "bonus": 1},
            {"ability_score": {"index": "wis", "name": "Wisdom", "url": "/api/ability-scores/wis"}, "value": 12,
             "bonus": 1},
            {"ability_score": {"index": "cha", "name": "Charisma", "url": "/api/ability-scores/cha"}, "value": 9,
             "bonus": -1}], speed=30, alignment="Chaotic Neutral", size="Medium",
                 proficiencies=[{"index": "longswords", "name": "Longswords", "url": "/api/proficiencies/longswords"},
                                {"index": "shortswords", "name": "Shortswords",
                                 "url": "/api/proficiencies/shortswords"},
                                {"index": "shortbows", "name": "Shortbows", "url": "/api/proficiencies/shortbows"},
                                {"index": "longbows", "name": "Longbows", "url": "/api/proficiencies/longbows"},
                                {"index": "all-armor", "name": "All armor", "url": "/api/proficiencies/all-armor"},
                                {"index": "shields", "name": "Shields", "url": "/api/proficiencies/shields"},
                                {"index": "simple-weapons", "name": "Simple weapons",
                                 "url": "/api/proficiencies/simple-weapons"},
                                {"index": "martial-weapons", "name": "Martial weapons",
                                 "url": "/api/proficiencies/martial-weapons"}],
                 languages=[{"index": "common", "name": "Common", "url": "/api/languages/common"},
                            {"index": "elvish", "name": "Elvish", "url": "/api/languages/elvish"},
                            {"index": "deep-speech", "name": "Deep Speech", "url": "/api/languages/deep-speech"}],
                 skills=[{"skill": {"index": "skill-perception", "name": "Skill: Perception",
                                    "url": "/api/proficiencies/skill-perception"}, "bonus": 3}, {
                             "skill": {"index": "skill-acrobatics", "name": "Skill: Acrobatics",
                                       "url": "/api/proficiencies/skill-acrobatics"}, "bonus": 5}, {
                             "skill": {"index": "skill-perception", "name": "Skill: Perception",
                                       "url": "/api/proficiencies/skill-perception"}, "bonus": 3}],
                 traits=[{"index": "darkvision", "name": "Darkvision", "url": "/api/traits/darkvision"},
                         {"index": "fey-ancestry", "name": "Fey Ancestry", "url": "/api/traits/fey-ancestry"},
                         {"index": "trance", "name": "Trance", "url": "/api/traits/trance"},
                         {"index": "elf-weapon-training", "name": "Elf Weapon Training",
                          "url": "/api/traits/elf-weapon-training"},
                         {"index": "high-elf-cantrip", "name": "High Elf Cantrip: Ray of Frost",
                          "url": "/api/traits/high-elf-cantrip"}],
                 classes={"index": "fighter", "name": "Fighter", "url": "/api/classes/fighter"}, hit_die=10,
                 hit_points=11, experience_points=0, armor_class=14, stats=
            {"level": 1, "ability_score_bonuses": 0, "prof_bonus": 2,
             "features": [{"index": "second-wind", "name": "Second Wind", "url": "/api/features/second-wind"},
                          {"index": "fighter-fighting-style-two-weapon-fighting",
                           "name": "Fighting Style: Two-Weapon Fighting",
                           "url": "/api/features/fighter-fighting-style-two-weapon-fighting"}],
             "class_specific": {"action_surges": 0, "indomitable_uses": 0, "extra_attacks": 0}}, initiative=3,
                 saving_throws=[
                     {"saving": {"index": "str", "name": "STR", "url": "/api/ability-scores/str"}, "bonus": 3},
                     {"saving": {"index": "con", "name": "CON", "url": "/api/ability-scores/con"}, "bonus": 3}],
                 equipment=[{"equipment": {"index": "leather", "name": "Leather", "url": "/api/equipment/leather"},
                             "quantity": 1},
                            {"equipment": {"index": "longbow", "name": "Longbow", "url": "/api/equipment/longbow"},
                             "quantity": 1},
                            {"equipment": {"index": "arrow", "name": "Arrow", "url": "/api/equipment/arrow"},
                             "quantity": 20}, {"equipment": {"index": "longsword", "name": "Longsword",
                                                             "url": "/api/equipment/longsword"}, "quantity": 1}, {
                                "equipment": {"index": "shortsword", "name": "Shortsword",
                                              "url": "/api/equipment/shortsword"}, "quantity": 1},
                            {"equipment": {"index": "handaxe", "name": "Handaxe", "url": "/api/equipment/handaxe"},
                             "quantity": 2}, {"equipment": {"index": "dungeoneers-pack", "name": "Dungeoneer's Pack",
                                                            "url": "/api/equipment/dungeoneers-pack"}, "quantity": 1}])

    return render(request, 'ficha.html', ficha)


def cria_Ficha(request):
    return render(request, 'cria_ficha.html')


def home(request):
    return render(request, 'home.html')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html",
                  context={"password_reset_form": password_reset_form})