from enum import Enum


class VolumeLevel(Enum):
    mute = 0
    low = 10
    medium = 60
    high = 100


current_volume_level = VolumeLevel.medium


def set_volume_level(level: VolumeLevel):
    global current_volume_level
    current_volume_level = level


def get_volume_level() -> VolumeLevel:
    global current_volume_level
    return current_volume_level


def get_volume_level_percent() -> float:
    global current_volume_level
    return float(current_volume_level.value) / 100.0
