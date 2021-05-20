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
    "prof_bonus": 0,
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
    global js_race, js_class, js_sub, js_level, renderize, lang, trait

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
            js_race = call(api_url)

            character["speed"] = js_race["speed"]

            character["size"] = js_race["size"]

            character["race"] = js_race["name"]

            for item in js_race["ability_bonuses"]:
                for num in range(len(character["ability"])):
                    if item["ability_score"]["url"] == character["ability"][num]["ability_score"]["url"]:
                        character["ability"][num]["value"] = item["bonus"]

            if js_race["starting_proficiencies"] != []:
                temp = js_race["starting_proficiencies"]
                for item in temp:
                    if item["index"][0:5] == "skill":
                        append = {"name": item["name"][7:], "url": item["url"]}
                        if append not in character["skills"]:
                            character["skills"].append(append)

                    else:
                        append = {"name": item["name"], "url": item["url"]}
                        if append not in character["proficiencies"]:
                            character["proficiencies"].append(append)

            if js_race["languages"] != []:
                temp = js_race["languages"]
                for item in temp:
                    append = {"name": item["name"], "url": item["url"]}
                    if append not in character["languages"]:
                        character["languages"].append(append)

            for item in js_race["traits"]:
                append = {"name": item["name"], "url": item["url"]}
                if append not in character["traits"]:
                    character["traits"].append(append)

            if "starting_proficiency_options" in js_race:
                renderize = "options"
                value = js_race["starting_proficiency_options"]["from"]

            if "language_options" in js_race:
                renderize = "options"
                value = js_race["language_options"]["from"]

            if renderize == "options":
                renderize = ""
                return render(request, "raca.html", {"name": "options", "value": value})

        if req.__contains__("options"):
            if "starting_proficiency_options" in js_race:
                temp = js_race["starting_proficiency_options"]["from"]
                for item in temp:
                    if item["name"] == req["race"]:
                        append = {"name": item["name"], "url": item["url"]}
                        if append not in character["proficiencies"]:
                            character["proficiencies"].append(append)

            if "language_options" in js_race:
                temp = js_race["language_options"]["from"]
                for item in temp:
                    if item["name"] == req["options"]:
                        append = {"name": item["name"], "url": item["url"]}
                        if append not in character["languages"]:
                            character["languages"].append(append)

        if js_race["subraces"] != [] and character["subrace"] == "":
            character["subrace"] = js_race["subraces"][0]["name"]
            api_url = url + js_race["subraces"][0]["url"]
            js_sub = call(api_url)

        if character["subrace"] != "" and js_sub != {}:
            for item in js_sub["ability_bonuses"]:
                for num in range(len(character["ability"])):
                    if item["ability_score"]["url"] == character["ability"][num]["ability_score"]["url"]:
                        character["ability"][num]["value"] = item["bonus"]

            if js_sub["starting_proficiencies"] != []:
                temp = js_sub["starting_proficiencies"]
                for item in temp:
                    if item["index"][0:5] == "skill":
                        append = {"name": item["name"][7:], "url": item["url"]}
                        if append not in character["skills"]:
                            character["skills"].append(append)

                    else:
                        append = {"name": item["name"], "url": item["url"]}
                        if append not in character["proficiencies"]:
                            character["proficiencies"].append(append)

            for item in js_sub["racial_traits"]:
                append = {"name": item["name"], "url": item["url"]}
                if append not in character["traits"]:
                    character["traits"].append(append)

            if "language_options" in js_sub:
                lang = js_sub["language_options"]["from"]
                js_sub.pop("language_options")
                return render(request, "raca.html", {"name": "language", "value": lang})

            if req.__contains__("language"):
                for item in lang:
                    if item["name"] == req["language"]:
                        append = {"name": item["name"], "url": item["url"]}
                        if append not in character["languages"]:
                            character["languages"].append(append)

            if "racial_trait_options" in js_sub:
                trait = js_sub["racial_trait_options"]["from"]
                js_sub.pop("racial_trait_options")
                return render(request, "raca.html", {"name": "trait", "value": trait})

            if req.__contains__("trait"):
                for item in trait:
                    if item["name"] == req["trait"]:
                        append = {"name": item["name"], "url": item["url"]}
                        if append not in character["traits"]:
                            character["traits"].append(append)

            js_sub = {}

        if character["class"] == "":
            character["class"] = "temp"
            return render(request, "raca.html", {"name": "class", "value": classes})

        if req.__contains__("class"):
            renderize = "skills"
            for item in classes:
                if item["name"] == req["class"]:
                    api_url = url + item["url"]

            js_class = call(api_url)

            js_level = call(url + js_class["class_levels"])

            character["class"] = js_class["name"]

            character["prof_bonus"] = 2

            character["level"] = 1

            character["hit_die"] = js_class["hit_die"]

            for item in js_class["proficiencies"]:
                append = {"name": item["name"], "url": item["url"]}
                if append not in character["proficiencies"]:
                    character["proficiencies"].append(append)

            for item in js_class["saving_throws"]:
                for item1 in character["ability"]:
                    if item["url"] == item1["ability_score"]["url"]:
                        append = {"name": item1["ability_score"]["name"], "url": item1["ability_score"]["url"]}
                        character["saving_throws"].append(append)

            if "starting_equipment" != []:
                for item in js_class["starting_equipment"]:
                    append = {"equipment": {"name": item["equipment"]["name"], "url": item["equipment"]["url"]},
                              "quantity": item["quantity"]}
                    character["equipment"].append(append)

        if renderize == "skills":
            renderize = ""
            choose = js_class["proficiency_choices"][0]["choose"]
            value = []

            for item in js_class["proficiency_choices"][0]["from"]:
                if character["skills"] != []:
                    for item1 in character["skills"]:
                        if item["url"] != item1["url"]:
                            append = {"index": item["index"], "name": item["name"][7:], "url": item["url"]}
                            value.append(append)
                else:
                    append = {"index": item["index"], "name": item["name"][7:], "url": item["url"]}
                    value.append(append)

            return render(request, "classe.html", {"name": "skills", "value": value, "choose": choose})

        if len(req) > 2:
            for item in req:
                for item1 in js_class["proficiency_choices"][0]["from"]:
                    if item != "csrfmiddlewaretoken":
                        if item == item1["index"]:
                            append = {"name": item1["name"][7:], "url": item1["url"]}
                            character["skills"].append(append)

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
