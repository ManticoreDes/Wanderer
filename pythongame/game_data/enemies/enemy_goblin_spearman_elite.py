from pythongame.core.common import Millis, NpcType, Sprite, Direction
from pythongame.core.damage_interactions import deal_npc_damage, DamageType
from pythongame.core.enemy_target_selection import EnemyTarget, get_target
from pythongame.core.game_data import register_npc_data, NpcData, SpriteSheet, register_entity_sprite_map
from pythongame.core.game_state import GameState, NonPlayerCharacter, WorldEntity
from pythongame.core.math import is_x_and_y_within_distance
from pythongame.core.npc_behaviors import register_npc_behavior, AbstractNpcMind
from pythongame.core.pathfinding.grid_astar_pathfinder import GlobalPathFinder
from pythongame.core.pathfinding.npc_pathfinding import NpcPathfinder
from pythongame.game_data.loot_tables import LOOT_TABLE_4

DAMAGE_AMOUNT = 6


class NpcMind(AbstractNpcMind):
    def __init__(self, global_path_finder: GlobalPathFinder):
        super().__init__(global_path_finder)
        self._attack_interval = 1000
        self._time_since_attack = self._attack_interval
        self._update_path_interval = 900
        self._time_since_updated_path = self._update_path_interval
        self.pathfinder = NpcPathfinder(global_path_finder)
        self.next_waypoint = None
        self._reevaluate_next_waypoint_direction_interval = 1000
        self._time_since_reevaluated = self._reevaluate_next_waypoint_direction_interval

    def control_npc(self, game_state: GameState, npc: NonPlayerCharacter, player_entity: WorldEntity,
                    is_player_invisible: bool, time_passed: Millis):
        self._time_since_attack += time_passed
        self._time_since_updated_path += time_passed
        self._time_since_reevaluated += time_passed

        enemy_entity = npc.world_entity
        target: EnemyTarget = get_target(enemy_entity, game_state)

        if self._time_since_updated_path > self._update_path_interval:
            self._time_since_updated_path = 0
            if not is_player_invisible:
                self.pathfinder.update_path_towards_target(enemy_entity, game_state, target.entity)

        new_next_waypoint = self.pathfinder.get_next_waypoint_along_path(enemy_entity)

        should_update_waypoint = self.next_waypoint != new_next_waypoint
        if self._time_since_reevaluated > self._reevaluate_next_waypoint_direction_interval:
            self._time_since_reevaluated = 0
            should_update_waypoint = True

        if should_update_waypoint:
            self.next_waypoint = new_next_waypoint
            if self.next_waypoint:
                direction = self.pathfinder.get_dir_towards_considering_collisions(
                    game_state, enemy_entity, self.next_waypoint)
                _move_in_dir(enemy_entity, direction)
            else:
                enemy_entity.set_not_moving()

        if self._time_since_attack > self._attack_interval:
            self._time_since_attack = 0
            if not is_player_invisible:
                enemy_position = enemy_entity.get_center_position()
                target_center_pos = target.entity.get_center_position()
                if is_x_and_y_within_distance(enemy_position, target_center_pos, 80):
                    deal_npc_damage(DAMAGE_AMOUNT, DamageType.PHYSICAL, game_state, enemy_entity, npc, target)


def _move_in_dir(enemy_entity, direction):
    if direction:
        enemy_entity.set_moving_in_dir(direction)
    else:
        enemy_entity.set_not_moving()


def register_goblin_spearman_elite_enemy():
    size = (28, 28)  # Must not align perfectly with grid cell size (pathfinding issues)
    sprite = Sprite.ENEMY_GOBLIN_SPEARMAN_ELITE
    npc_type = NpcType.GOBLIN_SPEARMAN_ELITE
    movement_speed = 0.11
    health = 60
    exp_reward = 32
    register_npc_data(npc_type, NpcData.enemy(sprite, size, health, 0, movement_speed, exp_reward, LOOT_TABLE_4))
    register_npc_behavior(npc_type, NpcMind)
    sprite_sheet = SpriteSheet("resources/graphics/enemy_sprite_sheet_2.png")
    original_sprite_size = (32, 32)
    scaled_sprite_size = (52, 52)
    sprite_sheet_x = 6
    sprite_sheet_y = 0
    indices_by_dir = {
        Direction.DOWN: [(sprite_sheet_x + i, sprite_sheet_y + 0) for i in range(3)],
        Direction.LEFT: [(sprite_sheet_x + i, sprite_sheet_y + 1) for i in range(3)],
        Direction.RIGHT: [(sprite_sheet_x + i, sprite_sheet_y + 2) for i in range(3)],
        Direction.UP: [(sprite_sheet_x + i, sprite_sheet_y + 3) for i in range(3)]
    }
    register_entity_sprite_map(sprite, sprite_sheet, original_sprite_size, scaled_sprite_size, indices_by_dir,
                               (-12, -24))
