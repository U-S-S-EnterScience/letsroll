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
    global js_race, js_class, js_sub, js_level, renderize, lang, trait, ability, abilities_name, ability_select
    global equipment, cantrips, level_1, option, value, value1

    if request.method == "POST":
        req = request.POST
        races = ["Dwarf", "Elf", "Halfling", "Human"]

        classes = ["Cleric", "Fighter", "Rogue", "Wizard"]

        if character["name"] == "":
            character["name"] = req["name"]
            renderize = "race"

        if renderize == "race":
            renderize = "class"
            label = "Choose a race for your character"
            return render(request, "raca.html", {"name": "races", "label": label, "value": races})

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
                renderize = "class"
                return render(request, "raca.html", {"name": "options", "label": label, "value": value})

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
                return render(request, "raca.html", {"name": "language", "label": label, "value": value})

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
                return render(request, "raca.html", {"name": "trait", "label": label, "value": value})

            if req.__contains__("trait"):
                for item in trait:
                    if item["name"] == req["trait"]:
                        append = {"name": item["name"], "url": item["url"]}
                        if append not in character["traits"]:
                            character["traits"].append(append)

        if renderize == "class":
            # renderize = "choose_equipment"
            renderize = "method_generate"
            label = "Choose a class for your character"
            return render(request, "raca.html", {"name": "class", "label": label, "value": classes})

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
            return render(request, "raca.html", {"name": "method_generate", "label": label, "value": value})

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
            return render(request, "raca.html", {"name": "abilities", "label": label, "value": ability})

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
                return render(request, "raca.html", {"name": "abilities", "label": label, "value": ability})

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
            return render(request, "classe.html", {"name": "skills", "value": value, "choose": choose})

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
                    return render(request, "raca.html", {"name": "Fighting Style", "label": label,
                                                         "value": value})

                elif renderize == "add_features":
                    renderize = "choose_equipment"
                    for item in temp["choice"]["from"]:
                        if req["feature_choices"] == item["name"]:
                            character["features"].append({"name": item["name"], "url": item["url"]})

            if character["class"] == "Rogue":
                if renderize == "choose_features":
                    renderize = "add_features"
                    choose = temp["choice"]["choose"]
                    for item in temp["choice"]["from"]:
                        for item1 in character["skills"]:
                            if item["name"][11:] == item1["name"]:
                                value.append({"name": item["name"][11:], "index": item["index"]})
                    return render(request, "classe.html", {"name": "Rogue Expertise", "value": value,
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
                append = {"equipment": {"name": item["equipment"]["name"], "url": item["equipment"]["url"]},
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

                    return render(request, "equipment.html", {"name": "equipment", "label": label,
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

                        return render(request, "equipment.html", {"name": "equipment", "label": label,
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

        # elif character["class"] == "Fighter":
        #     while len(js_class["starting_equipment_options"]) > 0:
        #         temp = js_class["starting_equipment_options"][0]
        #         if renderize == "choose_equipment":
        #             label = "Choose " + str(temp["choose"]) + " equipment from the list bellow: "
        #             renderize = "add_equipment"
        #             value = []
        #             value1 = []
        #             for item in temp["from"]:
        #                 if "equipment" in item:
        #                     append = {"index": temp["from"].index(item),
        #                               "name": item["equipment"]["name"],
        #                               "quantity": item["quantity"],
        #                               "url": item["equipment"]["url"]}
        #                     value.append(append)
        #                     value1.append(append)
        #
        #                 elif "equipment_option" in item:
        #                     renderize = "option_equipment"
        #                     append = {"index": temp["from"].index(item),
        #                               "name": item["equipment_option"]["from"]["equipment_category"]["name"],
        #                               "quantity": item["equipment_option"]["choose"]}
        #                     value.append(append)
        #                     value1.append(append)
        #
        #                 else:
        #                     if len(item) == 3:
        #                         name = item["0"]["equipment"]["name"] + "; " + item["1"]["equipment"]["name"]
        #                         qty = str(item["0"]["quantity"]) + "; " + str(item["1"]["quantity"])
        #                         append = {"index": temp["from"].index(item),
        #                                   "name": name,
        #                                   "quantity": qty}
        #                         value.append(append)
        #
        #                         append = [{"index": temp["from"].index(item),
        #                                    "name": item["0"]["equipment"]["name"],
        #                                    "quantity": item["0"]["quantity"],
        #                                    "url": item["0"]["equipment"]["url"]},
        #                                   {"index": temp["from"].index(item),
        #                                    "name": item["1"]["equipment"]["name"],
        #                                    "quantity": item["1"]["quantity"],
        #                                    "url": item["1"]["equipment"]["url"],
        #                                    "munition": {"name": item["2"]["equipment"]["name"],
        #                                                 "quantity": item["2"]["quantity"],
        #                                                 "url": item["2"]["equipment"]["url"]}}]
        #                         value1.extend(append)
        #
        #                     else:
        #                         renderize = "option_equipment"
        #                         name = item["0"]["equipment"]["name"] + "; " + \
        #                                item["1"]["equipment_option"]["from"]["equipment_category"]["name"]
        #                         qty = str(item["0"]["quantity"]) + "; " + str(item["1"]["equipment_option"]["choose"])
        #                         append = {"index": temp["from"].index(item),
        #                                   "name": name,
        #                                   "quantity": qty}
        #                         value.append(append)
        #
        #                         append = [{"index": temp["from"].index(item),
        #                                    "name": item["0"]["equipment"]["name"],
        #                                    "quantity": item["0"]["quantity"],
        #                                    "url": item["0"]["equipment"]["url"]},
        #                                   {"index": temp["from"].index(item),
        #                                    "name": item["1"]["equipment_option"]["from"]["equipment_category"]["name"],
        #                                    "quantity": item["1"]["equipment_option"]["choose"],
        #                                    "url": item["1"]["equipment_option"]["from"]["equipment_category"]["url"]}]
        #                         value1.extend(append)
        #
        #             return render(request, "equipment.html", {"name": "equipment", "label": label,
        #                                                       "value": value})
        #
        #         elif renderize == "option_equipment":
        #             if req["equipment"] == "/api/equipment-categories/martial-weapons":
        #                 label = "Choose 2 equipment from the list bellow: "
        #                 renderize = "add_equipment"
        #                 value = []
        #                 option = call(url + req["equipment"])
        #                 for item in option["equipment"]:
        #                     append = {"index": item["index"],
        #                               "name": item["name"],
        #                               "quantity": 1,
        #                               "url": item["url"]}
        #                     value.append(append)
        #                     value1.append(append)
        #
        #                 return render(request, "equipment_option.html", {"name": "equipment", "label": label,
        #                                                                  "value": value})
        #
        #             else:
        #                 renderize = "add_equipment"
        #
        #         elif renderize == "add_equipment":
        #             renderize = "choose_equipment"
        #             js_class["starting_equipment_options"].pop(0)
        #             for item in value1:
        #                 if req["equipment"] == item["index"]:
        #                     item.pop("index")
        #                     character["equipment"].append(item)

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

                    return render(request, "equipment.html", {"name": "equipment", "label": label,
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

                    return render(request, "equipment.html", {"name": "equipment", "label": label,
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

                        return render(request, "equipment.html", {"name": "equipment", "label": label,
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
                return render(request, "classe.html", {"name": "cantrips", "value": cantrips, "choose": choose})

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
                return render(request, "classe.html", {"name": "spell level 1", "value": level_1, "choose": choose})

            if renderize == "choosed_level_1":
                for item in req:
                    for item1 in level_1:
                        if item != "csrfmiddlewaretoken":
                            if item == item1["index"]:
                                append = {"name": item1["name"], "url": item1["url"]}
                                character["spells"]["spell_list"]["level_1"].append(append)

        else:
            character.pop("spells")

        return render(request, "ficha.html", character)
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
