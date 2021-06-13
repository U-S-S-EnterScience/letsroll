import json
import requests
import random
import math

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
from pages.models import character_Sheet

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate

@login_required     # pra acessar a view o usuário precisa estar logado
def home(request):
    value = character_Sheet.objects.all().filter(user=request.user)
    return render(request, "home.html", {"value": value})

def call(url):
    r = requests.get(url)
    return json.loads(r.text)


def sheet(request, id):
    char = character_Sheet.objects.get(id=id).sheet
    return render(request, "sheet.html", char)


def sheet_create(request):
    global js_race, js_class, js_sub, js_level, renderize, lang, trait, ability, abilities_name
    global equipment, cantrips, level_1, option, value, value1, finish, character, ability_select
    url = "https://www.dnd5eapi.co"

    if request.method == "GET":
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
            "hit_die": 0,
            "hit_points": 0,
            "experience_points": 0,
            "level": 0,
            "armor_class": 0,
            "features": [],
            "initiative": 0,
            "saving_throws": [],
            "equipment": [],
            "spells": {"spell_list": {"cantrips": [], "level_1": []}}
        }

    elif request.method == "POST":
        req = request.POST
        races = ["Dwarf", "Elf", "Halfling", "Human"]

        classes = ["Cleric", "Fighter", "Rogue", "Wizard"]

        if character["name"] == "":
            character["name"] = req["name"]
            renderize = "race"

        if renderize == "race":
            renderize = "alignment"
            label = "Choose a race for your character"
            return render(request, "radio.html", {"name": "races", "label": label, "value": races})

        if req.__contains__("races"):
            temp = [{"name": "Dwarf", "url": "/api/races/dwarf"},
                    {"name": "Elf", "url": "/api/races/elf"},
                    {"name": "Halfling", "url": "/api/races/halfling"},
                    {"name": "Human", "url": "/api/races/human"}]

            for item in temp:
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
                        character["skills"].append(append)

                    else:
                        append = {"name": item["name"], "url": item["url"]}
                        character["proficiencies"].append(append)

            if js_race["languages"] != []:
                temp = js_race["languages"]
                for item in temp:
                    append = {"name": item["name"], "url": item["url"]}
                    character["languages"].append(append)

            for item in js_race["traits"]:
                append = {"name": item["name"], "url": item["url"]}
                character["traits"].append(append)

            if "starting_proficiency_options" in js_race:
                renderize = "options"
                value = []
                for item in js_race["starting_proficiency_options"]["from"]:
                    value.append(item["name"])
                label = "Choose a proficiency for your character"

            if "language_options" in js_race:
                renderize = "options"
                value = []
                for item in js_race["language_options"]["from"]:
                    value.append(item["name"])
                label = "Choose an optional language for your character"

            if renderize == "options":
                renderize = "alignment"
                return render(request, "radio.html", {"name": "options", "label": label, "value": value})

        if req.__contains__("options"):
            if "starting_proficiency_options" in js_race:
                temp = js_race["starting_proficiency_options"]["from"]
                for item in temp:
                    if item["name"] == req["options"]:
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
                value = []
                for item in js_sub["language_options"]["from"]:
                    value.append(item["name"])
                js_sub.pop("language_options")
                label = "Choose an optional language for your character"
                return render(request, "radio.html", {"name": "language", "label": label, "value": value})

            if req.__contains__("language"):
                for item in lang:
                    if item["name"] == req["language"]:
                        append = {"name": item["name"], "url": item["url"]}
                        if append not in character["languages"]:
                            character["languages"].append(append)

            if "racial_trait_options" in js_sub:
                trait = js_sub["racial_trait_options"]["from"]
                value = []
                for item in js_sub["racial_trait_options"]["from"]:
                    value.append(item["name"])
                js_sub.pop("racial_trait_options")
                label = "Choose an optional trait for your character"
                return render(request, "radio.html", {"name": "trait", "label": label, "value": value})

            if req.__contains__("trait"):
                for item in trait:
                    if item["name"] == req["trait"]:
                        append = {"name": item["name"], "url": item["url"]}
                        if append not in character["traits"]:
                            character["traits"].append(append)

            js_sub = {}

        if renderize == "alignment":
            renderize = "class"
            alignment = ["Chaotic Evil", "Chaotic Neutral", "Chaotic Good",
                         "Neutral Evil", "Neutral", "Neutral Good",
                         "Lawful Evil", "Lawful Neutral", "Lawful Good"]
            label = "Choose an alignment for your character"
            return render(request, "radio.html", {"name": "alignment", "label": label, "value": alignment})

        if req.__contains__("alignment"):
            character["alignment"] = req["alignment"]

        if renderize == "class":
            renderize = "method_generate"
            label = "Choose a class for your character"
            return render(request, "radio.html", {"name": "class", "label": label, "value": classes})

        if req.__contains__("class"):
            temp = [{"name": "Cleric", "url": "/api/classes/cleric"},
                    {"name": "Fighter", "url": "/api/classes/fighter"},
                    {"name": "Rogue", "url": "/api/classes/rogue"},
                    {"name": "Wizard", "url": "/api/classes/wizard"}]

            for item in temp:
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

        if renderize == "method_generate":
            renderize = "abilities_select"
            label = "Choose the method to generate the abilities for your character"
            value = ["Randomize", "Standard"]
            return render(request, "radio.html", {"name": "method_generate", "label": label, "value": value})

        if req.__contains__("method_generate"):
            abilities_name = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
            if req["method_generate"] == "Randomize":
                ability = []
                for num in range(6):
                    dices = []
                    for num1 in range(4):
                        dices.append(random.randint(1, 6))
                    value = sum(dices) - min(dices)
                    ability.append(value)

            else:
                ability = [15, 14, 13, 12, 10, 8]

        if renderize == "abilities_select":
            renderize = "choosed_ability"
            ability_select = abilities_name[0]
            label = "Choose the value for " + ability_select
            return render(request, "radio.html", {"name": "abilities", "label": label, "value": ability})

        if renderize == "choosed_ability":
            for num in range(len(character["ability"])):
                if ability_select == character["ability"][num]["ability_score"]["name"]:
                    character["ability"][num]["value"] += int(req["abilities"])
                    character['ability'][num]['bonus'] = math.floor((character['ability'][num]['value'] - 10) / 2)

            ability.remove(int(req["abilities"]))
            abilities_name.pop(0)
            ability_select = abilities_name[0]
            label = "Choose the value for " + ability_select

            if len(ability) > 1:
                return render(request, "radio.html", {"name": "abilities", "label": label, "value": ability})

            else:
                renderize = "choose_skills"
                character["ability"][5]["value"] += ability[0]
                character['ability'][5]['bonus'] = math.floor((character['ability'][5]['value'] - 10) / 2)

        if character["hit_points"] == 0:
            if character["race"] == "Dwarf":
                character["hit_points"] = character["hit_die"] + character["ability"][2]["bonus"] + 1

            else:
                character["hit_points"] = character["hit_die"] + character["ability"][2]["bonus"]

        if character["initiative"] == 0:
            character["initiative"] = character["ability"][1]["bonus"]

        if renderize == "choose_skills":
            renderize = "add_skills"
            choose = js_class["proficiency_choices"][0]["choose"]
            value = []
            for item in js_class["proficiency_choices"][0]["from"]:
                if character["skills"] != []:
                    for item1 in character["skills"]:
                        if item["url"] != item1["url"]:
                            value.append({"name": item["name"][7:], "index": item["index"]})

                else:
                    value.append({"name": item["name"][7:], "index": item["index"]})
            return render(request, "checkbox.html", {"name": "skills", "value": value, "choose": choose})

        elif renderize == "add_skills":
            if js_level[0]["feature_choices"] != []:
                renderize = "choose_features"

            else:
                renderize = "choose_equipment"

            for item in req:
                for item1 in js_class["proficiency_choices"][0]["from"]:
                    if item != "csrfmiddlewaretoken":
                        if item == item1["index"]:
                            append = {"name": item1["name"][7:], "url": item1["url"]}
                            character["skills"].append(append)

        if js_level[0]["feature_choices"] != []:
            value = []
            temp = call(url + js_level[0]["feature_choices"][0]["url"])
            if character["class"] == "Fighter":
                if renderize == "choose_features":
                    renderize = "add_features"
                    label = "Choose " + str(temp["choice"]["choose"]) + " " + str(temp["name"][7:])
                    for item in temp["choice"]["from"]:
                        value.append(item["name"])
                    return render(request, "radio.html", {"name": "style", "label": label,
                                                          "value": value})

                elif renderize == "add_features":
                    renderize = "choose_equipment"
                    for item in temp["choice"]["from"]:
                        if req["style"] == item["name"]:
                            character["features"].append({"name": item["name"], "url": item["url"]})

            if character["class"] == "Rogue":
                if renderize == "choose_features":
                    renderize = "add_features"
                    choose = temp["choice"]["choose"]
                    for item in temp["choice"]["from"]:
                        for item1 in character["skills"]:
                            if item["name"][11:] == item1["name"]:
                                value.append({"name": item["name"][11:], "index": item["index"]})
                    return render(request, "checkbox.html", {"name": "expertise", "value": value,
                                                             "choose": choose})

                elif renderize == "add_features":
                    renderize = "choose_equipment"
                    for item in req:
                        if item != "csrfmiddlewaretoken":
                            for item1 in temp["choice"]["from"]:
                                if item == item1["index"]:
                                    character["features"].append({"name": item1["name"], "url": item1["url"]})

        if character["class"] == "Cleric":
            for num in range(2):
                for item in js_level[num]["features"]:
                    append = {"name": item["name"], "url": item["url"]}
                    if append not in character["features"]:
                        character["features"].append(append)

        else:
            for item in js_level[0]["features"]:
                append = {"name": item["name"], "url": item["url"]}
                if append not in character["features"]:
                    character["features"].append({"name": item["name"], "url": item["url"]})

        if js_class["starting_equipment"] != [] and character["equipment"] == []:
            for item in js_class["starting_equipment"]:
                append = {"name": item["equipment"]["name"], "url": item["equipment"]["url"],
                          "quantity": item["quantity"]}
                character["equipment"].append(append)

        if character["class"] == "Cleric":
            while len(js_class["starting_equipment_options"]) > 0:
                temp = js_class["starting_equipment_options"][0]
                label = "Choose " + str(temp["choose"]) + " equipment from the list bellow: "
                if renderize == "choose_equipment":
                    renderize = "add_equipment"
                    value = []
                    for item in temp["from"]:
                        if "equipment" in item:
                            append = {"index": item["equipment"]["index"],
                                      "name": item["equipment"]["name"],
                                      "quantity": item["quantity"],
                                      "url": item["equipment"]["url"]}
                            value.append(append)

                        elif "equipment_option" in item:
                            renderize = "option_equipment"
                            append = {"name": item["equipment_option"]["from"]["equipment_category"]["name"],
                                      "quantity": item["equipment_option"]["choose"],
                                      "index": item["equipment_option"]["from"]["equipment_category"]["url"]}
                            value.append(append)

                        elif "equipment_category" in item:
                            option = call(url + item["equipment_category"]["url"])
                            for item1 in option["equipment"]:
                                append = {"index": item1["index"],
                                          "name": item1["name"],
                                          "quantity": 1,
                                          "url": item1["url"]}
                                value.append(append)

                        else:
                            append = {"index": item["0"]["equipment"]["index"],
                                      "name": item["0"]["equipment"]["name"],
                                      "quantity": item["0"]["quantity"],
                                      "url": item["0"]["equipment"]["url"],
                                      "munition": {"name": item["1"]["equipment"]["name"],
                                                   "quantity": item["1"]["quantity"],
                                                   "url": item["1"]["equipment"]["url"]}}
                            value.append(append)

                    return render(request, "radio_2.html", {"name": "equipment", "label": label,
                                                            "value": value})

                elif renderize == "option_equipment":
                    if req["equipment"] == "/api/equipment-categories/simple-weapons":
                        renderize = "add_equipment"
                        value = []
                        option = call(url + req["equipment"])
                        for item in option["equipment"]:
                            append = {"index": item["index"],
                                      "name": item["name"],
                                      "quantity": 1,
                                      "url": item["url"]}
                            value.append(append)

                        return render(request, "radio_2.html", {"name": "equipment", "label": label,
                                                                "value": value})

                    else:
                        renderize = "add_equipment"

                elif renderize == "add_equipment":
                    renderize = "choose_equipment"
                    js_class["starting_equipment_options"].pop(0)
                    for item in value:
                        if req["equipment"] == item["index"]:
                            if req["equipment"] == "crossbow-light":
                                append = {"name": item["name"],
                                          "quantity": item["quantity"],
                                          "url": item["url"],
                                          "munition": item["munition"]}
                                character["equipment"].append(append)

                            else:
                                append = {"name": item["name"],
                                          "quantity": item["quantity"],
                                          "url": item["url"]}
                                character["equipment"].append(append)

        elif character["class"] == "Fighter":
            while len(js_class["starting_equipment_options"]) > 0:
                temp = js_class["starting_equipment_options"][0]
                if renderize == "choose_equipment":
                    label = "Choose " + str(temp["choose"]) + " equipment from the list bellow: "
                    renderize = "add_equipment"
                    value = []
                    value1 = []
                    for item in temp["from"]:
                        if "equipment" in item:
                            append = {"index": item["equipment"]["index"],
                                      "name": item["equipment"]["name"],
                                      "quantity": item["quantity"],
                                      "url": item["equipment"]["url"]}
                            value.append(append)
                            value1.append(append)

                        elif "equipment_option" in item:
                            renderize = "option_equipment"
                            append = {"index": item["equipment_option"]["from"]["equipment_category"]["index"],
                                      "name": item["equipment_option"]["from"]["equipment_category"]["name"],
                                      "quantity": item["equipment_option"]["choose"]}
                            value.append(append)

                        else:
                            name = ""
                            qty = ""
                            for num in item:
                                if "equipment" in item[num]:
                                    if item[num]["quantity"] < 3:
                                        if name == "":
                                            name = item[num]["equipment"]["name"]
                                            qty = str(item[num]["quantity"])

                                        else:
                                            name += "; " + item[num]["equipment"]["name"]
                                            qty += "; " + str(item[num]["quantity"])

                                    append = {"index": item["0"]["equipment"]["index"],
                                              "name": item[num]["equipment"]["name"],
                                              "quantity": item[num]["quantity"],
                                              "url": item[num]["equipment"]["url"]}
                                    value1.append(append)

                                else:
                                    name += "; " + item[num]["equipment_option"]["from"]["equipment_category"]["name"]
                                    qty += "; " + str(item[num]["equipment_option"]["choose"])
                                    renderize = "option_equipment"

                            append = {"index": item["0"]["equipment"]["index"],
                                      "name": name,
                                      "quantity": qty}
                            value.append(append)

                    if renderize == "option_equipment":
                        option = call(url + "/api/equipment-categories/martial-weapons")

                    return render(request, "radio_2.html", {"name": "equipment", "label": label,
                                                            "value": value})

                elif renderize == "option_equipment":
                    label = "Choose 1 equipment from the list bellow: "
                    if req["equipment"] != "martial-weapons":
                        renderize = "add_equipment"

                    if req["equipment"] == "shield":
                        append = {"name": value1[0]["name"],
                                  "quantity": value1[0]["quantity"],
                                  "url": value1[0]["url"]}
                        character["equipment"].append(append)

                    value = []
                    for item in option["equipment"]:
                        append = {"index": item["index"],
                                  "name": item["name"],
                                  "quantity": 1,
                                  "url": item["url"]}
                        value.append(append)
                        value1.append(append)

                    return render(request, "radio_2.html", {"name": "equipment", "label": label,
                                                            "value": value})

                elif renderize == "add_equipment":
                    renderize = "choose_equipment"
                    js_class["starting_equipment_options"].pop(0)
                    for item in value1:
                        if req["equipment"] == item["index"]:
                            item.pop("index")
                            character["equipment"].append(item)

        elif character["class"] == "Rogue":
            while len(js_class["starting_equipment_options"]) > 0:
                temp = js_class["starting_equipment_options"][0]
                label = "Choose " + str(temp["choose"]) + " equipment from the list bellow: "
                if renderize == "choose_equipment":
                    renderize = "add_equipment"
                    value = []
                    for item in temp["from"]:
                        if "equipment" in item:
                            append = {"index": item["equipment"]["index"],
                                      "name": item["equipment"]["name"],
                                      "quantity": item["quantity"],
                                      "url": item["equipment"]["url"]}
                            value.append(append)

                        else:
                            append = {"index": item["0"]["equipment"]["index"],
                                      "name": item["0"]["equipment"]["name"],
                                      "quantity": item["0"]["quantity"],
                                      "url": item["0"]["equipment"]["url"],
                                      "munition": {"name": item["1"]["equipment"]["name"],
                                                   "quantity": item["1"]["quantity"],
                                                   "url": item["1"]["equipment"]["url"]}}
                            value.append(append)

                    return render(request, "radio_2.html", {"name": "equipment", "label": label,
                                                            "value": value})

                elif renderize == "add_equipment":
                    renderize = "choose_equipment"
                    js_class["starting_equipment_options"].pop(0)
                    for item in value:
                        if req["equipment"] == item["index"]:
                            if req["equipment"] == "shortbow":
                                append = {"name": item["name"],
                                          "quantity": item["quantity"],
                                          "url": item["url"],
                                          "munition": item["munition"]}
                                character["equipment"].append(append)

                            else:
                                append = {"name": item["name"],
                                          "quantity": item["quantity"],
                                          "url": item["url"]}
                                character["equipment"].append(append)

        elif character["class"] == "Wizard":
            while len(js_class["starting_equipment_options"]) > 0:
                temp = js_class["starting_equipment_options"][0]
                label = "Choose " + str(temp["choose"]) + " equipment from the list bellow: "
                if renderize == "choose_equipment":
                    renderize = "add_equipment"
                    value = []
                    for item in temp["from"]:
                        if "equipment" in item:
                            append = {"index": item["equipment"]["index"],
                                      "name": item["equipment"]["name"],
                                      "quantity": item["quantity"],
                                      "url": item["equipment"]["url"]}
                            value.append(append)

                        else:
                            renderize = "option_equipment"
                            append = {"name": item["equipment_option"]["from"]["equipment_category"]["name"],
                                      "quantity": item["equipment_option"]["choose"],
                                      "index": item["equipment_option"]["from"]["equipment_category"]["url"]}
                            value.append(append)

                    return render(request, "radio_2.html", {"name": "equipment", "label": label,
                                                            "value": value})

                elif renderize == "option_equipment":
                    if req["equipment"] == "/api/equipment-categories/arcane-foci":
                        renderize = "add_equipment"
                        value = []
                        option = call(url + req["equipment"])
                        for item in option["equipment"]:
                            append = {"index": item["index"],
                                      "name": item["name"],
                                      "quantity": 1,
                                      "url": item["url"]}
                            value.append(append)

                        return render(request, "radio_2.html", {"name": "equipment", "label": label,
                                                                "value": value})

                    else:
                        renderize = "add_equipment"

                elif renderize == "add_equipment":
                    renderize = "choose_equipment"
                    js_class["starting_equipment_options"].pop(0)
                    for item in value:
                        if req["equipment"] == item["index"]:
                            append = {"name": item["name"],
                                      "quantity": item["quantity"],
                                      "url": item["url"]}
                            character["equipment"].append(append)

        if character["armor_class"] == 0:
            js = call(url + '/api/equipment-categories/armor')
            List = js['equipment']
            shield_armor = 0
            armor = 0

            for item in character['equipment']:
                for item1 in List:
                    if item['name'] == item1['name']:
                        if item1['index'] == 'shield':
                            shield = call(url + item1['url'])
                            shield_armor = shield['armor_class']['base']
                        else:
                            armor = call(url + item1['url'])

            if armor == 0:
                character['armor_class'] = 10 + character['ability'][1]['bonus']

            elif armor['armor_class']['dex_bonus'] == False:
                character['armor_class'] = armor['armor_class']['base'] + shield_armor

            elif armor['armor_class']['max_bonus'] != None:
                if character['ability'][1]['bonus'] > armor['armor_class']['max_bonus']:
                    character['armor_class'] = (armor['armor_class']['base'] +
                                                shield_armor +
                                                armor['armor_class']['max_bonus'])

                else:
                    character['armor_class'] = (armor['armor_class']['base'] +
                                                shield_armor +
                                                character['ability'][1]['bonus'])

            else:
                character['armor_class'] = (armor['armor_class']['base'] +
                                            shield_armor +
                                            character['ability'][1]['bonus'])

            if character["class"] == "Fighter":
                for item in character['features']:
                    if item['name'] == "Fighting Style: Defense":
                        character['armor_class'] += 1

        if "spellcasting" in js_level[0]:
            if len(character["spells"]) == 1:
                renderize = "spell_list"

            character["spells"]["spellcasting"] = js_level[0]["spellcasting"]

            if character["class"] == "Wizard":
                character["spells"]["spellcasting"]["spells_known"] = 6

            for item in character["ability"]:
                if item["ability_score"]["url"] == js_class["spellcasting"]["spellcasting_ability"]["url"]:
                    character["spells"]["ability"] = item["ability_score"]["name"]
                    character["spells"]["spell_save_dc"] = 8 + item["bonus"] + character["prof_bonus"]
                    character["spells"]["spell_attack_modifier"] = item["bonus"] + character["prof_bonus"]
                    character["spells"]["preparing_spells"] = item["bonus"] + character["level"]

            if renderize == "spell_list":
                renderize = "cantrips"
                spell_list = call(url + js_class["spells"])
                cantrips = []
                level_1 = []
                for item in spell_list["results"]:
                    spell = call(url + item["url"])
                    if spell["level"] == 0:
                        cantrips.append(item)

                    elif spell["level"] == 1:
                        level_1.append(item)

                    else:
                        break

            if renderize == "cantrips":
                renderize = "choosed_cantrips"
                choose = character["spells"]["spellcasting"]["cantrips_known"]
                return render(request, "checkbox.html", {"name": "cantrips", "value": cantrips, "choose": choose})

            if renderize == "choosed_cantrips":
                renderize = "level_1"
                for item in req:
                    for item1 in cantrips:
                        if item != "csrfmiddlewaretoken":
                            if item == item1["index"]:
                                append = {"name": item1["name"], "url": item1["url"]}
                                character["spells"]["spell_list"]["cantrips"].append(append)

            if renderize == "level_1":
                renderize = "choosed_level_1"
                choose = character["spells"]["spellcasting"]["spells_known"]
                return render(request, "checkbox.html",
                              {"name": "spell level 1", "value": level_1, "choose": choose})

            if renderize == "choosed_level_1":
                for item in req:
                    for item1 in level_1:
                        if item != "csrfmiddlewaretoken":
                            if item == item1["index"]:
                                append = {"name": item1["name"], "url": item1["url"]}
                                character["spells"]["spell_list"]["level_1"].append(append)

            finish = True

        else:
            finish = True
            character.pop("spells")

        if finish:
            sheet = character_Sheet(user=request.user,
                                    name=character["name"],
                                    race=character["race"],
                                    clas=character["class"],
                                    level=character["level"],
                                    sheet=character)
            sheet.save()
            return render(request, "sheet.html", character)

    return render(request, "text_name.html", {"name": "Name"})





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
