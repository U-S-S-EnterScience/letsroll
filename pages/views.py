import json

import requests
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

url = "https://www.dnd5eapi.co"
character = {
    "name": "",
    "race": "",
    "speed": 0,
    "ability": [
        {
            "ability_score": {
                "name": "Strength",
                "url": "/api/ability-scores/str"
            },
            "value": 0,
            "bonus": 0
        },
        {
            "ability_score": {
                "name": "Dexterity",
                "url": "/api/ability-scores/dex"
            },
            "value": 0,
            "bonus": 0
        },
        {
            "ability_score": {
                "name": "Constitution",
                "url": "/api/ability-scores/con"
            },
            "value": 0,
            "bonus": 0
        },
        {
            "ability_score": {
                "index": "int",
                "name": "Intelligence",
                "url": "/api/ability-scores/int"
            },
            "value": 0,
            "bonus": 0
        },
        {
            "ability_score": {
                "name": "Wisdom",
                "url": "/api/ability-scores/wis"
            },
            "value": 0,
            "bonus": 0
        },
        {
            "ability_score": {
                "name": "Charisma",
                "url": "/api/ability-scores/cha"
            },
            "value": 0,
            "bonus": 0
        }
    ],
    "age": 0,
    "alignment": "",
    "size": "",
    "subrace": "",
    "proficiencies": [],
    "languages": [],
    "skills": [],
    "traits": [],
    "class": "",
    "hit_die": [],
    "hit_points": 0,
    "experience_points": 0,
    "level": 0,
    "armor_class": 0,
    "stats": [],
    "initiative": 0,
    "saving_throws": [],
    "equipment": []
}


def call(url):
    r = requests.get(url)
    return json.loads(r.text)


def ficha(request):
    personagem = dict(character_name="Drezon Tizar", race={"index": "elf", "name": "Elf", "url": "/api/races/elf"},
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
                      proficiencies=[
                          {"index": "longswords", "name": "Longswords", "url": "/api/proficiencies/longswords"},
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
                                  "quantity": 2},
                                 {"equipment": {"index": "dungeoneers-pack", "name": "Dungeoneer's Pack",
                                                "url": "/api/equipment/dungeoneers-pack"}, "quantity": 1}])

    return render(request, "ficha.html", personagem)


def cria_Ficha(request):
    global jason, jason_class, sub_jason, renderize, lang, trait

    if request.method == "POST":
        req = request.POST
        races = [{"name": "Dwarf", "url": "/api/races/dwarf"},
                 {"name": "Elf", "url": "/api/races/elf"},
                 {"name": "Halfling", "url": "/api/races/halfling"},
                 {"name": "Human", "url": "/api/races/human"}]

        classes = [{"name": "Cleric", "url": "/api/classes/cleric"},
                   {"name": "Fighter", "url": "/api/classes/fighter"},
                   {"name": "Rogue", "url": "/api/classes/rogue"},
                   {"name": "Wizard", "url": "/api/classes/wizard"}]

        if character["name"] == "":
            character["name"] = req["name"]
            renderize = "race"

        if renderize == "race":
            renderize = ""
            return render(request, "raca.html", {"name": "races", "value": races})

        if req.__contains__("races"):
            for item in races:
                if item["name"] == req["races"]:
                    api_url = url + item["url"]
            jason = call(api_url)

            character['speed'] = jason['speed']

            character['size'] = jason['size']

            character['race'] = jason['name']

            for item in jason['ability_bonuses']:
                for num in range(len(character['ability'])):
                    if item['ability_score']['url'] == character['ability'][num]['ability_score']['url']:
                        character['ability'][num]['value'] = item['bonus']

            temp = jason['starting_proficiencies']
            if temp != []:
                for item in temp:
                    if item['index'][0:5] == 'skill':
                        append = {'name': item['name'][7:], 'url': item['url']}
                        if append not in character['skills']:
                            character['skills'].append(append)

                    else:
                        append = {'name': item['name'], 'url': item['url']}
                        if append not in character['proficiencies']:
                            character['proficiencies'].append(append)

            temp = jason['languages']
            if temp != []:
                for item in temp:
                    append = {'name': item['name'], 'url': item['url']}
                    if append not in character['languages']:
                        character['languages'].append(append)

            for item in jason['traits']:
                append = {'name': item['name'], 'url': item['url']}
                if append not in character['traits']:
                    character['traits'].append(append)

            if "starting_proficiency_options" in jason:
                renderize = "options"
                value = jason["starting_proficiency_options"]["from"]

            if "language_options" in jason:
                renderize = "options"
                value = jason["language_options"]["from"]

            if renderize == "options":
                renderize = ""
                return render(request, "raca.html", {"name": "options", "value": value})

        if req.__contains__("options"):
            if "starting_proficiency_options" in jason:
                temp = jason["starting_proficiency_options"]["from"]
                for item in temp:
                    if item["name"] == req["race"]:
                        append = {"name": item["name"], "url": item["url"]}
                        if append not in character["proficiencies"]:
                            character["proficiencies"].append(append)

            if "language_options" in jason:
                temp = jason["language_options"]["from"]
                for item in temp:
                    if item["name"] == req["options"]:
                        append = {"name": item["name"], "url": item["url"]}
                        if append not in character["languages"]:
                            character["languages"].append(append)

        if jason["subraces"] != [] and character["subrace"] == "":
            character["subrace"] = jason["subraces"][0]["name"]
            api_url = url + jason["subraces"][0]["url"]
            sub_jason = call(api_url)

        if character["subrace"] != "":
            for item in sub_jason['ability_bonuses']:
                for num in range(len(character['ability'])):
                    if item['ability_score']['url'] == character['ability'][num]['ability_score']['url']:
                        character['ability'][num]['value'] = item['bonus']

            temp = sub_jason['starting_proficiencies']
            if temp != []:
                for item in temp:
                    if item['index'][0:5] == 'skill':
                        append = {'name': item['name'][7:], 'url': item['url']}
                        if append not in character['skills']:
                            character['skills'].append(append)

                    else:
                        append = {'name': item['name'], 'url': item['url']}
                        if append not in character['proficiencies']:
                            character['proficiencies'].append(append)

            for item in sub_jason["racial_traits"]:
                append = {'name': item['name'], 'url': item['url']}
                if append not in character['traits']:
                    character['traits'].append(append)

            if "language_options" in sub_jason:
                lang = sub_jason["language_options"]["from"]
                sub_jason.pop("language_options")
                return render(request, "raca.html", {"name": "language", "value": lang})

            if req.__contains__("language"):
                for item in lang:
                    if item["name"] == req["language"]:
                        append = {"name": item["name"], "url": item["url"]}
                        if append not in character["languages"]:
                            character["languages"].append(append)

            if "racial_trait_options" in sub_jason:
                trait = sub_jason["racial_trait_options"]["from"]
                sub_jason.pop("racial_trait_options")
                return render(request, "raca.html", {"name": "trait", "value": trait})

            if req.__contains__("trait"):
                for item in trait:
                    if item["name"] == req["trait"]:
                        append = {"name": item["name"], "url": item["url"]}
                        if append not in character["traits"]:
                            character["traits"].append(append)

        if not req.__contains__("class"):
            return render(request, "raca.html", {"name": "class", "value": classes})

        if req.__contains__("class"):
            if character["class"] == "":
                for item in classes:
                    if item["name"] == req["class"]:
                        api_url = url + item["url"]
            jason_class = call(api_url)

        character["class"] = jason_class["name"]

        character["hit_die"] = jason_class["hit_die"]

        if not req.__contains__("skills"):
            value = jason_class["proficiency_choices"][0]["from"]
            choose = jason_class["proficiency_choices"][0]["choose"]
            return render(request, "classe.html", {"name": "skills", "value": value, "choose": choose})

        print(json.dumps(character, indent=2))
    return render(request, "cria_ficha.html", {"name": "Name"})


def home(request):
    return render(request, "home.html")


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data["email"]
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        "domain": "127.0.0.1:8000",
                        "site_name": "Website",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, "admin@example.com", [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse("Invalid header found.")
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html",
                  context={"password_reset_form": password_reset_form})
