#!/usr/bin/env python3
from pythongame.core.common import NpcType
from pythongame.core.game_data import NON_PLAYER_CHARACTERS, NpcCategory
from pythongame.register_game_data import register_all_game_data


def print_enemies():
    enemy_types_and_data = [(npc_type, NON_PLAYER_CHARACTERS[npc_type]) for npc_type in NpcType if
                            NON_PLAYER_CHARACTERS[npc_type].npc_category == NpcCategory.ENEMY]
    enemy_types_and_data.sort(key=lambda x: x[1].exp_reward)
    print_line("Name", "Health", "Exp", "Speed")
    for enemy_type, enemy_data in enemy_types_and_data:
        print_line(enemy_type.name, enemy_data.max_health, enemy_data.exp_reward, enemy_data.speed)


def print_line(name, health, exp, speed):
    print("{:<25}".format(name) + "{:<8}".format(health) + "{:<8}".format(speed) + "{:<8}".format(exp))


register_all_game_data()
print_enemies()
