from enum import Enum
import time


class Commands(Enum):
    LIST = "list"
    CHECK = "check"
    KILL = "kill"
    PROCEED = "proceed"
    VOTE = "vote"


class Role(Enum):
    SIMPLE = "simple"
    POLICE = "police"
    MAFIA = "mafia"


class Time(Enum):
    DAY = "day"
    NIGHT = "night"


NEEDED_PLAYERS_FOR_GAME = 5
NOTIFICATIONS_KEY = "notifications"
CONNECTED_OK = "OK"
EMPTY = ""

NEW_PLAYER_CONNECTED = "New player connected: {name}!"
PLAYER_IS_GREATING_YOU = "Player {name} is greating you!"
ALL_PLAYERS_CONNECTED = "All players connected!"
PLAYER_DISCONNECTED = "Player {name} disconnected"

BOT_NAMES = [
    "Jayson Christensen",
    "Darryl West",
    "Alexander Hardy",
    "Aryana Eaton",
    "Valery Mack",
    "Alivia Hughes",
    "Sadie Horne",
    "Finn Glass",
    "Sabrina Chang",
    "Brodie Everett",
    "Aryanna Mosley",
    "Camryn Leblanc",
    "Carly Daniels",
    "Zara Petersen",
    "Violet Moran",
    "Raymond Frazier",
    "Sierra Sims",
    "Angelique Brown",
    "Charlie Willis",
    "Lyric Dickson",
    "Jackson White",
    "Mason Atkins",
    "Myah Johnston",
    "Juliana Myers",
    "Aron Oconnor",
    "Victor White",
    "Melanie Reeves",
    "Desirae Jones",
    "Elaina Brennan",
    "Heather Keith",
    "Ingrid Collier",
    "Evangeline Stone",
    "Cailyn Rollins",
    "Regina David",
    "Tia May",
    "Reginald Abbott",
]

STREAM_RESPONSE_TIME_THREASHOLD = 1
BOT_WAIT_MAX_MILLIS = 2000
MAGIC_SEED = int(time.time() * 1000)

ROLES = [
    Role.MAFIA.value,
    Role.POLICE.value,
    Role.SIMPLE.value,
    Role.SIMPLE.value,
    Role.SIMPLE.value,
]
