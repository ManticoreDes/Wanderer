from pythongame.ability_aoe_attack import register_aoe_attack_ability
from pythongame.ability_channel_attack import register_channel_attack_ability
from pythongame.ability_fireball import register_fireball_ability
from pythongame.ability_frost_nova import register_frost_nova_ability
from pythongame.ability_heal import register_heal_ability
from pythongame.ability_teleport import register_teleport_ability
from pythongame.enemy_berserker import register_berserker_enemy
from pythongame.enemy_dark_reaper import register_dark_reaper_enemy
from pythongame.enemy_dumb import register_dumb_enemy
from pythongame.enemy_mage import register_mage_enemy
from pythongame.enemy_rat_1 import register_rat_1_enemy
from pythongame.enemy_rat_2 import register_rat_2_enemy
from pythongame.enemy_smart import register_smart_enemy
from pythongame.player_data import register_player_data
from pythongame.potion_health import register_health_potion
from pythongame.potion_invis import register_invis_potion
from pythongame.potion_mana import register_mana_potion
from pythongame.potion_speed import register_speed_potion


def register_all_game_data():
    register_fireball_ability()
    register_frost_nova_ability()
    register_heal_ability()
    register_aoe_attack_ability()
    register_channel_attack_ability()
    register_teleport_ability()
    register_health_potion()
    register_mana_potion()
    register_invis_potion()
    register_speed_potion()
    register_dumb_enemy()
    register_smart_enemy()
    register_mage_enemy()
    register_berserker_enemy()
    register_player_data()
    register_rat_1_enemy()
    register_rat_2_enemy()
    register_dark_reaper_enemy()