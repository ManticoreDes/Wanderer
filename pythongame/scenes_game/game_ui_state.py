from enum import Enum
from typing import Optional

from pythongame.core.common import AbilityType, Millis

MESSAGE_DURATION = 3500
HIGHLIGHT_consumable_ACTION_DURATION = 120
HIGHLIGHT_ABILITY_ACTION_DURATION = 120


class ToggleButtonId(Enum):
    STATS = 1
    TALENTS = 2
    HELP = 3


# This class maintains the UI state that's related to the game clock. For instance, when the player clicks a button in
# the UI, it should be highlighted but only for a while. Keeping that logic here lets main.py be free from UI details
# and it lets view.py be stateless.
class GameUiState:
    def __init__(self):
        self._ticks_since_message_updated = 0
        self._ticks_since_last_consumable_action = 0
        self._ticks_since_last_ability_action = 0

        self.message = ""
        self._enqueued_messages = []
        self.highlighted_consumable_action: Optional[int] = None
        self.highlighted_ability_action: Optional[AbilityType] = None

    def notify_ability_was_clicked(self, ability_type: AbilityType):
        self.highlighted_ability_action = ability_type
        self._ticks_since_last_ability_action = 0

    def notify_consumable_was_clicked(self, slot_number: int):
        self.highlighted_consumable_action = slot_number
        self._ticks_since_last_consumable_action = 0

    def set_message(self, message: str):
        self.message = message
        self._ticks_since_message_updated = 0

    def enqueue_message(self, message: str):
        self._enqueued_messages.append(message)

    def clear_messages(self):
        self.message = None
        self._enqueued_messages.clear()

    def notify_time_passed(self, time_passed: Millis):
        self._ticks_since_message_updated += time_passed
        if self.message != "" and self._ticks_since_message_updated > MESSAGE_DURATION:
            if self._enqueued_messages:
                new_message = self._enqueued_messages.pop(0)
                self.set_message(new_message)
            else:
                self.message = ""

        self._ticks_since_last_consumable_action += time_passed
        if self._ticks_since_last_consumable_action > HIGHLIGHT_consumable_ACTION_DURATION:
            self.highlighted_consumable_action = None

        self._ticks_since_last_ability_action += time_passed
        if self._ticks_since_last_ability_action > HIGHLIGHT_ABILITY_ACTION_DURATION:
            self.highlighted_ability_action = None
