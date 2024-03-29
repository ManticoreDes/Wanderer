from typing import Tuple

from pythongame.core.buff_effects import AbstractBuffEffect, register_buff_effect
from pythongame.core.common import Direction, PortalId, Millis, BuffType, SoundId
from pythongame.core.game_data import Sprite, register_entity_sprite_map, register_portal_data, PortalData
from pythongame.core.game_state import GameState, NonPlayerCharacter
from pythongame.core.sound_player import play_sound
from pythongame.core.view.image_loading import SpriteSheet
from pythongame.core.visual_effects import create_teleport_effects
from pythongame.core.world_entity import WorldEntity

PORTAL_SIZE = (42, 46)
PORTAL_SIZE_SKULL = (10, 10)
BUFF_TYPE = BuffType.TELEPORTING_WITH_PORTAL
PORTAL_DELAY = Millis(600)


class BeingTeleported(AbstractBuffEffect):
    def __init__(self, destination: Tuple[int, int]):
        self.destination = destination
        self.time_since_start = 0
        self.has_teleport_happened = False

    def apply_start_effect(self, game_state: GameState, buffed_entity: WorldEntity, buffed_npc: NonPlayerCharacter):
        game_state.player_state.stun_status.add_one()
        game_state.game_world.player_entity.set_not_moving()
        game_state.game_world.visual_effects += create_teleport_effects(buffed_entity.get_center_position())
        game_state.game_world.player_entity.visible = False

    def apply_middle_effect(self, game_state: GameState, buffed_entity: WorldEntity, buffed_npc: NonPlayerCharacter,
                            time_passed: Millis):
        self.time_since_start += time_passed
        if not self.has_teleport_happened and self.time_since_start > PORTAL_DELAY / 2:
            self.has_teleport_happened = True
            game_state.game_world.player_entity.set_position(self.destination)
            game_state.game_world.visual_effects += create_teleport_effects(buffed_entity.get_center_position())
            play_sound(SoundId.WARP)

    def apply_end_effect(self, game_state: GameState, buffed_entity: WorldEntity, buffed_npc: NonPlayerCharacter):
        game_state.player_state.stun_status.remove_one()
        game_state.game_world.player_entity.visible = True

    def get_buff_type(self):
        return BUFF_TYPE


def register_portals():
    original_sprite_size = (28, 62)
    original_sprite_size_2 = (32, 23)
    original_sprite_size_3 = (33, 69)
    original_sprite_size_4 = (90, 50)
    scaled_sprite_size = (46, 100)
    scaled_sprite_size_2 = (30, 30)
    scaled_sprite_size_3 = (60, 110)
    scaled_sprite_size_4 = (80, 60)
    indices_by_dir = {Direction.DOWN: [(0, 0)]}
    indices_by_dir_2 = {Direction.DOWN: [(1.95, 3.3)]}
    indices_by_dir_3 = {Direction.DOWN: [(2.8, 14)]}
    sprite_position_relative_to_entity = (-4, -54)
    sprite_position_relative_to_entity_2 = (32, 10)
    sprite_position_relative_to_entity_3 = (-6,0)

# TOWN NEIGHBOR JIMMYS JOHN
    register_entity_sprite_map(
        Sprite.PORTAL_TOWN_JIMMYS_JOHN,
        SpriteSheet("resources/graphics/human_tileset2.png"),
        original_sprite_size_3,
        scaled_sprite_size_3,
        indices_by_dir_2,
        sprite_position_relative_to_entity)

    register_entity_sprite_map(
        Sprite.PORTAL_TOWN_JIMMYS_JOHN_REMOTE,
        SpriteSheet("resources/graphics/town_village.png"),
        original_sprite_size_4,
        scaled_sprite_size_4,
        indices_by_dir_3,
        sprite_position_relative_to_entity_3)
    
# BETHILDAS WATER TOWER SKULL PORTAL TO ELVEN CASTLE
    register_entity_sprite_map(
        Sprite.PORTAL_BETHILDAS_ELVEN,
        SpriteSheet("resources/graphics/skeleton_sprite_map.png"),
        original_sprite_size_2,
        scaled_sprite_size_2,
        indices_by_dir,
        sprite_position_relative_to_entity_2)
    register_entity_sprite_map(
        Sprite.PORTAL_DISABLED,
        SpriteSheet("resources/graphics/statue.png"),
        original_sprite_size,
        scaled_sprite_size,
        indices_by_dir,
        sprite_position_relative_to_entity)
    register_entity_sprite_map(
        Sprite.PORTAL_BLUE,
        SpriteSheet("resources/graphics/statue_blue.png"),
        original_sprite_size,
        scaled_sprite_size,
        indices_by_dir,
        sprite_position_relative_to_entity)
    register_entity_sprite_map(
        Sprite.PORTAL_RED,
        SpriteSheet("resources/graphics/statue_red.png"),
        original_sprite_size,
        scaled_sprite_size,
        indices_by_dir,
        sprite_position_relative_to_entity)
    register_entity_sprite_map(
        Sprite.PORTAL_DARK,
        SpriteSheet("resources/graphics/statue_dark.png"),
        original_sprite_size,
        scaled_sprite_size,
        indices_by_dir,
        sprite_position_relative_to_entity)
    register_entity_sprite_map(
        Sprite.PORTAL_GREEN,
        SpriteSheet("resources/graphics/statue_green.png"),
        original_sprite_size,
        scaled_sprite_size,
        indices_by_dir,
        sprite_position_relative_to_entity)
    register_entity_sprite_map(
        Sprite.PORTAL_PURPLE,
        SpriteSheet("resources/graphics/statue_purple.png"),
        original_sprite_size,
        scaled_sprite_size,
        indices_by_dir,
        sprite_position_relative_to_entity)

    warp_home = "Home"

    warp_vanaheim = "Vanaheim"
    
    warp_red_barons_fortress = "Red Baron's Fortress"

    register_portal_data(PortalId.JIMMYS_JOHN_REMOTE,
                         _data(True, PortalId.JIMMYS_JOHN, Sprite.PORTAL_TOWN_JIMMYS_JOHN, "Heim"))
    register_portal_data(PortalId.JIMMYS_JOHN,
                         _data(True, PortalId.JIMMYS_JOHN_REMOTE, Sprite.PORTAL_TOWN_JIMMYS_JOHN_REMOTE, "JIMMYS JOHN"))
    register_portal_data(PortalId.BETHILDAS_ELVEN_BASE,
                         _data(True, PortalId.BETHILDAS_ELVEN_BASE_REMOTE, Sprite.PORTAL_BETHILDAS_ELVEN, "To the Castle of Huldra"))
    register_portal_data(PortalId.BETHILDAS_ELVEN_BASE_REMOTE,
                         _data(True, PortalId.BETHILDAS_ELVEN_BASE, Sprite.PORTAL_BETHILDAS_ELVEN, "To Bethildas house"))
    register_portal_data(PortalId.GOBLIN_HIDEOUT_BASE,
                         _data(False, PortalId.GOBLIN_HIDEOUT_REMOTE, Sprite.PORTAL_DISABLED, "Goblin Hideout"))
    register_portal_data(PortalId.GOBLIN_HIDEOUT_REMOTE,
                         _data(True, PortalId.GOBLIN_HIDEOUT_BASE, Sprite.PORTAL_BLUE, warp_home))
    register_portal_data(PortalId.DWARF_CAMP_BASE,
                         _data(False, PortalId.DWARF_CAMP_REMOTE, Sprite.PORTAL_DISABLED, "Dwarf Camp"))
    register_portal_data(PortalId.DWARF_CAMP_REMOTE,
                         _data(True, PortalId.DWARF_CAMP_BASE, Sprite.PORTAL_RED, warp_home))
    register_portal_data(PortalId.GOBLIN_FORTRESS_BASE,
                         _data(False, PortalId.GOBLIN_FORTRESS_REMOTE, Sprite.PORTAL_DISABLED, "Goblin Fortress"))
    register_portal_data(PortalId.GOBLIN_FORTRESS_REMOTE,
                         _data(True, PortalId.GOBLIN_FORTRESS_BASE, Sprite.PORTAL_DARK, warp_home))
    register_portal_data(PortalId.RED_BARON_FORTRESS_BASE,
                         _data(False, PortalId.RED_BARON_FORTRESS_REMOTE, Sprite.PORTAL_DISABLED,
                               warp_red_barons_fortress))
    register_portal_data(PortalId.RED_BARON_FORTRESS_REMOTE,
                         _data(True, PortalId.RED_BARON_FORTRESS_BASE, Sprite.PORTAL_GREEN, warp_home))
    register_portal_data(PortalId.DEMON_HALL_BASE,
                         _data(False, PortalId.DEMON_HALL_REMOTE, Sprite.PORTAL_DISABLED, "Demon Hall"))
    register_portal_data(PortalId.DEMON_HALL_REMOTE,
                         _data(True, PortalId.DEMON_HALL_BASE, Sprite.PORTAL_PURPLE, warp_red_barons_fortress))

    register_buff_effect(BUFF_TYPE, BeingTeleported)


def _data(starts_enabled: bool, leads_to: PortalId, sprite: Sprite, destination_name: str):
    return PortalData(starts_enabled, leads_to, sprite, PORTAL_SIZE, PORTAL_DELAY, destination_name)
