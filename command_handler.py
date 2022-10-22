#!/usr/bin/python3
import os
import urllib.request
import json

command = os.environ.get('IRCCAT_COMMAND').lower()
args = os.environ.get('IRCCAT_ARGS')

def get_membership():
    with urllib.request.urlopen("https://57north.org.uk/spaceapi") as url:
        spaceapi = json.load(url)
    return spaceapi["sensors"]["total_member_count"]

if command == "gary":
    gary = ["             |\\ ",
            "              \\\\______",
            "              /    \\  \\_ ",
            "             / \u000313 O\u000F   \\   \\ ",
            "            /  __     \\  | ",
            "           (__/  /     \\/ " ,
            "                /        \\__\u000304__\u000F",
            "            __--            \u000304/ \\______\u000F",
            "          --___/           \u000307/\\        \\__\u000F   ",
            "         ( (  __----     \u000303_/  \\__\u000310___    /\u000F___",
            "          || (     \\___ \u000306/ \\_       \\  /\u000F    \\ ",
            "           -\\_\\        \u000310\\_   \\___    \\/\u000F  /__/ ",
            "             \\_\\         \u000308\\___   \\__ /\u000F\\ /  ",
            "                           _/\u000312\\_____/\u000F  \\\\ ",
            "                          /  __/ _/    `",
            "                         |__/  _/ ",
            "                        /__\\__/ ",
            "                           /__| "]
    for line in gary:
        print(line)

if command == "ping":
    print("pong")

if command == "membership":
    print(f"Membership count: "+", ".join([f"{r['location']}: {r['value']}"
                                          for r in get_membership()[:2]]))

if command in ["membership-histogram", "histogram"]:
    for m in get_membership():
        bar = "|"*m["value"]
        print(f"{m['location']:>15}:{bar}")

if command in ["rule", "rules"]:
    with urllib.request.urlopen("https://raw.githubusercontent.com/hackerdeen/rules/master/rules.md") as url:
        rules  = url.readlines()
    rules = [r.decode().strip() for r in rules]
    if args:
        print(rules[int(args)+2])
    else:
        for r in rules:
            print(r)
    
if command == "help":
    print("!gary: summon gary")
    print("!ping: pong")
    print("!membership: how many members have paid?")
    print("!histogram: graph of how many members have paid")
    print("!rules: space rules")
    print("!rule <n>: the nth rule")
          
