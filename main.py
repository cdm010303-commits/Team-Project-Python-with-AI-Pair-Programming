import json
import math
import os
import random
import sys
from array import array

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

try:
    import pygame
except ImportError:
    print("pygame이 설치되어 있지 않습니다.")
    print("설치: pip install pygame")
    print("실행: python main.py")
    sys.exit(1)

WIDTH = 1280
HEIGHT = 720
FPS = 60
COMBAT_TOP = 300
COMBAT_BOTTOM = 660
FLOOR_TOP_Y = 890
FLOOR_BOTTOM_Y = 1150
MAX_EFFECTS = 90
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
SAVE_FILE = os.path.join(BASE_DIR, "highest_score.json")
SAVE_DATA_FILE = os.path.join(BASE_DIR, "save_data.json")
DEBUG_GACHA = False
DEBUG_WALKABLE = False
DEBUG_BOSS15_AREA = False
DEBUG_BOSS15 = False
DEBUG_BOSS15_FLOOR = False
BOSS15_WORLD_WIDTH = 2200
BOSS15_WORLD_HEIGHT = 1250
BOSS15_ASSET_CACHE = {}
PLAYER_SPRITE_CACHE = {}
BOSS_SKIN_CACHE = {}
PET_IMAGE_CACHE = {}
BOSS_OPTIONAL_IMAGE_WARNED = set()
BOSS_SKILL_IMAGE_CACHE = {}
BOSS_SKILL_SHEETS = {
    "inferno": ("boss_skill_11.png", ("inferno_breath", "inferno_claw", "inferno_roar", "inferno_meteor")),
    "forest": ("boss_skill_6.png", ("forest_thorns", "forest_poison", "forest_guard", "forest_fury")),
    "final": ("boss_skill_1.png", ("final_beam", "final_ring", "final_collapse", "final_burst")),
}
BOSS_SKILL_CROP_RATIOS = {
    "inferno": {
        "inferno_breath": (0.02, 0.03, 0.55, 0.34),
        "inferno_claw": (0.50, 0.03, 0.96, 0.36),
        "inferno_roar": (0.05, 0.42, 0.50, 0.88),
        "inferno_meteor": (0.50, 0.42, 0.98, 0.90),
    },
    "forest": {
        "forest_thorns": (0.00, 0.02, 0.60, 0.34),
        "forest_poison": (0.52, 0.00, 0.98, 0.34),
        "forest_guard": (0.02, 0.46, 0.50, 0.92),
        "forest_fury": (0.50, 0.43, 0.98, 0.94),
    },
}
BOSS_SKILL_KIND_TO_SHEET = {
    kind: sheet_key
    for sheet_key, (_, kinds) in BOSS_SKILL_SHEETS.items()
    for kind in kinds
}
MONSTER_20_16_SHEET = "20~16o.png"
MONSTER_20_16_FRAME_SIZE = (112, 112)
MONSTER_20_16_TYPES = ("ice_slime", "ice_wolf", "ice_bat")
MONSTER_20_16_FRAMES = None
MONSTER_20_16_LOAD_ATTEMPTED = False
MONSTER_15_11_SHEET = "15~11o.png"
MONSTER_15_11_TYPES = ("magma_slime", "frost_wolf", "magma_golem")
MONSTER_15_11_FRAMES = None
MONSTER_15_11_LOAD_ATTEMPTED = False
MONSTER_10_6_SHEET = "10~6o.png"
MONSTER_10_6_TYPES = ("forest_wisp", "forest_wolf", "forest_mage")
MONSTER_10_6_FRAMES = None
MONSTER_10_6_LOAD_ATTEMPTED = False
MONSTER_5_1_SHEET = "5~1o.png"
MONSTER_5_1_TYPES = ("storm_orb", "storm_wolf", "storm_mage")
MONSTER_5_1_FRAMES = None
MONSTER_5_1_LOAD_ATTEMPTED = False
DEBUG_PLAYER_SPRITE = False
DEBUG_PLAYER_ANIM = False
DEBUG_PLAYER_SPRITE_CROP = False
PLAYER_SPRITE_W = 128
PLAYER_SPRITE_H = 128
JEFFREY_FRAME_W = 128
JEFFREY_FRAME_H = 128
JEFFREY_CONTENT_H = 112
KNIGHT_SHEET_CROP_RATIO = (0.10, 0.078, 0.010, 0.012)
KNIGHT_REFERENCE_RECTS_RATIO = [ [(442 / 2816, 134 / 1536, 706 / 2816, 426 / 1536), (801 / 2816, 161 / 1536, 1022 / 2816, 431 / 1536), (1927 / 2816, 160 / 1536, 2198 / 2816, 428 / 1536), (2397 / 2816, 155 / 1536, 2710 / 2816, 421 / 1536)], [(462 / 2816, 477 / 1536, 680 / 2816, 772 / 1536), (800 / 2816, 482 / 1536, 1017 / 2816, 761 / 1536), (1902 / 2816, 485 / 1536, 2167 / 2816, 770 / 1536), (2396 / 2816, 483 / 1536, 2633 / 2816, 770 / 1536)], [(479 / 2816, 824 / 1536, 642 / 2816, 1125 / 1536), (821 / 2816, 825 / 1536, 984 / 2816, 1124 / 1536), (1939 / 2816, 828 / 1536, 2256 / 2816, 1123 / 1536), (2330 / 2816, 828 / 1536, 2651 / 2816, 1122 / 1536)], [(482 / 2816, 1181 / 1536, 646 / 2816, 1482 / 1536), (826 / 2816, 1179 / 1536, 989 / 2816, 1483 / 1536), (1854 / 2816, 1186 / 1536, 2143 / 2816, 1480 / 1536), (2334 / 2816, 1184 / 1536, 2654 / 2816, 1479 / 1536)], ]
KAKAO_KNIGHT_REFERENCE_SIZE = (1678, 937)
KAKAO_KNIGHT_REFERENCE_RECTS = [ [(238, 86, 420, 270), (494, 86, 648, 270), (1138, 74, 1354, 286), (1414, 80, 1596, 286)], [(205, 300, 394, 474), (482, 300, 642, 474), (1130, 296, 1340, 492), (1414, 300, 1588, 492)], [(202, 496, 386, 666), (450, 496, 628, 666), (1100, 488, 1358, 666), (1370, 488, 1598, 666)], [(248, 690, 398, 868), (512, 690, 638, 868), (1184, 682, 1380, 868), (1432, 682, 1620, 868)], ]
# 15F boss tuning: larger anchor y moves the boss down; smaller crop ratio hides more lower body.
BOSS15_FRAME_VISIBLE_RATIO = 0.78
BOSS15_BODY_CROP_BOTTOM_RATIO = 0.72
BOSS15_MAX_INNER_Y_RATIO = 0.57
BOSS15_FRAME_COUNTS = { "idle": 8, "skill1": 8, "skill2": 8, "groggy": 6, "defeat": 8, "telegraph": 6, }
BOSS15_ANIM_FPS = { "idle": 7, "skill1": 11, "skill2": 11, "groggy": 7, "defeat": 9, "telegraph": 10, }
BOSS15_CORE_HITBOX_RATIO = (0.43, 0.43, 0.14, 0.14)
STAGE_20_16_WALKABLE_POLYGON_RATIO = [ (0.09, 0.84), (0.91, 0.84), (0.83, 0.47), (0.64, 0.34), (0.36, 0.34), (0.17, 0.47), ]
STAGE_20_16_PLAYER_START_RATIO = (0.50, 0.76)
STAGE_20_16_EXIT_RATIO = (0.50, 0.42)
BOSS15_BACKGROUND = "boss_stage_15.png"
BOSS15_IMAGE = "boss15.png"
BOSS15_WALKABLE_POLYGON_RATIO = [ (0.08, 0.82), (0.92, 0.82), (0.87, 0.62), (0.72, 0.57), (0.28, 0.57), (0.13, 0.62), ]
BOSS15_VISUAL_POS_RATIO = (0.50, 0.34)
# Larger visual height makes the boss larger behind the floor.
BOSS15_VISUAL_HEIGHT_RATIO = 1.15
BOSS15_VISUAL_ANCHOR_RATIO = (0.50, 0.66)
BOSS15_ANCHOR_POS_RATIO = BOSS15_VISUAL_ANCHOR_RATIO
BOSS15_CORE_POS_RATIO = (0.50, 0.50)
BOSS15_EXIT_POS_RATIO = (0.50, 0.64)
BOSS15_MELEE_ZONE_RATIO = (0.30, 0.56, 0.40, 0.08)
BOSS15_TELEGRAPH_TIME = 1.0
BOSS15_ATTACK_ACTIVE_TIME = 0.30
BOSS15_ATTACK_INTERVAL = 3.0
BOSS15_WINDUP_TIME = 0.6
BOSS15_RECOVER_TIME = 0.7
BOSS15_HEAD_FOCUS_RATIO = (0.50, 0.30)
ICE_DRAGON_STAGE_BACKGROUND = "ice_dragon_stage.png"
ICE_DRAGON_SHEET = "ice_dragon_sheet.png"
ICE_DRAGON_FLOOR = 16
ICE_DRAGON_WORLD_WIDTH = 2200
ICE_DRAGON_WORLD_HEIGHT = 1250
ICE_DRAGON_ARENA_CENTER_RATIO = (0.50, 0.47)
ICE_DRAGON_ARENA_RADIUS_RATIO = 0.50
ICE_DRAGON_ARENA_RX_RATIO = 0.48
ICE_DRAGON_ARENA_RY_RATIO = 0.40
ICE_DRAGON_ARENA_MARGIN = 18
ICE_DRAGON_VISUAL_ANCHOR_RATIO = (0.50, 0.49)
ICE_DRAGON_VISUAL_HEIGHT_RATIO = 0.54
ICE_DRAGON_CORE_POS_RATIO = (0.50, 0.44)
ICE_DRAGON_MELEE_ZONE_RATIO = (0.43, 0.46, 0.14, 0.085)
ICE_DRAGON_EXIT_POS_RATIO = (0.50, 0.62)
ICE_DRAGON_HEAD_FOCUS_RATIO = (0.50, 0.26)
ICE_DRAGON_TELEGRAPH_TIME = 1.0
ICE_DRAGON_BREATH_ACTIVE_TIME = 0.42
ICE_DRAGON_BLIZZARD_TELEGRAPH_TIME = 0.9
ICE_DRAGON_TORNADO_CAST_ANIM_TIME = 1.0
ICE_DRAGON_TORNADO_RECOVER_TIME = 0.4
ICE_DRAGON_BREATH_RECOVER_TIME = 0.45
ICE_DRAGON_BLIZZARD_ACTIVE_TIME = 4.5
ICE_DRAGON_MAX_ACTIVE_TORNADOES = 4
ICE_DRAGON_MAX_HP = 2500
ICE_DRAGON_DEATH_ANIM_TIME = 2.0
ICE_DRAGON_BODY_FRAME_SIZE = (430, 390)
ICE_DRAGON_BREATH_DIRECTIONS = ("left", "left_diagonal", "center", "right_diagonal", "right")
ICE_DRAGON_TORNADO_VISUAL_SCALE = 1.35
ICE_DRAGON_PHASE2_BREATH_COMBOS = ( (2, 0), (2, 4), (3, 0), (1, 4), (2, 1), (2, 3), (0, 4), )

# 11F LIGER-X11 Inferno boss assets/tuning
INFERNO_LIGER_FLOOR = 11
INFERNO_LIGER_STAGE_BACKGROUND = "inferno_stage_11.png"
INFERNO_LIGER_WORLD_WIDTH = 2200
INFERNO_LIGER_WORLD_HEIGHT = 1250
INFERNO_LIGER_WALKABLE_POLYGON_RATIO = [ (0.08, 0.84), (0.92, 0.84), (0.82, 0.49), (0.62, 0.37), (0.38, 0.37), (0.18, 0.49), ]
INFERNO_LIGER_MAX_HP = 2700
INFERNO_LIGER_DEATH_ANIM_TIME = 1.35
DEBUG_ICE_ARENA_BOUNDS = False
DEBUG_BREATH_SECTORS = False
BOSS_CONFIGS = {
    INFERNO_LIGER_FLOOR: {
        "boss_id": "liger_x11_inferno",
        "name": "LIGER-X11 인페르노",
        "fallback_type": "inferno_liger",
        "hitbox": (190, 115),
        "skins": {
            "idle": "inferno_idle.png",
            "attack": "inferno_attack.png",
            "dash": "inferno_dash.png",
            "roar": "inferno_roar.png",
            "phase2": "inferno_phase2.png",
            "defeat": "inferno_defeat.png",
        },
    },
    ICE_DRAGON_FLOOR: {
        "boss_id": "ice_dragon_16",
        "name": "Ice Dragon",
        "fallback_type": "ice_dragon",
        "hitbox": (116, 116),
        "skins": {
            "idle": "boss15_idle.png",
            "attack": "boss15_skill1.png",
            "phase2": "boss15_skill2.png",
            "defeat": "boss15_defeat.png",
        },
    },
    10: {
        "boss_id": "boss10",
        "name": "Machine Core",
        "fallback_type": "core_machine",
        "hitbox": (108, 108),
        "skins": {
            "idle": "boss10_idle.png",
            "attack": "boss10_attack.png",
            "phase2": "boss10_phase2.png",
            "defeat": "boss10_defeat.png",
        },
    },
    5: {
        "boss_id": "boss5",
        "name": "Dark Beast",
        "fallback_type": "dark_beast",
        "hitbox": (118, 98),
        "skins": {
            "idle": "boss5_idle.png",
            "attack": "boss5_attack.png",
            "phase2": "boss5_phase2.png",
            "defeat": "boss5_defeat.png",
        },
    },
    1: {
        "boss_id": "boss1",
        "name": "Final Core",
        "fallback_type": "final_core",
        "hitbox": (132, 132),
        "skins": {
            "idle": "boss1_idle.png",
            "attack": "boss1_attack.png",
            "phase2": "boss1_phase2.png",
            "defeat": "boss1_defeat.png",
        },
    },
}
LOBBY_WALKABLE_POLYGON_RATIO = [ (0.06, 0.91), (0.94, 0.91), (0.80, 0.32), (0.20, 0.32), ]
LOBBY_INTERACTABLE_RATIOS = { "gacha_machine": (0.32, 0.45), "stairs_to_20f": (0.50, 0.40), "character_terminal": (0.73, 0.42), }
LOBBY_AUTO_ENTRY_RECT_RATIO = (0.40, 0.31, 0.20, 0.16)

BACKGROUND_IMAGES = { "inferno_stage_11": INFERNO_LIGER_STAGE_BACKGROUND, "ice_dragon_stage": ICE_DRAGON_STAGE_BACKGROUND, "stage_20_16": "stage_20_16.png", "20_16": "bg_20_16.png", "15_11": "bg_15_11.png", "10_6": "bg_10_6.png", "5_1": "bg_5_1.png", }

BACKGROUND_IMAGE_ALIASES = { "inferno_stage_11": [ "inferno_stage_11.png", "assets/inferno_stage_11.png", "liger_stage_11.png", ], "ice_dragon_stage": [ "ice_dragon_stage.png", "ice_dragon_stage.png.png", "boss_stage_15_ice.png", "boss_stage_15_ice.png.png", ], "boss_stage_15": [ "boss_stage_15.png", "boss_stage_15.png.png", "assetsboss_stage_15.png.png", ], "stage_20_16": [ "assets/stage_20_16.png", "stage_20_16.png", "stage_20_16.png.png", "20~16.png", "20_16.png", ], "20_16": [ "bg_20_16.png", "background_20_16.png", "quarantine_ward.png", "ChatGPT Image 2026년 6월 2일 오후 02_43_37 (1).png", ], "15_11": ["assets/bg_15_11.png", "bg_15_11.png", "background_15_11.png", "poison_lab.png"], "10_6": ["assets/bg_10_6.png", "bg_10_6.png", "background_10_6.png", "electric_lab.png"], "5_1": ["assets/bg_5_1.png", "bg_5_1.png", "background_5_1.png", "central_lobby.png"], }

ROOM_NORMAL = "일반 전투방"
ROOM_TRAP = "함정방"
ROOM_SURVIVAL = "생존방"
ROOM_REWARD = "보상방"
ROOM_SHOP = "상점방"
ROOM_REST = "휴식방"
ROOM_ELITE = "엘리트방"
ROOM_POISON = "독성방"
ROOM_ELECTRIC = "전기방"
ROOM_WILD = "야생방"
ROOM_EARTH = "대지방"
ROOM_BOSS = "보스방"
ROOM_FINAL = "최종 보스방"

WHITE = (235, 242, 246)
BLACK = (5, 8, 12)
RED = (230, 65, 70)
GREEN = (75, 230, 130)
CYAN = (75, 230, 230)
BLUE = (75, 130, 255)
PURPLE = (180, 90, 255)
YELLOW = (245, 220, 85)
ORANGE = (245, 145, 55)
GRAY = (120, 130, 138)
DARK = (12, 16, 22)

STARTER_CHARACTER_ID = "knight_blue"
OLD_MAIN_CHARACTER_ID = "C001"

CHARACTER_POOL = [
    {"id": "knight_blue", "name": "Blue Knight", "rank": 3, "desc": "처음부터 함께하는 파란 기사 캐릭터입니다.", "attack_bonus": 0.04, "speed_bonus": 0.02, "skill_cooldown_bonus": 0.00, "max_hp_bonus": 5, "dash_cooldown_bonus": 0.00, "ultimate_gain_bonus": 0.00, "sprite_path": "knight_blue_sheet.png", "starter": True, "default_unlocked": True, "obtain_method": "starter", "sprite_layout": "knight_4x4", "anim_type": "default"},
    {"id": "C001", "name": "Zeppili", "rank": 1, "desc": "뽑기로 획득할 수 있는 전기 숲 정령입니다.", "attack_bonus": 0.00, "speed_bonus": 0.00, "skill_cooldown_bonus": 0.00, "max_hp_bonus": 0, "dash_cooldown_bonus": 0.00, "ultimate_gain_bonus": 0.00, "sprite_path": "old_main_sheet.png", "starter": False, "default_unlocked": False, "obtain_method": "gacha", "sprite_layout": "zeppili_sheet", "anim_type": "zeppili"},
    {"id": "C002", "name": "전기 견습생", "rank": 1, "desc": "조금 빠른 이동으로 전투를 시작합니다.", "attack_bonus": 0.02, "speed_bonus": 0.03, "skill_cooldown_bonus": 0.00, "max_hp_bonus": 0, "dash_cooldown_bonus": 0.00, "ultimate_gain_bonus": 0.00, "sprite_path": None},
    {"id": "C003", "name": "민첩한 청소로봇", "rank": 1, "desc": "가벼운 공격 보너스를 가집니다.", "attack_bonus": 0.03, "speed_bonus": 0.01, "skill_cooldown_bonus": 0.00, "max_hp_bonus": 0, "dash_cooldown_bonus": 0.00, "ultimate_gain_bonus": 0.00, "sprite_path": None},
    {"id": "C101", "name": "번개 수습요원", "rank": 2, "desc": "스킬을 더 자주 사용할 수 있습니다.", "attack_bonus": 0.05, "speed_bonus": 0.02, "skill_cooldown_bonus": 0.05, "max_hp_bonus": 5, "dash_cooldown_bonus": 0.00, "ultimate_gain_bonus": 0.00, "sprite_path": None},
    {"id": "C102", "name": "격리 드론조사", "rank": 2, "desc": "안정적인 체력과 공격 보너스를 제공합니다.", "attack_bonus": 0.04, "speed_bonus": 0.00, "skill_cooldown_bonus": 0.05, "max_hp_bonus": 8, "dash_cooldown_bonus": 0.00, "ultimate_gain_bonus": 0.00, "sprite_path": None},
    {"id": "C103", "name": "실험체 파쇄꾼", "rank": 2, "desc": "근접 전투에 유리한 2성 캐릭터입니다.", "attack_bonus": 0.07, "speed_bonus": 0.00, "skill_cooldown_bonus": 0.00, "max_hp_bonus": 5, "dash_cooldown_bonus": 0.00, "ultimate_gain_bonus": 0.00, "sprite_path": None},
    {"id": "C201", "name": "폭주 전기기사", "rank": 3, "desc": "강력한 공격과 궁극기 충전 보너스를 가집니다.", "attack_bonus": 0.10, "speed_bonus": 0.03, "skill_cooldown_bonus": 0.10, "max_hp_bonus": 10, "dash_cooldown_bonus": 0.10, "ultimate_gain_bonus": 0.10, "sprite_path": None},
    {"id": "C202", "name": "파편 검사", "rank": 3, "desc": "대시와 스킬 순환이 뛰어난 3성 캐릭터입니다.", "attack_bonus": 0.08, "speed_bonus": 0.05, "skill_cooldown_bonus": 0.10, "max_hp_bonus": 8, "dash_cooldown_bonus": 0.10, "ultimate_gain_bonus": 0.10, "sprite_path": None},
    {"id": "C203", "name": "코어 해방자", "rank": 3, "desc": "최종 구역 돌파에 특화된 3성 캐릭터입니다.", "attack_bonus": 0.12, "speed_bonus": 0.02, "skill_cooldown_bonus": 0.10, "max_hp_bonus": 12, "dash_cooldown_bonus": 0.10, "ultimate_gain_bonus": 0.10, "sprite_path": None},
]

CHARACTER_CONFIGS = {character["id"]: character for character in CHARACTER_POOL}
CHARACTER_BY_ID = CHARACTER_CONFIGS

def get_character_anim_type(character_id):
    config = CHARACTER_CONFIGS.get(character_id, CHARACTER_CONFIGS.get(STARTER_CHARACTER_ID, {}))
    return config.get("anim_type", "default")

PET_DEFS = {
    "heal": {
        "name": "메디캣",
        "image": "pet_heal.png",
        "style": "pill",
        "desc": "자동 회복 보조 펫입니다. 회복 속도와 회복량이 증가하고, 방 클리어 시 추가 회복합니다.",
        "short": "회복 보조",
        "hp_regen_rate_bonus": 0.30,
        "hp_regen_amount_bonus": 2,
        "stage_clear_heal": 10,
        "color": (95, 230, 150),
    },
    "attack": {
        "name": "불꽃링",
        "image": "pet_attack.png",
        "style": "firework",
        "desc": "공격 보조 펫입니다. 공격 사거리, 공격력, 공격 속도를 강화합니다.",
        "short": "공격 강화",
        "attack_range_bonus": 40,
        "attack_damage_bonus": 3,
        "attack_speed_bonus": 0.20,
        "color": (255, 145, 80),
    },
    "zone": {
        "name": "루미존",
        "image": "pet_field.png",
        "fallback_images": ["pet_zone.png", "zone_pet.png"],
        "style": "spotlight",
        "desc": "주기적으로 아군 장판을 생성하고 범위, 피해, 흡혈 효과를 제공합니다.",
        "short": "장판 생성",
        "type": "zone",
        "zone_radius": 120,
        "zone_damage": 8,
        "zone_boss_damage": 4,
        "zone_tick_interval": 0.35,
        "zone_color": (160, 70, 255),
        "zone_alpha": 80,
        "zone_radius_bonus": 25,
        "zone_damage_bonus": 2,
        "zone_lifesteal": 0.05,
        "color": (155, 170, 255),
    },
}

def clamp(value, low, high):
    return max(low, min(high, value))

def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def circle_intersects_rect(center, radius, rect):
    center = pygame.Vector2(center)
    closest_x = clamp(center.x, rect.left, rect.right)
    closest_y = clamp(center.y, rect.top, rect.bottom)
    return distance(center, (closest_x, closest_y)) <= radius

def lerp(a, b, t):
    return a + (b - a) * t

def point_in_polygon(point, polygon):
    x, y = point
    inside = False
    j = len(polygon) - 1
    for i in range(len(polygon)):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        crosses = (yi > y) != (yj > y)
        if crosses:
            denom = yj - yi
            if abs(denom) < 0.0001:
                denom = 0.0001
            x_intersect = (xj - xi) * (y - yi) / denom + xi
            if x < x_intersect:
                inside = not inside
        j = i
    return inside

def polygon_x_bounds(y, polygon):
    intersections = []
    j = len(polygon) - 1
    for i in range(len(polygon)):
        x1, y1 = polygon[i]
        x2, y2 = polygon[j]
        if (y1 <= y < y2) or (y2 <= y < y1):
            denom = y2 - y1
            if abs(denom) < 0.0001:
                denom = 0.0001
            x = x1 + (y - y1) * (x2 - x1) / denom
            intersections.append(x)
        j = i
    if len(intersections) < 2:
        xs = [p[0] for p in polygon]
        return min(xs), max(xs)
    intersections.sort()
    return intersections[0], intersections[-1]

def is_circle_inside_polygon(pos, radius, polygon):
    diagonal = radius * 0.7
    samples = ( (pos.x, pos.y), (pos.x - radius, pos.y), (pos.x + radius, pos.y), (pos.x, pos.y - radius), (pos.x, pos.y + radius), (pos.x - diagonal, pos.y - diagonal), (pos.x + diagonal, pos.y - diagonal), (pos.x - diagonal, pos.y + diagonal), (pos.x + diagonal, pos.y + diagonal), )
    return all(point_in_polygon(sample, polygon) for sample in samples)

def clamp_point_to_polygon(pos, polygon, padding=0):
    ys = [p[1] for p in polygon]
    y = clamp(pos.y, min(ys) + padding, max(ys) - padding)
    left, right = polygon_x_bounds(y, polygon)
    x = clamp(pos.x, left + padding, right - padding)
    result = pygame.Vector2(x, y)
    if padding > 0 and not is_circle_inside_polygon(result, padding, polygon):
        center = pygame.Vector2( sum(point[0] for point in polygon) / len(polygon), sum(point[1] for point in polygon) / len(polygon), )
        for _ in range(12):
            result = result.lerp(center, 0.18)
            if is_circle_inside_polygon(result, padding, polygon):
                break
    return result

def get_random_point_in_walkable_polygon(polygon, floor_top_y, floor_bottom_y, padding=24):
    for _ in range(50):
        y = random.randint(int(floor_top_y + padding), int(floor_bottom_y - padding))
        left, right = polygon_x_bounds(y, polygon)
        if right - left <= padding * 2:
            continue
        x = random.randint(int(left + padding), int(right - padding))
        pos = pygame.Vector2(x, y)
        if is_circle_inside_polygon(pos, padding, polygon):
            return x, y
    point = clamp_point_to_polygon( pygame.Vector2(sum(p[0] for p in polygon) / len(polygon), (floor_top_y + floor_bottom_y) * 0.5), polygon, padding, )
    return int(point.x), int(point.y)

def get_background_key(floor):
    if 16 <= floor <= 20:
        return "20_16"
    if 11 <= floor <= 15:
        return "15_11"
    if 6 <= floor <= 10:
        return "10_6"
    return "5_1"

def get_normal_stage_background_key_for_floor(floor):
    if 16 <= floor <= 20:
        return "stage_20_16"
    if 11 <= floor <= 15:
        return "15_11"
    if 6 <= floor <= 10:
        return "10_6"
    return "5_1"

def is_stage_20_16_combat_room(floor, room_type):
    return 16 <= floor <= 20 and room_type not in (ROOM_BOSS, ROOM_FINAL, ROOM_REWARD, ROOM_SHOP, ROOM_REST)

def make_ratio_polygon(width, height, ratios):
    return [(width * x, height * y) for x, y in ratios]

def make_ice_dragon_walkable_polygon(width, height, steps=30):
    cx, cy, rx, ry = get_ice_dragon_arena_geometry(width, height)
    points = []
    for index in range(steps + 1):
        theta = math.pi - (math.pi * index / steps)
        points.append((cx + math.cos(theta) * rx, cy + math.sin(theta) * ry))
    return points

def get_ice_dragon_arena_geometry(width, height, shrink=0):
    cx = width * ICE_DRAGON_ARENA_CENTER_RATIO[0]
    cy = height * ICE_DRAGON_ARENA_CENTER_RATIO[1]
    rx = width * ICE_DRAGON_ARENA_RX_RATIO - ICE_DRAGON_ARENA_MARGIN - shrink
    ry = height * ICE_DRAGON_ARENA_RY_RATIO - ICE_DRAGON_ARENA_MARGIN - shrink
    return cx, cy, max(1, rx), max(1, ry)

def get_ice_dragon_arena_values(width, height):
    cx, cy, rx, ry = get_ice_dragon_arena_geometry(width, height)
    return cx, cy, (rx, ry)

def ice_dragon_sector_angle_range(sector_index):
    sector_index = int(clamp(sector_index, 0, 4))
    sector_size = math.pi / 5
    start_angle = math.pi - sector_size * sector_index
    end_angle = math.pi - sector_size * (sector_index + 1)
    return start_angle, end_angle

def ice_dragon_sector_from_point(point, arena_center, arena_rx, arena_ry, radius=0):
    pos = pygame.Vector2(point)
    center = pygame.Vector2(arena_center)
    rx = max(1, arena_rx + radius)
    ry = max(1, arena_ry + radius)
    rel = pos - center
    if rel.y < -radius:
        return None
    nx = rel.x / rx
    ny = rel.y / ry
    if nx * nx + ny * ny > 1.0:
        return None
    angle = math.atan2(max(0.0, ny), nx)
    return int(clamp((math.pi - angle) / (math.pi / 5), 0, 4.999))

def ice_dragon_sector_polygon(arena_center, arena_rx, arena_ry, sector_index, steps=18):
    if sector_index is None:
        return []
    center = pygame.Vector2(arena_center)
    start_angle, end_angle = ice_dragon_sector_angle_range(sector_index)
    points = [(center.x, center.y)]
    for index in range(steps + 1):
        t = index / max(1, steps)
        angle = start_angle + (end_angle - start_angle) * t
        points.append(( center.x + math.cos(angle) * arena_rx, center.y + math.sin(angle) * arena_ry, ))
    return points

def get_zone_info(floor):
    if 16 <= floor <= 20:
        return ("빙결 실험 구역", "차가운 실험장이 펼쳐진 빙결 구역입니다.", (105, 205, 255))
    if 11 <= floor <= 15:
        return ("야생 격리 구역", "야생화된 실험체들이 격리된 구역입니다.", (255, 125, 55))
    if 6 <= floor <= 10:
        return ("대지 상태구역", "대지의 힘이 뒤틀린 상태 구역입니다.", (95, 215, 125))
    return ("전력제어 구역", "최종 전력망이 집중된 제어 구역입니다.", (145, 110, 255))
def find_asset_path(*relative_paths):
    roots = []
    for root in (PROJECT_DIR, BASE_DIR, os.getcwd()):
        if root not in roots:
            roots.append(root)
    for relative_path in relative_paths:
        for root in roots:
            path = os.path.join(root, relative_path)
            if os.path.exists(path):
                return path
    return None

def optional_asset_candidates(filename):
    if not filename:
        return []
    names = [filename]
    if not filename.lower().endswith(".png"):
        names.append(f"{filename}.png")
    else:
        names.append(f"{filename}.png")
    candidates = []
    for name in names:
        candidates.append(name)
        candidates.append(os.path.join("assets", name))
    return candidates

def is_valid_background_filename(filename, allow_boss_stage=True):
    if not filename:
        return False
    lower = os.path.basename(str(filename)).lower()
    allowed_exact = {
        "20_16",
        "15_11",
        "10_6",
        "5_1",
        "ice_dragon_stage",
        "stage_20_16",
        "inferno_stage_11",
        "forest_guardian_stage",
        "forest_guardian_stage.png",
        "final_core_stage",
        "final_core_stage.png",
    }
    if lower in allowed_exact:
        return True
    if lower.startswith("stage_") or lower.startswith("bg_") or lower.startswith("background_") or lower.startswith("lobby") or lower.startswith("inferno_stage"):
        return True
    if "ice_dragon_stage" in lower or "boss_stage_15_ice" in lower:
        return True
    if allow_boss_stage and lower.startswith("boss_stage_"):
        return True
    blocked_keywords = ( "sheet", "player", "character", "knight", "zepp", "zeppli", "old_main", "eff", "effect", "pet", "slime", "sprite", "icon", "skill", "attack", "idle", "walk", "groggy", "defeat", "telegraph", "boss", )
    if any(keyword in lower for keyword in blocked_keywords):
        return False
    return False

def load_image_optional(filename, size=None, alpha=True):
    if not filename:
        return None
    cache_key = (filename, size, alpha)
    if cache_key in BOSS_SKIN_CACHE:
        return BOSS_SKIN_CACHE[cache_key]

    path = find_asset_path(*optional_asset_candidates(filename))
    if not path:
        warn_key = ("missing", filename)
        if warn_key not in BOSS_OPTIONAL_IMAGE_WARNED:
            print(f"[WARN] optional boss image missing: {filename}")
            BOSS_OPTIONAL_IMAGE_WARNED.add(warn_key)
        BOSS_SKIN_CACHE[cache_key] = None
        return None

    try:
        image = pygame.image.load(path)
        if pygame.display.get_surface():
            image = image.convert_alpha() if alpha else image.convert()
        else:
            image = image.copy()
        if size:
            image = pygame.transform.smoothscale(image, size)
        BOSS_SKIN_CACHE[cache_key] = image
        return image
    except (pygame.error, OSError, FileNotFoundError, ValueError) as exc:
        warn_key = ("failed", filename)
        if warn_key not in BOSS_OPTIONAL_IMAGE_WARNED:
            print(f"[WARN] optional boss image failed: {filename} / {exc}")
            BOSS_OPTIONAL_IMAGE_WARNED.add(warn_key)
        BOSS_SKIN_CACHE[cache_key] = None
        return None

def load_boss_skill_images(sheet_key):
    if sheet_key in BOSS_SKILL_IMAGE_CACHE:
        return BOSS_SKILL_IMAGE_CACHE[sheet_key]
    config = BOSS_SKILL_SHEETS.get(sheet_key)
    if not config:
        BOSS_SKILL_IMAGE_CACHE[sheet_key] = {}
        return {}
    filename, kinds = config
    path = find_asset_path(os.path.join("assets", filename), filename)
    if not path:
        BOSS_SKILL_IMAGE_CACHE[sheet_key] = {}
        return {}
    try:
        sheet = pygame.image.load(path)
        sheet = sheet.convert_alpha() if pygame.display.get_surface() else sheet.copy()
        cell_w = sheet.get_width() // 2
        cell_h = sheet.get_height() // 2
        frames = {}
        for index, kind in enumerate(kinds):
            crop = BOSS_SKILL_CROP_RATIOS.get(sheet_key, {}).get(kind)
            if crop:
                art = crop_by_ratio(sheet, *crop)
            else:
                col = index % 2
                row = index // 2
                cell = sheet.subsurface(pygame.Rect(col * cell_w, row * cell_h, cell_w, cell_h)).copy()
                art_rect = pygame.Rect(int(cell_w * 0.02), int(cell_h * 0.02), int(cell_w * 0.96), int(cell_h * 0.96))
                art_rect = art_rect.clip(cell.get_rect())
                art = cell.subsurface(art_rect).copy()
            art = remove_skill_checker_background(art, sheet_key)
            art = trim_transparent(art, padding=10)
            frames[kind] = art
        BOSS_SKILL_IMAGE_CACHE[sheet_key] = frames
        return frames
    except (pygame.error, OSError, ValueError) as exc:
        print(f"[WARN] boss skill sheet failed: {filename} / {exc}")
        BOSS_SKILL_IMAGE_CACHE[sheet_key] = {}
        return {}

def remove_skill_checker_background(surface, sheet_key):
    image = surface.copy().convert_alpha()
    w, h = image.get_size()
    sample_points = [
        (0, 0),
        (max(0, w - 1), 0),
        (0, max(0, h - 1)),
        (max(0, w - 1), max(0, h - 1)),
        (w // 2, 0),
        (0, h // 2),
    ]
    samples = [image.get_at(point) for point in sample_points]
    bg = sorted(samples, key=lambda c: c.r + c.g + c.b)[len(samples) // 2]

    def close_to_bg(color, tolerance):
        return (
            abs(color.r - bg.r)
            + abs(color.g - bg.g)
            + abs(color.b - bg.b)
        ) <= tolerance

    if sheet_key in ("inferno", "forest"):
        tolerance = 68 if sheet_key == "inferno" else 76
        visited = set()
        stack = []
        for x in range(w):
            stack.append((x, 0))
            stack.append((x, h - 1))
        for y in range(h):
            stack.append((0, y))
            stack.append((w - 1, y))

        while stack:
            x, y = stack.pop()
            if (x, y) in visited or x < 0 or y < 0 or x >= w or y >= h:
                continue
            visited.add((x, y))
            c = image.get_at((x, y))
            if c.a >= 8 and not close_to_bg(c, tolerance):
                continue
            image.set_at((x, y), (c.r, c.g, c.b, 0))
            stack.append((x + 1, y))
            stack.append((x - 1, y))
            stack.append((x, y + 1))
            stack.append((x, y - 1))

        for y in range(h):
            for x in range(w):
                c = image.get_at((x, y))
                if c.a < 8:
                    image.set_at((x, y), (c.r, c.g, c.b, 0))
        return image

    for y in range(h):
        for x in range(w):
            c = image.get_at((x, y))
            if c.a < 8:
                image.set_at((x, y), (c.r, c.g, c.b, 0))
                continue
            mx = max(c.r, c.g, c.b)
            mn = min(c.r, c.g, c.b)
            saturation = mx - mn
            brightness = (c.r + c.g + c.b) // 3
            remove = False
            if sheet_key == "inferno":
                gray_background = saturation < 24 and 52 <= brightness <= 118
                remove = close_to_bg(c, 62) or gray_background
            elif sheet_key == "forest":
                white_background = saturation < 34 and brightness >= 205
                remove = close_to_bg(c, 72) or white_background
            else:
                gray_background = saturation < 20 and 22 <= brightness <= 86
                remove = close_to_bg(c, 50) or gray_background
            if remove:
                image.set_at((x, y), (c.r, c.g, c.b, 0))
    return image

def get_boss_skill_image(kind):
    sheet_key = BOSS_SKILL_KIND_TO_SHEET.get(kind)
    if not sheet_key:
        return None
    return load_boss_skill_images(sheet_key).get(kind)

def draw_boss_skill_warning_image(surface, warning):
    image = get_boss_skill_image(warning.kind)
    if image is None:
        return False
    warning_total = max(0.01, getattr(warning, "max_warning_time", warning.warning_time))
    active_total = max(0.01, getattr(warning, "max_active_time", warning.active_time))
    if warning.warning_time > 0:
        progress = clamp(1.0 - warning.warning_time / warning_total, 0.0, 1.0)
        pulse = 0.50 + 0.50 * abs(math.sin(pygame.time.get_ticks() * 0.016))
        alpha = int(38 + progress * 72 + pulse * 28)
        grow = 0.62 + progress * 0.34
    else:
        progress = clamp(1.0 - warning.active_time / active_total, 0.0, 1.0)
        fade = clamp(warning.active_time / active_total, 0.0, 1.0)
        pulse = 0.50 + 0.50 * abs(math.sin(pygame.time.get_ticks() * 0.020))
        alpha = int((178 + pulse * 45) * fade)
        grow = 1.0 + 0.10 * math.sin(progress * math.pi)
    if warning.shape == "laser":
        length, laser_width = warning.size
        if warning.kind in ("inferno_claw",):
            target_w = max(90, int(length * 0.92 * grow))
            target_h = max(64, int(laser_width * (10.0 if warning.active else 6.8) * grow))
        elif warning.kind in ("forest_thorns",):
            target_w = max(90, int(length * 0.82 * grow))
            target_h = max(58, int(laser_width * (9.0 if warning.active else 6.2) * grow))
        else:
            target_w = max(90, int(length * grow))
            target_h = max(46, int(laser_width * (9.5 if warning.active else 5.8) * grow))
        center = warning.pos + pygame.Vector2(1, 0).rotate(warning.angle) * (length * 0.5)
        scaled = pygame.transform.smoothscale(image, (target_w, target_h))
        scaled = pygame.transform.rotate(scaled, -warning.angle)
        scaled.set_alpha(alpha)
        surface.blit(scaled, scaled.get_rect(center=(int(center.x), int(center.y))), special_flags=pygame.BLEND_RGBA_ADD)
        if warning.active:
            pygame.draw.circle(surface, (*warning.color, 70), (int(warning.pos.x), int(warning.pos.y)), max(8, int(laser_width * 2.2)))
        return True
    if warning.shape == "circle":
        if warning.kind in ("inferno_meteor", "final_collapse", "forest_fury"):
            size = max(80, int(warning.size * (2.45 if warning.active else 1.65) * grow))
        elif warning.kind in ("forest_poison",):
            size = max(90, int(warning.size * (2.65 if warning.active else 1.80) * grow))
        else:
            size = max(84, int(warning.size * (2.15 if warning.active else 1.55) * grow))
        scaled = pygame.transform.smoothscale(image, (size, size))
        scaled.set_alpha(alpha)
        surface.blit(scaled, scaled.get_rect(center=(int(warning.pos.x), int(warning.pos.y))), special_flags=pygame.BLEND_RGBA_ADD)
        if warning.active and warning.kind in ("inferno_meteor", "final_collapse", "forest_fury"):
            pygame.draw.circle(surface, (*warning.color, 58), (int(warning.pos.x), int(warning.pos.y)), max(10, int(warning.size * 0.55)))
        return True
    if warning.shape == "ellipse":
        rx, ry = warning.size
        target_w = max(72, int(rx * (2.7 if warning.active else 1.9) * grow))
        target_h = max(54, int(ry * (4.5 if warning.active else 2.6) * grow))
        scaled = pygame.transform.smoothscale(image, (target_w, target_h))
        scaled.set_alpha(alpha)
        surface.blit(scaled, scaled.get_rect(center=(int(warning.pos.x), int(warning.pos.y))), special_flags=pygame.BLEND_RGBA_ADD)
        if warning.active:
            pygame.draw.ellipse(surface, (*warning.color, 55), pygame.Rect(0, 0, int(rx * 2), int(ry * 2)).move(int(warning.pos.x - rx), int(warning.pos.y - ry)))
        return True
    return False

def list_asset_images():
    images = []
    for root in (os.path.join(PROJECT_DIR, "assets"), os.path.join(BASE_DIR, "assets")):
        if not os.path.isdir(root):
            continue
        try:
            for name in os.listdir(root):
                lower = name.lower()
                if lower.endswith((".png", ".jpg", ".jpeg", ".webp")):
                    images.append(os.path.join(root, name))
        except OSError:
            pass
    return images

def scale_cover(image, size):
    target_w, target_h = size
    src_w, src_h = image.get_size()
    scale = max(target_w / max(1, src_w), target_h / max(1, src_h))
    scaled_w = max(1, int(src_w * scale))
    scaled_h = max(1, int(src_h * scale))
    scaled = pygame.transform.smoothscale(image, (scaled_w, scaled_h))
    x = max(0, (scaled_w - target_w) // 2)
    y = max(0, (scaled_h - target_h) // 2)
    return scaled.subsurface(pygame.Rect(x, y, target_w, target_h)).copy()

def crop_by_ratio(surface, x1, y1, x2, y2):
    width, height = surface.get_size()
    rect = pygame.Rect( int(width * x1), int(height * y1), max(1, int(width * (x2 - x1))), max(1, int(height * (y2 - y1))), )
    rect.clamp_ip(surface.get_rect())
    return surface.subsurface(rect).copy()

def remove_white_background(surface):
    image = surface.copy().convert_alpha()
    width, height = image.get_size()

    def is_sheet_background(color):
        if color.a < 12:
            return True
        bright = color.r > 238 and color.g > 238 and color.b > 238
        neutral_light = ( color.r > 212 and color.g > 212 and color.b > 212 and max(color.r, color.g, color.b) - min(color.r, color.g, color.b) < 32 )
        return bright or neutral_light

    stack = []
    visited = set()
    for x in range(width):
        stack.append((x, 0))
        stack.append((x, height - 1))
    for y in range(height):
        stack.append((0, y))
        stack.append((width - 1, y))

    while stack:
        x, y = stack.pop()
        if (x, y) in visited or x < 0 or y < 0 or x >= width or y >= height:
            continue
        visited.add((x, y))
        color = image.get_at((x, y))
        if not is_sheet_background(color):
            continue
        image.set_at((x, y), (color.r, color.g, color.b, 0))
        stack.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))

    original = image.copy()
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            color = original.get_at((x, y))
            if color.a <= 0 or not is_sheet_background(color):
                continue
            if any(original.get_at((x + dx, y + dy)).a == 0 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                image.set_at((x, y), (color.r, color.g, color.b, 0))
    return image

def _monster_cell_content_top(cell):
    width, height = cell.get_size()
    occupied_rows = []
    for y in range(height):
        pixel_count = 0
        for x in range(width):
            color = cell.get_at((x, y))
            if color.a > 8 and (color.r < 245 or color.g < 245 or color.b < 245):
                pixel_count += 1
                if pixel_count >= 3:
                    occupied_rows.append(y)
                    break
    bands = []
    for y in occupied_rows:
        if not bands or y > bands[-1][1] + 8:
            bands.append([y, y])
        else:
            bands[-1][1] = y
    if (
        len(bands) >= 2
        and bands[0][1] - bands[0][0] <= 40
        and bands[1][1] - bands[1][0] >= 60
        and bands[1][0] - bands[0][1] >= 10
    ):
        return max(0, bands[1][0] - 6)
    if bands:
        return max(0, bands[0][0] - 6)
    return 0

def normalize_monster_20_16_frame(frame, output_size=MONSTER_20_16_FRAME_SIZE):
    bounds = frame.get_bounding_rect(min_alpha=8)
    if bounds.width <= 0 or bounds.height <= 0:
        return None
    bounds.inflate_ip(16, 16)
    bounds = bounds.clip(frame.get_rect())
    trimmed = frame.subsurface(bounds).copy()
    out_w, out_h = output_size
    max_w = out_w - 6
    max_h = out_h - 6
    scale = min(max_w / max(1, trimmed.get_width()), max_h / max(1, trimmed.get_height()))
    scaled_size = (
        max(1, int(trimmed.get_width() * scale)),
        max(1, int(trimmed.get_height() * scale)),
    )
    scaled = pygame.transform.smoothscale(trimmed, scaled_size)
    normalized = pygame.Surface(output_size, pygame.SRCALPHA)
    normalized.blit(scaled, scaled.get_rect(midbottom=(out_w // 2, out_h - 3)))
    return normalized

def split_monster_20_16_row(row_surface, cell_w):
    crop_top = _monster_cell_content_top(row_surface)
    content = row_surface.subsurface(
        pygame.Rect(0, crop_top, row_surface.get_width(), row_surface.get_height() - crop_top)
    ).copy()
    cleaned = remove_white_background(content)
    mask = pygame.mask.from_surface(cleaned, 8)
    assigned = [
        pygame.Surface(cleaned.get_size(), pygame.SRCALPHA)
        for _ in range(8)
    ]
    centers = [(col + 0.5) * cell_w for col in range(8)]
    components = []
    primary_by_col = {}
    for component in mask.connected_components(2):
        center = component.centroid()
        area = component.count()
        components.append((component, center, area))
        nearest_col = min(range(8), key=lambda index: abs(center[0] - centers[index]))
        current = primary_by_col.get(nearest_col)
        if current is None or area > current[2]:
            primary_by_col[nearest_col] = (component, center, area)
    primary_centers = {
        col: data[1]
        for col, data in primary_by_col.items()
    }
    for component, center, _ in components:
        if primary_centers:
            col = min(
                primary_centers,
                key=lambda index: (
                    (center[0] - primary_centers[index][0]) ** 2
                    + (center[1] - primary_centers[index][1]) ** 2
                ),
            )
        else:
            col = min(range(8), key=lambda index: abs(center[0] - centers[index]))
        for bounds in component.get_bounding_rects():
            for y in range(bounds.top, bounds.bottom):
                for x in range(bounds.left, bounds.right):
                    if component.get_at((x, y)):
                        assigned[col].set_at((x, y), cleaned.get_at((x, y)))
    return [normalize_monster_20_16_frame(frame) for frame in assigned]

def load_monster_20_16_frames():
    global MONSTER_20_16_FRAMES, MONSTER_20_16_LOAD_ATTEMPTED
    if MONSTER_20_16_LOAD_ATTEMPTED:
        return MONSTER_20_16_FRAMES
    MONSTER_20_16_LOAD_ATTEMPTED = True
    path = find_asset_path(os.path.join("assets", MONSTER_20_16_SHEET))
    if not path:
        MONSTER_20_16_FRAMES = None
        return None
    try:
        sheet = pygame.image.load(path).convert_alpha()
        cell_w = sheet.get_width() // 8
        cell_h = sheet.get_height() // 3
        if cell_w <= 0 or cell_h <= 0:
            return None
        frame_keys = (
            "up",
            "down",
            "left",
            "right",
            "attack_up",
            "attack_down",
            "attack_left",
            "attack_right",
        )
        frames = {}
        for row, monster_type in enumerate(MONSTER_20_16_TYPES):
            row_rect = pygame.Rect(0, row * cell_h, sheet.get_width(), cell_h)
            row_surface = sheet.subsurface(row_rect).copy()
            row_frames = split_monster_20_16_row(row_surface, cell_w)
            monster_frames = {}
            for col, frame_key in enumerate(frame_keys):
                normalized = row_frames[col]
                if normalized is not None:
                    monster_frames[frame_key] = normalized
            if monster_frames:
                frames[monster_type] = monster_frames
        MONSTER_20_16_FRAMES = frames or None
        return MONSTER_20_16_FRAMES
    except (pygame.error, OSError, ValueError) as exc:
        print(f"[WARN] monster sprite sheet failed: {MONSTER_20_16_SHEET} / {exc}")
        MONSTER_20_16_FRAMES = None
        return None

def load_monster_15_11_frames():
    global MONSTER_15_11_FRAMES, MONSTER_15_11_LOAD_ATTEMPTED
    if MONSTER_15_11_LOAD_ATTEMPTED:
        return MONSTER_15_11_FRAMES
    MONSTER_15_11_LOAD_ATTEMPTED = True
    path = find_asset_path(os.path.join("assets", MONSTER_15_11_SHEET))
    if not path:
        MONSTER_15_11_FRAMES = None
        return None
    try:
        sheet = pygame.image.load(path).convert_alpha()
        cell_w = sheet.get_width() // 8
        cell_h = sheet.get_height() // 3
        if cell_w <= 0 or cell_h <= 0:
            return None
        frame_keys = (
            "up",
            "down",
            "left",
            "right",
            "attack_up",
            "attack_down",
            "attack_left",
            "attack_right",
        )
        frames = {}
        for row, monster_type in enumerate(MONSTER_15_11_TYPES):
            row_rect = pygame.Rect(0, row * cell_h, sheet.get_width(), cell_h)
            row_surface = sheet.subsurface(row_rect).copy()
            row_frames = split_monster_20_16_row(row_surface, cell_w)
            monster_frames = {}
            for col, frame_key in enumerate(frame_keys):
                normalized = row_frames[col]
                if normalized is not None:
                    monster_frames[frame_key] = normalized
            if monster_frames:
                frames[monster_type] = monster_frames
        MONSTER_15_11_FRAMES = frames or None
        if MONSTER_15_11_FRAMES:
            print(f"[OK] 15F-11F monster sheet loaded: {path}")
        return MONSTER_15_11_FRAMES
    except (pygame.error, OSError, ValueError) as exc:
        print(f"[WARN] monster sprite sheet failed: {MONSTER_15_11_SHEET} / {exc}")
        MONSTER_15_11_FRAMES = None
        return None

def load_monster_10_6_frames():
    global MONSTER_10_6_FRAMES, MONSTER_10_6_LOAD_ATTEMPTED
    if MONSTER_10_6_LOAD_ATTEMPTED:
        return MONSTER_10_6_FRAMES
    MONSTER_10_6_LOAD_ATTEMPTED = True
    path = find_asset_path(os.path.join("assets", MONSTER_10_6_SHEET))
    if not path:
        MONSTER_10_6_FRAMES = None
        return None
    try:
        sheet = pygame.image.load(path).convert_alpha()
        cell_w = sheet.get_width() // 8
        cell_h = sheet.get_height() // 3
        if cell_w <= 0 or cell_h <= 0:
            return None
        frame_keys = (
            "up",
            "down",
            "left",
            "right",
            "attack_up",
            "attack_down",
            "attack_left",
            "attack_right",
        )
        frames = {}
        for row, monster_type in enumerate(MONSTER_10_6_TYPES):
            row_rect = pygame.Rect(0, row * cell_h, sheet.get_width(), cell_h)
            row_surface = sheet.subsurface(row_rect).copy()
            row_frames = split_monster_20_16_row(row_surface, cell_w)
            monster_frames = {}
            for col, frame_key in enumerate(frame_keys):
                normalized = row_frames[col]
                if normalized is not None:
                    monster_frames[frame_key] = normalized
            if monster_frames:
                frames[monster_type] = monster_frames
        MONSTER_10_6_FRAMES = frames or None
        if MONSTER_10_6_FRAMES:
            print(f"[OK] 10F-6F monster sheet loaded: {path}")
        return MONSTER_10_6_FRAMES
    except (pygame.error, OSError, ValueError) as exc:
        print(f"[WARN] monster sprite sheet failed: {MONSTER_10_6_SHEET} / {exc}")
        MONSTER_10_6_FRAMES = None
        return None

def load_monster_5_1_frames():
    global MONSTER_5_1_FRAMES, MONSTER_5_1_LOAD_ATTEMPTED
    if MONSTER_5_1_LOAD_ATTEMPTED:
        return MONSTER_5_1_FRAMES
    MONSTER_5_1_LOAD_ATTEMPTED = True
    path = find_asset_path(os.path.join("assets", MONSTER_5_1_SHEET))
    if not path:
        MONSTER_5_1_FRAMES = None
        return None
    try:
        sheet = pygame.image.load(path).convert_alpha()
        cell_w = sheet.get_width() // 8
        cell_h = sheet.get_height() // 3
        if cell_w <= 0 or cell_h <= 0:
            return None
        frame_keys = (
            "up",
            "down",
            "left",
            "right",
            "attack_up",
            "attack_down",
            "attack_left",
            "attack_right",
        )
        frames = {}
        for row, monster_type in enumerate(MONSTER_5_1_TYPES):
            row_rect = pygame.Rect(0, row * cell_h, sheet.get_width(), cell_h)
            row_surface = sheet.subsurface(row_rect).copy()
            row_frames = split_monster_20_16_row(row_surface, cell_w)
            monster_frames = {}
            for col, frame_key in enumerate(frame_keys):
                normalized = row_frames[col]
                if normalized is not None:
                    monster_frames[frame_key] = normalized
            if monster_frames:
                frames[monster_type] = monster_frames
        MONSTER_5_1_FRAMES = frames or None
        if MONSTER_5_1_FRAMES:
            print(f"[OK] 5F-1F monster sheet loaded: {path}")
        return MONSTER_5_1_FRAMES
    except (pygame.error, OSError, ValueError) as exc:
        print(f"[WARN] monster sprite sheet failed: {MONSTER_5_1_SHEET} / {exc}")
        MONSTER_5_1_FRAMES = None
        return None

def direction_4way(vector, fallback="down"):
    if vector is None or vector.length_squared() < 0.0001:
        return fallback
    if abs(vector.x) > abs(vector.y):
        return "right" if vector.x > 0 else "left"
    return "down" if vector.y > 0 else "up"

def remove_neutral_edge_background(surface, tolerance=86):
    image = surface.copy().convert_alpha()
    width, height = image.get_size()
    samples = [ image.get_at((0, 0)), image.get_at((width - 1, 0)), image.get_at((0, height - 1)), image.get_at((width - 1, height - 1)), ]
    bg = min(samples, key=lambda c: max(c.r, c.g, c.b) - min(c.r, c.g, c.b))

    def is_background(color):
        if color.a < 12:
            return True
        neutral = max(color.r, color.g, color.b) - min(color.r, color.g, color.b) < 42
        close = abs(color.r - bg.r) + abs(color.g - bg.g) + abs(color.b - bg.b) < tolerance
        light_gray = color.r > 125 and color.g > 125 and color.b > 125 and neutral
        return close or light_gray

    stack = []
    visited = set()
    for x in range(width):
        stack.append((x, 0))
        stack.append((x, height - 1))
    for y in range(height):
        stack.append((0, y))
        stack.append((width - 1, y))

    while stack:
        x, y = stack.pop()
        if (x, y) in visited or x < 0 or y < 0 or x >= width or y >= height:
            continue
        visited.add((x, y))
        color = image.get_at((x, y))
        if not is_background(color):
            continue
        image.set_at((x, y), (color.r, color.g, color.b, 0))
        stack.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    return image

def remove_effect_sheet_background(surface):
    image = remove_white_background(surface)
    width, height = image.get_size()
    for y in range(height):
        for x in range(width):
            color = image.get_at((x, y))
            if color.a <= 0:
                continue
            maximum = max(color.r, color.g, color.b)
            minimum = min(color.r, color.g, color.b)
            saturation = maximum - minimum
            average = (color.r + color.g + color.b) / 3
            paper_tone = average > 205 and saturation < 95 and color.b > 150
            near_white = average > 228 and saturation < 120
            if paper_tone or near_white:
                image.set_at((x, y), (color.r, color.g, color.b, 0))
    return image

def apply_edge_fade(surface, margin_ratio=0.10):
    image = surface.copy().convert_alpha()
    width, height = image.get_size()
    margin_x = max(1, int(width * margin_ratio))
    margin_y = max(1, int(height * margin_ratio))
    for y in range(height):
        edge_y = min(y, height - 1 - y)
        fy = clamp(edge_y / margin_y, 0.0, 1.0)
        for x in range(width):
            edge_x = min(x, width - 1 - x)
            fade = min(clamp(edge_x / margin_x, 0.0, 1.0), fy)
            if fade >= 0.999:
                continue
            color = image.get_at((x, y))
            if color.a > 0:
                image.set_at((x, y), (color.r, color.g, color.b, int(color.a * fade)))
    return image

def keep_significant_alpha_components(surface, min_alpha=12):
    width, height = surface.get_size()
    visited = set()
    components = []
    for sy in range(height):
        for sx in range(width):
            if (sx, sy) in visited or surface.get_at((sx, sy)).a < min_alpha:
                continue
            stack = [(sx, sy)]
            visited.add((sx, sy))
            pixels = []
            while stack:
                x, y = stack.pop()
                pixels.append((x, y))
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if nx < 0 or ny < 0 or nx >= width or ny >= height or (nx, ny) in visited:
                        continue
                    visited.add((nx, ny))
                    if surface.get_at((nx, ny)).a >= min_alpha:
                        stack.append((nx, ny))
            components.append(pixels)

    if not components:
        return surface

    largest = max(len(component) for component in components)
    keep_threshold = max(42, int(largest * 0.045))
    cleaned = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    for component in components:
        if len(component) < keep_threshold:
            continue
        for x, y in component:
            cleaned.set_at((x, y), surface.get_at((x, y)))
    return cleaned

def clean_player_sprite(surface):
    cleaned = remove_white_background(surface)
    cleaned = keep_significant_alpha_components(cleaned)
    return trim_transparent(cleaned, padding=3)

def make_player_sprite_frame(frame, canvas_size=(PLAYER_SPRITE_W, PLAYER_SPRITE_H)):
    try:
        cleaned = remove_white_background(frame)
        cleaned = keep_significant_alpha_components(cleaned)
        cleaned = trim_transparent(cleaned, padding=8)
    except (pygame.error, ValueError):
        cleaned = frame.copy()
    if cleaned.get_width() <= 2 or cleaned.get_height() <= 2:
        return None

    canvas_w, canvas_h = canvas_size
    max_w = int(canvas_w * 0.95)
    max_h = int(canvas_h * 0.96)
    scale = min(max_w / max(1, cleaned.get_width()), max_h / max(1, cleaned.get_height()))
    target_w = max(1, int(cleaned.get_width() * scale))
    target_h = max(1, int(cleaned.get_height() * scale))
    scaled = pygame.transform.smoothscale(cleaned, (target_w, target_h))
    canvas = pygame.Surface((canvas_w, canvas_h), pygame.SRCALPHA)
    canvas.blit(scaled, ((canvas_w - target_w) // 2, canvas_h - target_h))
    return canvas

def normalize_jeffrey_frame(frame):
    try:
        cleaned = clean_player_sprite(frame)
    except (pygame.error, ValueError):
        cleaned = frame.copy()
    if cleaned.get_width() <= 2 or cleaned.get_height() <= 2:
        return None
    max_w = JEFFREY_FRAME_W - 10
    max_h = JEFFREY_CONTENT_H
    scale = min(max_w / max(1, cleaned.get_width()), max_h / max(1, cleaned.get_height()))
    target_w = max(1, int(cleaned.get_width() * scale))
    target_h = max(1, int(cleaned.get_height() * scale))
    scaled = pygame.transform.smoothscale(cleaned, (target_w, target_h))
    canvas = pygame.Surface((JEFFREY_FRAME_W, JEFFREY_FRAME_H), pygame.SRCALPHA)
    rect = scaled.get_rect(midbottom=(JEFFREY_FRAME_W // 2, JEFFREY_FRAME_H - 4))
    canvas.blit(scaled, rect)
    return canvas

def crop_knight_sprite_area(sheet):
    width, height = sheet.get_size()
    labeled_reference_sheet = width / max(1, height) > 1.45
    if not labeled_reference_sheet:
        return sheet.copy()
    left_r, top_r, right_r, bottom_r = KNIGHT_SHEET_CROP_RATIO
    left = int(width * left_r)
    top = int(height * top_r)
    right = int(width * (1.0 - right_r))
    bottom = int(height * (1.0 - bottom_r))
    rect = pygame.Rect(left, top, max(1, right - left), max(1, bottom - top)).clip(sheet.get_rect())
    if DEBUG_PLAYER_SPRITE_CROP:
        print("knight sprite crop:", rect)
    return sheet.subsurface(rect).copy()

def knight_reference_frame_rect(sheet, row, col):
    width, height = sheet.get_size()
    x1, y1, x2, y2 = KNIGHT_REFERENCE_RECTS_RATIO[row][col]
    pad_x = int(width * 0.010)
    pad_y = int(height * 0.012)
    left = int(width * x1) - pad_x
    top = int(height * y1) - pad_y
    right = int(width * x2) + pad_x
    bottom = int(height * y2) + pad_y
    rect = pygame.Rect(left, top, max(1, right - left), max(1, bottom - top)).clip(sheet.get_rect())
    if DEBUG_PLAYER_SPRITE_CROP:
        print("knight frame crop:", row, col, rect)
    return rect

def kakao_knight_reference_frame_rect(sheet, row, col):
    width, height = sheet.get_size()
    base_w, base_h = KAKAO_KNIGHT_REFERENCE_SIZE
    x1, y1, x2, y2 = KAKAO_KNIGHT_REFERENCE_RECTS[row][col]
    scale_x = width / max(1, base_w)
    scale_y = height / max(1, base_h)
    pad_x = int(width * 0.006)
    pad_y = int(height * 0.008)
    rect = pygame.Rect( int(x1 * scale_x) - pad_x, int(y1 * scale_y) - pad_y, int((x2 - x1) * scale_x) + pad_x * 2, int((y2 - y1) * scale_y) + pad_y * 2, ).clip(sheet.get_rect())
    if DEBUG_PLAYER_SPRITE_CROP:
        print("kakao knight frame crop:", row, col, rect)
    return rect

def trim_transparent(surface, padding=6):
    rect = surface.get_bounding_rect(min_alpha=10)
    if rect.width <= 0 or rect.height <= 0:
        return surface
    left = max(0, rect.left - padding)
    top = max(0, rect.top - padding)
    right = min(surface.get_width(), rect.right + padding)
    bottom = min(surface.get_height(), rect.bottom + padding)
    safe_rect = pygame.Rect(left, top, max(1, right - left), max(1, bottom - top))
    return surface.subsurface(safe_rect).copy()

def pad_sprite_bottom_center(surface, width, height):
    canvas = pygame.Surface((max(1, width), max(1, height)), pygame.SRCALPHA)
    rect = surface.get_rect(midbottom=(canvas.get_width() // 2, canvas.get_height()))
    canvas.blit(surface, rect)
    return canvas

def mirror_player_left_frames(sprites):
    right_to_left = { "right": "left", "right_walk_0": "left_walk_0", "right_walk_1": "left_walk_1", "right_attack_0": "left_attack_0", "right_attack_1": "left_attack_1", "right_attack": "left_attack", "right_skill_0": "left_skill_0", "right_skill_1": "left_skill_1", "right_skill": "left_skill", "down_right": "down_left", "down_right_walk_0": "down_left_walk_0", "down_right_walk_1": "down_left_walk_1", "down_right_attack_0": "down_left_attack_0", "down_right_attack_1": "down_left_attack_1", "up_right": "up_left", "up_right_walk_0": "up_left_walk_0", "up_right_walk_1": "up_left_walk_1", "up_right_attack_0": "up_left_attack_0", "up_right_attack_1": "up_left_attack_1", "diagonal_front_right": "diagonal_front_left", "diagonal_back_right": "diagonal_back_left", }
    for right_key, left_key in right_to_left.items():
        if sprites.get(right_key) and not sprites.get(left_key):
            sprites[left_key] = pygame.transform.flip(sprites[right_key], True, False)
    return sprites

def align_player_sprite_pairs(sprites):
    groups = [ ("left", "right"), ("left_walk_0", "right_walk_0"), ("left_walk_1", "right_walk_1"), ("left_attack_0", "right_attack_0"), ("left_attack_1", "right_attack_1"), ("left_attack", "right_attack"), ("down_left", "down_right"), ("up_left", "up_right"), ]
    for left_key, right_key in groups:
        left = sprites.get(left_key)
        right = sprites.get(right_key)
        if not left or not right:
            continue
        width = max(left.get_width(), right.get_width())
        height = max(left.get_height(), right.get_height())
        sprites[left_key] = pad_sprite_bottom_center(left, width, height)
        sprites[right_key] = pad_sprite_bottom_center(right, width, height)
    return sprites

def normalize_player_direction_sprites(sprites):
    mirror_player_left_frames(sprites)
    align_player_sprite_pairs(sprites)
    return sprites

def player_sprite_candidates(character_id):
    if character_id == STARTER_CHARACTER_ID:
        return [ os.path.join("assets", "KakaoTalk_20260604_153249267.png"), os.path.join("assets", "knight_blue_sheet.png"), os.path.join("assets", "knight_blue_sheet.png.png"), os.path.join("assets", "assetsknight_blue_sheet.png.png"), os.path.join("assets", "player_sheet.png"), os.path.join("assets", "player.png"), ]
    if character_id == OLD_MAIN_CHARACTER_ID:
        return [ os.path.join("assets", "old_main_sheet.png"), os.path.join("assets", "old_main_sheet.png.png"), os.path.join("assets", "assetsold_main_sheet.png.png"), os.path.join("assets", "ee38ae34-30e9-47e7-a6c3-bb50cb55690a.png"), os.path.join("assets", "zeppili_sheet.png"), os.path.join("assets", "zeppili.png"), os.path.join("assets", "eaab73a7-d497-4d9e-b05b-1a5628166365.png"), ]
    return player_sprite_candidates(STARTER_CHARACTER_ID)

def load_knight_blue_sprites(sheet, force_grid=False):
    width, height = sheet.get_size()
    cols, rows = 4, 4
    kakao_reference_sheet = force_grid
    labeled_reference_sheet = (width / max(1, height) > 1.45) and not kakao_reference_sheet
    if not labeled_reference_sheet and not kakao_reference_sheet:
        sheet = crop_knight_sprite_area(sheet)
        width, height = sheet.get_size()
    frame_w = width // cols
    frame_h = height // rows
    row_keys = ["back", "front", "left", "right"]
    sprites = {}
    for row, facing in enumerate(row_keys):
        frames = []
        attacks = []
        for col in range(cols):
            if kakao_reference_sheet:
                rect = kakao_knight_reference_frame_rect(sheet, row, col)
            elif labeled_reference_sheet:
                rect = knight_reference_frame_rect(sheet, row, col)
            else:
                rect = pygame.Rect(col * frame_w, row * frame_h, frame_w, frame_h)
                if col == cols - 1:
                    rect.width = width - rect.x
                if row == rows - 1:
                    rect.height = height - rect.y
            cropped = sheet.subsurface(rect.clip(sheet.get_rect())).copy()
            cleaned = make_player_sprite_frame(cropped)
            if cleaned is None:
                continue
            if col < 2:
                sprites[f"{facing}_walk_{col}"] = cleaned
                frames.append(cleaned)
            else:
                sprites[f"{facing}_attack_{col - 2}"] = cleaned
                attacks.append(cleaned)
        if frames:
            sprites[facing] = frames[0]
        if attacks:
            sprites[f"{facing}_attack"] = attacks[0]
    sprites["up"] = sprites.get("back")
    sprites["down"] = sprites.get("front")
    sprites["up_walk_0"] = sprites.get("back_walk_0")
    sprites["up_walk_1"] = sprites.get("back_walk_1")
    sprites["down_walk_0"] = sprites.get("front_walk_0")
    sprites["down_walk_1"] = sprites.get("front_walk_1")
    sprites["up_attack_0"] = sprites.get("back_attack_0")
    sprites["up_attack_1"] = sprites.get("back_attack_1")
    sprites["down_attack_0"] = sprites.get("front_attack_0")
    sprites["down_attack_1"] = sprites.get("front_attack_1")
    sprites["up_attack"] = sprites.get("back_attack")
    sprites["down_attack"] = sprites.get("front_attack")
    sprites["attack"] = sprites.get("front_attack") or sprites.get("right_attack") or sprites.get("front")
    sprites["dodge"] = sprites.get("front_walk_1") or sprites.get("front")
    sprites["skill"] = sprites.get("front_attack_1") or sprites.get("front_attack") or sprites.get("attack")
    return normalize_player_direction_sprites(sprites)

def load_zeppili_sprites(sheet):
    crop_map = { "front": (0.035, 0.145, 0.235, 0.425), "back": (0.285, 0.145, 0.470, 0.425), "left": (0.520, 0.145, 0.705, 0.425), "right": (0.760, 0.145, 0.955, 0.425), "attack": (0.030, 0.480, 0.320, 0.688), "dodge": (0.355, 0.485, 0.635, 0.692), "skill": (0.685, 0.480, 0.955, 0.705), "diagonal_front_left": (0.040, 0.760, 0.225, 0.895), "diagonal_front_right": (0.275, 0.760, 0.465, 0.895), "diagonal_back_left": (0.540, 0.760, 0.725, 0.895), "diagonal_back_right": (0.775, 0.760, 0.955, 0.895), }

    sprites = {}
    for name, ratio in crop_map.items():
        try:
            cropped = crop_by_ratio(sheet, *ratio)
            cleaned = normalize_jeffrey_frame(cropped)
            if cleaned and cleaned.get_width() > 8 and cleaned.get_height() > 8:
                sprites[name] = cleaned
        except pygame.error:
            continue
    sprites["up"] = sprites.get("back")
    sprites["down"] = sprites.get("front")
    sprites["up_left"] = sprites.get("diagonal_back_left") or sprites.get("left") or sprites.get("back")
    sprites["up_right"] = sprites.get("diagonal_back_right") or sprites.get("right") or sprites.get("back")
    sprites["down_left"] = sprites.get("diagonal_front_left") or sprites.get("left") or sprites.get("front")
    sprites["down_right"] = sprites.get("diagonal_front_right") or sprites.get("right") or sprites.get("front")
    left_attack = sprites.get("attack")
    right_attack = pygame.transform.flip(left_attack, True, False) if left_attack else None
    left_skill = sprites.get("skill")
    right_skill = pygame.transform.flip(left_skill, True, False) if left_skill else None
    for direction in ("up", "down", "left", "right", "up_left", "up_right", "down_left", "down_right"):
        uses_right = direction in ("right", "up_right", "down_right")
        attack_sprite = right_attack if uses_right else left_attack
        skill_sprite = right_skill if uses_right else left_skill
        if sprites.get(direction):
            sprites[f"{direction}_walk_0"] = sprites.get(direction)
            sprites[f"{direction}_walk_1"] = sprites.get(direction)
            sprites[f"{direction}_attack_0"] = attack_sprite or sprites.get(direction)
            sprites[f"{direction}_attack_1"] = attack_sprite or sprites.get(direction)
            sprites[f"{direction}_attack"] = attack_sprite or sprites.get(direction)
            sprites[f"{direction}_skill_0"] = skill_sprite or sprites.get(direction)
            sprites[f"{direction}_skill_1"] = skill_sprite or sprites.get(direction)
            sprites[f"{direction}_skill"] = skill_sprite or sprites.get(direction)
    return normalize_player_direction_sprites(sprites)

def load_player_sprites(character_id=None):
    character_id = character_id or STARTER_CHARACTER_ID
    anim_type = get_character_anim_type(character_id)
    if character_id in PLAYER_SPRITE_CACHE:
        return PLAYER_SPRITE_CACHE[character_id]
    path = find_asset_path(*player_sprite_candidates(character_id))
    if not path:
        return {}
    try:
        sheet = pygame.image.load(path).convert_alpha()
    except (pygame.error, OSError):
        return {}
    if anim_type == "zeppili":
        sprites = load_zeppili_sprites(sheet)
    else:
        force_grid = os.path.basename(path).lower() == "kakaotalk_20260604_153249267.png"
        sprites = load_knight_blue_sprites(sheet, force_grid=force_grid)
    PLAYER_SPRITE_CACHE[character_id] = sprites
    return sprites

def load_high_score():
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return int(data.get("highest_score", 0))
    except (OSError, ValueError, json.JSONDecodeError):
        return 0

def save_high_score(score):
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump({"highest_score": int(score)}, f, ensure_ascii=False, indent=2)
    except OSError:
        pass

def default_game_data():
    return { "highest_score": load_high_score(), "normal_tickets": 0, "premium_tickets": 0, "owned_characters": [STARTER_CHARACTER_ID, OLD_MAIN_CHARACTER_ID], "selected_character_id": STARTER_CHARACTER_ID, "character_shards": {}, "selected_pet_type": None, "first_boss_pet_reward_taken": False, }

def normalize_game_data(data):
    base = default_game_data()
    if isinstance(data, dict):
        base.update(data)

    owned = base.get("owned_characters", [])
    if not isinstance(owned, list):
        owned = []
    owned = [character_id for character_id in owned if character_id in CHARACTER_BY_ID]
    if STARTER_CHARACTER_ID not in owned:
        owned.insert(0, STARTER_CHARACTER_ID)
    if OLD_MAIN_CHARACTER_ID not in owned:
        owned.insert(1, OLD_MAIN_CHARACTER_ID)
    base["owned_characters"] = sorted(set(owned), key=owned.index)

    selected_id = base.get("selected_character_id")
    if selected_id not in base["owned_characters"]:
        selected_id = STARTER_CHARACTER_ID
    base["selected_character_id"] = selected_id

    shards = base.get("character_shards", {})
    if not isinstance(shards, dict):
        shards = {}
    base["character_shards"] = {key: int(value) for key, value in shards.items() if key in CHARACTER_BY_ID}
    base["normal_tickets"] = max(0, int(base.get("normal_tickets", 0)))
    base["premium_tickets"] = max(0, int(base.get("premium_tickets", 0)))
    base["highest_score"] = max(0, int(base.get("highest_score", 0)))
    selected_pet_type = base.get("selected_pet_type")
    if selected_pet_type not in PET_DEFS:
        selected_pet_type = None
    base["selected_pet_type"] = selected_pet_type
    base["first_boss_pet_reward_taken"] = bool(base.get("first_boss_pet_reward_taken", False)) or selected_pet_type is not None
    return base

def load_game_data():
    try:
        with open(SAVE_DATA_FILE, "r", encoding="utf-8") as f:
            return normalize_game_data(json.load(f))
    except (OSError, ValueError, json.JSONDecodeError):
        return normalize_game_data({})

def save_game_data(data):
    data = normalize_game_data(data)
    try:
        with open(SAVE_DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError:
        pass
    return data

def make_font(size, bold=False):
    candidates = ["malgungothic", "맑은 고딕", "gulim", "arialunicode"]
    font_name = None
    for candidate in candidates:
        font_name = pygame.font.match_font(candidate)
        if font_name:
            break
    return pygame.font.Font(font_name, size) if font_name else pygame.font.SysFont(None, size, bold=bold)

def draw_text(surface, font, text, x, y, color=WHITE, center=False):
    rendered = font.render(str(text), True, color)
    rect = rendered.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(rendered, rect)
    return rect

def draw_bar(surface, x, y, w, h, value, maximum, color, back=(45, 48, 54)):
    value = clamp(value, 0, maximum)
    pygame.draw.rect(surface, back, (x, y, w, h), border_radius=4)
    if maximum > 0:
        pygame.draw.rect(surface, color, (x, y, int(w * value / maximum), h), border_radius=4)
    pygame.draw.rect(surface, (190, 200, 205), (x, y, w, h), 1, border_radius=4)

def draw_hud_backdrop(surface, height):
    panel = pygame.Surface((WIDTH, height), pygame.SRCALPHA)
    panel_rect = pygame.Rect(8, 6, WIDTH - 16, height - 12)
    pygame.draw.rect(panel, (3, 8, 14, 72), panel_rect, border_radius=12)
    pygame.draw.rect(panel, (175, 220, 245, 58), panel_rect, 1, border_radius=12)
    pygame.draw.line(panel, (105, 205, 235, 28), (22, height - 7), (WIDTH - 22, height - 7), 1)
    surface.blit(panel, (0, 0))

def draw_hud_bar(surface, x, y, w, h, value, maximum, color, ready=False):
    value = clamp(value, 0, maximum)
    bar = pygame.Surface((w, h), pygame.SRCALPHA)
    radius = max(2, h // 2)
    pygame.draw.rect(bar, (4, 9, 15, 94), (0, 0, w, h), border_radius=radius)
    if maximum > 0:
        fill_w = int(w * value / maximum)
        if fill_w > 0:
            fill_color = tuple(color[:3]) + ((245 if ready else 218),)
            pygame.draw.rect(bar, fill_color, (0, 0, fill_w, h), border_radius=radius)
            if h >= 6:
                pygame.draw.line(bar, (255, 255, 255, 72), (radius, 2), (max(radius, fill_w - radius), 2), 1)
    border_alpha = 125 if ready else 68
    pygame.draw.rect(bar, (190, 225, 245, border_alpha), (0, 0, w, h), 1, border_radius=radius)
    surface.blit(bar, (x, y))

def depth_t(y):
    return clamp((FLOOR_BOTTOM_Y - y) / max(1, FLOOR_BOTTOM_Y - FLOOR_TOP_Y), 0.0, 1.0)

def depth_scale(y):
    return lerp(1.06, 0.92, depth_t(y))

def tint_color(color, factor=0.82):
    return tuple(clamp(int(channel * factor), 0, 255) for channel in color)

def draw_ellipse_shadow(surface, pos, radius, alpha=105, width_scale=2.15, height_scale=0.48):
    scale = depth_scale(pos.y)
    w = int(radius * width_scale * scale)
    h = max(8, int(radius * height_scale * scale))
    alpha = int(alpha * (1.05 - depth_t(pos.y) * 0.25))
    temp = pygame.Surface((w + 8, h + 8), pygame.SRCALPHA)
    pygame.draw.ellipse(temp, (0, 0, 0, alpha), (4, 4, w, h))
    surface.blit(temp, (pos.x - w / 2 - 4, pos.y + radius * 0.66 - h / 2 - 4))

class Camera:
    def __init__(self):
        self.pos = pygame.Vector2(0, 0)
        self.shake_timer = 0
        self.shake_strength = 0

    def update(self, target_pos, world_width, world_height, dt, room=None):
        if room and getattr(room, "bg_key", "") == "ice_dragon_stage":
            focus = pygame.Vector2(target_pos)
            if getattr(room, "boss", None) and not room.boss.dead:
                focus = focus.lerp(room.boss.visual_pos, 0.38)
            target_x = clamp(focus.x - WIDTH * 0.5, 0, max(0, world_width - WIDTH))
            target_y = clamp(focus.y - HEIGHT * 0.58, 0, max(0, world_height - HEIGHT))
            self.pos.x += (target_x - self.pos.x) * min(1.0, dt * 5.0)
            self.pos.y += (target_y - self.pos.y) * min(1.0, dt * 2.6)
            return
        if room and getattr(room, "bg_key", "") == "boss_stage_15":
            focus = pygame.Vector2(target_pos)
            if getattr(room, "boss", None) and not room.boss.dead:
                depth = clamp((room.floor_bottom_y - focus.y) / max(1, room.floor_bottom_y - room.floor_top_y), 0.0, 1.0)
                head_focus = room.boss.get_floor15_head_focus_pos() if hasattr(room.boss, "get_floor15_head_focus_pos") else room.boss.visual_pos
                focus = focus.lerp(head_focus, depth * 0.35)
            target_x = clamp(focus.x - WIDTH * 0.5, 0, max(0, world_width - WIDTH))
            target_y = clamp(focus.y - HEIGHT * 0.60, 0, max(0, world_height - HEIGHT))
            if getattr(room, "boss", None):
                boss_keep_y = clamp(room.boss.visual_pos.y - HEIGHT * 0.70, 0, max(0, world_height - HEIGHT))
                target_y = min(target_y, boss_keep_y)
            self.pos.x += (target_x - self.pos.x) * min(1.0, dt * 4.5)
            self.pos.y += (target_y - self.pos.y) * min(1.0, dt * 2.2)
            return
        focus = pygame.Vector2(target_pos)
        if room and hasattr(room, "floor_top_y"):
            depth = clamp((room.floor_bottom_y - focus.y) / max(1, room.floor_bottom_y - room.floor_top_y), 0.0, 1.0)
            vanish_x = room.world_width * 0.5
            focus.x = lerp(focus.x, vanish_x, depth * 0.34)
            focus.y -= depth * 70
        target_x = focus.x - WIDTH * 0.5
        target_y = focus.y - HEIGHT * 0.58
        target_x = clamp(target_x, 0, max(0, world_width - WIDTH))
        target_y = clamp(target_y, 0, max(0, world_height - HEIGHT))
        follow_x = min(1.0, dt * 9.0)
        follow_y = min(1.0, dt * 2.2)
        self.pos.x += (target_x - self.pos.x) * follow_x
        self.pos.y += (target_y - self.pos.y) * follow_y

    def reset(self, target_pos, world_width, world_height, room=None):
        if room and getattr(room, "bg_key", "") == "ice_dragon_stage":
            focus = pygame.Vector2(target_pos)
            if getattr(room, "boss", None) and not room.boss.dead:
                focus = focus.lerp(room.boss.visual_pos, 0.38)
            target_x = clamp(focus.x - WIDTH * 0.5, 0, max(0, world_width - WIDTH))
            target_y = clamp(focus.y - HEIGHT * 0.58, 0, max(0, world_height - HEIGHT))
            self.pos.update(target_x, target_y)
            self.shake_timer = 0
            self.shake_strength = 0
            return
        if room and getattr(room, "bg_key", "") == "boss_stage_15":
            focus = pygame.Vector2(target_pos)
            if getattr(room, "boss", None) and not room.boss.dead:
                depth = clamp((room.floor_bottom_y - focus.y) / max(1, room.floor_bottom_y - room.floor_top_y), 0.0, 1.0)
                head_focus = room.boss.get_floor15_head_focus_pos() if hasattr(room.boss, "get_floor15_head_focus_pos") else room.boss.visual_pos
                focus = focus.lerp(head_focus, depth * 0.35)
            target_x = clamp(focus.x - WIDTH * 0.5, 0, max(0, world_width - WIDTH))
            target_y = clamp(focus.y - HEIGHT * 0.60, 0, max(0, world_height - HEIGHT))
            if getattr(room, "boss", None):
                boss_keep_y = clamp(room.boss.visual_pos.y - HEIGHT * 0.70, 0, max(0, world_height - HEIGHT))
                target_y = min(target_y, boss_keep_y)
            self.pos.update(target_x, target_y)
            self.shake_timer = 0
            self.shake_strength = 0
            return
        focus = pygame.Vector2(target_pos)
        if room and hasattr(room, "floor_top_y"):
            depth = clamp((room.floor_bottom_y - focus.y) / max(1, room.floor_bottom_y - room.floor_top_y), 0.0, 1.0)
            focus.x = lerp(focus.x, room.world_width * 0.5, depth * 0.34)
            focus.y -= depth * 70
        self.pos.x = clamp(focus.x - WIDTH * 0.5, 0, max(0, world_width - WIDTH))
        self.pos.y = clamp(focus.y - HEIGHT * 0.58, 0, max(0, world_height - HEIGHT))

    def shake(self, strength=8, duration=0.18):
        self.shake_strength = max(self.shake_strength, strength)
        self.shake_timer = max(self.shake_timer, duration)

    def offset(self, dt=0):
        if self.shake_timer <= 0:
            return pygame.Vector2(self.pos)
        self.shake_timer = max(0, self.shake_timer - dt)
        amount = self.shake_strength * 0.35 * (self.shake_timer / max(0.01, self.shake_timer + dt))
        return self.pos + pygame.Vector2(random.uniform(-amount, amount), 0)

class SoundBank:
    def __init__(self):
        self.enabled = False
        self.sounds = {}
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=256)
            self.enabled = True
            self.sounds["hit"] = self.load_sound("attack.mp3") or self.make_tone(440, 0.05, 0.25)
            self.sounds["skill"] = self.load_sound("skill.mp3") or self.make_tone(660, 0.04, 0.18)
            self.sounds["shoot"] = self.make_tone(660, 0.04, 0.18)
            self.sounds["hurt"] = self.make_tone(180, 0.08, 0.22)
            self.sounds["clear"] = self.make_tone(880, 0.12, 0.20)
            self.sounds["ultimate"] = self.load_sound("ultimate.mp3") or self.make_tone(980, 0.18, 0.28)
        except pygame.error:
            self.enabled = False

    def make_tone(self, frequency, duration, volume):
        sample_rate = 22050
        samples = int(sample_rate * duration)
        buf = array("h")
        for i in range(samples):
            wave = math.sin(2 * math.pi * frequency * i / sample_rate)
            buf.append(int(32767 * volume * wave))
        return pygame.mixer.Sound(buffer=buf)

    def play(self, name):
        if self.enabled and name in self.sounds:
            self.sounds[name].play()

    def load_sound(self, filename):
        path = find_asset_path(os.path.join("assets", filename), filename)
        if not path:
            return None
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(0.55)
            return sound
        except pygame.error:
            return None

class Projectile:
    def __init__(self, x, y, vx, vy, radius, damage, owner, color, life=3.0):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(vx, vy)
        self.radius = radius
        self.damage = damage
        self.owner = owner
        self.color = color
        self.life = life
        self.dead = False

    def update(self, dt, world_width=WIDTH, world_height=HEIGHT):
        self.pos += self.vel * dt
        self.life -= dt
        if self.life <= 0:
            self.dead = True
        if self.pos.x < -120 or self.pos.x > world_width + 120 or self.pos.y < -120 or self.pos.y > world_height + 120:
            self.dead = True

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.radius)
        pygame.draw.circle(surface, WHITE, self.pos, max(2, self.radius // 2))

class Effect:
    def __init__(self, x, y, radius, color, life=0.25, kind="ring"):
        self.pos = pygame.Vector2(x, y)
        self.radius = radius
        self.color = color
        self.life = life
        self.max_life = life
        self.kind = kind

    @property
    def dead(self):
        return self.life <= 0

    def update(self, dt):
        self.life -= dt

    def draw(self, surface):
        alpha = clamp(int(255 * self.life / self.max_life), 0, 255)
        temp = pygame.Surface((self.radius * 2 + 8, self.radius * 2 + 8), pygame.SRCALPHA)
        color = (*self.color, alpha)
        center = (self.radius + 4, self.radius + 4)
        if self.kind == "slash":
            pygame.draw.arc(temp, color, (4, 4, self.radius * 2, self.radius * 2), 0.2, 2.7, 8)
        else:
            pygame.draw.circle(temp, color, center, self.radius, 4)
        surface.blit(temp, (self.pos.x - self.radius - 4, self.pos.y - self.radius - 4))

class SpriteEffect:
    def __init__(self, frames, pos, duration=0.28, flip_x=False, angle=0, alpha=230, offset=None):
        self.frames = frames or []
        self.pos = pygame.Vector2(pos)
        self.duration = max(0.01, duration)
        self.life = self.duration
        self.flip_x = flip_x
        self.angle = angle
        self.alpha = alpha
        self.offset = pygame.Vector2(offset) if offset else pygame.Vector2(0, 0)
        self.cache = {}

    @property
    def dead(self):
        return self.life <= 0 or not self.frames

    def update(self, dt):
        self.life -= dt

    def draw(self, surface):
        if not self.frames:
            return
        progress = clamp(1.0 - self.life / self.duration, 0.0, 0.999)
        frame_index = min(len(self.frames) - 1, int(progress * len(self.frames)))
        frame = self.frames[frame_index]
        cache_key = (frame_index, self.flip_x, int(self.angle), int(self.alpha))
        image = self.cache.get(cache_key)
        if image is None:
            image = frame
            if self.flip_x:
                image = pygame.transform.flip(image, True, False)
            if abs(self.angle) > 0.1:
                image = pygame.transform.rotozoom(image, self.angle, 1.0)
            if self.alpha < 255:
                image = image.copy()
                image.set_alpha(self.alpha)
            self.cache[cache_key] = image
        pos = self.pos + self.offset
        rect = image.get_rect(center=(int(pos.x), int(pos.y)))
        surface.blit(image, rect)

class DashParticle:
    def __init__(self, x, y, vx, vy, radius, color, life=0.28):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(vx, vy)
        self.radius = radius
        self.color = color
        self.life = life
        self.max_life = life

    @property
    def dead(self):
        return self.life <= 0

    def update(self, dt):
        self.life -= dt
        self.pos += self.vel * dt
        self.vel *= max(0.0, 1.0 - dt * 6.5)

    def draw(self, surface):
        alpha = clamp(int(210 * self.life / self.max_life), 0, 210)
        temp = pygame.Surface((self.radius * 2 + 4, self.radius * 2 + 4), pygame.SRCALPHA)
        pygame.draw.circle(temp, (*self.color, alpha), (self.radius + 2, self.radius + 2), self.radius)
        surface.blit(temp, (self.pos.x - self.radius - 2, self.pos.y - self.radius - 2))

class EnvironmentParticle:
    def __init__(self, key):
        self.reset(key, fresh=True)

    def reset(self, key, fresh=False):
        self.key = key
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(COMBAT_TOP - 80, HEIGHT) if fresh else random.uniform(COMBAT_TOP - 60, COMBAT_BOTTOM + 35)
        self.life = random.uniform(4.0, 9.0)
        self.max_life = self.life
        self.size = random.uniform(1.2, 4.4)
        if key == "15_11":
            self.color = (175, 220, 55)
            self.vx = random.uniform(-8, 10)
            self.vy = random.uniform(-18, -5)
        elif key == "10_6":
            self.color = (95, 145, 255)
            self.vx = random.uniform(-20, 22)
            self.vy = random.uniform(-12, 10)
            self.life = random.uniform(0.45, 1.2)
            self.max_life = self.life
            self.size = random.uniform(1.0, 2.6)
        elif key == "5_1":
            self.color = (225, 75, 68)
            self.vx = random.uniform(-12, 12)
            self.vy = random.uniform(-16, -4)
        else:
            self.color = (95, 220, 210)
            self.vx = random.uniform(-8, 8)
            self.vy = random.uniform(-10, -2)

    def update(self, dt, key):
        if key != self.key:
            self.reset(key, fresh=True)
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt
        if self.life <= 0 or self.x < -30 or self.x > WIDTH + 30 or self.y < COMBAT_TOP - 120:
            self.reset(key)

    def draw(self, surface, front=False):
        if front != (self.y > COMBAT_BOTTOM - 75):
            return
        alpha = clamp(int(58 * self.life / self.max_life), 0, 58)
        if self.key == "10_6":
            alpha = clamp(alpha + 40, 0, 120)
        temp = pygame.Surface((int(self.size * 8), int(self.size * 8)), pygame.SRCALPHA)
        center = (temp.get_width() // 2, temp.get_height() // 2)
        pygame.draw.circle(temp, (*self.color, alpha), center, max(1, int(self.size)))
        if self.key == "10_6":
            pygame.draw.line(temp, (*self.color, alpha), (center[0] - 5, center[1]), (center[0] + 5, center[1]), 1)
        surface.blit(temp, (self.x - center[0], self.y - center[1]))

class BossWarning:
    def __init__(self, shape, pos, size, warning_time, active_time, damage, color, kind="hit", angle=0):
        self.shape = shape
        self.pos = pygame.Vector2(pos)
        self.size = size
        self.warning_time = warning_time
        self.active_time = active_time
        self.max_warning_time = warning_time
        self.max_active_time = active_time
        self.damage = damage
        self.color = color
        self.kind = kind
        self.angle = angle
        self.done = False
        self.triggered = False

    @property
    def active(self):
        return self.warning_time <= 0 and self.active_time > 0

    def update(self, dt, player):
        if self.done:
            return None
        if self.warning_time > 0:
            self.warning_time -= dt
            if self.warning_time <= 0:
                self.triggered = True
            return None

        self.active_time -= dt
        result = None
        if self.damage > 0 and self.hits_player(player):
            result = player.take_damage(self.damage)
        if self.active_time <= 0:
            self.done = True
        return result

    def hits_player(self, player):
        if self.shape == "circle":
            return distance(self.pos, player.pos) <= self.size + player.radius
        if self.shape == "ellipse":
            rx, ry = self.size
            if rx <= 0 or ry <= 0:
                return False
            dx = (player.pos.x - self.pos.x) / rx
            dy = (player.pos.y - self.pos.y) / ry
            return dx * dx + dy * dy <= 1.0
        if self.shape == "laser":
            length, width = self.size
            direction = pygame.Vector2(1, 0).rotate(self.angle)
            rel = player.pos - self.pos
            along = rel.dot(direction)
            if along < 0 or along > length:
                return False
            closest = self.pos + direction * along
            return distance(closest, player.pos) <= width + player.radius
        return False

    def draw(self, surface):
        temp = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        image_drawn = draw_boss_skill_warning_image(temp, self)
        if self.warning_time > 0:
            pulse = 0.45 + 0.55 * abs(math.sin(pygame.time.get_ticks() * 0.012))
            alpha = int(58 + pulse * 70)
            color = (*self.color, alpha if not image_drawn else 42)
            width = 3
        else:
            color = (*self.color, 118 if not image_drawn else 16)
            width = 0

        if self.shape == "circle":
            pygame.draw.circle(temp, color, self.pos, int(self.size), width)
            if self.warning_time > 0:
                pygame.draw.circle(temp, (*self.color, 34), self.pos, int(self.size * 0.65), 1)
        elif self.shape == "ellipse":
            rx, ry = self.size
            rect = pygame.Rect(0, 0, int(rx * 2), int(ry * 2))
            rect.center = self.pos
            pygame.draw.ellipse(temp, color, rect, width)
        elif self.shape == "laser":
            length, laser_width = self.size
            direction = pygame.Vector2(1, 0).rotate(self.angle)
            end = self.pos + direction * length
            pygame.draw.line(temp, color, self.pos, end, int(laser_width * (2.3 if self.active else 1.0)))
        surface.blit(temp, (0, 0))

class Trap:
    def __init__(self, trap_type, rect, damage=12, cycle=1.8, offset=0.0, friendly=False, life=None, shape="rect"):
        self.trap_type = trap_type
        self.rect = pygame.Rect(rect)
        self.damage = damage
        self.cycle = cycle
        self.timer = offset
        self.active = False
        self.warning = False
        self.friendly = friendly
        self.life = life
        self.shape = shape

    def update(self, dt):
        if self.life is not None:
            self.life -= dt
        if self.friendly:
            self.active = True
            self.warning = False
            return
        self.timer = (self.timer + dt) % self.cycle
        phase = self.timer / max(0.01, self.cycle)
        self.warning = 0.36 <= phase < 0.76
        self.active = phase >= 0.76

    @property
    def dead(self):
        return self.life is not None and self.life <= 0

    def hits_player(self, player):
        if self.friendly or not self.active:
            return False
        return self.rect.colliderect(player.rect)

    def hits_enemy(self, enemy):
        if not self.friendly or not self.active:
            return False
        return self.rect.collidepoint(enemy.pos.x, enemy.pos.y)

    def draw(self, surface):
        temp = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        original_rect = self.rect
        if not self.friendly:
            scale = depth_scale(self.rect.centery)
            if abs(scale - 1.0) > 0.01:
                scaled = pygame.Rect(0, 0, max(8, int(self.rect.width * scale)), max(8, int(self.rect.height * scale)))
                scaled.center = self.rect.center
                self.rect = scaled
        if self.friendly:
            color = (85, 230, 105)
        elif "독" in self.trap_type:
            color = (145, 190, 35) if self.active else (90, 120, 35)
        elif "전" in self.trap_type:
            color = (90, 160, 255) if self.active else (45, 85, 150)
        else:
            color = (245, 70, 65) if self.active else (120, 45, 45)

        if self.warning and not self.active:
            pulse = 0.55 + 0.45 * abs(math.sin(pygame.time.get_ticks() * 0.014))
            warn_color = (255, 215, 85, int(70 + 90 * pulse))
            pygame.draw.rect(temp, warn_color, self.rect, border_radius=3)
            pygame.draw.rect(temp, (255, 235, 120, 210), self.rect, 3, border_radius=3)
            self.draw_platform_pattern(temp, (255, 245, 165, int(90 + 60 * pulse)), warning=True)
        if self.active:
            pygame.draw.rect(temp, (*color, 150), self.rect, border_radius=4)
            pygame.draw.rect(temp, (*WHITE, 170), self.rect, 2, border_radius=4)
            self.draw_platform_pattern(temp, (*WHITE, 120), warning=False)
        else:
            pygame.draw.rect(temp, (*color, 45), self.rect, border_radius=3)
            pygame.draw.rect(temp, (*color, 105), self.rect, 1, border_radius=3)
        self.rect = original_rect
        surface.blit(temp, (0, 0))

    def draw_platform_pattern(self, surface, color, warning=False):
        if self.shape == "tile":
            tile = 34
            for x in range(self.rect.left, self.rect.right, tile):
                pygame.draw.line(surface, color, (x, self.rect.top), (x, self.rect.bottom), 1)
            for y in range(self.rect.top, self.rect.bottom, tile):
                pygame.draw.line(surface, color, (self.rect.left, y), (self.rect.right, y), 1)
        elif self.shape == "line":
            if self.rect.width >= self.rect.height:
                for y in range(self.rect.top + 5, self.rect.bottom, 12):
                    pygame.draw.line(surface, color, (self.rect.left + 8, y), (self.rect.right - 8, y), 2 if warning else 1)
            else:
                for x in range(self.rect.left + 5, self.rect.right, 12):
                    pygame.draw.line(surface, color, (x, self.rect.top + 8), (x, self.rect.bottom - 8), 2 if warning else 1)
        else:
            step = 22
            for x in range(self.rect.left - self.rect.height, self.rect.right, step):
                pygame.draw.line(surface, color, (x, self.rect.bottom), (x + self.rect.height, self.rect.top), 2 if warning else 1)

class Player:
    def __init__(self, character_id=None):
        self.pos = pygame.Vector2(WIDTH // 2, COMBAT_BOTTOM - 38)
        self.radius = 18
        self.max_hp = 100
        self.hp = self.max_hp
        self.speed = 255
        self.attack_damage = 20
        self.damage_reduce = 0.0
        self.dash_cooldown_max = 0.95
        self.dash_cooldown = 0
        self.dash_distance = 225
        self.is_dashing = False
        self.dash_timer = 0
        self.dash_duration = 0.18
        self.dash_velocity = pygame.Vector2(0, 0)
        self.dash_dir = pygame.Vector2(1, 0)
        self.dash_particle_timer = 0
        self.special_cooldown_max = 2.2
        self.special_cooldown = 0
        self.attack_cooldown = 0
        self.attack_timer = 0
        self.attack_duration = 0.22
        self.attack_direction = "right"
        self.skill_timer = 0
        self.skill_duration = 0.35
        self.skill_direction = "right"
        self.ultimate_timer = 0
        self.ultimate_duration = 0.42
        self.ultimate_direction = "right"
        self.dash_flash_timer = 0
        self.dash_invuln_timer = 0
        self.just_dodge_lock = 0
        self.just_dodge_event = False
        self.just_dodge_text_timer = 0
        self.counter_boost_timer = 0
        self.counter_boost_multiplier = 1.0
        self.ultimate = 0
        self.ultimate_gain_multiplier = 1.0
        self.invuln = 0
        self.last_dir = pygame.Vector2(1, 0)
        self.facing = "right"
        self.last_horizontal_facing = "right"
        self.is_moving = False
        self.upgrades = []
        self.special_items = []
        self.special_item_flags = {}
        self.pet_names = []
        self.pets = []
        self.selected_pet_type = None
        self.selected_pet_data = None
        self.hp_regen_rate_bonus = 0.0
        self.hp_regen_amount_bonus = 0
        self.stage_clear_heal = 0
        self.attack_range_bonus = 0
        self.attack_damage_bonus = 0
        self.attack_speed_bonus = 0.0
        self.zone_radius_bonus = 0
        self.zone_damage_bonus = 0
        self.zone_lifesteal = 0.0
        self.hp_regen_timer = 0.0
        self.pet_zone_timer = 0.0
        self.auto_shield_ready = False
        self.auto_shield_timer = 0
        self.emergency_syringe_used = False
        self.boss_mark_stacks = 0
        self.unstable_vulnerable_timer = 0
        self.frost_slow_timer = 0
        self.ice_hazard_cooldowns = {"breath": 0.0, "blizzard": 0.0}
        self.gold = 0
        self.afterimages = []
        self.dash_particles = []
        self.character_id = character_id or STARTER_CHARACTER_ID
        self.anim_type = get_character_anim_type(self.character_id)
        self.sprites = load_player_sprites(self.character_id)

    def set_character(self, character_id):
        self.character_id = character_id or STARTER_CHARACTER_ID
        self.anim_type = get_character_anim_type(self.character_id)
        self.sprites = load_player_sprites(self.character_id)

    @property
    def rect(self):
        return pygame.Rect(self.pos.x - self.radius, self.pos.y - self.radius, self.radius * 2, self.radius * 2)

    def can_occupy(self, pos, arena_rect=None, walkable_polygon=None):
        pos = pygame.Vector2(pos)
        if walkable_polygon:
            return is_circle_inside_polygon(pos, self.radius, walkable_polygon)
        if arena_rect:
            return ( arena_rect.left + self.radius <= pos.x <= arena_rect.right - self.radius and arena_rect.top + self.radius <= pos.y <= arena_rect.bottom - self.radius )
        return 40 <= pos.x <= WIDTH - 40 and COMBAT_TOP <= pos.y <= COMBAT_BOTTOM

    def try_axis_move(self, dx, dy, arena_rect=None, walkable_polygon=None):
        blocked = False
        if abs(dx) > 0.001:
            next_pos = pygame.Vector2(self.pos.x + dx, self.pos.y)
            if self.can_occupy(next_pos, arena_rect, walkable_polygon):
                self.pos = next_pos
            else:
                blocked = True
        if abs(dy) > 0.001:
            next_pos = pygame.Vector2(self.pos.x, self.pos.y + dy)
            if self.can_occupy(next_pos, arena_rect, walkable_polygon):
                self.pos = next_pos
            else:
                blocked = True
        return blocked

    def update(self, dt, keys, arena_rect=None, walkable_polygon=None):
        move = pygame.Vector2(0, 0)
        if not self.can_occupy(self.pos, arena_rect, walkable_polygon):
            if walkable_polygon:
                self.pos = clamp_point_to_polygon(self.pos, walkable_polygon, self.radius)
            elif arena_rect:
                self.pos.x = clamp(self.pos.x, arena_rect.left + self.radius, arena_rect.right - self.radius)
                self.pos.y = clamp(self.pos.y, arena_rect.top + self.radius, arena_rect.bottom - self.radius)
            else:
                self.pos.x = clamp(self.pos.x, 40, WIDTH - 40)
                self.pos.y = clamp(self.pos.y, COMBAT_TOP, COMBAT_BOTTOM)
        if self.is_dashing:
            self.is_moving = True
            dash_delta = self.dash_velocity * dt
            steps = max(1, int(dash_delta.length() / 8))
            step = dash_delta / steps
            for _ in range(steps):
                next_pos = self.pos + step
                if self.can_occupy(next_pos, arena_rect, walkable_polygon):
                    self.pos = next_pos
                else:
                    self.is_dashing = False
                    self.dash_timer = 0
                    break
            self.dash_timer = max(0, self.dash_timer - dt)
            self.dash_particle_timer -= dt
            if self.dash_particle_timer <= 0:
                self.dash_particle_timer = 0.025
                self.afterimages.append({"pos": pygame.Vector2(self.pos), "life": 0.16, "radius": self.radius})
            if self.dash_timer <= 0:
                self.is_dashing = False
        else:
            if keys[pygame.K_a]:
                move.x -= 1
            if keys[pygame.K_d]:
                move.x += 1
            if keys[pygame.K_w]:
                move.y -= 1
            if keys[pygame.K_s]:
                move.y += 1
            self.is_moving = move.length_squared() > 0
            if self.is_moving:
                move = move.normalize()
                self.last_dir = move
                if move.x < -0.2:
                    self.last_horizontal_facing = "left"
                elif move.x > 0.2:
                    self.last_horizontal_facing = "right"
                self.facing = self.direction_key(move)
            speed_multiplier = 0.62 if self.frost_slow_timer > 0 else 1.0
            delta = move * self.speed * speed_multiplier * dt
            self.try_axis_move(delta.x, delta.y, arena_rect, walkable_polygon)

        self.dash_cooldown = max(0, self.dash_cooldown - dt)
        self.special_cooldown = max(0, self.special_cooldown - dt)
        self.attack_cooldown = max(0, self.attack_cooldown - dt)
        self.attack_timer = max(0, self.attack_timer - dt)
        self.skill_timer = max(0, self.skill_timer - dt)
        self.ultimate_timer = max(0, self.ultimate_timer - dt)
        self.dash_flash_timer = max(0, self.dash_flash_timer - dt)
        self.dash_invuln_timer = max(0, self.dash_invuln_timer - dt)
        if self.dash_invuln_timer <= 0 and self.dash_timer <= 0:
            self.is_dashing = False
        self.just_dodge_lock = max(0, self.just_dodge_lock - dt)
        self.just_dodge_text_timer = max(0, self.just_dodge_text_timer - dt)
        self.counter_boost_timer = max(0, self.counter_boost_timer - dt)
        self.unstable_vulnerable_timer = max(0, self.unstable_vulnerable_timer - dt)
        self.frost_slow_timer = max(0, self.frost_slow_timer - dt)
        for source in self.ice_hazard_cooldowns:
            self.ice_hazard_cooldowns[source] = max(0, self.ice_hazard_cooldowns[source] - dt)
        if self.selected_pet_type == "heal":
            self.hp_regen_timer = max(0, self.hp_regen_timer - dt)
            if self.hp_regen_timer <= 0:
                self.hp_regen_timer = max(1.8, 4.8 - self.hp_regen_rate_bonus * 5.0)
                if self.hp < self.max_hp:
                    self.heal(1 + self.hp_regen_amount_bonus)
        if self.special_item_flags.get("auto_shield") and not self.auto_shield_ready:
            self.auto_shield_timer = max(0, self.auto_shield_timer - dt)
            if self.auto_shield_timer <= 0:
                self.auto_shield_ready = True
        self.invuln = max(0, self.invuln - dt)
        for image in self.afterimages:
            image["life"] -= dt
        self.afterimages = [image for image in self.afterimages if image["life"] > 0]
        for particle in self.dash_particles:
            particle.update(dt)
        self.dash_particles = [particle for particle in self.dash_particles if not particle.dead]

    def attack_value(self, multiplier=1.0):
        boost = self.counter_boost_multiplier if self.counter_boost_timer > 0 else 1.0
        return int((self.attack_damage + self.attack_damage_bonus) * multiplier * boost)

    def gain_ultimate(self, amount):
        gained = amount * self.ultimate_gain_multiplier
        self.ultimate = clamp(self.ultimate + gained, 0, 100)

    def nearest_enemy(self, enemies, boss=None):
        targets = [enemy for enemy in enemies if not enemy.dead]
        if boss and not boss.dead:
            targets.append(boss)
        if not targets:
            return None
        return min(targets, key=lambda target: distance(self.pos, target.pos))

    def melee_attack(self, enemies, boss, effects, sounds, projectiles=None, effect_sprites=None):
        if self.attack_cooldown > 0 or self.skill_timer > 0 or self.ultimate_timer > 0:
            return
        self.attack_cooldown = max(0.18, 0.36 * (1.0 - self.attack_speed_bonus))
        self.attack_duration = 0.22
        self.attack_timer = self.attack_duration
        self.attack_direction = self.facing_key()
        sounds.play("hit")
        attack_range = 78 + self.attack_range_bonus
        attack_center = self.pos + self.last_dir * (44 + self.attack_range_bonus * 0.35)
        targets = list(enemies)
        if boss:
            targets.append(boss)
        for target in targets:
            if boss and target is boss and getattr(target, "floor", None) == ICE_DRAGON_FLOOR:
                melee_zone = target.get_floor15_melee_zone() if hasattr(target, "get_floor15_melee_zone") else None
                if melee_zone and circle_intersects_rect(attack_center, attack_range, melee_zone):
                    target.take_damage(self.attack_value())
                    self.gain_ultimate(8)
                    self.on_boss_hit(boss, effects)
                continue
            if distance(attack_center, target.pos) <= attack_range + target.radius:
                target.take_damage(self.attack_value())
                self.gain_ultimate(8)
                if boss and target is boss:
                    self.on_boss_hit(boss, effects)

        if self.special_item_flags.get("ghost_blade") and projectiles is not None and random.random() < 0.33:
            target = self.nearest_enemy(enemies, boss)
            if target:
                direction = target.pos - self.pos
                if direction.length_squared() > 0:
                    direction = direction.normalize()
                    projectiles.append(Projectile(self.pos.x, self.pos.y, direction.x * 540, direction.y * 540, 9, self.attack_value(1.15), "player", (190, 85, 255), 1.6))
                    effects.append(Effect(self.pos.x, self.pos.y, 36, (190, 85, 255), 0.18, "slash"))

    def dash(self, effects, sounds, traps=None, arena_rect=None, walkable_polygon=None):
        if self.dash_cooldown > 0:
            return
        self.dash_cooldown = self.dash_cooldown_max
        self.invuln = max(self.invuln, 0.30)
        self.dash_invuln_timer = 0.30
        self.dash_flash_timer = 0.20
        start = pygame.Vector2(self.pos)
        dash_dir = pygame.Vector2(self.last_dir)
        if dash_dir.length_squared() <= 0:
            dash_dir = pygame.Vector2(1, 0)
        dash_dir = dash_dir.normalize()
        self.dash_dir = dash_dir
        self.is_dashing = True
        self.dash_timer = self.dash_duration
        self.dash_velocity = dash_dir * (self.dash_distance / self.dash_duration)
        self.dash_particle_timer = 0
        end = start + dash_dir * self.dash_distance

        for step in range(1, 6):
            t = step / 6
            trail_pos = start.lerp(end, t)
            self.afterimages.append({"pos": trail_pos, "life": 0.24 - step * 0.018, "radius": self.radius})

        side = pygame.Vector2(-dash_dir.y, dash_dir.x)
        for _ in range(22):
            spread = side * random.uniform(-145, 145)
            backward = -dash_dir * random.uniform(150, 360)
            velocity = backward + spread
            spawn = start.lerp(end, random.random())
            self.dash_particles.append( DashParticle( spawn.x, spawn.y, velocity.x, velocity.y, random.randint(3, 7), random.choice([CYAN, BLUE, WHITE]), random.uniform(0.18, 0.34), ) )

        effects.append(Effect(start.x, start.y, 42, BLUE, 0.18))
        effects.append(Effect(self.pos.x, self.pos.y, 62, CYAN, 0.26))
        if self.special_item_flags.get("toxic_dash") and traps is not None:
            effects.append(Effect(self.pos.x, self.pos.y, 52, GREEN, 0.35))
        sounds.play("shoot")

    def special(self, projectiles, effects, sounds, enemies=None, boss=None, effect_sprites=None):
        if self.special_cooldown > 0 or self.attack_timer > 0 or self.ultimate_timer > 0:
            return
        self.special_cooldown = self.special_cooldown_max
        self.skill_duration = 0.35
        self.skill_timer = self.skill_duration
        self.skill_direction = self.facing_key()
        vel = self.last_dir * 650
        projectiles.append(Projectile(self.pos.x, self.pos.y, vel.x, vel.y, 13, self.attack_value(2), "player", PURPLE, 1.5))
        if self.special_item_flags.get("electric_overload") and enemies is not None:
            chain_targets = sorted([enemy for enemy in enemies if not enemy.dead], key=lambda enemy: distance(self.pos, enemy.pos))[:4]
            for enemy in chain_targets:
                if distance(self.pos, enemy.pos) <= 260:
                    enemy.take_damage(self.attack_value(0.9))
                    effects.append(Effect(enemy.pos.x, enemy.pos.y, 30, BLUE, 0.24))
            if boss and distance(self.pos, boss.pos) <= 300:
                boss.take_damage(self.attack_value(0.6))
                self.on_boss_hit(boss, effects)
        sounds.play("skill")

    def ultimate_attack(self, enemies, boss, effects, sounds, effect_sprites=None, enemy_damage_scale=1.0):
        if self.ultimate < 100 or self.attack_timer > 0 or self.skill_timer > 0:
            return
        self.ultimate = 0
        self.ultimate_duration = 0.42
        self.ultimate_timer = self.ultimate_duration
        self.ultimate_direction = self.facing_key()
        ultimate_multiplier = 1.28 if self.special_item_flags.get("unstable_core") else 1.0
        for enemy in enemies:
            enemy.take_damage(self.attack_value(4 * ultimate_multiplier * enemy_damage_scale))
        if boss:
            boss.take_damage(self.attack_value(5 * ultimate_multiplier))
            self.on_boss_hit(boss, effects)
        if self.special_item_flags.get("unstable_core"):
            self.invuln = 0
            self.unstable_vulnerable_timer = 2.0
        sounds.play("ultimate")

    def take_damage(self, amount):
        if self.is_dashing or self.dash_invuln_timer > 0:
            if self.just_dodge_lock <= 0:
                self.trigger_just_dodge()
            return "dodged"
        if self.invuln > 0:
            if self.dash_invuln_timer > 0 and self.just_dodge_lock <= 0:
                self.trigger_just_dodge()
                return "dodged"
            return "blocked"
        if self.auto_shield_ready:
            self.auto_shield_ready = False
            self.auto_shield_timer = 12.0
            self.invuln = 0.25
            return "shield"
        vulnerability = 1.25 if self.unstable_vulnerable_timer > 0 else 1.0
        final = max(1, int(amount * vulnerability * (1.0 - self.damage_reduce)))
        self.hp -= final
        self.invuln = 0.55
        if self.special_item_flags.get("emergency_syringe") and not self.emergency_syringe_used and self.hp <= 30:
            self.heal(25)
            self.emergency_syringe_used = True
        return "hit"

    def take_ice_hazard_damage(self, amount, source):
        if self.is_dashing or self.dash_invuln_timer > 0:
            if self.just_dodge_lock <= 0:
                self.trigger_just_dodge()
            return "dodged"
        if self.invuln > 0:
            return "blocked"
        if self.ice_hazard_cooldowns.get(source, 0) > 0:
            return "blocked"
        if self.auto_shield_ready:
            self.auto_shield_ready = False
            self.auto_shield_timer = 12.0
            self.invuln = 0.25
            return "shield"
        vulnerability = 1.25 if self.unstable_vulnerable_timer > 0 else 1.0
        final = max(1, int(amount * vulnerability * (1.0 - self.damage_reduce)))
        self.hp -= final
        self.ice_hazard_cooldowns[source] = 0.48 if source == "blizzard" else 0.42
        if self.special_item_flags.get("emergency_syringe") and not self.emergency_syringe_used and self.hp <= 30:
            self.heal(25)
            self.emergency_syringe_used = True
        return "hit"

    def trigger_just_dodge(self):
        self.just_dodge_lock = 0.22
        self.just_dodge_event = True
        self.just_dodge_text_timer = 0.75
        self.counter_boost_timer = 4.0 if self.special_item_flags.get("time_core") else 2.8
        self.counter_boost_multiplier = 1.95 if self.special_item_flags.get("time_core") else 1.65
        self.gain_ultimate(36 if self.special_item_flags.get("time_core") else 28)
        for angle in range(0, 360, 24):
            direction = pygame.Vector2(1, 0).rotate(angle)
            self.dash_particles.append( DashParticle( self.pos.x, self.pos.y, direction.x * random.uniform(180, 360), direction.y * random.uniform(180, 360), random.randint(3, 6), random.choice([CYAN, YELLOW, WHITE]), random.uniform(0.18, 0.32), ) )

    def on_boss_hit(self, boss, effects):
        if not self.special_item_flags.get("reaper_mark") or boss.dead:
            return
        self.boss_mark_stacks += 1
        effects.append(Effect(boss.pos.x, boss.pos.y, 34 + self.boss_mark_stacks * 5, PURPLE, 0.22))
        if self.boss_mark_stacks >= 5:
            self.boss_mark_stacks = 0
            boss.take_damage(self.attack_value(2.2))
            effects.append(Effect(boss.pos.x, boss.pos.y, 115, (210, 80, 255), 0.45))

    def heal(self, amount):
        self.hp = clamp(self.hp + amount, 0, self.max_hp)

    def update_pets(self, dt, room):
        for index, pet in enumerate(self.pets):
            pet.update(dt, self, room, index, len(self.pets))

    def direction_key(self, direction):
        if direction.x < -0.2 and direction.y > 0.2:
            return "down_left"
        if direction.x > 0.2 and direction.y > 0.2:
            return "down_right"
        if direction.x < -0.2 and direction.y < -0.2:
            return "up_left"
        if direction.x > 0.2 and direction.y < -0.2:
            return "up_right"
        if abs(direction.x) > abs(direction.y):
            return "left" if direction.x < 0 else "right"
        return "up" if direction.y < 0 else "down"

    def facing_key(self):
        return self.facing

    def sprite_for_key(self, key):
        walk_key = key
        if not self.is_zeppili_anim() and key in ("up_left", "down_left"):
            walk_key = "left"
        elif not self.is_zeppili_anim() and key in ("up_right", "down_right"):
            walk_key = "right"
        if self.is_moving:
            frame = int(pygame.time.get_ticks() * 0.010) % 2
            sprite = self.sprites.get(f"{walk_key}_walk_{frame}")
            if sprite:
                return sprite
        fallback_keys = { "up_left": ("up_left", "diagonal_back_left", "left", "up", "back"), "up_right": ("up_right", "diagonal_back_right", "right", "up", "back"), "down_left": ("down_left", "diagonal_front_left", "left", "down", "front"), "down_right": ("down_right", "diagonal_front_right", "right", "down", "front"), "diagonal_front_left": ("diagonal_front_left", "left", "front"), "diagonal_front_right": ("diagonal_front_right", "right", "front"), "diagonal_back_left": ("diagonal_back_left", "left", "back"), "diagonal_back_right": ("diagonal_back_right", "right", "back"), "up": ("up", "back", "front"), "down": ("down", "front"), "left": ("left", "front"), "right": ("right", "front"), "back": ("back", "front"), "front": ("front",), }
        for candidate in fallback_keys.get(key, (key, "front")):
            sprite = self.sprites.get(candidate)
            if sprite:
                return sprite
        return next(iter(self.sprites.values()), None)

    def normalize_sprite_direction(self, facing):
        if facing in ("up_left", "down_left"):
            facing = "left"
        elif facing in ("up_right", "down_right"):
            facing = "right"
        elif facing == "up":
            facing = "up" if self.sprites.get("up") else "back"
        elif facing == "down":
            facing = "down" if self.sprites.get("down") else "front"
        elif facing.startswith("diagonal_front"):
            facing = "left" if facing.endswith("left") else "right"
        elif facing.startswith("diagonal_back"):
            facing = "left" if facing.endswith("left") else "right"
        return facing

    def is_zeppili_anim(self):
        return getattr(self, "anim_type", "default") == "zeppili"

    def default_attack_direction(self, direction):
        if direction in ("right", "up_right", "down_right"):
            return "right"
        if direction in ("left", "up_left", "down_left"):
            return "left"
        if direction == "up" and (self.sprites.get("up_attack_0") or self.sprites.get("up_attack")):
            return "up"
        if direction == "down" and (self.sprites.get("down_attack_0") or self.sprites.get("down_attack")):
            return "down"
        return getattr(self, "last_horizontal_facing", "right")

    def action_sprite_for_facing(self, action, direction=None, timer=None, duration=None):
        if action == "attack":
            source_direction = direction or self.attack_direction
            facing = self.normalize_sprite_direction(source_direction)
            timer = self.attack_timer if timer is None else timer
            duration = self.attack_duration if duration is None else duration
            progress = 1.0 - clamp(timer / max(0.001, duration), 0.0, 1.0)
            frame = min(1, int(progress * 2))
            if not self.is_zeppili_anim():
                if self.character_id == STARTER_CHARACTER_ID and source_direction == "up":
                    return ( self.sprites.get("up_attack_0") or self.sprites.get("up_attack") or self.sprite_for_key("up") )
                attack_direction = self.default_attack_direction(source_direction)
                preferred_frame = 0 if attack_direction in ("left", "right") else frame
                return ( self.sprites.get(f"{attack_direction}_attack_{preferred_frame}") or self.sprites.get(f"{attack_direction}_attack") or self.sprites.get(f"{attack_direction}_attack_{frame}") or self.sprite_for_key(attack_direction) or self.sprite_for_key(facing) )
            return ( self.sprites.get(f"{source_direction}_attack_{frame}") or self.sprites.get(f"{source_direction}_attack") or self.sprites.get(f"{facing}_attack_{frame}") or self.sprites.get(f"{facing}_attack") or self.sprite_for_key(facing) )
        if action == "skill":
            source_direction = direction or self.skill_direction
            facing = self.normalize_sprite_direction(source_direction)
            timer = self.skill_timer if timer is None else timer
            duration = self.skill_duration if duration is None else duration
            progress = 1.0 - clamp(timer / max(0.001, duration), 0.0, 1.0)
            frame = min(1, int(progress * 2))
            if not self.is_zeppili_anim():
                return ( self.sprites.get(f"{source_direction}_skill_{frame}") or self.sprites.get(f"{source_direction}_skill") or self.sprites.get(f"{facing}_skill_{frame}") or self.sprites.get(f"{facing}_skill") or self.sprites.get("skill") or self.sprite_for_key(facing) )
            return ( self.sprites.get(f"{source_direction}_skill_{frame}") or self.sprites.get(f"{source_direction}_skill") or self.sprites.get(f"{facing}_skill_{frame}") or self.sprites.get(f"{facing}_skill") or self.sprites.get("skill") or self.sprite_for_key(facing) )
        if action == "ultimate":
            source_direction = direction or self.ultimate_direction
            return self.action_sprite_for_facing("skill", source_direction, timer, duration)
        return None

    def flip_for_rightward_action(self, sprite, action_key):
        return sprite

    def get_current_sprite(self):
        if not self.sprites:
            return None, "fallback"
        if self.ultimate_timer > 0:
            return self.action_sprite_for_facing("ultimate", self.ultimate_direction, self.ultimate_timer, self.ultimate_duration), "ultimate"
        if self.skill_timer > 0:
            return self.action_sprite_for_facing("skill"), "skill"
        if self.is_dashing or self.dash_flash_timer > 0:
            facing = self.normalize_sprite_direction(self.facing_key())
            sprite = self.sprites.get(f"{facing}_walk_1") or self.sprites.get("dodge") or self.sprite_for_key(facing)
            return sprite, "dodge"
        if self.attack_timer > 0:
            sprite = self.action_sprite_for_facing("attack")
            return sprite, "attack"
        return self.sprite_for_key(self.facing_key()), "normal"

    def can_use_fallback_body(self, body_state):
        return body_state in ("normal", "fallback")

    def draw_sprite_body(self, surface, sprite, scale, flash, body_state="normal"):
        if sprite is None:
            return False
        target_h = int(84 * scale)
        if body_state == "attack":
            target_h = int(92 * scale)
        elif body_state == "dodge":
            target_h = int(78 * scale)
        elif body_state == "skill":
            target_h = int(96 * scale)
        elif body_state == "ultimate":
            target_h = int(100 * scale)
        target_w = max(1, int(sprite.get_width() * target_h / max(1, sprite.get_height())))
        draw_sprite = pygame.transform.smoothscale(sprite, (target_w, target_h))
        if flash:
            flash_sprite = draw_sprite.copy()
            flash_sprite.fill((255, 255, 255, 90), special_flags=pygame.BLEND_RGBA_ADD)
            draw_sprite = flash_sprite
        bob = 0
        if body_state == "normal" and self.is_moving:
            bob = math.sin(pygame.time.get_ticks() * 0.018) * 3 * scale
        rect = draw_sprite.get_rect(midbottom=(self.pos.x, self.pos.y + self.radius * scale + 9 + bob))
        surface.blit(draw_sprite, rect)
        return True

    def draw_fallback_body(self, surface, visual_radius, scale, color):
        pygame.draw.circle(surface, (4, 12, 16), self.pos, visual_radius + 6)
        pygame.draw.circle(surface, color, self.pos, visual_radius)
        pygame.draw.circle(surface, (15, 70, 78), self.pos + self.last_dir * (8 * scale), max(4, int(6 * scale)))
        pygame.draw.circle(surface, (185, 250, 245), self.pos - pygame.Vector2(visual_radius * 0.28, visual_radius * 0.30), max(3, int(4 * scale)))
        pygame.draw.circle(surface, (0, 0, 0), self.pos, visual_radius, 2)

    def draw(self, surface):
        flash = self.invuln > 0 and int(self.invuln * 20) % 2 == 0
        scale = depth_scale(self.pos.y)
        visual_radius = max(12, int(self.radius * scale))
        color = (95, 205, 215) if not flash else WHITE
        draw_ellipse_shadow(surface, self.pos, self.radius, 120, 2.35, 0.55)
        for image in self.afterimages:
            alpha = clamp(int(150 * image["life"] / 0.24), 0, 150)
            temp = pygame.Surface((self.radius * 2 + 14, self.radius * 2 + 14), pygame.SRCALPHA)
            pygame.draw.circle(temp, (80, 220, 255, alpha), (self.radius + 7, self.radius + 7), image["radius"] + 2)
            pygame.draw.circle(temp, (255, 255, 255, alpha // 2), (self.radius + 7, self.radius + 7), max(5, image["radius"] // 2))
            surface.blit(temp, (image["pos"].x - self.radius - 7, image["pos"].y - self.radius - 7))
        for particle in self.dash_particles:
            particle.draw(surface)
        if self.dash_flash_timer > 0:
            pygame.draw.circle(surface, (155, 235, 255), self.pos, visual_radius + 18, 3)
        if self.invuln > 0:
            pygame.draw.circle(surface, (170, 230, 255), self.pos, visual_radius + 10, 2)
        body_sprite, body_state = self.get_current_sprite()
        body_drawn = self.draw_sprite_body(surface, body_sprite, scale, flash, body_state)
        if not body_drawn and self.can_use_fallback_body(body_state):
            self.draw_fallback_body(surface, visual_radius, scale, color)
        if DEBUG_PLAYER_SPRITE or DEBUG_PLAYER_ANIM:
            draw_text(surface, pygame.font.Font(None, 18), f"{self.facing_key()} {body_state}", self.pos.x, self.pos.y - 92 * scale, WHITE, center=True)
            pygame.draw.rect(surface, YELLOW, self.rect, 1)

class Enemy:
    def __init__(self, enemy_type, x, y, level=1, zone_key="20_16", floor=None):
        self.enemy_type = enemy_type
        self.pos = pygame.Vector2(x, y)
        self.zone_key = zone_key
        self.floor = floor if floor is not None else max(1, 21 - level)
        self.radius = 17
        self.dead = False
        self.shoot_cd = random.uniform(0.5, 1.8)
        self.shoot_speed = 330
        self.charge_cd = random.uniform(1.2, 2.5)
        self.charge_warning = 0
        self.level = level
        self.sprite_set = None
        self.sprite_monster_type = None
        self.sprite_hitbox = (34, 34)
        self.facing = "down"
        self.attack_direction = "down"
        self.attack_anim_timer = 0.0
        self.contact_attack_cd = random.uniform(0.0, 0.35)
        if enemy_type == "감염체":
            self.max_hp = 35 + level * 6
            self.speed = 110 + level * 4
            self.damage = 11 + level
            self.color = (80, 225, 145)
        elif enemy_type == "경비 드론":
            self.max_hp = 26 + level * 5
            self.speed = 70
            self.damage = 9 + level
            self.color = (85, 155, 245)
        elif enemy_type == "돌진 실험체":
            self.max_hp = 32 + level * 6
            self.speed = 90
            self.damage = 16 + level
            self.color = (245, 115, 75)
        else:
            self.max_hp = 70 + level * 9
            self.speed = 55
            self.damage = 20 + level
            self.radius = 22
            self.color = (185, 185, 195)
        if 18 <= self.floor <= 20:
            self.max_hp = int(self.max_hp * 0.80)
            self.damage = max(4, int(self.damage * 0.80))
            self.speed *= 0.92
            self.shoot_speed *= 0.85
            if self.enemy_type == "돌진 실험체":
                self.speed *= 0.82
                self.damage = max(5, int(self.damage * 0.75))
        self.hp = self.max_hp

    def use_ice_monster_sprite(self, monster_type):
        all_frames = load_monster_20_16_frames()
        if not all_frames or monster_type not in all_frames:
            return False
        self.sprite_monster_type = monster_type
        self.sprite_set = all_frames[monster_type]
        hitboxes = {
            "ice_slime": (44, 34),
            "ice_wolf": (42, 38),
            "ice_bat": (44, 34),
        }
        self.sprite_hitbox = hitboxes.get(monster_type, (40, 36))
        self.radius = max(16, min(self.sprite_hitbox) // 2)
        return True

    def use_15_11_monster_sprite(self, monster_type):
        all_frames = load_monster_15_11_frames()
        if not all_frames or monster_type not in all_frames:
            return False
        self.sprite_monster_type = monster_type
        self.sprite_set = all_frames[monster_type]
        hitboxes = {
            "magma_slime": (44, 34),
            "frost_wolf": (46, 38),
            "magma_golem": (48, 42),
        }
        self.sprite_hitbox = hitboxes.get(monster_type, (42, 38))
        self.radius = max(16, min(self.sprite_hitbox) // 2)
        return True

    def use_10_6_monster_sprite(self, monster_type):
        all_frames = load_monster_10_6_frames()
        if not all_frames or monster_type not in all_frames:
            return False
        self.sprite_monster_type = monster_type
        self.sprite_set = all_frames[monster_type]
        hitboxes = {
            "forest_wisp": (44, 36),
            "forest_wolf": (48, 40),
            "forest_mage": (42, 40),
        }
        self.sprite_hitbox = hitboxes.get(monster_type, (42, 38))
        self.radius = max(16, min(self.sprite_hitbox) // 2)
        return True

    def use_5_1_monster_sprite(self, monster_type):
        all_frames = load_monster_5_1_frames()
        if not all_frames or monster_type not in all_frames:
            return False
        self.sprite_monster_type = monster_type
        self.sprite_set = all_frames[monster_type]
        hitboxes = {
            "storm_orb": (44, 38),
            "storm_wolf": (48, 40),
            "storm_mage": (42, 40),
        }
        self.sprite_hitbox = hitboxes.get(monster_type, (42, 38))
        self.radius = max(16, min(self.sprite_hitbox) // 2)
        return True

    def face_vector(self, vector):
        self.facing = direction_4way(vector, self.facing)

    def trigger_attack_animation(self, vector=None, duration=0.35):
        self.attack_direction = direction_4way(vector, self.facing)
        self.facing = self.attack_direction
        self.attack_anim_timer = max(self.attack_anim_timer, duration)

    def current_sprite(self):
        if not self.sprite_set:
            return None
        if self.attack_anim_timer > 0:
            attack_key = f"attack_{self.attack_direction}"
            return self.sprite_set.get(attack_key) or self.sprite_set.get(self.attack_direction)
        return self.sprite_set.get(self.facing) or self.sprite_set.get("down")

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.dead = True

    def update(self, dt, player, projectiles, effects, arena_rect=None, walkable_polygon=None):
        old_pos = pygame.Vector2(self.pos)
        self.attack_anim_timer = max(0.0, self.attack_anim_timer - dt)
        self.contact_attack_cd = max(0.0, self.contact_attack_cd - dt)
        to_player = player.pos - self.pos
        dist = max(1, to_player.length())
        direction = to_player / dist

        if self.enemy_type == "감염체":
            self.pos += direction * self.speed * dt
        elif self.enemy_type == "경비 드론":
            if dist > 360:
                self.pos += direction * self.speed * dt
            elif dist < 220:
                self.pos -= direction * self.speed * dt
            self.shoot_cd -= dt
            if self.shoot_cd <= 0:
                self.shoot_cd = random.uniform(1.0, 1.7)
                self.trigger_attack_animation(direction, 0.38)
                projectiles.append(Projectile(self.pos.x, self.pos.y, direction.x * self.shoot_speed, direction.y * self.shoot_speed, 8, self.damage, "enemy", RED, 3.0))
        elif self.enemy_type == "돌진 실험체":
            self.charge_cd -= dt
            if self.charge_cd <= 0 and self.charge_warning <= 0:
                self.charge_warning = 0.55
            if self.charge_warning > 0:
                self.charge_warning -= dt
                self.trigger_attack_animation(direction, 0.12)
                effects.append(Effect(self.pos.x, self.pos.y, 32, ORANGE, 0.08))
                if self.charge_warning <= 0:
                    self.pos += direction * 175
                    self.trigger_attack_animation(direction, 0.42)
                    self.charge_cd = random.uniform(1.7, 2.5)
            else:
                self.pos += direction * self.speed * dt
        else:
            self.pos += direction * self.speed * dt

        if dist <= self.radius + player.radius + 22 and self.contact_attack_cd <= 0:
            self.trigger_attack_animation(direction, 0.32)
            self.contact_attack_cd = 0.65

        if walkable_polygon:
            self.pos = clamp_point_to_polygon(self.pos, walkable_polygon, self.radius)
        elif arena_rect:
            self.pos.x = clamp(self.pos.x, arena_rect.left + self.radius, arena_rect.right - self.radius)
            self.pos.y = clamp(self.pos.y, arena_rect.top + self.radius, arena_rect.bottom - self.radius)
        else:
            self.pos.x = clamp(self.pos.x, 35, WIDTH - 35)
            self.pos.y = clamp(self.pos.y, COMBAT_TOP, COMBAT_BOTTOM)
        movement = self.pos - old_pos
        if movement.length_squared() > 0.25 and self.attack_anim_timer <= 0:
            self.face_vector(movement)

    def draw(self, surface):
        scale = depth_scale(self.pos.y)
        visual_radius = max(10, int(self.radius * scale))
        body_color = tint_color(self.color, 0.82)
        draw_ellipse_shadow(surface, self.pos, self.radius, 105, 2.2, 0.5)
        sprite = self.current_sprite()
        if sprite is not None:
            target_w = max(1, int(sprite.get_width() * scale))
            target_h = max(1, int(sprite.get_height() * scale))
            draw_sprite = pygame.transform.smoothscale(sprite, (target_w, target_h))
            sprite_rect = draw_sprite.get_rect(
                midbottom=(int(self.pos.x), int(self.pos.y + self.radius * scale + 8))
            )
            surface.blit(draw_sprite, sprite_rect)
            bar_y = sprite_rect.top - 10
            draw_bar(surface, self.pos.x - 22 * scale, bar_y, 44 * scale, 5, self.hp, self.max_hp, RED)
            return
        pygame.draw.circle(surface, (8, 8, 10), self.pos, visual_radius + 4)
        if self.enemy_type == "경비 드론":
            rect = pygame.Rect(0, 0, int(34 * scale), int(24 * scale))
            rect.center = self.pos
            pygame.draw.rect(surface, body_color, rect, border_radius=5)
            pygame.draw.circle(surface, (210, 70, 70), self.pos, max(3, int(5 * scale)))
        elif self.enemy_type == "방패병":
            pygame.draw.circle(surface, body_color, self.pos, visual_radius)
            pygame.draw.rect(surface, (62, 66, 74), (self.pos.x - 24 * scale, self.pos.y - 15 * scale, 12 * scale, 30 * scale), border_radius=3)
        else:
            pygame.draw.circle(surface, body_color, self.pos, visual_radius)
            if self.enemy_type == "감염체":
                pygame.draw.circle(surface, (120, 240, 150), self.pos - pygame.Vector2(visual_radius * 0.25, visual_radius * 0.25), max(3, int(4 * scale)))
            elif self.enemy_type == "돌진 실험체":
                pygame.draw.polygon(surface, (210, 100, 65), [ (self.pos.x, self.pos.y - visual_radius - 7), (self.pos.x - 7 * scale, self.pos.y - visual_radius + 5), (self.pos.x + 7 * scale, self.pos.y - visual_radius + 5), ])
        pygame.draw.circle(surface, (0, 0, 0), self.pos, visual_radius, 2)
        draw_bar(surface, self.pos.x - 22 * scale, self.pos.y - visual_radius - 13, 44 * scale, 5, self.hp, self.max_hp, RED)

class Boss:
    DATA = { 15: ("오염 관리자 G", (170, 210, 55), 560), 11: ("LIGER-X11 인페르노", (255, 95, 35), INFERNO_LIGER_MAX_HP), 10: ("고전압 감시자", (80, 130, 255), 650), 5: ("폭주 진압병", (210, 65, 65), 760), 1: ("코어 통합체", (230, 70, 85), 980), }

    def __init__(self, floor):
        self.floor = floor
        self.config = BOSS_CONFIGS.get(floor, BOSS_CONFIGS[1])
        self.boss_id = self.config.get("boss_id", f"boss{floor}")
        self.fallback_type = self.config.get("fallback_type", "default")
        self.state = "idle"
        self.attack_timer = 0
        self.skin_images = {}
        self.has_image_skin = False
        self.skin_scaled_cache = {}
        self.name, self.color, hp = self.DATA.get(floor, self.DATA[1])
        self.max_hp = hp
        self.hp = hp
        self.pos = pygame.Vector2(WIDTH // 2, COMBAT_TOP + 42)
        self.arena_rect = pygame.Rect(40, COMBAT_TOP, WIDTH - 80, COMBAT_BOTTOM - COMBAT_TOP)
        self.floor_top_y = self.arena_rect.top
        self.floor_bottom_y = self.arena_rect.bottom
        self.walkable_polygon = [ (self.arena_rect.left, self.arena_rect.bottom), (self.arena_rect.right, self.arena_rect.bottom), (self.arena_rect.right, self.arena_rect.top), (self.arena_rect.left, self.arena_rect.top), ]
        if floor == ICE_DRAGON_FLOOR:
            self.radius = 92
        else:
            self.radius = 44 if floor != 1 else 56
        hitbox_size = self.config.get("hitbox", (self.radius * 2, self.radius * 2))
        self.hitbox_w = int(hitbox_size[0])
        self.hitbox_h = int(hitbox_size[1])
        self.visual_pos = pygame.Vector2(self.pos)
        self.visual_height = 0
        self.visual_rect = pygame.Rect(0, 0, 0, 0)
        self.dead = False
        self.timer = 0
        self.pattern_cd = 1.0
        self.phase2 = False
        self.warning_lines = []
        self.floor15_frames = self.load_floor15_motion_frames() if floor == ICE_DRAGON_FLOOR else {}
        self.floor15_scaled_cache = {}
        idle_frames = self.floor15_frames.get("idle", []) if floor == ICE_DRAGON_FLOOR else []
        self.floor15_sprite = idle_frames[0] if isinstance(idle_frames, (list, tuple)) and idle_frames else idle_frames
        self.floor15_phase_text = False
        self.warning_attacks = []
        self.active_tornadoes = []
        self.pattern_count = 0
        self.vulnerable_timer = 0
        self.floor15_summon_queue = []
        self.floor15_logged = False
        if floor != ICE_DRAGON_FLOOR:
            self.skin_images = self.load_optional_skins()
            self.has_image_skin = any(self.skin_images.values())
        if floor == INFERNO_LIGER_FLOOR:
            self.name = "LIGER-X11 인페르노"
            self.color = (255, 95, 35)
            self.max_hp = INFERNO_LIGER_MAX_HP
            self.hp = self.max_hp
            self.radius = 82
            self.hitbox_w, self.hitbox_h = 190, 115
            self.pattern_cd = 1.0
            self.liger_direction = 1
            self.liger_dash_timer = 0.0
            self.liger_roar_opening = 0.45
            self.liger_last_pattern = None
            print("11층 LIGER-X11 인페르노 보스 로드")

        if floor == ICE_DRAGON_FLOOR:
            self.pos = pygame.Vector2(BOSS15_WORLD_WIDTH * BOSS15_CORE_POS_RATIO[0], BOSS15_WORLD_HEIGHT * BOSS15_CORE_POS_RATIO[1])
            self.name = "격리 관리자 G"
            self.visual_pos = pygame.Vector2(BOSS15_WORLD_WIDTH * BOSS15_ANCHOR_POS_RATIO[0], BOSS15_WORLD_HEIGHT * BOSS15_ANCHOR_POS_RATIO[1])
            self.visual_height = int(HEIGHT * BOSS15_VISUAL_HEIGHT_RATIO)
            self.radius = 58
            self.hitbox_w, self.hitbox_h = 116, 116
            self.pattern_cd = 1.4
            self.name = "Ice Dragon"
            self.boss_id = "ice_dragon_16"
            self.fallback_type = "ice_dragon"
            self.color = (105, 205, 255)
            self.max_hp = ICE_DRAGON_MAX_HP
            self.hp = self.max_hp
            self.pos = pygame.Vector2( ICE_DRAGON_WORLD_WIDTH * ICE_DRAGON_CORE_POS_RATIO[0], ICE_DRAGON_WORLD_HEIGHT * ICE_DRAGON_CORE_POS_RATIO[1], )
            self.visual_pos = pygame.Vector2( ICE_DRAGON_WORLD_WIDTH * ICE_DRAGON_VISUAL_ANCHOR_RATIO[0], ICE_DRAGON_WORLD_HEIGHT * ICE_DRAGON_VISUAL_ANCHOR_RATIO[1], )
            self.visual_height = int(HEIGHT * ICE_DRAGON_VISUAL_HEIGHT_RATIO)
            self.radius = 72
            self.hitbox_w, self.hitbox_h = 180, 150
            self.pattern_cd = 1.2
            self.ice_dragon_ai_state = "idle"
            self.ice_dragon_state_timer = 0.0
            self.ice_dragon_current_pattern = None
            self.ice_dragon_anim_state = "idle"
            self.ice_dragon_animation = "idle"
            self.ice_dragon_animation_locked = False
            self.ice_dragon_anim_timer = 0.0
            self.ice_dragon_frame_index = 0
            self.ice_dragon_death_timer = 0.0
            self.is_dying = False
            self.ready_to_clear = False
            print("16층 Ice Dragon 보스 로드")

    @property
    def hitbox(self):
        scale = depth_scale(self.pos.y) if self.floor != ICE_DRAGON_FLOOR else 1.0
        w = max(8, int(self.hitbox_w * scale))
        h = max(8, int(self.hitbox_h * scale))
        return pygame.Rect(int(self.pos.x - w // 2), int(self.pos.y - h // 2), w, h)

    @property
    def rect(self):
        return self.hitbox

    def load_optional_skins(self):
        skins = {}
        for key, filename in self.config.get("skins", {}).items():
            image = load_image_optional(filename)
            if image is not None:
                skins[key] = image
        return skins

    def set_arena(self, arena_rect, walkable_polygon=None, floor_top_y=None, floor_bottom_y=None):
        self.arena_rect = pygame.Rect(arena_rect)
        self.walkable_polygon = list(walkable_polygon) if walkable_polygon else [ (self.arena_rect.left, self.arena_rect.bottom), (self.arena_rect.right, self.arena_rect.bottom), (self.arena_rect.right, self.arena_rect.top), (self.arena_rect.left, self.arena_rect.top), ]
        self.floor_top_y = floor_top_y if floor_top_y is not None else self.arena_rect.top
        self.floor_bottom_y = floor_bottom_y if floor_bottom_y is not None else self.arena_rect.bottom
        if self.floor == INFERNO_LIGER_FLOOR:
            self.pos = self.clamp_to_walkable(pygame.Vector2(self.arena_rect.centerx, self.floor_top_y + self.arena_rect.height * 0.42), self.radius)
            self.visual_pos = pygame.Vector2(self.pos)
            return
        if self.floor == ICE_DRAGON_FLOOR:
            self.pos = pygame.Vector2( ICE_DRAGON_WORLD_WIDTH * ICE_DRAGON_CORE_POS_RATIO[0], ICE_DRAGON_WORLD_HEIGHT * ICE_DRAGON_CORE_POS_RATIO[1], )
            self.visual_pos = pygame.Vector2( ICE_DRAGON_WORLD_WIDTH * ICE_DRAGON_VISUAL_ANCHOR_RATIO[0], ICE_DRAGON_WORLD_HEIGHT * ICE_DRAGON_VISUAL_ANCHOR_RATIO[1], )
            self.visual_height = int(HEIGHT * ICE_DRAGON_VISUAL_HEIGHT_RATIO)
        else:
            self.pos = pygame.Vector2(self.arena_rect.centerx, self.floor_top_y + 54)

    def random_walkable_point(self, padding=40):
        return get_random_point_in_walkable_polygon(self.walkable_polygon, self.floor_top_y, self.floor_bottom_y, padding)

    def random_walkable_rect(self, w, h, padding=36):
        max_h = max(24, int(self.floor_bottom_y - self.floor_top_y - padding * 2))
        max_w = max(24, int(self.arena_rect.width - padding * 2))
        w = min(w, max_w)
        h = min(h, max_h)
        for _ in range(40):
            low_y = int(self.floor_top_y + h // 2 + padding)
            high_y = int(self.floor_bottom_y - h // 2 - padding)
            if low_y > high_y:
                break
            center_y = random.randint(low_y, high_y)
            left, right = polygon_x_bounds(center_y, self.walkable_polygon)
            if right - left <= w + padding * 2:
                continue
            x = random.randint(int(left + padding), int(right - w - padding))
            y = int(center_y - h // 2)
            rect = pygame.Rect(x, y, w, h)
            corners = [(rect.left, rect.top), (rect.right, rect.top), (rect.left, rect.bottom), (rect.right, rect.bottom)]
            if all(point_in_polygon(corner, self.walkable_polygon) for corner in corners):
                return rect
        x, y = self.random_walkable_point(padding + max(w, h) // 2)
        return pygame.Rect(int(x - w // 2), int(y - h // 2), w, h)

    def clamp_to_walkable(self, pos, padding=0):
        return clamp_point_to_polygon(pygame.Vector2(pos), self.walkable_polygon, padding)

    def load_floor15_sprite(self):
        path = find_asset_path( os.path.join("assets", BOSS15_IMAGE), os.path.join("assets", "boss15.png"), os.path.join("assets", "boss15_reference.png"), os.path.join("assets", "boss15_reference.png.png"), os.path.join("assets", "assetsboss15_reference.png.png"), os.path.join("assets", "boss_floor15.png"), )
        if not path:
            return None
        try:
            image = pygame.image.load(path).convert_alpha()
            image = self.prepare_floor15_sprite(image)
            height = 235
            width = max(110, int(image.get_width() * height / max(1, image.get_height())))
            return pygame.transform.smoothscale(image, (width, height))
        except (pygame.error, OSError):
            return None

    def load_floor15_motion_frames(self):
        motion_path = find_asset_path(os.path.join("assets", "a.png"))
        frames = {}
        if motion_path:
            try:
                sheet = pygame.image.load(motion_path)
                sheet = sheet.convert_alpha() if pygame.display.get_surface() else sheet.copy()
                crop_defs = { "idle": (0.31, 0.00, 0.66, 0.58), "slash": (0.00, 0.45, 0.58, 0.98), "summon": (0.50, 0.45, 0.98, 0.98), }
                target_heights = { "idle": 390, "slash": 330, "summon": 360, }
                for name, crop in crop_defs.items():
                    frame = crop_by_ratio(sheet, *crop)
                    frame = trim_transparent(remove_neutral_edge_background(frame), padding=10)
                    height = target_heights[name]
                    width = max(160, int(frame.get_width() * height / max(1, frame.get_height())))
                    frames[name] = pygame.transform.smoothscale(frame, (width, height))
            except (pygame.error, OSError, ValueError):
                frames = {}

        if not frames:
            fallback = self.load_floor15_sprite()
            if fallback:
                frames = {"idle": fallback, "slash": fallback, "summon": fallback}
        return frames

    def get_floor15_frame(self):
        if not self.floor15_frames:
            return None
        active_kinds = {warning.kind for warning in self.warning_attacks}
        if self.vulnerable_timer > 0:
            return self.floor15_frames.get("idle")
        if "summon" in active_kinds or "rune" in active_kinds:
            return self.floor15_frames.get("summon") or self.floor15_frames.get("idle")
        if active_kinds:
            return self.floor15_frames.get("slash") or self.floor15_frames.get("idle")
        if self.pattern_count % 3 == 1 and math.sin(self.timer * 1.6) > 0.78:
            return self.floor15_frames.get("summon") or self.floor15_frames.get("idle")
        return self.floor15_frames.get("idle")

    def prepare_floor15_sprite(self, image):
        width, height = image.get_size()
        if width > 700 and height > 500:
            crop = pygame.Rect( int(width * 0.005), int(height * 0.02), int(width * 0.255), int(height * 0.535), )
            crop.clamp_ip(image.get_rect())
            image = image.subsurface(crop).copy()

        bg = image.get_at((image.get_width() - 4, 4))
        bg_r, bg_g, bg_b = bg.r, bg.g, bg.b
        for y in range(image.get_height()):
            for x in range(image.get_width()):
                color = image.get_at((x, y))
                delta = abs(color.r - bg_r) + abs(color.g - bg_g) + abs(color.b - bg_b)
                neutral = max(color.r, color.g, color.b) - min(color.r, color.g, color.b) < 18
                bright = (color.r + color.g + color.b) / 3 > 135
                if delta < 58 or (neutral and bright and delta < 115):
                    image.set_at((x, y), (color.r, color.g, color.b, 0))
        return image

    def take_damage(self, amount):
        if self.floor == ICE_DRAGON_FLOOR and self.vulnerable_timer > 0:
            amount *= 1.35
        self.hp -= amount
        if self.hp <= self.max_hp * 0.5 and self.floor in (1, ICE_DRAGON_FLOOR, INFERNO_LIGER_FLOOR):
            if self.floor == ICE_DRAGON_FLOOR and not self.phase2:
                self.floor15_phase_text = True
            if self.floor == INFERNO_LIGER_FLOOR and not self.phase2:
                self.liger_roar_opening = 1.4
                self.pattern_cd = max(self.pattern_cd, 1.1)
                self.liger_last_pattern = "roar"
            self.phase2 = True
        if self.hp <= 0:
            self.dead = True

    def update(self, dt, player, projectiles, traps, effects, spawn_enemy):
        self.timer += dt
        self.attack_timer = max(0, self.attack_timer - dt)
        if self.attack_timer <= 0 and self.state == "attack":
            self.state = "idle"
        self.pattern_cd -= dt
        self.vulnerable_timer = max(0, self.vulnerable_timer - dt)
        if self.floor == INFERNO_LIGER_FLOOR:
            self.update_liger_x11(dt, player, projectiles, traps, effects, spawn_enemy)
            return
        if self.floor == ICE_DRAGON_FLOOR:
            self.update_floor15(dt, player, projectiles, traps, effects, spawn_enemy)
            return
        speed = 56 if not self.phase2 else 88
        arena = self.arena_rect
        self.pos.x = arena.centerx + math.sin(self.timer * 0.9) * min(420, arena.width * 0.28)
        self.pos.y = self.floor_top_y + 54 + math.sin(self.timer * 1.3) * 18
        self.warning_lines = []
        if self.pattern_cd > 0:
            return

        to_player = player.pos - self.pos
        dist = to_player.length()
        direction = to_player.normalize() if to_player.length_squared() else pygame.Vector2(0, 1)
        self.state = "attack"
        self.attack_timer = 0.38

        if self.floor == 10:
            self.pattern_cd = max(0.55, 1.7 - (0.08 if self.phase2 else 0) - (21 - self.floor) * 0.025)
            for angle in range(0, 360, 45):
                d = pygame.Vector2(1, 0).rotate(angle)
                projectiles.append(Projectile(self.pos.x, self.pos.y, d.x * 250, d.y * 250, 9, 13, "enemy", BLUE, 3.2))
        elif self.floor == 5:
            self.pattern_cd = max(0.55, 1.7 - (0.08 if self.phase2 else 0) - (21 - self.floor) * 0.025)
            self.pos += direction * speed
            self.pos = self.clamp_to_walkable(self.pos, 54)
            for spread in (-18, 0, 18):
                d = direction.rotate(spread)
                projectiles.append(Projectile(self.pos.x, self.pos.y, d.x * 360, d.y * 360, 10, 16, "enemy", RED, 3.0))
            if random.random() < 0.35:
                spawn_enemy("방패병")
        else:
            self.pattern_cd = max(0.55, 1.7 - (0.08 if self.phase2 else 0) - (21 - self.floor) * 0.025)
            for spread in (-28, -12, 0, 12, 28):
                d = direction.rotate(spread)
                projectiles.append(Projectile(self.pos.x, self.pos.y, d.x * 380, d.y * 380, 10, 18, "enemy", (245, 70, 90), 3.4))
            if random.random() < 0.30:
                spawn_enemy(random.choice(["감염체", "경비 드론", "돌진 실험체"]))

        effects.append(Effect(self.pos.x, self.pos.y, self.radius + 26, self.color, 0.25))

    def update_liger_x11(self, dt, player, projectiles, traps, effects, spawn_enemy):
        # 실험 실패로 불 능력을 얻어 폭주하는 11층 보스.
        # 얼음드래곤보다 체력/패턴 압박이 강하게 잡혀 있음.
        self.warning_lines = []
        self.visual_pos = pygame.Vector2(self.pos)

        # 등장 포효: 처음에는 중앙에서 크게 울부짖고 작은 화염 파동을 냄.
        if getattr(self, "liger_roar_opening", 0) > 0:
            self.liger_roar_opening -= dt
            self.state = "roar"
            self.liger_last_pattern = "roar"
            self.attack_timer = max(self.attack_timer, 0.18)
            if random.random() < 0.22:
                effects.append(Effect(self.pos.x + random.randint(-70, 70), self.pos.y + random.randint(-50, 40), 38, ORANGE, 0.22))
            return

        # 좌우로 계속 움직이며 플레이어를 압박
        speed = 185 if not self.phase2 else 255
        self.pos.x += self.liger_direction * speed * dt
        if self.pos.x < self.arena_rect.left + 170:
            self.pos.x = self.arena_rect.left + 170
            self.liger_direction = 1
        elif self.pos.x > self.arena_rect.right - 170:
            self.pos.x = self.arena_rect.right - 170
            self.liger_direction = -1
        target_y = self.floor_top_y + self.arena_rect.height * (0.43 + 0.07 * math.sin(self.timer * 1.9))
        self.pos.y += (target_y - self.pos.y) * min(1.0, dt * 4.0)
        self.pos = self.clamp_to_walkable(self.pos, self.radius)

        for warning in self.warning_attacks:
            was_triggered = warning.triggered
            result = warning.update(dt, player)
            if warning.triggered and not was_triggered:
                effects.append(Effect(warning.pos.x, warning.pos.y, 88, (255, 95, 35), 0.28))
            if result == "hit":
                effects.append(Effect(player.pos.x, player.pos.y, 54, RED, 0.20))
            elif result == "dodged":
                effects.append(Effect(player.pos.x, player.pos.y, 62, YELLOW, 0.22))
            elif result == "shield":
                effects.append(Effect(player.pos.x, player.pos.y, 58, CYAN, 0.22))
        self.warning_attacks = [warning for warning in self.warning_attacks if not warning.done]

        if self.pattern_cd > 0 or self.warning_attacks:
            return

        direction = player.pos - self.pos
        if direction.length_squared() == 0:
            direction = pygame.Vector2(1, 0)
        angle = math.degrees(math.atan2(direction.y, direction.x))

        self.state = "attack"
        self.attack_timer = 0.46
        phase_bonus = 1.0 if self.phase2 else 0.0
        pattern = random.choices( ["dash", "breath", "claw", "roar", "meteors"], weights=[4 + phase_bonus, 4 + phase_bonus, 3, 3 + phase_bonus, 2 + phase_bonus], k=1, )[0]
        self.liger_last_pattern = pattern

        if pattern == "dash":
            # 길게 돌진하는 화염 몸통박치기
            self.state = "dash"
            self.attack_timer = 0.55
            self.warning_attacks.append(BossWarning("laser", self.pos, (760 if not self.phase2 else 930, 22), 0.55, 0.28, 30 if self.phase2 else 24, (255, 105, 35), "inferno_dash", angle))
            self.pos += pygame.Vector2(1, 0).rotate(angle) * (150 if not self.phase2 else 210)
            self.pos = self.clamp_to_walkable(self.pos, self.radius)
            self.pattern_cd = 1.05 if not self.phase2 else 0.75
        elif pattern == "breath":
            # 화염 브레스: 플레이어 방향으로 넓게 불길을 뿜음
            self.state = "breath"
            self.attack_timer = 0.72
            spreads = (-28, -14, 0, 14, 28) if not self.phase2 else (-36, -24, -12, 0, 12, 24, 36)
            for spread in spreads:
                d = pygame.Vector2(1, 0).rotate(angle + spread)
                projectiles.append(Projectile(self.pos.x, self.pos.y - 20, d.x * 430, d.y * 430, 13, 18 if self.phase2 else 14, "enemy", ORANGE, 2.4))
            self.warning_attacks.append(BossWarning("laser", self.pos, (650 if not self.phase2 else 780, 34), 0.38, 0.22, 22 if self.phase2 else 17, (255, 135, 35), "inferno_breath", angle))
            self.pattern_cd = 1.25 if not self.phase2 else 0.9
        elif pattern == "claw":
            # 플레이어 주변 3연속 할퀴기
            for spread in (-18, 0, 18):
                self.warning_attacks.append(BossWarning("laser", self.pos, (520, 16), 0.48, 0.24, 22 if self.phase2 else 18, (255, 145, 45), "inferno_claw", angle + spread))
            self.pattern_cd = 1.15 if not self.phase2 else 0.82
        elif pattern == "roar":
            # 포효: 원형 충격파 + 탄막
            self.warning_attacks.append(BossWarning("circle", self.pos, 185 if not self.phase2 else 235, 0.65, 0.34, 26 if self.phase2 else 20, (255, 80, 35), "inferno_roar"))
            shots = 10 if self.phase2 else 7
            for i in range(shots):
                d = pygame.Vector2(1, 0).rotate(i * 360 / shots + self.timer * 25)
                projectiles.append(Projectile(self.pos.x, self.pos.y, d.x * 360, d.y * 360, 9, 16 if self.phase2 else 12, "enemy", ORANGE, 3.0))
            self.pattern_cd = 1.35 if not self.phase2 else 1.0
        else:
            # 멜트다운: 플레이어 위치와 랜덤 위치에 화염 낙하
            count = 7 if self.phase2 else 5
            for i in range(count):
                if i == 0:
                    point = self.clamp_to_walkable(player.pos, 65)
                    pos = (point.x, point.y)
                else:
                    pos = self.random_walkable_point(72)
                self.warning_attacks.append(BossWarning("circle", pos, 54 if self.phase2 else 46, 0.72, 0.30, 24 if self.phase2 else 18, (255, 120, 35), "inferno_meteor"))
            self.pattern_cd = 1.45 if not self.phase2 else 1.05

        effects.append(Effect(self.pos.x, self.pos.y, 96, (255, 95, 35), 0.28))

    def update_floor15(self, dt, player, projectiles, traps, effects, spawn_enemy):
        arena = self.arena_rect
        self.pos = self.clamp_to_walkable( pygame.Vector2(arena.centerx + math.sin(self.timer * 1.7) * 6, arena.top + arena.height * 0.08), self.radius, )
        self.visual_pos = pygame.Vector2( arena.left + arena.width * BOSS15_VISUAL_POS_RATIO[0], arena.top + arena.height * BOSS15_VISUAL_POS_RATIO[1], )
        self.warning_lines = []

        for warning in self.warning_attacks:
            was_triggered = warning.triggered
            result = warning.update(dt, player)
            if warning.triggered and not was_triggered:
                effects.append(Effect(warning.pos.x, warning.pos.y, 70, warning.color[:3], 0.26))
            if result == "dodged":
                effects.append(Effect(player.pos.x, player.pos.y, 64, YELLOW, 0.26))
            elif result == "shield":
                effects.append(Effect(player.pos.x, player.pos.y, 58, CYAN, 0.24))
            elif result == "hit":
                effects.append(Effect(player.pos.x, player.pos.y, 42, RED, 0.18))
        self.warning_attacks = [warning for warning in self.warning_attacks if not warning.done]

        ready_summons = []
        for summon in self.floor15_summon_queue:
            summon["timer"] -= dt
            if summon["timer"] <= 0:
                ready_summons.append(summon)
        self.floor15_summon_queue = [summon for summon in self.floor15_summon_queue if summon not in ready_summons]
        for summon in ready_summons:
            for _ in range(summon["count"]):
                spawn_enemy(random.choice(["감염체", "감염체", "돌진 실험체"]))
            effects.append(Effect(summon["pos"][0], summon["pos"][1], 88, PURPLE, 0.38))

        if self.pattern_cd > 0 or self.warning_attacks or self.vulnerable_timer > 0:
            return

        if self.floor15_phase_text:
            effects.append(Effect(self.arena_rect.centerx, self.arena_rect.top + 70, 180, (230, 95, 255), 0.6))
            self.floor15_phase_text = False

        self.pattern_count += 1
        if self.pattern_count % 4 == 0:
            self.vulnerable_timer = 2.0
            self.pattern_cd = 2.2
            effects.append(Effect(self.pos.x, self.pos.y + 40, 110, (210, 255, 160), 0.55))
            return

        pattern = random.choices( ["stomp", "fall", "laser", "rune", "summon"], weights=[4, 4, 3, 3 if self.phase2 else 2, 2], k=1, )[0]
        if pattern == "stomp":
            self.floor15_stomp(player)
            self.pattern_cd = 1.35 if not self.phase2 else 1.05
        elif pattern == "fall":
            self.floor15_fall(player)
            self.pattern_cd = 1.6 if not self.phase2 else 1.2
        elif pattern == "laser":
            self.floor15_laser()
            self.pattern_cd = 1.55 if not self.phase2 else 1.15
        elif pattern == "rune":
            self.floor15_runes(player)
            self.pattern_cd = 1.5 if not self.phase2 else 1.12
        else:
            self.floor15_summon(player)
            self.pattern_cd = 1.9 if not self.phase2 else 1.45

    def floor15_stomp(self, player):
        pos = self.clamp_to_walkable(player.pos, 70)
        pos = (pos.x, pos.y)
        self.warning_attacks.append(BossWarning("ellipse", pos, (118, 48), BOSS15_TELEGRAPH_TIME, BOSS15_ATTACK_ACTIVE_TIME, 22 if self.phase2 else 18, (190, 80, 255), "stomp"))

    def floor15_fall(self, player):
        count = 6 if self.phase2 else 4
        for i in range(count):
            if i == 0:
                point = self.clamp_to_walkable(player.pos, 58)
                pos = (point.x, point.y)
            else:
                pos = self.random_walkable_point(70)
            roll = random.random()
            damage = 20 if roll < 0.72 else 8
            radius = 44 if roll < 0.9 else 34
            self.warning_attacks.append(BossWarning("circle", pos, radius, BOSS15_TELEGRAPH_TIME, BOSS15_ATTACK_ACTIVE_TIME, damage, (220, 80, 235), "fall"))

    def floor15_laser(self):
        lines = 5 if self.phase2 else random.randint(2, 3)
        base_angles = random.sample([20, 45, 70, 110, 135, 160, 200, 225, 250, 290, 315, 340], lines)
        origin = pygame.Vector2(self.arena_rect.centerx, self.floor_top_y + 38)
        for angle in base_angles:
            self.warning_attacks.append(BossWarning("laser", origin, (min(980, self.arena_rect.width * 0.62), 9), BOSS15_TELEGRAPH_TIME, BOSS15_ATTACK_ACTIVE_TIME, 18 if self.phase2 else 15, (185, 80, 255), "laser", angle))

    def floor15_runes(self, player):
        count = 4 if self.phase2 else 3
        colors = [(80, 235, 120), (230, 85, 75), (180, 80, 245)]
        for i in range(count):
            if i == 0:
                point = self.clamp_to_walkable(player.pos, 58)
                pos = (point.x, point.y)
            else:
                pos = self.random_walkable_point(68)
            self.warning_attacks.append(BossWarning("ellipse", pos, (70, 34), BOSS15_TELEGRAPH_TIME, 2.45, 7 + i * 2, colors[i % len(colors)], "rune"))

    def floor15_summon(self, player):
        pos = self.random_walkable_point(82)
        count = random.randint(3, 4) if self.phase2 else 2
        self.warning_attacks.append(BossWarning("circle", pos, 58, BOSS15_TELEGRAPH_TIME, BOSS15_ATTACK_ACTIVE_TIME, 0, (160, 85, 255), "summon"))
        self.floor15_summon_queue.append({"timer": 1.05, "count": count, "pos": pos})

    def draw_warnings(self, surface):
        for warning in self.warning_attacks:
            warning.draw(surface)

    def get_current_skin_image(self):
        if self.dead:
            return self.skin_images.get("defeat") or self.skin_images.get("idle")
        if self.floor == INFERNO_LIGER_FLOOR:
            last_pattern = getattr(self, "liger_last_pattern", None)
            if getattr(self, "liger_roar_opening", 0) > 0 or (self.attack_timer > 0 and last_pattern == "roar"):
                return self.skin_images.get("roar") or self.skin_images.get("phase2") or self.skin_images.get("attack") or self.skin_images.get("idle")
            if self.attack_timer > 0 and last_pattern == "dash":
                return self.skin_images.get("dash") or self.skin_images.get("attack") or self.skin_images.get("idle")
            if self.attack_timer > 0:
                return self.skin_images.get("attack") or self.skin_images.get("phase2") or self.skin_images.get("idle")
            if self.phase2:
                return self.skin_images.get("phase2") or self.skin_images.get("idle")
            return self.skin_images.get("idle")
        if self.attack_timer > 0:
            return self.skin_images.get("attack") or self.skin_images.get("phase2") or self.skin_images.get("idle")
        if self.phase2:
            return self.skin_images.get("phase2") or self.skin_images.get("idle")
        return self.skin_images.get("idle")

    def draw_image_boss(self, surface, image):
        scale = depth_scale(self.pos.y)
        target_h = max(60, int((self.radius * 2.6) * scale))
        target_w = max(60, int(image.get_width() * target_h / max(1, image.get_height())))
        cache_key = (id(image), target_w, target_h)
        draw_image = self.skin_scaled_cache.get(cache_key)
        if draw_image is None:
            draw_image = pygame.transform.smoothscale(image, (target_w, target_h))
            if len(self.skin_scaled_cache) > 12:
                self.skin_scaled_cache.clear()
            self.skin_scaled_cache[cache_key] = draw_image
        bob = math.sin(self.timer * 4.0) * 3
        rect = draw_image.get_rect(midbottom=(int(self.pos.x), int(self.pos.y + self.radius * 0.58 * scale + bob)))
        draw_ellipse_shadow(surface, self.pos, self.radius, 135, 2.55, 0.5)
        surface.blit(draw_image, rect)

    def draw_code_boss(self, surface):
        if self.fallback_type == "core_machine":
            self.draw_core_machine_boss(surface)
        elif self.fallback_type == "dark_beast":
            self.draw_dark_beast_boss(surface)
        elif self.fallback_type == "final_core":
            self.draw_final_core_boss(surface)
        elif self.fallback_type == "giant_skeleton":
            draw_boss15_shape_fallback(self, surface)
        elif self.fallback_type == "inferno_liger":
            self.draw_dark_beast_boss(surface)
        else:
            self.draw_default_boss(surface)

    def draw_default_boss(self, surface):
        scale = depth_scale(self.pos.y)
        visual_radius = int(self.radius * scale)
        draw_ellipse_shadow(surface, self.pos, self.radius, 135, 2.55, 0.5)
        pygame.draw.circle(surface, (16, 16, 22), self.pos, visual_radius + 8)
        points = []
        for i in range(8):
            angle = i * math.pi / 4 + pygame.time.get_ticks() * 0.0007
            r = visual_radius if i % 2 == 0 else visual_radius * 0.68
            points.append((self.pos.x + math.cos(angle) * r, self.pos.y + math.sin(angle) * r))
        pygame.draw.polygon(surface, tint_color(self.color, 0.84), points)
        pygame.draw.circle(surface, WHITE, self.pos, max(5, int(8 * scale)))

    def draw_core_machine_boss(self, surface):
        scale = depth_scale(self.pos.y)
        x, y = self.pos.x, self.pos.y
        r = int(self.radius * scale)
        pulse = 0.5 + 0.5 * math.sin(self.timer * 7.0)
        draw_ellipse_shadow(surface, self.pos, self.radius, 145, 2.7, 0.52)
        pygame.draw.circle(surface, (10, 16, 28), self.pos, r + 20)
        pygame.draw.circle(surface, (35, 55, 80), self.pos, r + 14, 7)
        for angle in range(0, 360, 60):
            d = pygame.Vector2(1, 0).rotate(angle)
            p1 = pygame.Vector2(x, y) + d * (r * 0.55)
            p2 = pygame.Vector2(x, y) + d * (r * 1.38)
            pygame.draw.line(surface, (95, 160, 255), p1, p2, max(3, int(5 * scale)))
            pygame.draw.circle(surface, (20, 34, 54), p2, max(8, int(12 * scale)))
        pygame.draw.circle(surface, (80, 150, 255), self.pos, max(18, int((24 + pulse * 6) * scale)))
        pygame.draw.circle(surface, WHITE, self.pos, max(6, int(8 * scale)))

    def draw_dark_beast_boss(self, surface):
        scale = depth_scale(self.pos.y)
        x, y = self.pos.x, self.pos.y
        r = int(self.radius * scale)
        bob = math.sin(self.timer * 4.5) * 3
        draw_ellipse_shadow(surface, self.pos, self.radius, 155, 2.6, 0.55)
        body = pygame.Rect(0, 0, int(r * 2.3), int(r * 1.35))
        body.center = (int(x), int(y + bob))
        pygame.draw.ellipse(surface, (26, 20, 28), body)
        pygame.draw.ellipse(surface, (92, 30, 42), body, max(3, int(4 * scale)))
        head = pygame.Rect(0, 0, int(r * 1.18), int(r * 0.95))
        head.center = (int(x), int(y - r * 0.55 + bob))
        pygame.draw.ellipse(surface, (35, 28, 38), head)
        pygame.draw.polygon(surface, (70, 26, 34), [(x - r * 0.36, y - r * 0.95 + bob), (x - r * 0.78, y - r * 1.42 + bob), (x - r * 0.12, y - r * 1.12 + bob)])
        pygame.draw.polygon(surface, (70, 26, 34), [(x + r * 0.36, y - r * 0.95 + bob), (x + r * 0.78, y - r * 1.42 + bob), (x + r * 0.12, y - r * 1.12 + bob)])
        pygame.draw.circle(surface, (255, 75, 75), (int(x - r * 0.22), int(y - r * 0.60 + bob)), max(4, int(6 * scale)))
        pygame.draw.circle(surface, (255, 75, 75), (int(x + r * 0.22), int(y - r * 0.60 + bob)), max(4, int(6 * scale)))
        for side in (-1, 1):
            pygame.draw.line(surface, (155, 52, 54), (x + side * r * 0.35, y + r * 0.25 + bob), (x + side * r * 0.92, y + r * 0.72 + bob), max(4, int(6 * scale)))

    def draw_final_core_boss(self, surface):
        scale = depth_scale(self.pos.y)
        x, y = self.pos.x, self.pos.y
        r = int(self.radius * scale)
        pulse = 0.5 + 0.5 * math.sin(self.timer * 6.0)
        draw_ellipse_shadow(surface, self.pos, self.radius, 150, 2.75, 0.52)
        for angle in range(0, 360, 45):
            d = pygame.Vector2(1, 0).rotate(angle + self.timer * 20)
            p1 = pygame.Vector2(x, y) + d * (r * 0.85)
            p2 = pygame.Vector2(x, y) + d * (r * 1.45)
            pygame.draw.line(surface, (150, 35, 55), p1, p2, max(2, int(4 * scale)))
        points = []
        for i in range(6):
            angle = -math.pi / 2 + i * math.tau / 6 + self.timer * 0.45
            points.append((x + math.cos(angle) * r, y + math.sin(angle) * r))
        pygame.draw.polygon(surface, (38, 24, 34), points)
        pygame.draw.polygon(surface, (230, 70, 85), points, max(4, int(5 * scale)))
        pygame.draw.circle(surface, (255, 95, 110), self.pos, max(18, int((24 + pulse * 10) * scale)))
        pygame.draw.circle(surface, WHITE, self.pos, max(6, int(8 * scale)))

    def draw(self, surface, font):
        if self.floor == INFERNO_LIGER_FLOOR:
            current_img = self.get_current_skin_image()
            if current_img is not None:
                self.draw_image_boss(surface, current_img)
            else:
                self.draw_code_boss(surface)
            if self.phase2:
                draw_text(surface, font, "LIGER-X11이 완전히 폭주합니다!", WIDTH // 2, 106, (255, 120, 40), center=True)
            draw_bar(surface, WIDTH // 2 - 260, 82, 520, 16, self.hp, self.max_hp, self.color)
            draw_text(surface, font, f"11층 보스 - {self.name}  HP {int(self.hp)}/{self.max_hp}", WIDTH // 2, 54, WHITE, center=True)
            return
        if self.floor == ICE_DRAGON_FLOOR:
            self.draw_floor15(surface, font)
            return
        current_img = self.get_current_skin_image()
        if current_img is not None:
            self.draw_image_boss(surface, current_img)
        else:
            self.draw_code_boss(surface)
        draw_bar(surface, WIDTH // 2 - 260, 82, 520, 16, self.hp, self.max_hp, self.color)
        draw_text(surface, font, self.name, WIDTH // 2, 54, WHITE, center=True)

    def draw_floor15(self, surface, font):
        x, y = self.pos.x, self.pos.y
        scale = depth_scale(self.pos.y)
        pulse = 0.5 + 0.5 * math.sin(self.timer * 5.0)
        aura_radius = int((76 + pulse * 12 + (18 if self.phase2 else 0)) * scale)

        draw_ellipse_shadow(surface, self.pos, self.radius, 150, 2.9, 0.56)
        aura = pygame.Surface((aura_radius * 2 + 8, aura_radius * 2 + 8), pygame.SRCALPHA)
        pygame.draw.circle(aura, (160, 60, 235, 48), (aura_radius + 4, aura_radius + 4), aura_radius, 5)
        pygame.draw.circle(aura, (120, 230, 80, 26), (aura_radius + 4, aura_radius + 4), max(8, aura_radius - 18), 2)
        surface.blit(aura, (x - aura_radius - 4, y - aura_radius - 38))

        sprite = self.get_floor15_frame()
        if sprite:
            bob = math.sin(self.timer * 4.0) * 4
            draw_sprite = sprite
            if abs(scale - 1.0) > 0.03:
                cache_key = (id(sprite), round(scale, 2))
                draw_sprite = self.floor15_scaled_cache.get(cache_key)
                if draw_sprite is None:
                    draw_sprite = pygame.transform.smoothscale(sprite, (max(1, int(sprite.get_width() * scale)), max(1, int(sprite.get_height() * scale))))
                    if len(self.floor15_scaled_cache) > 18:
                        self.floor15_scaled_cache.clear()
                    self.floor15_scaled_cache[cache_key] = draw_sprite
            rect = draw_sprite.get_rect(midbottom=(x, y + 28 * scale + bob))
            surface.blit(draw_sprite, rect)
        else:
            self.draw_floor15_fallback(surface, scale)

        for i in range(6 if self.phase2 else 4):
            angle = self.timer * (1.6 + i * 0.12) + i * math.tau / 6
            orb_pos = pygame.Vector2(x + math.cos(angle) * (62 + i * 4), y - 70 + math.sin(angle * 1.4) * 18)
            pygame.draw.circle(surface, (120, 230, 80), orb_pos, 5)
            pygame.draw.circle(surface, (190, 85, 255), orb_pos, 9, 1)

        if self.phase2:
            draw_text(surface, font, "Ice Dragon이 2페이즈에 돌입합니다!", WIDTH // 2, 106, (105, 205, 255), center=True)
        draw_bar(surface, WIDTH // 2 - 260, 82, 520, 16, self.hp, self.max_hp, self.color)
        draw_text(surface, font, f"16층 보스 - {self.name}  HP {int(self.hp)}/{self.max_hp}", WIDTH // 2, 54, WHITE, center=True)

    def draw_floor15_fallback(self, surface, scale=1.0):
        x, y = self.pos.x, self.pos.y
        bob = math.sin(self.timer * 4.0) * 4
        cloak_dark = (22, 18, 28)
        cloak_edge = (75, 42, 95)
        glow = (185, 75, 255)
        poison = (120, 230, 80)

        cloak = [ (x - 72 * scale, y + 38 * scale + bob), (x + 72 * scale, y + 38 * scale + bob), (x + 43 * scale, y - 72 * scale + bob), (x + 20 * scale, y - 104 * scale + bob), (x - 20 * scale, y - 104 * scale + bob), (x - 43 * scale, y - 72 * scale + bob), ]
        pygame.draw.polygon(surface, cloak_dark, cloak)
        pygame.draw.lines(surface, cloak_edge, True, cloak, 3)
        pygame.draw.polygon(surface, (36, 32, 42), [(x - 38, y + 32 + bob), (x + 38, y + 32 + bob), (x + 26, y - 60 + bob), (x - 26, y - 60 + bob)])

        pygame.draw.circle(surface, (28, 22, 34), (x, y - 98 + bob), 27)
        pygame.draw.polygon(surface, (34, 30, 40), [(x - 18, y - 105 + bob), (x - 48, y - 130 + bob), (x - 28, y - 92 + bob)])
        pygame.draw.polygon(surface, (34, 30, 40), [(x + 18, y - 105 + bob), (x + 48, y - 130 + bob), (x + 28, y - 92 + bob)])
        pygame.draw.circle(surface, glow, (x - 9, y - 100 + bob), 5)
        pygame.draw.circle(surface, glow, (x + 9, y - 100 + bob), 5)
        pygame.draw.circle(surface, poison, (x, y - 28 + bob), 15)
        pygame.draw.circle(surface, glow, (x, y - 28 + bob), 24, 3)

        left_hand = pygame.Vector2(x - 54, y - 22 + bob)
        right_hand = pygame.Vector2(x + 58, y - 28 + bob)
        pygame.draw.line(surface, cloak_edge, (x - 23, y - 46 + bob), left_hand, 8)
        pygame.draw.line(surface, cloak_edge, (x + 24, y - 44 + bob), right_hand, 8)
        pygame.draw.circle(surface, glow, left_hand, 12)
        pygame.draw.circle(surface, poison, left_hand, 5)

        staff_tip = pygame.Vector2(x + 86, y - 115 + bob)
        pygame.draw.line(surface, (30, 22, 38), right_hand, staff_tip, 8)
        pygame.draw.circle(surface, glow, staff_tip, 16)
        pygame.draw.circle(surface, WHITE, staff_tip, 5)

        for i in range(5):
            offset = math.sin(self.timer * 3 + i) * 7
            wisp_x = x - 64 + i * 32
            pygame.draw.circle(surface, (140, 70, 210), (wisp_x + offset, y + 18 - i * 9 + bob), 5, 1)

class Upgrade:
    POOL = [ ("체력 강화", "최대 체력 +20", "max_hp"), ("공격력 강화", "근접 및 스킬 피해 증가", "damage"), ("신속한 회피", "대시 쿨타임 감소", "dash"), ("전투 집중", "스킬 쿨타임 감소", "special"), ("응급 회복", "층 클리어 시 체력 회복량 증가", "regen"), ("흡혈 코어", "적 처치 시 체력 3 회복", "lifesteal"), ("과부하 칼날", "공격력 증가, 받는 피해 소폭 증가", "glass"), ("방탄 인피", "받는 피해 감소", "armor"), ("궁극기 충전", "공격 시 궁극기 게이지 추가 증가", "ultimate"), ("쌍검 공격", "근접 공격 피해 추가 증가", "double"), ]

    def __init__(self, name, desc, code):
        self.name = name
        self.desc = desc
        self.code = code

    @classmethod
    def random_choices(cls, count=3):
        picks = random.sample(cls.POOL, count)
        return [Upgrade(*p) for p in picks]

    def apply(self, player):
        player.upgrades.append(self.name)
        if self.code == "max_hp":
            player.max_hp += 20
            player.hp += 20
        elif self.code == "damage":
            player.attack_damage += 6
        elif self.code == "dash":
            player.dash_cooldown_max = max(0.55, player.dash_cooldown_max - 0.18)
        elif self.code == "special":
            player.special_cooldown_max = max(0.9, player.special_cooldown_max - 0.25)
        elif self.code == "regen":
            player.heal(28)
        elif self.code == "lifesteal":
            player.heal(12)
        elif self.code == "glass":
            player.attack_damage += 9
            player.damage_reduce -= 0.05
        elif self.code == "armor":
            player.damage_reduce = min(0.45, player.damage_reduce + 0.08)
        elif self.code == "ultimate":
            player.gain_ultimate(45)
        elif self.code == "double":
            player.attack_damage += 7

class SpecialItem:
    POOL = [ ("시간 균열 코어", "저스트 회피 반격 시간이 늘고 피해와 궁극기 충전이 증가합니다.", "time_core"), ("자동 방어막", "12초마다 피해를 1회 완전히 막는 보호막을 준비합니다.", "auto_shield"), ("피의 계약", "최대 체력 -20, 공격력 크게 증가, 적 처치 시 회복합니다.", "blood_pact"), ("망령 칼날", "근접 공격 시 확률적으로 가까운 적을 향해 유도 칼날을 발사합니다.", "ghost_blade"), ("전기 과부하", "스킬 사용 시 주변 적에게 연쇄 번개 피해를 줍니다.", "electric_overload"), ("독성 발자국", "대시 도착 지점에 적에게 피해를 주는 독성 장판을 남깁니다.", "toxic_dash"), ("사신의 표식", "보스에게 공격을 맞히면 표식이 쌓이고 5개마다 추가 폭발 피해를 줍니다.", "reaper_mark"), ("긴급 주사기", "체력이 30 이하로 떨어지면 한 번 자동으로 25 회복합니다.", "emergency_syringe"), ("불안정한 코어", "궁극기 피해가 증가하지만 궁극기 사용 직후 잠시 받는 피해가 늘어납니다.", "unstable_core"), ("평각 렌치", "스킬 쿨타임이 줄어들고 스킬 적중 보상이 좋아집니다.", "focus_wrench"), ]

    def __init__(self, name, desc, code):
        self.name = name
        self.desc = desc
        self.code = code

    @classmethod
    def random_choices(cls, player, count=3):
        owned = set(player.special_items)
        available = [item for item in cls.POOL if item[0] not in owned]
        if len(available) < count:
            available = cls.POOL
        return [SpecialItem(*item) for item in random.sample(available, min(count, len(available)))]

    def apply(self, player):
        if self.name not in player.special_items:
            player.special_items.append(self.name)
        player.special_item_flags[self.code] = True
        if self.code == "auto_shield":
            player.auto_shield_ready = True
            player.auto_shield_timer = 0
        elif self.code == "blood_pact":
            player.max_hp = max(45, player.max_hp - 20)
            player.hp = min(player.hp, player.max_hp)
            player.attack_damage += 14
        elif self.code == "focus_wrench":
            player.special_cooldown_max = max(0.75, player.special_cooldown_max - 0.35)
        elif self.code == "unstable_core":
            player.gain_ultimate(35)

def load_pet_image(code, size=(42, 42)):
    key = (code, size)
    if key in PET_IMAGE_CACHE:
        return PET_IMAGE_CACHE[key]
    pet = PET_DEFS.get(code)
    if not pet:
        PET_IMAGE_CACHE[key] = None
        return None
    names = []
    if code == "zone":
        names.append(pet.get("image"))
        names.extend(pet.get("fallback_images", ["pet_zone.png", "zone_pet.png"]))
    else:
        names.append(pet.get("image"))
    if code == "attack":
        names.append("pet_range.png")
    candidates = []
    for name in names:
        if name:
            candidates.extend([name, os.path.join("assets", name), f"{name}.png", os.path.join("assets", f"{name}.png")])
    path = find_asset_path(*candidates)
    image = None
    if path:
        try:
            image = pygame.image.load(path)
            image = image.convert_alpha() if pygame.display.get_surface() else image.copy()
            image = trim_transparent(remove_white_background(image), padding=4)
            image = pygame.transform.smoothscale(image, size)
        except (pygame.error, OSError, ValueError):
            image = None
    PET_IMAGE_CACHE[key] = image
    return image

class CompanionPet:
    DATA = {code: (data["name"], data["desc"], data["color"]) for code, data in PET_DEFS.items()}

    def __init__(self, code):
        self.code = code
        self.data = PET_DEFS[code]
        self.name, self.desc, self.color = self.DATA[code]
        self.pos = pygame.Vector2(WIDTH // 2, COMBAT_BOTTOM - 70)
        self.timer = random.uniform(0.8, 1.6)
        self.float_timer = random.random() * 10
        self.icon = load_pet_image(code)
        if self.code == "zone":
            self.timer = 0.0

    def update(self, dt, player, room, index=0, total=1):
        self.float_timer += dt
        angle = self.float_timer * 1.8 + index * (math.tau / max(1, total))
        side = -1 if player.last_dir.x >= 0 else 1
        offset = pygame.Vector2(side * (42 + index * 18), -28 + math.sin(angle) * 7)
        if total > 1:
            offset.x += math.cos(angle) * 14
        target = player.pos + offset
        self.pos += (target - self.pos) * min(1.0, dt * 6.8)

        self.timer -= dt
        if self.code == "heal":
            if self.timer <= 0:
                self.timer = 5.8
                if player.hp < player.max_hp:
                    player.heal(3 + player.hp_regen_amount_bonus)
                    room.effects.append(Effect(self.pos.x, self.pos.y, 34, self.color, 0.35))
        elif self.code == "attack":
            if self.timer <= 0:
                self.timer = 3.4
                room.effects.append(Effect(self.pos.x, self.pos.y, 42, self.color, 0.32))
        elif self.code == "zone":
            if self.timer <= 0:
                self.timer += float(self.data.get("zone_tick_interval", 0.35))
                radius = float(self.data.get("zone_radius", 120))
                damage = float(self.data.get("zone_damage", 8))
                damage_dealt = 0.0
                for enemy in room.enemies:
                    if not enemy.dead and distance(player.pos, enemy.pos) <= radius:
                        enemy.take_damage(damage)
                        damage_dealt += damage
                boss = room.boss
                if boss and not boss.dead:
                    boss_center = pygame.Vector2(boss.hitbox.center)
                    if distance(player.pos, boss_center) <= radius:
                        boss_damage = float(self.data.get("zone_boss_damage", damage * 0.5))
                        boss.take_damage(boss_damage)
                        damage_dealt += boss_damage
                if damage_dealt > 0 and player.zone_lifesteal > 0:
                    player.heal(damage_dealt * player.zone_lifesteal)

    def draw(self, surface):
        draw_ellipse_shadow(surface, self.pos, 10, 64, 1.9, 0.42)
        bob = math.sin(self.float_timer * 6) * 2
        center = (int(self.pos.x), int(self.pos.y + bob))
        if self.icon:
            surface.blit(self.icon, self.icon.get_rect(center=center))
            return
        pygame.draw.circle(surface, (8, 16, 18), center, 13)
        pygame.draw.circle(surface, self.color, center, 11)
        pygame.draw.circle(surface, WHITE, (center[0] - 3, center[1] - 3), 3)
        if self.code == "heal":
            pygame.draw.rect(surface, WHITE, (center[0] - 2, center[1] - 8, 4, 16), border_radius=2)
            pygame.draw.rect(surface, WHITE, (center[0] - 8, center[1] - 2, 16, 4), border_radius=2)
        elif self.code == "attack":
            pygame.draw.circle(surface, (255, 240, 150), center, 15, 2)
        elif self.code == "zone":
            pygame.draw.circle(surface, WHITE, center, 15, 2)

def draw_lumizone_aura(surface, player):
    if player.selected_pet_type != "zone":
        return
    data = PET_DEFS["zone"]
    radius = int(data.get("zone_radius", 120))
    color = data.get("zone_color", (160, 70, 255))
    alpha = int(data.get("zone_alpha", 80))
    pulse = 0.5 + 0.5 * math.sin(pygame.time.get_ticks() * 0.0045)
    aura = pygame.Surface((radius * 2 + 24, radius + 36), pygame.SRCALPHA)
    center = (aura.get_width() // 2, aura.get_height() // 2)
    rect = pygame.Rect(12, 12, radius * 2, radius)
    pygame.draw.ellipse(aura, (*color, alpha), rect)
    pygame.draw.ellipse(aura, (*color, int(alpha * 0.72)), rect, 3)
    inner = rect.inflate(-24 - int(pulse * 8), -14 - int(pulse * 5))
    pygame.draw.ellipse(aura, (220, 170, 255, int(28 + pulse * 22)), inner, 2)
    glow_radius = 9 + int(pulse * 3)
    pygame.draw.circle(aura, (235, 205, 255, int(42 + pulse * 24)), center, glow_radius)
    surface.blit(aura, aura.get_rect(center=(int(player.pos.x), int(player.pos.y + 8))))

class PetReward:
    POOL = [(data["name"], data["desc"], code) for code, data in PET_DEFS.items()]

    def __init__(self, name, desc, code):
        self.name = name
        self.desc = desc
        self.code = code

    @classmethod
    def random_choices(cls, player, count=3):
        return [PetReward(data["name"], data["desc"], code) for code, data in PET_DEFS.items()]

    def apply(self, player):
        player.pet_names.clear()
        player.pets.clear()
        player.selected_pet_type = self.code
        player.selected_pet_data = PET_DEFS[self.code]
        player.pet_names.append(self.name)
        player.pets.append(CompanionPet(self.code))
        apply_pet_passive_stats(player, self.code)

def apply_pet_passive_stats(player, code):
    data = PET_DEFS.get(code)
    if not data:
        return
    player.hp_regen_rate_bonus = float(data.get("hp_regen_rate_bonus", 0.0))
    player.hp_regen_amount_bonus = int(data.get("hp_regen_amount_bonus", 0))
    player.stage_clear_heal = int(data.get("stage_clear_heal", 0))
    player.attack_range_bonus = int(data.get("attack_range_bonus", 0))
    player.attack_damage_bonus = int(data.get("attack_damage_bonus", 0))
    player.attack_speed_bonus = float(data.get("attack_speed_bonus", 0.0))
    player.zone_radius_bonus = int(data.get("zone_radius_bonus", 0))
    player.zone_damage_bonus = int(data.get("zone_damage_bonus", 0))
    player.zone_lifesteal = float(data.get("zone_lifesteal", 0.0))

class Shop:
    ITEMS = [ ("체력 30 회복", 30, "heal"), ("공격력 +3", 50, "damage"), ("최대 체력 +15", 60, "max_hp"), ("스킬 쿨타임 감소", 50, "special"), ("궁극기 게이지 +40", 40, "ultimate"), ]

    @classmethod
    def random_items(cls):
        return random.sample(cls.ITEMS, 3)

    @staticmethod
    def buy(item, player):
        name, cost, code = item
        if player.gold < cost:
            return False
        player.gold -= cost
        if code == "heal":
            player.heal(30)
        elif code == "damage":
            player.attack_damage += 3
        elif code == "max_hp":
            player.max_hp += 15
            player.hp += 15
        elif code == "special":
            player.special_cooldown_max = max(0.8, player.special_cooldown_max - 0.25)
        elif code == "ultimate":
            player.gain_ultimate(40)
        return True

class Room:
    def __init__(self, floor, room_type):
        self.floor = floor
        self.room_type = room_type
        self.zone_name, self.zone_desc, self.zone_color = get_zone_info(floor)
        self.bg_key = get_background_key(floor)
        if room_type in (ROOM_REWARD, ROOM_REST):
            self.bg_key = get_normal_stage_background_key_for_floor(floor)
        if room_type in (ROOM_BOSS, ROOM_FINAL):
            if floor == INFERNO_LIGER_FLOOR:
                self.bg_key = "inferno_stage_11"
                self.world_width = INFERNO_LIGER_WORLD_WIDTH
                self.world_height = INFERNO_LIGER_WORLD_HEIGHT
                self.walkable_polygon = make_ratio_polygon(self.world_width, self.world_height, INFERNO_LIGER_WALKABLE_POLYGON_RATIO)
                ys = [point[1] for point in self.walkable_polygon]
                self.floor_top_y = min(ys)
                self.floor_bottom_y = max(ys)
            elif floor == ICE_DRAGON_FLOOR:
                self.bg_key = "ice_dragon_stage"
                self.world_width = ICE_DRAGON_WORLD_WIDTH
                self.world_height = ICE_DRAGON_WORLD_HEIGHT
                self.walkable_polygon = make_ice_dragon_walkable_polygon(self.world_width, self.world_height)
                self.ice_arena_cx, self.ice_arena_cy, self.ice_arena_r = get_ice_dragon_arena_values( self.world_width, self.world_height, )
                ys = [point[1] for point in self.walkable_polygon]
                self.floor_top_y = self.ice_arena_cy
                self.floor_bottom_y = max(ys)
            else:
                self.world_width = 2400
                self.world_height = 1300
                self.floor_top_y = FLOOR_TOP_Y
                self.floor_bottom_y = FLOOR_BOTTOM_Y
                self.walkable_polygon = [ (230, self.floor_bottom_y), (2170, self.floor_bottom_y), (1650, self.floor_top_y), (750, self.floor_top_y), ]
            self.movement_mode = "floor_depth"
            self.stair_zones = []
        elif room_type in (ROOM_REWARD, ROOM_SHOP, ROOM_REST):
            self.world_width = WIDTH
            self.world_height = HEIGHT
            self.floor_top_y = COMBAT_TOP
            self.floor_bottom_y = COMBAT_BOTTOM
            self.walkable_polygon = [ (40, COMBAT_BOTTOM), (WIDTH - 40, COMBAT_BOTTOM), (WIDTH - 40, COMBAT_TOP), (40, COMBAT_TOP), ]
            self.movement_mode = "fixed_room"
            self.stair_zones = []
        else:
            self.world_width = 2200
            self.world_height = 1300
            self.floor_top_y = FLOOR_TOP_Y
            self.floor_bottom_y = FLOOR_BOTTOM_Y
            self.walkable_polygon = [ (215, self.floor_bottom_y), (1985, self.floor_bottom_y), (1515, self.floor_top_y), (685, self.floor_top_y), ]
            self.movement_mode = "floor_depth"
            self.stair_zones = []
            if is_stage_20_16_combat_room(floor, room_type):
                self.bg_key = "stage_20_16"
                self.walkable_polygon = make_ratio_polygon( self.world_width, self.world_height, STAGE_20_16_WALKABLE_POLYGON_RATIO, )
                ys = [point[1] for point in self.walkable_polygon]
                self.floor_top_y = min(ys)
                self.floor_bottom_y = max(ys)
            elif floor <= 15:
                self.walkable_polygon = make_ratio_polygon( self.world_width, self.world_height, STAGE_20_16_WALKABLE_POLYGON_RATIO, )
                ys = [point[1] for point in self.walkable_polygon]
                self.floor_top_y = min(ys)
                self.floor_bottom_y = max(ys)
        xs = [p[0] for p in self.walkable_polygon]
        ys = [p[1] for p in self.walkable_polygon]
        self.arena_rect = pygame.Rect(min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))
        self.enemies = []
        self.projectiles = []
        self.traps = []
        self.effects = []
        self.boss = None
        self.cleared = False
        self.timer = 0
        self.spawn_timer = 1.0
        self.survival_goal = 15.0
        self.clear_delay = 0

    def setup(self):
        level = 21 - self.floor
        if self.room_type in (ROOM_BOSS, ROOM_FINAL):
            self.boss = Boss(self.floor)
            self.boss.set_arena(self.arena_rect, self.walkable_polygon, self.floor_top_y, self.floor_bottom_y)
            if self.floor not in (ICE_DRAGON_FLOOR, INFERNO_LIGER_FLOOR):
                self.spawn_enemies(random.randint(1, 2), level)
        elif self.room_type == ROOM_NORMAL:
            if self.floor == 20:
                count = random.randint(2, 3)
            elif 18 <= self.floor <= 19:
                count = random.randint(3, 4)
            elif 16 <= self.floor <= 17:
                count = random.randint(3, 4)
            else:
                count = random.randint(4, 6)
            self.spawn_enemies(count, level)
        elif self.room_type == ROOM_ELITE:
            count = 7 if 7 <= self.floor <= 9 or 2 <= self.floor <= 4 else random.randint(1, 2)
            self.spawn_enemies(count, level, elite=True)
        elif self.room_type == ROOM_TRAP:
            self.spawn_traps(4 if self.floor >= 16 else 7, level)
            self.spawn_enemies(1 if self.floor >= 18 else random.randint(1, 2), level)
            self.survival_goal = 10.0
        elif self.room_type == ROOM_SURVIVAL:
            self.survival_goal = 15.0
        elif self.room_type in (ROOM_POISON, ROOM_WILD):
            self.spawn_traps(5, level, "독성")
            self.spawn_enemies(random.randint(2, 4), level)
        elif self.room_type in (ROOM_ELECTRIC, ROOM_EARTH):
            self.spawn_traps(5, level, "전기")
            self.spawn_enemies(random.randint(2, 4), level)

    def spawn_enemy(self, enemy_type=None):
        level = 21 - self.floor
        types = ["감염체", "경비 드론", "돌진 실험체", "방패병"]
        if self.floor == 20:
            weights = [8, 1, 0, 0]
        elif 18 <= self.floor <= 19:
            weights = [6, 2, 0.3, 0.1]
        elif 16 <= self.floor <= 17:
            weights = [5, 2, 0.8, 0.4]
        elif self.bg_key == "20_16":
            weights = [4, 2, 1, 1]
        elif self.bg_key == "15_11":
            weights = [3, 2, 2, 1]
        elif self.bg_key == "10_6":
            weights = [1, 4, 2, 2]
        else:
            weights = [2, 3, 3, 3]
        chosen = enemy_type or random.choices(types, weights=weights, k=1)[0]
        x, y = self.random_walkable_point(48)
        enemy = Enemy(chosen, x, y, level, self.bg_key, self.floor)
        if 7 <= self.floor <= 9:
            enemy.max_hp = int(enemy.max_hp * 1.3)
            enemy.hp = enemy.max_hp
        elif 2 <= self.floor <= 4:
            enemy.max_hp = int(enemy.max_hp * 1.5)
            enemy.hp = enemy.max_hp
        if (
            17 <= self.floor <= 20
            and self.room_type not in (ROOM_BOSS, ROOM_FINAL)
            and self.bg_key == "stage_20_16"
        ):
            enemy.use_ice_monster_sprite(random.choice(MONSTER_20_16_TYPES))
        elif (
            11 <= self.floor <= 15
            and self.room_type not in (ROOM_BOSS, ROOM_FINAL)
            and self.bg_key == "15_11"
        ):
            enemy.use_15_11_monster_sprite(random.choice(MONSTER_15_11_TYPES))
        elif (
            6 <= self.floor <= 10
            and self.room_type not in (ROOM_BOSS, ROOM_FINAL)
            and self.bg_key == "10_6"
        ):
            enemy.use_10_6_monster_sprite(random.choice(MONSTER_10_6_TYPES))
        elif (
            2 <= self.floor <= 5
            and self.room_type not in (ROOM_BOSS, ROOM_FINAL)
            and self.bg_key == "5_1"
        ):
            enemy.use_5_1_monster_sprite(random.choice(MONSTER_5_1_TYPES))
        self.enemies.append(enemy)

    def spawn_enemies(self, count, level, elite=False):
        for _ in range(count):
            chosen = "방패병" if elite else None
            self.spawn_enemy(chosen)

    def random_walkable_point(self, padding=24):
        if self.bg_key == "stage_20_16":
            for _ in range(80):
                x, y = get_random_point_in_walkable_polygon(self.walkable_polygon, self.floor_top_y, self.floor_bottom_y, padding)
                if self.world_width * 0.16 < x < self.world_width * 0.84 and self.floor_top_y + 30 < y < self.floor_bottom_y - 20:
                    return x, y
        return get_random_point_in_walkable_polygon(self.walkable_polygon, self.floor_top_y, self.floor_bottom_y, padding)

    def random_walkable_rect(self, w, h, padding=24):
        max_h = max(24, int(self.floor_bottom_y - self.floor_top_y - padding * 2))
        max_w = max(24, int(self.arena_rect.width - padding * 2))
        w = min(w, max_w)
        h = min(h, max_h)
        for _ in range(40):
            low_y = int(self.floor_top_y + h // 2 + padding)
            high_y = int(self.floor_bottom_y - h // 2 - padding)
            if low_y > high_y:
                break
            center_y = random.randint(low_y, high_y)
            left, right = polygon_x_bounds(center_y, self.walkable_polygon)
            if right - left <= w + padding * 2:
                continue
            x = random.randint(int(left + padding), int(right - w - padding))
            y = int(center_y - h // 2)
            rect = pygame.Rect(x, y, w, h)
            corners = [ (rect.left, rect.top), (rect.right, rect.top), (rect.left, rect.bottom), (rect.right, rect.bottom), ]
            if all(point_in_polygon(corner, self.walkable_polygon) for corner in corners):
                return rect
        x, y = self.random_walkable_point(padding + max(w, h) // 2)
        return pygame.Rect(int(x - w // 2), int(y - h // 2), w, h)

    def spawn_traps(self, count, level, forced=None):
        self.traps.clear()

    def update(self, dt, player, sounds):
        self.timer += dt
        for effect in self.effects:
            effect.update(dt)
        self.effects = [e for e in self.effects if not e.dead]
        if len(self.effects) > MAX_EFFECTS:
            self.effects = self.effects[-MAX_EFFECTS:]
        player.update_pets(dt, self)

        for trap in self.traps:
            trap.update(dt)
            if trap.friendly:
                for enemy in self.enemies:
                    if trap.hits_enemy(enemy):
                        enemy.take_damage(trap.damage * dt * 3.2)
                if self.boss and trap.hits_enemy(self.boss):
                    self.boss.take_damage(trap.damage * dt * 2.0)
                    player.on_boss_hit(self.boss, self.effects)
                continue
            if trap.hits_player(player):
                damage_result = player.take_damage(trap.damage)
                if damage_result == "hit":
                    sounds.play("hurt")
                elif damage_result == "dodged":
                    sounds.play("clear")
                elif damage_result == "shield":
                    sounds.play("clear")
                    self.effects.append(Effect(player.pos.x, player.pos.y, 58, CYAN, 0.28))
        self.traps = [trap for trap in self.traps if not trap.dead]

        for projectile in self.projectiles:
            projectile.update(dt, self.world_width, self.world_height)
        for projectile in self.projectiles:
            if projectile.dead:
                continue
            if projectile.owner == "enemy" and distance(projectile.pos, player.pos) < projectile.radius + player.radius:
                damage_result = player.take_damage(projectile.damage)
                if damage_result == "hit":
                    sounds.play("hurt")
                    projectile.dead = True
                elif damage_result == "dodged":
                    sounds.play("clear")
                    projectile.dead = True
                elif damage_result == "shield":
                    sounds.play("clear")
                    projectile.dead = True
                    self.effects.append(Effect(player.pos.x, player.pos.y, 58, CYAN, 0.28))
            elif projectile.owner == "player":
                for enemy in self.enemies:
                    if not enemy.dead and distance(projectile.pos, enemy.pos) < projectile.radius + enemy.radius:
                        enemy.take_damage(projectile.damage)
                        projectile.dead = True
                        player.gain_ultimate(9)
                        break
                boss_projectile_hit = False
                if self.boss and not self.boss.dead and getattr(self.boss, "floor", None) == ICE_DRAGON_FLOOR and hasattr(self.boss, "get_floor15_core_hitbox"):
                    boss_projectile_hit = self.boss.get_floor15_core_hitbox().collidepoint(projectile.pos.x, projectile.pos.y)
                elif self.boss and not self.boss.dead:
                    boss_projectile_hit = distance(projectile.pos, self.boss.pos) < projectile.radius + self.boss.radius
                if boss_projectile_hit:
                    self.boss.take_damage(projectile.damage)
                    player.on_boss_hit(self.boss, self.effects)
                    projectile.dead = True
                    player.gain_ultimate(10)
        self.projectiles = [p for p in self.projectiles if not p.dead]

        for enemy in self.enemies:
            enemy.update(dt, player, self.projectiles, self.effects, self.arena_rect, self.walkable_polygon)
            if distance(enemy.pos, player.pos) < enemy.radius + player.radius:
                damage_result = player.take_damage(enemy.damage)
                if damage_result == "hit":
                    sounds.play("hurt")
                elif damage_result == "dodged":
                    sounds.play("clear")
                elif damage_result == "shield":
                    sounds.play("clear")
                    self.effects.append(Effect(player.pos.x, player.pos.y, 58, CYAN, 0.28))
        before = len(self.enemies)
        self.enemies = [enemy for enemy in self.enemies if not enemy.dead]
        killed = before - len(self.enemies)
        if killed:
            player.gold += killed * random.randint(8, 14)
            player.gain_ultimate(killed * 6)
            if any(name == "흡혈 코어" for name in player.upgrades):
                player.heal(killed * 3)
            if player.special_item_flags.get("blood_pact"):
                player.heal(killed * 4)

        if self.boss:
            self.boss.update(dt, player, self.projectiles, self.traps, self.effects, self.spawn_enemy)
            if self.boss.dead:
                self.cleared = True

        if self.room_type == ROOM_SURVIVAL:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                self.spawn_timer = max(0.55, 2.0 - self.timer * 0.05)
                self.spawn_enemy()
            if self.timer >= self.survival_goal:
                self.cleared = True
        elif self.room_type == ROOM_TRAP:
            if self.timer >= self.survival_goal and not self.enemies:
                self.cleared = True
        elif self.room_type not in (ROOM_BOSS, ROOM_FINAL):
            if self.room_type in (ROOM_NORMAL, ROOM_ELITE, ROOM_POISON, ROOM_ELECTRIC, ROOM_WILD, ROOM_EARTH) and not self.enemies:
                self.cleared = True

    def draw_entities(self, surface, font, player=None):
        if player:
            draw_lumizone_aura(surface, player)
        if self.boss and hasattr(self.boss, "draw_warnings"):
            self.boss.draw_warnings(surface)
        for trap in self.traps:
            trap.draw(surface)
        for projectile in self.projectiles:
            projectile.draw(surface)

        actors = []
        for enemy in self.enemies:
            actors.append((enemy.pos.y, enemy.draw))
        if self.boss:
            actors.append((self.boss.pos.y, lambda target_surface, boss=self.boss: boss.draw(target_surface, font)))
        if player:
            for pet in player.pets:
                actors.append((pet.pos.y, pet.draw))
            actors.append((player.pos.y, player.draw))
        for _, draw_actor in sorted(actors, key=lambda item: item[0]):
            draw_actor(surface)

        for effect in self.effects:
            effect.draw(surface)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("시코어 생각: 20층 격리구역")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font_sm = make_font(18)
        self.font = make_font(24)
        self.font_md = make_font(34)
        self.font_lg = make_font(58)
        self.sounds = SoundBank()
        self.current_music = None
        self.music_tracks = {
            "title": find_asset_path(os.path.join("assets", "intro_bgm.mp3"), "intro_bgm.mp3"),
            "lobby": find_asset_path(os.path.join("assets", "lobby_bgm.mp3"), "lobby_bgm.mp3"),
            "floor": find_asset_path(os.path.join("assets", "floor_bgm.mp3"), "floor_bgm.mp3"),
            "death": find_asset_path(os.path.join("assets", "death_bgm.mp3"), "death_bgm.mp3"),
            "win": find_asset_path(os.path.join("assets", "ending_bgm.mp3"), "ending_bgm.mp3"),
        }
        self.game_data = load_game_data()
        self.high_score = max(load_high_score(), int(self.game_data.get("highest_score", 0)))
        self.game_data["highest_score"] = self.high_score
        self.game_data = save_game_data(self.game_data)
        self.reset_pet_for_run(save=True)
        self.backgrounds = self.load_backgrounds()
        self.lab_arena_image = self.load_lab_arena_image()
        self.effect_sprites = self.load_effect_sprites()
        self.title_image = self.load_title_image()
        self.ending_image = self.load_ending_image()
        self.lobby_image = self.load_lobby_image()
        self.world_backgrounds = {}
        self.preload_ice_dragon_world_background()
        self.boss15_assets = {}
        self.preload_entry_assets()
        self.camera = Camera()
        self.state = "title"
        self.show_controls_overlay = False
        self.title_buttons = { "start": pygame.Rect(132, 591, 205, 85), "characters": pygame.Rect(356, 591, 180, 85), "gacha": pygame.Rect(553, 591, 189, 85), "controls": pygame.Rect(760, 591, 173, 85), "quit": pygame.Rect(949, 591, 191, 85), "close_controls": pygame.Rect(WIDTH // 2 - 90, HEIGHT // 2 + 174, 180, 42), }
        self.gacha_buttons = { "normal": pygame.Rect(WIDTH // 2 - 335, 560, 210, 48), "premium": pygame.Rect(WIDTH // 2 - 105, 560, 210, 48), "back": pygame.Rect(WIDTH // 2 + 125, 560, 210, 48), }
        self.character_card_rects = []
        self.gacha_result = None
        self.menu_message = ""
        self.run_reward_log = []
        self.ticket_rewards_claimed = set()
        self.message = ""
        self.message_timer = 0
        self.announcement_timer = 0
        self.transition_timer = 0
        self.clear_timer = 0
        self.slow_timer = 0
        self.upgrade_choices = []
        self.special_choices = []
        self.pet_choices = []
        self.pet_reward_rects = []
        self.pending_boss_upgrade = False
        self.shop_items = []
        self.rooms = {}
        self.player = Player(self.game_data.get("selected_character_id", STARTER_CHARACTER_ID))
        self.current_floor = 20
        self.current_room = None
        self.room_started = False
        self.score = 0
        self.best_updated = False
        self.debug_camera = False
        self.lobby_interactables = []
        self.room_interactables = []
        self.active_prompt = None
        self.menu_return_state = "title"
        self.final_exit_ready = False
        self.floor_transition_timer = 0
        self.environment_particles = [EnvironmentParticle(get_background_key(self.current_floor)) for _ in range(20)]

    def load_title_image(self):
        path = find_asset_path(os.path.join("assets", "시작.png"), "시작.png", os.path.join("assets", "n.png"), "n.png")
        if not path:
            print("n.png 없음: 기존 기본 타이틀 화면 사용")
            return None
        try:
            image = pygame.image.load(path).convert()
            print("타이틀 이미지 로드 성공:", path)
            return scale_cover(image, (WIDTH, HEIGHT))
        except (pygame.error, OSError) as exc:
            print("n.png 로드 실패: 기존 기본 타이틀 화면 사용", exc)
            return None

    def load_ending_image(self):
        path = find_asset_path(os.path.join("assets", "ending_true.png"), "ending_true.png", os.path.join("assets", "ending_true.jpg"), "ending_true.jpg", os.path.join("assets", "엔딩1.jpg"), "엔딩1.jpg")
        if not path:
            return None
        try:
            image = pygame.image.load(path).convert()
            return scale_cover(image, (WIDTH, HEIGHT))
        except (pygame.error, OSError) as exc:
            print("ending image load failed:", exc)
            return None

    def update_music(self):
        if self.state == "title":
            target = "title"
        elif self.state == "lab_lobby":
            target = "lobby"
        elif self.state == "win":
            target = "win"
        elif self.state == "game_over":
            target = "death"
        elif self.state in ("playing", "floor_transition", "upgrade", "special_reward", "pet_reward", "shop"):
            target = "floor"
        else:
            target = None
        if target == self.current_music:
            return
        self.current_music = target
        try:
            pygame.mixer.music.stop()
            if target and self.music_tracks.get(target):
                pygame.mixer.music.load(self.music_tracks[target])
                pygame.mixer.music.set_volume(0.45)
                pygame.mixer.music.play(-1)
        except pygame.error:
            self.current_music = None

    def draw_title_button(self, text, rect, mouse_pos):
        hovered = rect.collidepoint(mouse_pos)
        fill = (26, 34, 48) if not hovered else (38, 50, 70)
        border = CYAN if not hovered else YELLOW
        pygame.draw.rect(self.screen, fill, rect, border_radius=8)
        pygame.draw.rect(self.screen, border, rect, 2, border_radius=8)
        draw_text(self.screen, self.font, text, rect.centerx, rect.centery - 10, WHITE, center=True)

    def draw_controls_overlay(self, mouse_pos=None):
        mouse_pos = mouse_pos or pygame.mouse.get_pos()
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 178))
        self.screen.blit(overlay, (0, 0))

        panel = pygame.Rect(WIDTH // 2 - 360, HEIGHT // 2 - 235, 720, 470)
        pygame.draw.rect(self.screen, (14, 18, 26), panel, border_radius=8)
        pygame.draw.rect(self.screen, CYAN, panel, 2, border_radius=8)
        draw_text(self.screen, self.font_md, "조작법", panel.centerx, panel.y + 34, CYAN, center=True)

        lines = [
            "방향키 / 이동: W A S D",
            "J: 기본공격",
            "K: 스킬",
            "L: 궁극기",
            "Space bar: 대쉬",
            "상호작용/선택: ENTER",
            "가챠/캐릭터 화면: 숫자키 또는 마우스 클릭",
            "뒤로가기: ESC 또는 뒤로 버튼",
        ]
        y = panel.y + 92
        for line in lines:
            draw_text(self.screen, self.font, line, panel.x + 60, y, WHITE)
            y += 40

        close_rect = self.title_buttons["close_controls"]
        self.draw_title_button("닫기", close_rect, mouse_pos)

    def load_effect_sprites(self):
        path = find_asset_path(os.path.join("assets", "eff.png"), "eff.png")
        if not path:
            print("eff.png 없음: 기존 도형 이펙트 사용")
            return None
        try:
            sheet = pygame.image.load(path).convert_alpha()
            crop_defs = { "attack": [ (0.42, 0.12, 0.50, 0.28), (0.63, 0.20, 0.78, 0.32), (0.88, 0.14, 0.98, 0.34), ], "skill": [ (0.20, 0.35, 0.42, 0.57), (0.43, 0.35, 0.66, 0.57), (0.67, 0.35, 0.95, 0.57), ], "ultimate": [ (0.18, 0.61, 0.42, 0.95), (0.43, 0.61, 0.68, 0.95), (0.69, 0.61, 0.97, 0.95), ], }
            target_heights = {"attack": 118, "ultimate": 420}
            sprites = {}
            for key, crops in crop_defs.items():
                frames = []
                for crop in crops:
                    frame = crop_by_ratio(sheet, *crop)
                    frame = trim_transparent(remove_effect_sheet_background(frame), padding=8)
                    if frame.get_bounding_rect(min_alpha=10).width <= 1:
                        raise ValueError("empty effect frame")
                    if key == "skill":
                        scale = 170 / max(1, max(frame.get_width(), frame.get_height()))
                        width = max(24, int(frame.get_width() * scale))
                        height = max(24, int(frame.get_height() * scale))
                    else:
                        height = target_heights[key]
                        width = max(24, int(frame.get_width() * height / max(1, frame.get_height())))
                    scaled = pygame.transform.smoothscale(frame, (width, height))
                    fade = 0.08 if key == "attack" else (0.06 if key == "ultimate" else 0.13)
                    frames.append(apply_edge_fade(scaled, fade))
                sprites[key] = frames
            print("이펙트 시트 로드 성공:", path)
            return sprites
        except (pygame.error, OSError, ValueError) as exc:
            print("eff.png 로드 실패: 기존 도형 이펙트 사용", exc)
            return None

    def load_backgrounds(self):
        loaded = {}
        loose_backgrounds = [ path for path in list_asset_images() if is_valid_background_filename(path) ]
        for key, filename in BACKGROUND_IMAGES.items():
            candidates = []
            for alias in BACKGROUND_IMAGE_ALIASES.get(key, [filename]):
                candidates.extend([alias, os.path.join("assets", alias)])
            path = find_asset_path(*candidates)
            if path and not is_valid_background_filename(path):
                path = None
            if not path and key == "20_16" and loose_backgrounds:
                path = loose_backgrounds[0]
            if not path:
                if key == "boss_stage_15":
                    print("15층 보스방 배경 없음: 기존 보스방 배경 사용")
                if key == "stage_20_16":
                    print("20~16층 배경 없음: 기존 배경 사용")
                loaded[key] = None
                continue
            try:
                image = pygame.image.load(path).convert()
                if key == "boss_stage_15":
                    print("15층 보스방 배경 로드 성공:", path)
                if key == "stage_20_16":
                    print("20~16층 배경 로드 성공:", path)
                loaded[key] = image if key in ("boss_stage_15", "ice_dragon_stage") else scale_cover(image, (WIDTH, HEIGHT))
            except pygame.error:
                if key == "boss_stage_15":
                    print("15층 보스방 배경 없음: 기존 보스방 배경 사용")
                if key == "stage_20_16":
                    print("20~16층 배경 없음: 기존 배경 사용")
                loaded[key] = None
            except OSError:
                if key == "boss_stage_15":
                    print("15층 보스방 배경 없음: 기존 보스방 배경 사용")
                if key == "stage_20_16":
                    print("20~16층 배경 없음: 기존 배경 사용")
                loaded[key] = None
        return loaded

    def preload_boss15_world_background(self):
        base = self.backgrounds.get("boss_stage_15")
        if not base:
            return
        key = ("boss_stage_15", BOSS15_WORLD_WIDTH, BOSS15_WORLD_HEIGHT)
        if key not in self.world_backgrounds:
            self.world_backgrounds[key] = pygame.transform.smoothscale(base, (BOSS15_WORLD_WIDTH, BOSS15_WORLD_HEIGHT))
            print("15층 보스방 월드 배경 캐싱 완료")

    def preload_ice_dragon_world_background(self):
        key = ("ice_dragon_stage", ICE_DRAGON_WORLD_WIDTH, ICE_DRAGON_WORLD_HEIGHT)
        if key in self.world_backgrounds:
            return
        base = self.backgrounds.get("ice_dragon_stage")
        if base:
            self.world_backgrounds[key] = pygame.transform.smoothscale(base, (ICE_DRAGON_WORLD_WIDTH, ICE_DRAGON_WORLD_HEIGHT))
            print("16층 Ice Dragon 월드 배경 캐싱 완료")
        else:
            self.world_backgrounds[key] = self.create_ice_dragon_fallback_background(ICE_DRAGON_WORLD_WIDTH, ICE_DRAGON_WORLD_HEIGHT)
            print("16층 Ice Dragon fallback 배경 캐싱 완료")

    def preload_entry_assets(self):
        class DummyRoom:
            pass

        room_specs = [
            ("stage_20_16", 2200, 1300, 20, ROOM_NORMAL),
            ("ice_dragon_stage", ICE_DRAGON_WORLD_WIDTH, ICE_DRAGON_WORLD_HEIGHT, ICE_DRAGON_FLOOR, ROOM_BOSS),
            ("inferno_stage_11", INFERNO_LIGER_WORLD_WIDTH, INFERNO_LIGER_WORLD_HEIGHT, INFERNO_LIGER_FLOOR, ROOM_BOSS),
        ]
        if "FOREST_GUARDIAN_WORLD_WIDTH" in globals():
            room_specs.append(("forest_guardian_stage", FOREST_GUARDIAN_WORLD_WIDTH, FOREST_GUARDIAN_WORLD_HEIGHT, FOREST_GUARDIAN_FLOOR, ROOM_BOSS))
        if "FINAL_CORE_WORLD_WIDTH" in globals():
            room_specs.append(("final_core_stage", FINAL_CORE_WORLD_WIDTH, FINAL_CORE_WORLD_HEIGHT, FINAL_CORE_PATTERN_FLOOR, ROOM_FINAL))
        for bg_key, width, height, floor, room_type in room_specs:
            room = DummyRoom()
            room.bg_key = bg_key
            room.world_width = width
            room.world_height = height
            room.floor = floor
            room.room_type = room_type
            try:
                self.get_world_background(room)
            except Exception as exc:
                print(f"[WARN] preload background skipped: {bg_key} / {exc}")
        for loader in (
            load_monster_20_16_frames,
            load_monster_15_11_frames,
            load_monster_10_6_frames,
            load_monster_5_1_frames,
        ):
            try:
                loader()
            except Exception as exc:
                print(f"[WARN] preload monster skipped: {loader.__name__} / {exc}")

    def create_boss15_fallback_background(self, width, height):
        surface = pygame.Surface((width, height))
        surface.fill((6, 10, 16))
        for y in range(height):
            t = y / max(1, height - 1)
            pygame.draw.line(surface, (int(7 + 10 * t), int(12 + 20 * t), int(20 + 28 * t)), (0, y), (width, y))

        center_x = width // 2
        back_top = int(height * 0.12)
        floor_top = int(height * BOSS15_MAX_INNER_Y_RATIO)
        floor_bottom = int(height * 0.88)
        pygame.draw.rect(surface, (10, 18, 28), (0, 0, width, floor_top))
        pygame.draw.rect(surface, (12, 24, 34), (int(width * 0.08), back_top, int(width * 0.84), floor_top - back_top), border_radius=18)
        pygame.draw.rect(surface, (36, 80, 92), (int(width * 0.08), back_top, int(width * 0.84), floor_top - back_top), 3, border_radius=18)
        for i in range(9):
            x = int(width * (0.12 + i * 0.095))
            pygame.draw.line(surface, (28, 55, 70), (x, back_top), (x - int(width * 0.04), floor_top), 2)
        for i in range(5):
            y = int(back_top + i * (floor_top - back_top) / 5)
            pygame.draw.line(surface, (25, 68, 82), (int(width * 0.1), y), (int(width * 0.9), y), 2)
        for side in (-1, 1):
            x = int(center_x + side * width * 0.30)
            pygame.draw.rect(surface, (14, 28, 38), (x - 80, int(height * 0.22), 160, int(height * 0.42)), border_radius=10)
            pygame.draw.rect(surface, (65, 210, 215), (x - 80, int(height * 0.22), 160, int(height * 0.42)), 2, border_radius=10)
            pygame.draw.circle(surface, (180, 70, 95), (x, int(height * 0.24)), 12)

        floor_poly = make_ratio_polygon(width, height, BOSS15_WALKABLE_POLYGON_RATIO)
        pygame.draw.polygon(surface, (18, 35, 43), floor_poly)
        pygame.draw.polygon(surface, (70, 230, 230), floor_poly, 3)
        for i in range(13):
            y = int(floor_top + i * (floor_bottom - floor_top) / 12)
            left, right = polygon_x_bounds(y, floor_poly)
            pygame.draw.line(surface, (50, 92, 100), (int(left), y), (int(right), y), 1)
        for i in range(10):
            x = int(width * (0.12 + i * 0.085))
            pygame.draw.line(surface, (42, 82, 92), (x, floor_top), (x + int(width * 0.06), floor_bottom), 1)
        pygame.draw.rect(surface, (5, 8, 12), (0, int(height * 0.91), width, int(height * 0.09)))
        return surface

    def create_ice_dragon_fallback_background(self, width, height):
        surface = pygame.Surface((width, height))
        for y in range(height):
            t = y / max(1, height - 1)
            color = ( int(7 + 12 * t), int(18 + 42 * t), int(34 + 70 * t), )
            pygame.draw.line(surface, color, (0, y), (width, y))

        cx, cy, (rx, ry) = get_ice_dragon_arena_values(width, height)
        arena_rect = pygame.Rect(int(cx - rx), int(cy - ry), int(rx * 2), int(ry * 2))
        pygame.draw.ellipse(surface, (12, 30, 54), arena_rect)
        pygame.draw.rect(surface, (6, 12, 24), (0, 0, width, int(cy)))

        floor_poly = make_ice_dragon_walkable_polygon(width, height)
        floor = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.polygon(floor, (18, 65, 92, 132), floor_poly)
        surface.blit(floor, (0, 0))

        altar = pygame.Rect(0, 0, int(width * 0.18), int(height * 0.12))
        altar.center = (int(cx), int(cy - height * 0.08))
        pygame.draw.ellipse(surface, (16, 38, 66), altar)
        return surface

    def load_lab_arena_image(self):
        candidates = [ os.path.join("assets", "bg_lab_arena.png"), "assets/bg_lab_arena.png", os.path.join("assets", "bg_lab_arena.png.png"), "assets/bg_lab_arena.png.png", ]
        path = find_asset_path(*candidates)
        if not path:
            print("배경 이미지 없음, 대체 배경 사용:", candidates)
            return None
        try:
            image = pygame.image.load(path).convert()
            print("배경 이미지 로드 성공:", path)
            return image
        except (pygame.error, OSError) as exc:
            print("배경 이미지 로드 실패, 대체 배경 사용:", path, exc)
            return None

    def generate_rooms(self):
        rooms = {}
        for floor in range(20, 0, -1):
            if floor == 1:
                rooms[floor] = Room(floor, ROOM_FINAL)
            elif floor in (ICE_DRAGON_FLOOR, INFERNO_LIGER_FLOOR, 10, 5):
                rooms[floor] = Room(floor, ROOM_BOSS)
            elif floor == 15:
                rooms[floor] = Room(floor, ROOM_NORMAL)
            elif floor == 20:
                rooms[floor] = Room(floor, ROOM_NORMAL)
            elif 16 <= floor <= 20:
                rooms[floor] = Room(floor, random.choices( [ROOM_NORMAL, ROOM_REWARD, ROOM_REST], weights=[6, 1.2, 1], k=1, )[0])
            elif 11 <= floor <= 14:
                rooms[floor] = Room(floor, random.choices( [ROOM_NORMAL, ROOM_POISON, ROOM_SURVIVAL, ROOM_REWARD, ROOM_SHOP], weights=[3, 4, 2, 1.2, 1], k=1, )[0])
            elif 6 <= floor <= 9:
                rooms[floor] = Room(floor, random.choices( [ROOM_ELECTRIC, ROOM_ELITE, ROOM_NORMAL, ROOM_SHOP, ROOM_REWARD], weights=[4, 2, 3, 1, 1.2], k=1, )[0])
            else:
                rooms[floor] = Room(floor, random.choices( [ROOM_ELITE, ROOM_SURVIVAL, ROOM_ELECTRIC, ROOM_POISON, ROOM_SHOP, ROOM_REWARD], weights=[3, 2, 2, 2, 1, 1.2], k=1, )[0])
        return rooms

    def save_progress(self):
        self.game_data["highest_score"] = max(int(self.game_data.get("highest_score", 0)), self.high_score)
        self.game_data = save_game_data(self.game_data)

    def reset_pet_for_run(self, save=False):
        self.game_data["selected_pet_type"] = None
        self.game_data["first_boss_pet_reward_taken"] = False
        self.pet_choices = []
        self.pet_reward_rects = []
        self.pending_boss_upgrade = False
        player = getattr(self, "player", None)
        if player:
            player.pet_names.clear()
            player.pets.clear()
            player.selected_pet_type = None
            player.selected_pet_data = None
            player.hp_regen_rate_bonus = 0.0
            player.hp_regen_amount_bonus = 0
            player.stage_clear_heal = 0
            player.attack_range_bonus = 0
        if save:
            self.save_progress()

    def selected_character(self):
        character_id = self.game_data.get("selected_character_id", STARTER_CHARACTER_ID)
        return CHARACTER_BY_ID.get(character_id, CHARACTER_BY_ID[STARTER_CHARACTER_ID])

    def character_rank_color(self, rank):
        if rank == 3:
            return (255, 210, 90)
        if rank == 2:
            return (155, 215, 255)
        return (220, 225, 230)

    def apply_selected_character_bonus(self):
        character = self.selected_character()
        self.player.set_character(character["id"])
        self.player.max_hp += int(character.get("max_hp_bonus", 0))
        self.player.hp = self.player.max_hp
        self.player.attack_damage = max(1, int(round(self.player.attack_damage * (1.0 + character.get("attack_bonus", 0.0)))))
        self.player.speed *= 1.0 + character.get("speed_bonus", 0.0)
        self.player.special_cooldown_max *= 1.0 - character.get("skill_cooldown_bonus", 0.0)
        self.player.dash_cooldown_max *= 1.0 - character.get("dash_cooldown_bonus", 0.0)
        self.player.ultimate_gain_multiplier = 1.0 + character.get("ultimate_gain_bonus", 0.0)
        self.apply_saved_pet()

    def apply_saved_pet(self):
        pet_type = self.game_data.get("selected_pet_type")
        if pet_type not in PET_DEFS:
            return
        reward = PetReward(PET_DEFS[pet_type]["name"], PET_DEFS[pet_type]["desc"], pet_type)
        reward.apply(self.player)

    def roll_gacha_character(self, ticket_type):
        if ticket_type == "premium":
            rank = random.choices([2, 3], weights=[80, 20], k=1)[0]
        else:
            rank = random.choices([1, 2, 3], weights=[75, 23, 2], k=1)[0]
        candidates = [ character for character in CHARACTER_POOL if character["rank"] == rank and character.get("obtain_method") != "starter" ]
        if not candidates:
            candidates = [character for character in CHARACTER_POOL if character["rank"] == rank]
        return random.choice(candidates)

    def perform_gacha(self, ticket_type):
        ticket_key = "premium_tickets" if ticket_type == "premium" else "normal_tickets"
        if self.game_data.get(ticket_key, 0) <= 0:
            self.menu_message = "뽑기권이 부족합니다."
            return

        self.game_data[ticket_key] -= 1
        character = self.roll_gacha_character(ticket_type)
        owned = character["id"] in self.game_data["owned_characters"]
        if owned:
            shard_gain = 30 if character["rank"] == 3 else (15 if character["rank"] == 2 else 8)
            shards = self.game_data.setdefault("character_shards", {})
            shards[character["id"]] = int(shards.get(character["id"], 0)) + shard_gain
            reward_text = f"중복 보상: 조각 +{shard_gain}"
        else:
            self.game_data["owned_characters"].append(character["id"])
            reward_text = "신규 캐릭터 획득!"

        self.gacha_result = { "character": character, "owned": owned, "reward_text": reward_text, "ticket_type": ticket_type, }
        self.menu_message = reward_text
        self.save_progress()

    def select_character(self, character_id):
        if character_id not in self.game_data["owned_characters"]:
            self.menu_message = "아직 보유하지 않은 캐릭터입니다."
            return
        self.game_data["selected_character_id"] = character_id
        if hasattr(self, "player") and self.player:
            self.player.set_character(character_id)
        self.save_progress()
        self.menu_message = f"{CHARACTER_BY_ID[character_id]['name']} 선택 완료"

    def award_boss_ticket_reward(self, room):
        if room.floor in self.ticket_rewards_claimed:
            return
        normal_gain = 0
        premium_gain = 0
        if room.floor == ICE_DRAGON_FLOOR:
            normal_gain = 1
        elif room.floor == 10:
            normal_gain = 1
        elif room.floor == 5:
            normal_gain = 2
        elif room.floor == 1:
            premium_gain = 1
        else:
            return

        self.ticket_rewards_claimed.add(room.floor)
        self.game_data["normal_tickets"] = self.game_data.get("normal_tickets", 0) + normal_gain
        self.game_data["premium_tickets"] = self.game_data.get("premium_tickets", 0) + premium_gain
        parts = []
        if normal_gain:
            parts.append(f"일반 뽑기권 +{normal_gain}")
        if premium_gain:
            parts.append(f"프리미엄 뽑기권 +{premium_gain}")
        reward_text = f"{room.floor}층 보스 보상: {', '.join(parts)}"
        self.run_reward_log.append(reward_text)
        self.message = reward_text
        self.message_timer = 2.0
        print(reward_text)
        self.save_progress()

    def start_game(self):
        self.reset_pet_for_run(save=True)
        self.player = Player(self.game_data.get("selected_character_id", STARTER_CHARACTER_ID))
        self.apply_selected_character_bonus()
        self.current_floor = 20
        self.score = 0
        self.best_updated = False
        self.slow_timer = 0
        self.run_reward_log = []
        self.ticket_rewards_claimed = set()
        self.rooms = self.generate_rooms()
        self.enter_floor(20)

    def enter_floor(self, floor):
        self.current_floor = floor
        self.current_room = self.rooms[floor]
        self.announcement_timer = 0.0
        self.room_started = False
        self.clear_timer = 0
        self.message = ""
        self.message_timer = 0
        if self.current_room.room_type in (ROOM_BOSS, ROOM_FINAL):
            self.player.pos = clamp_point_to_polygon(pygame.Vector2(self.current_room.world_width // 2, self.current_room.floor_bottom_y - 120), self.current_room.walkable_polygon, self.player.radius)
        else:
            self.player.pos = clamp_point_to_polygon(pygame.Vector2(self.current_room.world_width // 2, self.current_room.floor_bottom_y - 120), self.current_room.walkable_polygon, self.player.radius)
        self.camera.reset(self.player.pos, self.current_room.world_width, self.current_room.world_height, self.current_room)

        if self.current_room.room_type == ROOM_REWARD:
            self.current_room.setup()
            self.room_started = True
            self.special_choices = SpecialItem.random_choices(self.player)
            self.state = "special_reward"
        elif self.current_room.room_type == ROOM_SHOP:
            self.current_room.setup()
            self.room_started = True
            self.shop_items = Shop.random_items()
            self.state = "shop"
        elif self.current_room.room_type == ROOM_REST:
            self.current_room.setup()
            self.room_started = True
            self.player.heal(20)
            self.state = "rest"
            self.transition_timer = 2.0
            self.message = "안전한 쉼을 고릅니다. 체력이 20 회복되었습니다."
            self.message_timer = 2.0
        else:
            self.state = "playing"

    def next_floor(self):
        if self.current_floor <= 1:
            self.win_game()
            return
        self.current_floor -= 1
        self.enter_floor(self.current_floor)

    def should_give_upgrade(self, room):
        room_type = room.room_type
        if room.floor == 20 and room_type not in (ROOM_REWARD, ROOM_SHOP, ROOM_REST):
            return True
        if room_type == ROOM_NORMAL:
            return random.random() < 0.50
        if room_type in (ROOM_POISON, ROOM_WILD):
            return random.random() < 0.55
        if room_type in (ROOM_ELECTRIC, ROOM_EARTH):
            return random.random() < 0.55
        if room_type == ROOM_SURVIVAL:
            return random.random() < 0.60
        if room_type == ROOM_TRAP:
            return random.random() < 0.50
        if room_type in (ROOM_ELITE, ROOM_BOSS):
            return True
        return False

    def complete_room(self):
        room = self.current_room
        print(f"{room.floor}층 {room.room_type} 클리어")
        gained = 80 + (21 - room.floor) * 12
        if room.room_type in (ROOM_BOSS, ROOM_FINAL):
            gained += 350
        elif room.room_type == ROOM_ELITE:
            gained += 180
        self.score += gained
        self.player.gold += 18 + (21 - room.floor)
        self.player.heal(6 if any(name == "응급 회복" for name in self.player.upgrades) else 0)
        self.sounds.play("clear")

        if room.room_type in (ROOM_BOSS, ROOM_FINAL):
            self.award_boss_ticket_reward(room)

        if room.room_type == ROOM_FINAL:
            print("최종 보스 클리어 - 게임 클리어 화면 이동")
            self.win_game()
            return

        if room.room_type == ROOM_BOSS:
            self.pet_choices = PetReward.random_choices(self.player)
            self.pending_boss_upgrade = self.should_give_upgrade(room)
            self.state = "pet_reward"
            print("펫 선택 보상 발생")
            return

        if self.should_give_upgrade(room):
            self.upgrade_choices = Upgrade.random_choices()
            self.state = "upgrade"
            print("일반 능력 강화 보상 발생")
        else:
            print("보상 없이 다음 층 이동")
            self.next_floor()

    def win_game(self):
        self.reset_pet_for_run(save=True)
        self.state = "win"
        self.score += 1000 + self.player.hp * 8 + self.player.gold * 2
        self.update_high_score()

    def game_over(self):
        self.reset_pet_for_run(save=True)
        self.state = "game_over"
        self.update_high_score()

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.best_updated = True
            save_high_score(self.high_score)
            self.game_data["highest_score"] = self.high_score
            self.save_progress()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.state in ("title", "gacha", "characters"):
                if self.state == "title":
                    self.handle_title_click(event.pos)
                elif self.state == "gacha":
                    self.handle_gacha_click(event.pos)
                elif self.state == "characters":
                    self.handle_character_click(event.pos)
                continue
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE and self.state == "title" and self.show_controls_overlay:
                self.show_controls_overlay = False
                continue
            if event.key == pygame.K_ESCAPE and self.state in ("gacha", "characters"):
                self.state = "title"
                self.menu_message = ""
                continue
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_F3:
                self.debug_camera = not self.debug_camera
                continue
            if DEBUG_GACHA and event.key == pygame.K_F8:
                self.game_data["normal_tickets"] = self.game_data.get("normal_tickets", 0) + 1
                self.save_progress()
                self.menu_message = "디버그: 일반 뽑기권 +1"
                continue
            if DEBUG_GACHA and event.key == pygame.K_F9:
                self.game_data["premium_tickets"] = self.game_data.get("premium_tickets", 0) + 1
                self.save_progress()
                self.menu_message = "디버그: 프리미엄 뽑기권 +1"
                continue
            if self.state == "title":
                if event.key == pygame.K_RETURN:
                    self.start_game()
                elif event.key == pygame.K_c:
                    self.show_controls_overlay = not self.show_controls_overlay
                elif event.key == pygame.K_g:
                    self.state = "gacha"
                elif event.key == pygame.K_h:
                    self.state = "characters"
            elif self.state == "gacha":
                if event.key == pygame.K_1:
                    self.perform_gacha("normal")
                elif event.key == pygame.K_2:
                    self.perform_gacha("premium")
                elif event.key in (pygame.K_3, pygame.K_BACKSPACE):
                    self.state = "title"
            elif self.state == "characters":
                if event.key in (pygame.K_1, pygame.K_2):
                    idx = event.key - pygame.K_1
                    if idx < len(CHARACTER_POOL):
                        self.select_character(CHARACTER_POOL[idx]["id"])
                elif event.key in (pygame.K_RETURN, pygame.K_BACKSPACE):
                    self.state = "title"
            elif self.state == "playing":
                if not self.room_started:
                    continue
                if event.key == pygame.K_j:
                    self.player.melee_attack(self.current_room.enemies, self.current_room.boss, self.current_room.effects, self.sounds, self.current_room.projectiles, self.effect_sprites)
                elif event.key == pygame.K_SPACE:
                    self.player.dash(self.current_room.effects, self.sounds, self.current_room.traps, self.current_room.arena_rect, self.current_room.walkable_polygon)
                elif event.key == pygame.K_k:
                    self.player.special(self.current_room.projectiles, self.current_room.effects, self.sounds, self.current_room.enemies, self.current_room.boss, self.effect_sprites)
                elif event.key == pygame.K_l:
                    elite_floor = self.current_room.room_type == ROOM_ELITE and (7 <= self.current_room.floor <= 9 or 2 <= self.current_room.floor <= 4)
                    self.player.ultimate_attack(self.current_room.enemies, self.current_room.boss, self.current_room.effects, self.sounds, self.effect_sprites, 0.5 if elite_floor else 1.0)
            elif self.state == "upgrade":
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    idx = event.key - pygame.K_1
                    if idx < len(self.upgrade_choices):
                        self.upgrade_choices[idx].apply(self.player)
                        self.message = f"{self.upgrade_choices[idx].name} 획득"
                        self.message_timer = 1.4
                        self.next_floor()
            elif self.state == "special_reward":
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    idx = event.key - pygame.K_1
                    if idx < len(self.special_choices):
                        self.special_choices[idx].apply(self.player)
                        self.message = f"{self.special_choices[idx].name} 획득!"
                        self.message_timer = 1.4
                        self.next_floor()
            elif self.state == "pet_reward":
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    idx = event.key - pygame.K_1
                    if idx < len(self.pet_choices):
                        self.pet_choices[idx].apply(self.player)
                        self.message = f"{self.pet_choices[idx].name} 동행 시작!"
                        self.message_timer = 1.4
                        if self.pending_boss_upgrade:
                            self.pending_boss_upgrade = False
                            self.upgrade_choices = Upgrade.random_choices()
                            self.state = "upgrade"
                        else:
                            self.next_floor()
            elif self.state == "shop":
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    idx = event.key - pygame.K_1
                    if idx < len(self.shop_items):
                        if Shop.buy(self.shop_items[idx], self.player):
                            self.message = f"{self.shop_items[idx][0]} 구매 완료"
                            self.next_floor()
                        else:
                            self.message = "골드가 부족합니다."
                            self.message_timer = 1.2
                elif event.key == pygame.K_RETURN:
                    self.next_floor()
            elif self.state in ("game_over", "win"):
                if event.key == pygame.K_r:
                    self.start_game()

    def handle_title_click(self, pos):
        if self.show_controls_overlay:
            if self.title_buttons["close_controls"].collidepoint(pos):
                self.show_controls_overlay = False
            return
        if self.title_buttons["start"].collidepoint(pos):
            self.start_game()
        elif self.title_buttons["characters"].collidepoint(pos):
            self.state = "characters"
            self.menu_message = ""
        elif self.title_buttons["gacha"].collidepoint(pos):
            self.state = "gacha"
            self.menu_message = ""
        elif self.title_buttons["controls"].collidepoint(pos):
            self.show_controls_overlay = True
        elif self.title_buttons["quit"].collidepoint(pos):
            pygame.quit()
            sys.exit()

    def handle_gacha_click(self, pos):
        if self.gacha_buttons["normal"].collidepoint(pos):
            self.perform_gacha("normal")
        elif self.gacha_buttons["premium"].collidepoint(pos):
            self.perform_gacha("premium")
        elif self.gacha_buttons["back"].collidepoint(pos):
            self.state = "title"
            self.menu_message = ""

    def handle_character_click(self, pos):
        for character_id, rect in self.character_card_rects:
            if rect.collidepoint(pos):
                self.select_character(character_id)
                return
        back_rect = pygame.Rect(WIDTH // 2 - 105, HEIGHT - 76, 210, 44)
        if back_rect.collidepoint(pos):
            self.state = "title"
            self.menu_message = ""

    def update(self, dt):
        self.announcement_timer = max(0, self.announcement_timer - dt)
        self.message_timer = max(0, self.message_timer - dt)
        self.update_environment_particles(dt)

        if self.state == "playing":
            keys = pygame.key.get_pressed()
            self.player.update(dt, keys, self.current_room.arena_rect, self.current_room.walkable_polygon)
            camera_target = self.player.pos
            if self.current_room.boss and not self.current_room.boss.dead:
                if self.current_room.bg_key in ("boss_stage_15", "ice_dragon_stage"):
                    camera_target = self.player.pos * 0.82 + self.current_room.boss.visual_pos * 0.18
                else:
                    camera_target = self.player.pos * 0.78 + self.current_room.boss.pos * 0.22
            self.camera.update(camera_target, self.current_room.world_width, self.current_room.world_height, dt, self.current_room)
            if not self.room_started:
                self.player.invuln = max(self.player.invuln, self.announcement_timer + 0.45)
                if self.announcement_timer <= 0:
                    self.current_room.setup()
                    self.room_started = True
                    self.player.invuln = max(self.player.invuln, 0.55)
                    self.message = "전투 시작!"
                    self.message_timer = 0.45
                return
            if keys[pygame.K_j]:
                self.player.melee_attack( self.current_room.enemies, self.current_room.boss, self.current_room.effects, self.sounds, self.current_room.projectiles, self.effect_sprites, )
            self.current_room.update(dt, self.player, self.sounds)
            if self.player.just_dodge_event:
                self.slow_timer = 0.32
                self.message = "저스트 회피! 반격 피해 증가"
                self.message_timer = 0.9
                self.player.just_dodge_event = False
            if self.player.hp <= 0:
                self.game_over()
                return
            if self.current_room.cleared:
                if self.clear_timer <= 0:
                    self.clear_timer = 1.1
                    self.message = "방 클리어"
                    self.message_timer = 1.1
                else:
                    self.clear_timer -= dt
                    if self.clear_timer <= 0:
                        self.complete_room()
        elif self.state == "rest":
            self.transition_timer -= dt
            if self.transition_timer <= 0:
                self.next_floor()

    def update_environment_particles(self, dt):
        key = get_background_key(self.current_floor)
        for particle in self.environment_particles:
            particle.update(dt, key)

    def get_world_background(self, room):
        if room.room_type in (ROOM_REWARD, ROOM_REST):
            forced_key = get_normal_stage_background_key_for_floor(room.floor)
            if room.bg_key != forced_key:
                print("reward/rest 배경 강제:", room.bg_key, "->", forced_key)
                room.bg_key = forced_key
        if not is_valid_background_filename(room.bg_key, allow_boss_stage=room.room_type in (ROOM_BOSS, ROOM_FINAL)):
            fallback_key = get_normal_stage_background_key_for_floor(room.floor)
            print("잘못된 배경 키 차단:", room.bg_key, "->", fallback_key)
            room.bg_key = fallback_key
        if not is_valid_background_filename(room.bg_key):
            fallback_key = get_background_key(room.floor)
            print("잘못된 배경 키 차단:", room.bg_key, "->", fallback_key)
            room.bg_key = fallback_key
        key = (room.bg_key, room.world_width, room.world_height)
        if key in self.world_backgrounds:
            return self.world_backgrounds[key]
        base = self.backgrounds.get(room.bg_key) if room.bg_key == "inferno_stage_11" else (self.lab_arena_image or self.backgrounds.get(room.bg_key))
        if base:
            bg = pygame.transform.smoothscale(base, (room.world_width, room.world_height))
        else:
            bg = pygame.Surface((room.world_width, room.world_height))
            old_screen = self.screen
            temp_screen = pygame.Surface((WIDTH, HEIGHT))
            self.screen = temp_screen
            self.draw_fallback_background(room.bg_key)
            self.screen = old_screen
            bg = pygame.transform.smoothscale(temp_screen, (room.world_width, room.world_height))
        self.world_backgrounds[key] = bg
        return bg

    def draw_world_background(self, surface, room):
        surface.blit(self.get_world_background(room), (0, 0))
        self.draw_world_decorations(surface, room)

    def draw_world_decorations(self, surface, room):
        arena = room.arena_rect
        key = room.bg_key
        if key == "inferno_stage_11":
            tint = (255, 95, 35)
            panel = (55, 28, 24)
        elif key == "20_16":
            tint = (70, 205, 195)
            panel = (22, 52, 58)
        elif key == "15_11":
            tint = (165, 190, 45)
            panel = (58, 62, 26)
        elif key == "10_6":
            tint = (85, 130, 255)
            panel = (28, 34, 70)
        else:
            tint = (210, 65, 70)
            panel = (56, 42, 46)

        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0, 0, 0, 74), (0, 0, room.world_width, max(0, arena.top - 80)))
        pygame.draw.rect(overlay, (0, 0, 0, 86), (0, arena.bottom + 58, room.world_width, room.world_height - arena.bottom))
        for x in range(80, room.world_width, 260):
            pygame.draw.rect(overlay, (*panel, 86), (x, arena.top - 210, 72, arena.height + 245), border_radius=5)
            pygame.draw.line(overlay, (*tint, 58), (x + 18, arena.top - 180), (x + 18, arena.bottom + 10), 2)
        for x in range(140, room.world_width, 340):
            pygame.draw.rect(overlay, (*tint, 48), (x, arena.bottom - 42, 150, 30), border_radius=4)
            pygame.draw.rect(overlay, (0, 0, 0, 60), (x + 12, arena.bottom - 18, 126, 10), border_radius=3)
        for x in range(0, room.world_width, 190):
            pygame.draw.line(overlay, (0, 0, 0, 34), (x, arena.top - 62), (x + 90, arena.bottom + 28), 1)
        pygame.draw.polygon(overlay, (*tint, 18), room.walkable_polygon)
        pygame.draw.rect(overlay, (0, 0, 0, 42), (arena.left, arena.top - 34, arena.width, 40), border_radius=16)
        pygame.draw.rect(overlay, (0, 0, 0, 68), (arena.left, arena.bottom - 8, arena.width, 60), border_radius=18)
        surface.blit(overlay, (0, 0))

    def draw_world_combat_floor(self, surface, room):
        floor = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        arena = room.arena_rect
        key = room.bg_key
        if key == "inferno_stage_11":
            tint = (255, 95, 35)
        elif key == "20_16":
            tint = (70, 205, 195)
        elif key == "15_11":
            tint = (160, 185, 45)
        elif key == "10_6":
            tint = (75, 120, 215)
        else:
            tint = (195, 60, 65)

        pygame.draw.polygon(floor, (4, 7, 9, 24), room.walkable_polygon)
        for i in range(22):
            t = i / 21
            y = int(room.floor_top_y + t * (room.floor_bottom_y - room.floor_top_y))
            alpha = int(12 + t * 38)
            left, right = polygon_x_bounds(y, room.walkable_polygon)
            pygame.draw.rect(floor, (0, 0, 0, alpha), (left, y, right - left, 16))
        pygame.draw.ellipse(floor, (*tint, 18), (arena.centerx - 460, room.floor_top_y + 120, 920, 260))
        pygame.draw.rect(floor, (0, 0, 0, 58), (arena.left, room.floor_bottom_y - 8, arena.width, 62), border_radius=14)
        pygame.draw.polygon(floor, (*tint, 26), room.walkable_polygon)
        surface.blit(floor, (0, 0))

    def draw_background(self):
        key = get_background_key(self.current_floor)
        image = self.backgrounds.get(key)
        if image:
            self.screen.blit(image, (0, 0))
            self.draw_background_depth(key, image=True)
            return

        self.draw_fallback_background(key)
        self.draw_background_depth(key, image=False)

    def draw_background_depth(self, key, image=True):
        if key == "20_16":
            tint = (55, 225, 215)
        elif key == "15_11":
            tint = (185, 215, 45)
        elif key == "10_6":
            tint = (85, 130, 255)
        else:
            tint = (220, 65, 70)

        depth = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(depth, (0, 0, 0, 105 if image else 60), (0, 0, WIDTH, COMBAT_TOP - 64))

        for i in range(18):
            alpha = int((i / 17) * (92 if image else 52))
            pygame.draw.rect(depth, (0, 0, 0, alpha), (0, i * 16, WIDTH, 16))

        left_wall = [(0, 80), (150, COMBAT_TOP), (82, COMBAT_BOTTOM), (0, HEIGHT)]
        right_wall = [(WIDTH, 80), (WIDTH - 150, COMBAT_TOP), (WIDTH - 82, COMBAT_BOTTOM), (WIDTH, HEIGHT)]
        pygame.draw.polygon(depth, (0, 0, 0, 48), left_wall)
        pygame.draw.polygon(depth, (0, 0, 0, 48), right_wall)

        transition = pygame.Surface((WIDTH, 100), pygame.SRCALPHA)
        for i in range(100):
            alpha = int(34 * (1 - abs(i - 50) / 50))
            pygame.draw.line(transition, (*tint, alpha), (0, i), (WIDTH, i))
        depth.blit(transition, (0, COMBAT_TOP - 76))

        self.screen.blit(depth, (0, 0))

    def draw_fallback_background(self, key):
        if key == "20_16":
            base, accent, alarm = (12, 35, 42), (60, 215, 205), (220, 55, 65)
        elif key == "15_11":
            base, accent, alarm = (34, 38, 16), (180, 210, 38), (220, 85, 45)
        elif key == "10_6":
            base, accent, alarm = (14, 20, 48), (75, 135, 255), (180, 75, 255)
        else:
            base, accent, alarm = (22, 22, 26), (210, 52, 58), (235, 235, 245)

        self.screen.fill(base)
        pygame.draw.rect(self.screen, (8, 10, 12), (0, 0, WIDTH, 76))
        pygame.draw.rect(self.screen, (6, 8, 10), (0, HEIGHT - 34, WIDTH, 34))
        for x in range(0, WIDTH, 96):
            pygame.draw.line(self.screen, (35, 42, 48), (x, 100), (x + 30, HEIGHT - 46), 1)
        for y in range(110, HEIGHT - 40, 78):
            pygame.draw.line(self.screen, (40, 48, 54), (0, y), (WIDTH, y), 1)
        for x in range(80, WIDTH, 210):
            pygame.draw.rect(self.screen, (38, 44, 50), (x, 160, 46, 330), border_radius=6)
            pygame.draw.rect(self.screen, accent, (x + 12, 185, 22, 95), 2, border_radius=6)
        for x in (90, 320, 680, 1030):
            pygame.draw.rect(self.screen, alarm, (x, 104, 36, 12), border_radius=4)
        for x in range(120, WIDTH, 250):
            pygame.draw.rect(self.screen, (55, 60, 65), (x, HEIGHT - 125, 120, 28), border_radius=6)
            pygame.draw.line(self.screen, accent, (x, HEIGHT - 97), (x + 120, HEIGHT - 97), 2)
        if key == "15_11":
            for x in (260, 620, 930):
                pygame.draw.circle(self.screen, (150, 180, 35), (x, 395), 54, 5)
                pygame.draw.line(self.screen, accent, (x - 42, 395), (x + 42, 395), 2)
        if key == "10_6":
            for _ in range(12):
                x1 = random.randint(120, WIDTH - 120)
                y1 = random.randint(170, HEIGHT - 150)
                x2 = x1 + random.randint(-80, 80)
                y2 = y1 + random.randint(-50, 50)
                pygame.draw.line(self.screen, accent, (x1, y1), (x2, y2), 2)
        if key == "5_1":
            pygame.draw.rect(self.screen, (55, 28, 31), (WIDTH // 2 - 75, 120, 150, 270), 3)
            for x in (220, WIDTH - 270):
                pygame.draw.rect(self.screen, (40, 42, 47), (x, 320, 150, 70), border_radius=5)
                pygame.draw.line(self.screen, accent, (x + 75, 320), (x + 120, 270), 5)

    def draw_combat_floor(self):
        floor = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        key = get_background_key(self.current_floor)
        if key == "20_16":
            tint = (70, 205, 195)
        elif key == "15_11":
            tint = (160, 185, 45)
        elif key == "10_6":
            tint = (75, 120, 215)
        else:
            tint = (195, 60, 65)

        stage = [ (140, COMBAT_TOP - 6), (WIDTH - 140, COMBAT_TOP - 6), (WIDTH + 85, COMBAT_BOTTOM + 36), (-85, COMBAT_BOTTOM + 36), ]
        pygame.draw.polygon(floor, (4, 7, 9, 30), stage)

        for i in range(18):
            t = i / 17
            y = int(COMBAT_TOP - 26 + t * (COMBAT_BOTTOM - COMBAT_TOP + 74))
            alpha = int(10 + t * 42)
            inset = int(95 - t * 150)
            rect = pygame.Rect(inset, y, WIDTH - inset * 2, 18)
            pygame.draw.rect(floor, (0, 0, 0, alpha), rect)

        boundary = pygame.Surface((WIDTH, 90), pygame.SRCALPHA)
        for i in range(90):
            alpha = int(48 * (1 - i / 90))
            pygame.draw.line(boundary, (0, 0, 0, alpha), (0, i), (WIDTH, i))
        floor.blit(boundary, (0, COMBAT_TOP - 60))

        shine = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.ellipse(shine, (*tint, 18), (WIDTH // 2 - 360, COMBAT_TOP + 88, 720, 230))
        floor.blit(shine, (0, 0))

        foreground = [ (-40, COMBAT_BOTTOM - 6), (WIDTH + 40, COMBAT_BOTTOM - 6), (WIDTH + 80, HEIGHT), (-80, HEIGHT), ]
        pygame.draw.polygon(floor, (0, 0, 0, 105), foreground)
        pygame.draw.ellipse(floor, (0, 0, 0, 38), (-120, COMBAT_BOTTOM - 52, WIDTH + 240, 110))

        edge = pygame.Surface((WIDTH, 58), pygame.SRCALPHA)
        edge.fill((0, 0, 0, 42))
        floor.blit(edge, (0, COMBAT_TOP - 58))
        self.screen.blit(floor, (0, 0))

    def draw_environment_particles(self, front=False):
        for particle in self.environment_particles:
            particle.draw(self.screen, front=front)

    def draw_scene_color_grade(self):
        key = get_background_key(self.current_floor)
        if key == "20_16":
            color = (35, 160, 155)
        elif key == "15_11":
            color = (145, 160, 30)
        elif key == "10_6":
            color = (45, 75, 170)
        else:
            color = (145, 40, 44)

        grade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        grade.fill((*color, 12))
        if self.current_room and self.current_room.room_type in (ROOM_BOSS, ROOM_FINAL):
            grade.fill((120, 35, 110, 10), special_flags=pygame.BLEND_RGBA_ADD)
        self.screen.blit(grade, (0, 0))

        vignette = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for i in range(18):
            alpha = int((18 - i) * 2.4)
            inset_x = i * 12
            inset_y = i * 8
            pygame.draw.rect(vignette, (0, 0, 0, alpha), (0, inset_y, WIDTH, 8))
            pygame.draw.rect(vignette, (0, 0, 0, alpha), (0, HEIGHT - inset_y - 8, WIDTH, 8))
            pygame.draw.rect(vignette, (0, 0, 0, alpha), (inset_x, 0, 12, HEIGHT))
            pygame.draw.rect(vignette, (0, 0, 0, alpha), (WIDTH - inset_x - 12, 0, 12, HEIGHT))
        self.screen.blit(vignette, (0, 0))

    def draw_hud(self):
        draw_hud_backdrop(self.screen, 98)
        room = self.current_room
        draw_text(self.screen, self.font, f"{self.current_floor}층 - {room.room_type}", 18, 12, WHITE)
        draw_text(self.screen, self.font_sm, f"구역: {room.zone_name}", 18, 42, room.zone_color)
        draw_hud_bar(self.screen, 250, 14, 190, 14, self.player.hp, self.player.max_hp, (245, 85, 115))
        draw_text(self.screen, self.font_sm, f"체력 {int(self.player.hp)}/{self.player.max_hp}", 256, 36, WHITE)
        draw_text(self.screen, self.font_sm, f"점수 {self.score}", 470, 12, WHITE)
        draw_text(self.screen, self.font_sm, f"골드 {self.player.gold}", 470, 38, YELLOW)
        dash_ready = self.player.dash_cooldown <= 0
        dash_color = CYAN if dash_ready else BLUE
        draw_hud_bar(self.screen, 585, 14, 130, 12, self.player.dash_cooldown_max - self.player.dash_cooldown, self.player.dash_cooldown_max, dash_color, dash_ready)
        dash_label = "대시 READY" if dash_ready else f"대시 {self.player.dash_cooldown:.1f}s"
        draw_text(self.screen, self.font_sm, dash_label, 600, 35, CYAN if dash_ready else WHITE)
        skill_ready = self.player.special_cooldown <= 0
        skill_color = (190, 105, 255) if skill_ready else (115, 100, 205)
        draw_hud_bar(self.screen, 735, 14, 130, 12, self.player.special_cooldown_max - self.player.special_cooldown, self.player.special_cooldown_max, skill_color, skill_ready)
        draw_text(self.screen, self.font_sm, "스킬", 772, 35, WHITE)
        draw_hud_bar(self.screen, 885, 14, 160, 12, self.player.ultimate, 100, ORANGE)
        draw_text(self.screen, self.font_sm, "궁극기", 932, 35, WHITE)
        upgrades = ", ".join(self.player.upgrades[-4:]) if self.player.upgrades else "없음"
        special_items = ", ".join(self.player.special_items[-3:]) if self.player.special_items else "없음"
        pets = ", ".join(self.player.pet_names[-2:]) if self.player.pet_names else "없음"
        draw_text(self.screen, self.font_sm, f"강화: {upgrades}", 1070, 10, WHITE)
        draw_text(self.screen, self.font_sm, f"특별: {special_items}", 1070, 31, (215, 190, 255))
        draw_text(self.screen, self.font_sm, f"펫: {pets}", 1070, 52, (235, 225, 160))
        if self.player.special_item_flags.get("auto_shield"):
            shield = "방어막 준비" if self.player.auto_shield_ready else f"방어막 {self.player.auto_shield_timer:.0f}s"
            draw_text(self.screen, self.font_sm, shield, 585, 63, CYAN if self.player.auto_shield_ready else WHITE)
        if self.player.counter_boost_timer > 0:
            max_timer = 4.0 if self.player.special_item_flags.get("time_core") else 2.8
            draw_bar(self.screen, 1070, 56, 150, 10, self.player.counter_boost_timer, max_timer, YELLOW)
            draw_text(self.screen, self.font_sm, f"반격 x{self.player.counter_boost_multiplier:.2f}", 1070, 68, YELLOW)

    def draw_announcement(self):
        if self.announcement_timer <= 0 or not self.current_room:
            return
        room = self.current_room
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 130))
        self.screen.blit(overlay, (0, 0))
        draw_text(self.screen, self.font_md, f"현재 구역: {room.zone_name}", WIDTH // 2, 250, room.zone_color, center=True)
        draw_text(self.screen, self.font_md, f"{room.floor}층 - {room.room_type}", WIDTH // 2, 295, WHITE, center=True)
        draw_text(self.screen, self.font, room.zone_desc, WIDTH // 2, 340, WHITE, center=True)

    def draw_message(self):
        if self.message and self.message_timer > 0:
            draw_text(self.screen, self.font_md, self.message, WIDTH // 2, HEIGHT - 95, YELLOW, center=True)

    def draw_camera_debug(self):
        if not self.debug_camera or not self.current_room:
            return
        cam = self.camera.pos
        room = self.current_room
        polygon = [(x - int(cam.x), y - int(cam.y)) for x, y in room.walkable_polygon]
        view_rect = getattr(self, "last_view_rect", None)
        view_zoom = getattr(self, "last_view_zoom", 1.0)
        if view_rect:
            polygon = [((x - view_rect.x) * view_zoom, (y - view_rect.y) * view_zoom) for x, y in room.walkable_polygon]
        pygame.draw.lines(self.screen, (255, 235, 90), True, polygon, 2)
        panel = pygame.Surface((390, 96), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 170))
        self.screen.blit(panel, (14, 108))
        draw_text(self.screen, self.font_sm, f"F3 DEBUG  camera=({cam.x:.0f}, {cam.y:.0f})", 24, 118, YELLOW)
        draw_text(self.screen, self.font_sm, f"player=({self.player.pos.x:.0f}, {self.player.pos.y:.0f})", 24, 146, WHITE)
        draw_text(self.screen, self.font_sm, f"world={room.world_width}x{room.world_height}  arena={room.arena_rect}", 24, 174, WHITE)

    def draw_just_dodge_text(self, surface=None):
        if self.player.just_dodge_text_timer <= 0:
            return
        target = surface or self.screen
        t = self.player.just_dodge_text_timer / 0.75
        y = self.player.pos.y - 72 - (1.0 - t) * 28
        pulse = 1.0 + math.sin(pygame.time.get_ticks() * 0.025) * 0.04
        text = self.font_md.render("저스트 회피!", True, YELLOW)
        text = pygame.transform.rotozoom(text, 0, pulse)
        shadow = self.font_md.render("저스트 회피!", True, BLACK)
        shadow = pygame.transform.rotozoom(shadow, 0, pulse)
        rect = text.get_rect(center=(self.player.pos.x, y))
        shadow_rect = shadow.get_rect(center=(self.player.pos.x + 2, y + 2))
        target.blit(shadow, shadow_rect)
        target.blit(text, rect)

    def draw_title(self):
        if self.title_image:
            self.screen.blit(self.title_image, (0, 0))
        else:
            self.screen.fill((8, 10, 14))
            self.current_floor = 20
            self.draw_fallback_background("20_16")
        mouse_pos = pygame.mouse.get_pos()
        for rect in (self.title_buttons["start"], self.title_buttons["characters"], self.title_buttons["gacha"], self.title_buttons["controls"], self.title_buttons["quit"]):
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, (255, 235, 120), rect, 3, border_radius=8)
        if self.show_controls_overlay:
            self.draw_controls_overlay(mouse_pos)

    def draw_gacha(self):
        if self.title_image:
            self.screen.blit(self.title_image, (0, 0))
        else:
            self.screen.fill((8, 10, 14))
            self.draw_fallback_background("20_16")
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 166))
        self.screen.blit(shade, (0, 0))

        panel = pygame.Rect(WIDTH // 2 - 430, 74, 860, 560)
        pygame.draw.rect(self.screen, (14, 18, 24), panel, border_radius=8)
        pygame.draw.rect(self.screen, (255, 210, 90), panel, 2, border_radius=8)
        draw_text(self.screen, self.font_md, "가챠", panel.centerx, panel.y + 32, YELLOW, center=True)
        draw_text(self.screen, self.font, f"일반 뽑기권: {self.game_data.get('normal_tickets', 0)}", panel.x + 72, panel.y + 88, WHITE)
        draw_text(self.screen, self.font, f"프리미엄 뽑기권: {self.game_data.get('premium_tickets', 0)}", panel.x + 72, panel.y + 124, WHITE)
        draw_text(self.screen, self.font_sm, "일반: 1성 75% / 2성 23% / 3성 2%", panel.x + 72, panel.y + 170, (205, 220, 225))
        draw_text(self.screen, self.font_sm, "프리미엄: 2성 80% / 3성 20%", panel.x + 72, panel.y + 198, (205, 220, 225))

        if self.gacha_result:
            character = self.gacha_result["character"]
            result_rect = pygame.Rect(panel.centerx - 240, panel.y + 248, 480, 172)
            color = self.character_rank_color(character["rank"])
            pygame.draw.rect(self.screen, (24, 30, 38), result_rect, border_radius=8)
            pygame.draw.rect(self.screen, color, result_rect, 2, border_radius=8)
            draw_text(self.screen, self.font_md, f"{'★' * character['rank']} {character['name']}", result_rect.centerx, result_rect.y + 24, color, center=True)
            draw_text(self.screen, self.font, self.gacha_result["reward_text"], result_rect.centerx, result_rect.y + 72, WHITE, center=True)
            draw_text(self.screen, self.font_sm, character["desc"], result_rect.centerx, result_rect.y + 112, (215, 225, 230), center=True)
        else:
            draw_text(self.screen, self.font, "보스 처치로 얻은 뽑기권을 사용하세요.", panel.centerx, panel.y + 318, WHITE, center=True)

        if self.menu_message:
            draw_text(self.screen, self.font_sm, self.menu_message, panel.centerx, panel.bottom - 82, CYAN, center=True)
        mouse_pos = pygame.mouse.get_pos()
        self.draw_title_button("1 일반 뽑기", self.gacha_buttons["normal"], mouse_pos)
        self.draw_title_button("2 프리미엄", self.gacha_buttons["premium"], mouse_pos)
        self.draw_title_button("3 뒤로", self.gacha_buttons["back"], mouse_pos)

    def draw_characters(self):
        if self.title_image:
            self.screen.blit(self.title_image, (0, 0))
        else:
            self.screen.fill((8, 10, 14))
            self.draw_fallback_background("20_16")
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 170))
        self.screen.blit(shade, (0, 0))

        draw_text(self.screen, self.font_md, "캐릭터 선택", WIDTH // 2, 54, CYAN, center=True)
        draw_text(self.screen, self.font_sm, "숫자키 또는 보유 캐릭터 카드를 눌러 선택하세요.", WIDTH // 2, 92, WHITE, center=True)
        self.character_card_rects = []
        owned = set(self.game_data["owned_characters"])
        selected_id = self.game_data.get("selected_character_id", STARTER_CHARACTER_ID)
        for idx, character in enumerate(CHARACTER_POOL):
            col = idx % 3
            row = idx // 3
            rect = pygame.Rect(62 + col * 406, 122 + row * 116, 358, 98)
            locked = character["id"] not in owned or idx >= 2
            selected = character["id"] == selected_id
            color = self.character_rank_color(character["rank"])
            fill = (24, 31, 38) if not locked else (14, 17, 22)
            pygame.draw.rect(self.screen, fill, rect, border_radius=8)
            pygame.draw.rect(self.screen, color if selected or not locked else GRAY, rect, 2 if selected else 1, border_radius=8)
            label = f"{idx + 1}. {'★' * character['rank']} {character['name']}"
            draw_text(self.screen, self.font, label, rect.x + 18, rect.y + 12, color if not locked else GRAY)
            status = "선택중" if selected else ("선택 가능" if not locked else "잠금")
            draw_text(self.screen, self.font_sm, status, rect.right - 76, rect.y + 16, YELLOW if selected else (WHITE if not locked else GRAY), center=True)
            draw_text(self.screen, self.font_sm, character["desc"], rect.x + 18, rect.y + 42, (210, 220, 225) if not locked else GRAY)
            bonus = f"공격 +{int(character['attack_bonus'] * 100)}%  속도 +{int(character['speed_bonus'] * 100)}%  체력 +{character['max_hp_bonus']}"
            draw_text(self.screen, self.font_sm, bonus, rect.x + 18, rect.y + 68, (190, 230, 230) if not locked else GRAY)
            if not locked:
                self.character_card_rects.append((character["id"], rect))

        if self.menu_message:
            draw_text(self.screen, self.font_sm, self.menu_message, WIDTH // 2, HEIGHT - 108, CYAN, center=True)
        back_rect = pygame.Rect(WIDTH // 2 - 105, HEIGHT - 76, 210, 44)
        self.draw_title_button("뒤로", back_rect, pygame.mouse.get_pos())

    def draw_room_ui_background(self):
        if self.current_room:
            self.draw_playing()
        else:
            self.draw_background()
            self.draw_hud()

    def draw_upgrade(self):
        if self.current_room:
            self.draw_playing()
        else:
            self.draw_background()
            self.draw_hud()
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 175))
        self.screen.blit(overlay, (0, 0))
        title = "강적 처치 보상" if self.current_room and self.current_room.room_type in (ROOM_BOSS, ROOM_ELITE) else "전투 보상"
        draw_text(self.screen, self.font_md, title, WIDTH // 2, 135, CYAN, center=True)
        draw_text(self.screen, self.font, "능력 강화 1개를 선택하세요.", WIDTH // 2, 174, WHITE, center=True)
        for i, upgrade in enumerate(self.upgrade_choices):
            rect = pygame.Rect(WIDTH // 2 - 300, 225 + i * 105, 600, 78)
            pygame.draw.rect(self.screen, (24, 32, 38), rect, border_radius=8)
            pygame.draw.rect(self.screen, CYAN, rect, 2, border_radius=8)
            draw_text(self.screen, self.font, f"{i + 1}. {upgrade.name}", rect.x + 24, rect.y + 13, WHITE)
            draw_text(self.screen, self.font_sm, upgrade.desc, rect.x + 24, rect.y + 45, (205, 220, 225))

    def draw_special_reward(self):
        self.draw_room_ui_background()
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 182))
        self.screen.blit(overlay, (0, 0))
        draw_text(self.screen, self.font_md, "특별 보상방", WIDTH // 2, 130, (215, 190, 255), center=True)
        draw_text(self.screen, self.font, "희귀 아이템 1개를 선택하세요", WIDTH // 2, 170, WHITE, center=True)
        for i, item in enumerate(self.special_choices):
            rect = pygame.Rect(WIDTH // 2 - 330, 225 + i * 108, 660, 82)
            pygame.draw.rect(self.screen, (32, 24, 42), rect, border_radius=8)
            pygame.draw.rect(self.screen, (215, 190, 255), rect, 2, border_radius=8)
            draw_text(self.screen, self.font, f"{i + 1}. {item.name}", rect.x + 24, rect.y + 13, WHITE)
            draw_text(self.screen, self.font_sm, item.desc, rect.x + 24, rect.y + 47, (225, 215, 245))

    def draw_pet_reward(self):
        self.draw_room_ui_background()
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 184))
        self.screen.blit(overlay, (0, 0))
        draw_text(self.screen, self.font_md, "첫 보스 처치 보상", WIDTH // 2, 125, YELLOW, center=True)
        draw_text(self.screen, self.font, "동행할 펫 1마리를 선택하세요.", WIDTH // 2, 165, WHITE, center=True)
        self.pet_reward_rects = []
        for i, pet in enumerate(self.pet_choices):
            rect = pygame.Rect(WIDTH // 2 - 330, 220 + i * 108, 660, 82)
            self.pet_reward_rects.append(rect)
            pygame.draw.rect(self.screen, (34, 31, 24), rect, border_radius=8)
            pygame.draw.rect(self.screen, YELLOW, rect, 2, border_radius=8)
            color = CompanionPet.DATA[pet.code][2]
            icon = load_pet_image(pet.code, (48, 48))
            if icon:
                self.screen.blit(icon, icon.get_rect(center=(rect.x + 44, rect.y + 41)))
            else:
                pygame.draw.circle(self.screen, (8, 16, 18), (rect.x + 44, rect.y + 41), 18)
                pygame.draw.circle(self.screen, color, (rect.x + 44, rect.y + 41), 14)
                pygame.draw.circle(self.screen, WHITE, (rect.x + 39, rect.y + 36), 4)
            draw_text(self.screen, self.font, f"{i + 1}. {pet.name}", rect.x + 78, rect.y + 13, WHITE)
            draw_text(self.screen, self.font_sm, pet.desc, rect.x + 78, rect.y + 47, (235, 225, 190))
        draw_text(self.screen, self.font_sm, "숫자키 1,2,3 / 클릭 / Enter로 선택", WIDTH // 2, 560, (230, 230, 210), center=True)

    def draw_shop(self):
        self.draw_room_ui_background()
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 175))
        self.screen.blit(overlay, (0, 0))
        draw_text(self.screen, self.font_md, "상점방", WIDTH // 2, 140, YELLOW, center=True)
        draw_text(self.screen, self.font, "숫자 1, 2, 3으로 구매 / Enter로 지나가기", WIDTH // 2, 180, WHITE, center=True)
        for i, item in enumerate(self.shop_items):
            name, cost, _ = item
            rect = pygame.Rect(WIDTH // 2 - 300, 245 + i * 95, 600, 68)
            pygame.draw.rect(self.screen, (34, 30, 22), rect, border_radius=8)
            pygame.draw.rect(self.screen, YELLOW, rect, 2, border_radius=8)
            draw_text(self.screen, self.font, f"{i + 1}. {name}", rect.x + 24, rect.y + 12, WHITE)
            draw_text(self.screen, self.font_sm, f"가격: {cost} 골드", rect.x + 24, rect.y + 42, YELLOW)
        self.draw_message()

    def draw_end_screen(self, title, subtitle, color):
        if self.state == "win" and self.ending_image:
            self.screen.blit(self.ending_image, (0, 0))
            return
        self.draw_background()
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        draw_text(self.screen, self.font_lg, title, WIDTH // 2, 170, color, center=True)
        draw_text(self.screen, self.font_md, subtitle, WIDTH // 2, 245, WHITE, center=True)
        draw_text(self.screen, self.font, f"최종 점수: {self.score}", WIDTH // 2, 325, WHITE, center=True)
        draw_text(self.screen, self.font, f"최고 기록: {self.high_score}", WIDTH // 2, 365, YELLOW, center=True)
        if self.run_reward_log:
            draw_text(self.screen, self.font_sm, "이번 런 티켓 보상", WIDTH // 2, 410, CYAN, center=True)
            for idx, reward in enumerate(self.run_reward_log[-4:]):
                draw_text(self.screen, self.font_sm, reward, WIDTH // 2, 438 + idx * 24, WHITE, center=True)
        if self.best_updated:
            draw_text(self.screen, self.font, "최고 기록 갱신", WIDTH // 2, 405, CYAN, center=True)
        draw_text(self.screen, self.font_md, "R 다시 시작    ESC 종료", WIDTH // 2, 515, WHITE, center=True)

    def draw_end_screen(self, title, subtitle, color):
        self.draw_background()
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        draw_text(self.screen, self.font_lg, title, WIDTH // 2, 150, color, center=True)
        draw_text(self.screen, self.font_md, subtitle, WIDTH // 2, 225, WHITE, center=True)
        draw_text(self.screen, self.font, f"최종 점수: {self.score}", WIDTH // 2, 300, WHITE, center=True)
        draw_text(self.screen, self.font, f"최고 기록: {self.high_score}", WIDTH // 2, 340, YELLOW, center=True)

        y = 386
        if self.best_updated:
            draw_text(self.screen, self.font, "최고 기록 갱신", WIDTH // 2, y, CYAN, center=True)
            y += 42
        if self.run_reward_log:
            draw_text(self.screen, self.font_sm, "이번 런 티켓 보상", WIDTH // 2, y, CYAN, center=True)
            y += 28
            for reward in self.run_reward_log[-4:]:
                draw_text(self.screen, self.font_sm, reward, WIDTH // 2, y, WHITE, center=True)
                y += 24
        draw_text(self.screen, self.font_md, "R 다시 시작    ESC 종료", WIDTH // 2, 590, WHITE, center=True)

    def draw_playing(self):
        room = self.current_room
        world = pygame.Surface((room.world_width, room.world_height))
        self.draw_world_background(world, room)
        self.draw_world_combat_floor(world, room)
        room.draw_entities(world, self.font_sm, self.player)
        self.draw_just_dodge_text(world)
        camera_pos = self.camera.offset()
        if room.floor_bottom_y > room.floor_top_y:
            rear_depth = clamp((room.floor_bottom_y - self.player.pos.y) / (room.floor_bottom_y - room.floor_top_y), 0.0, 1.0)
        else:
            rear_depth = 0.0
        zoom = 1.0 + rear_depth * 0.045
        view_w = max(1, min(room.world_width, int(WIDTH / zoom)))
        view_h = max(1, min(room.world_height, int(HEIGHT / zoom)))
        view_x = int(clamp(camera_pos.x + (WIDTH - view_w) * 0.5, 0, max(0, room.world_width - view_w)))
        view_y = int(clamp(camera_pos.y + (HEIGHT - view_h) * 0.5, 0, max(0, room.world_height - view_h)))
        view_rect = pygame.Rect(view_x, view_y, view_w, view_h)
        self.last_view_rect = view_rect
        self.last_view_zoom = WIDTH / view_w
        if zoom > 1.003:
            self.screen.blit(pygame.transform.smoothscale(world.subsurface(view_rect), (WIDTH, HEIGHT)), (0, 0))
        else:
            self.screen.blit(world, (-int(camera_pos.x), -int(camera_pos.y)))
        self.draw_scene_color_grade()
        self.draw_hud()
        if self.current_room.room_type == ROOM_SURVIVAL:
            left = max(0, self.current_room.survival_goal - self.current_room.timer)
            draw_text(self.screen, self.font_md, f"버티기: {left:.1f}초", WIDTH // 2, 96, YELLOW, center=True)
        self.draw_camera_debug()
        self.draw_announcement()
        self.draw_message()

    def draw(self):
        self.update_music()
        if self.state == "title":
            self.draw_title()
        elif self.state == "gacha":
            self.draw_gacha()
        elif self.state == "characters":
            self.draw_characters()
        elif self.state == "upgrade":
            self.draw_upgrade()
            self.draw_announcement()
        elif self.state == "special_reward":
            self.draw_special_reward()
            self.draw_announcement()
        elif self.state == "pet_reward":
            self.draw_pet_reward()
            self.draw_announcement()
        elif self.state == "shop":
            self.draw_shop()
            self.draw_announcement()
        elif self.state == "rest":
            self.draw_background()
            self.draw_hud()
            self.draw_announcement()
            self.draw_message()
        elif self.state == "game_over":
            self.draw_end_screen("게임 오버", f"도달한 최저 층: {self.current_floor}층", RED)
        elif self.state == "win":
            self.draw_end_screen("탈출 성공", "20층 격리구역을 돌파했습니다.", CYAN)
        else:
            self.draw_playing()
        pygame.display.flip()

    def draw(self):
        self.update_music()
        if self.state == "title":
            self.draw_title()
        elif self.state == "gacha":
            self.draw_gacha()
        elif self.state == "characters":
            self.draw_characters()
        elif self.state == "upgrade":
            self.draw_upgrade()
            self.draw_announcement()
        elif self.state == "special_reward":
            self.draw_special_reward()
            self.draw_announcement()
        elif self.state == "pet_reward":
            self.draw_pet_reward()
            self.draw_announcement()
        elif self.state == "shop":
            self.draw_shop()
            self.draw_announcement()
        elif self.state == "rest":
            self.draw_background()
            self.draw_hud()
            self.draw_announcement()
            self.draw_message()
        elif self.state == "game_over":
            self.draw_end_screen("게임 오버", f"도달한 최저 층: {self.current_floor}층", RED)
        elif self.state == "win":
            self.draw_end_screen("탈출 성공", "20층 격리구역을 돌파했습니다.", CYAN)
        else:
            self.draw_playing()
        pygame.display.flip()

    def make_interactable(self, kind, pos, radius, label, prompt, active=True):
        return { "kind": kind, "pos": pygame.Vector2(pos), "radius": radius, "label": label, "prompt": prompt, "active": active, "used": False, }

    def lobby_point(self, ratio_x, ratio_y):
        return pygame.Vector2(WIDTH * ratio_x, HEIGHT * ratio_y)

    def lobby_walkable_polygon(self):
        return [(WIDTH * x, HEIGHT * y) for x, y in LOBBY_WALKABLE_POLYGON_RATIO]

    def lobby_auto_entry_rect(self):
        x, y, w, h = LOBBY_AUTO_ENTRY_RECT_RATIO
        return pygame.Rect(int(WIDTH * x), int(HEIGHT * y), int(WIDTH * w), int(HEIGHT * h))

    def player_in_lobby_auto_entry(self):
        return self.lobby_auto_entry_rect().collidepoint(int(self.player.pos.x), int(self.player.pos.y))

    def nearest_interactable(self, items):
        active_items = [item for item in items if item.get("active") and not item.get("used")]
        if not active_items:
            return None
        item = min(active_items, key=lambda value: self.player.pos.distance_to(value["pos"]))
        return item if self.player.pos.distance_to(item["pos"]) <= item["radius"] else None

    def enter_lobby(self):
        self.state = "lab_lobby"
        self.menu_return_state = "lab_lobby"
        self.current_floor = 20
        self.current_room = None
        self.player = Player(self.game_data.get("selected_character_id", STARTER_CHARACTER_ID))
        self.apply_selected_character_bonus()
        self.player.pos = pygame.Vector2(WIDTH // 2, 560)
        self.player.hp = self.player.max_hp
        self.lobby_interactables = [ self.make_interactable("gacha_machine", (230, 470), 82, "실험 뽑기기계", "ENTER: 가챠 열기"), self.make_interactable("character_terminal", (1035, 470), 82, "캐릭터 관리 단말기", "ENTER: 캐릭터 선택"), self.make_interactable("stairs_to_20f", (WIDTH // 2, 300), 95, "격리구역 진입문", "ENTER: 20층으로 내려가기"), self.make_interactable("records_terminal", (WIDTH // 2, 500), 76, "기록 안내 단말기", "ENTER: 조작법 보기"), ]
        self.message = "시연구소 로비입니다. 격리구역으로 내려갈 준비를 하세요."
        self.message_timer = 2.2
        self.active_prompt = None
        self.gacha_result = None

    def start_game(self):
        self.reset_pet_for_run(save=True)
        self.enter_lobby()

    def begin_run(self):
        self.reset_pet_for_run(save=True)
        self.player = Player(self.game_data.get("selected_character_id", STARTER_CHARACTER_ID))
        self.apply_selected_character_bonus()
        self.current_floor = 20
        self.score = 0
        self.best_updated = False
        self.slow_timer = 0
        self.run_reward_log = []
        self.ticket_rewards_claimed = set()
        self.room_interactables = []
        self.final_exit_ready = False
        self.rooms = self.generate_rooms()
        self.message = "20F 격리구역으로 내려갑니다."
        self.message_timer = 1.2
        self.enter_floor(20)

    def enter_floor(self, floor):
        self.current_floor = floor
        self.current_room = self.rooms[floor]
        self.current_room.reward_processed = False
        self.room_interactables = []
        self.active_prompt = None
        self.announcement_timer = 0.0
        self.room_started = False
        self.clear_timer = 0
        self.message = ""
        self.message_timer = 0
        if self.current_room.bg_key == "ice_dragon_stage":
            start = pygame.Vector2(self.current_room.world_width * 0.50, self.current_room.floor_bottom_y - 110)
        elif self.current_room.bg_key == "stage_20_16":
            start = pygame.Vector2( self.current_room.world_width * STAGE_20_16_PLAYER_START_RATIO[0], self.current_room.world_height * STAGE_20_16_PLAYER_START_RATIO[1], )
        else:
            start = pygame.Vector2(self.current_room.world_width // 2, self.current_room.floor_bottom_y - 120)
        self.player.pos = clamp_point_to_polygon(start, self.current_room.walkable_polygon, self.player.radius)
        self.camera.reset(self.player.pos, self.current_room.world_width, self.current_room.world_height, self.current_room)

        if self.current_room.room_type == ROOM_REWARD:
            self.current_room.setup()
            self.room_started = True
            self.state = "playing"
            self.room_interactables.append(self.make_interactable("reward_chest", (self.current_room.world_width // 2, self.current_room.floor_top_y + 160), 82, "보상 상자", "ENTER: 상자 열기"))
            self.message = "보상 상자가 있습니다."
            self.message_timer = 1.5
        elif self.current_room.room_type == ROOM_SHOP:
            self.current_room.setup()
            self.room_started = True
            self.state = "playing"
            self.shop_items = Shop.random_items()
            self.room_interactables.append(self.make_interactable("shop_terminal", (self.current_room.arena_rect.centerx - 220, self.current_room.arena_rect.centery), 80, "상점 단말기", "ENTER: 상점 이용"))
            self.open_floor_exit("상점 이용 후 아래층 통로로 이동하세요.")
        elif self.current_room.room_type == ROOM_REST:
            self.current_room.setup()
            self.room_started = True
            self.state = "playing"
            self.room_interactables.append(self.make_interactable("rest_device", (self.current_room.arena_rect.centerx - 220, self.current_room.arena_rect.centery), 80, "회복 캡슐", "ENTER: 회복 장치 사용"))
            self.open_floor_exit("회복 후 아래층 통로로 이동하세요.")
        else:
            self.state = "playing"

    def open_floor_exit(self, text=None):
        if any(item["kind"] in ("exit_stairs", "exit_door") and item.get("active") for item in self.room_interactables):
            return
        room = self.current_room
        if not room:
            return
        if room.room_type == ROOM_FINAL:
            kind = "exit_door"
            label = "탈출 리프트"
            prompt = "ENTER: 결과 화면으로 이동"
            pos = (room.world_width * 0.5, room.floor_top_y + 88)
        elif room.room_type in (ROOM_REWARD, ROOM_SHOP, ROOM_REST):
            kind = "exit_stairs"
            label = "아래층 통로"
            prompt = "ENTER: 다음 층으로 이동"
            pos = (room.arena_rect.right - 130, room.arena_rect.top + 92)
        else:
            kind = "exit_stairs"
            label = "아래층 계단"
            prompt = "ENTER: 다음 층으로 이동"
            if room.floor == ICE_DRAGON_FLOOR and room.room_type == ROOM_BOSS and room.bg_key == "ice_dragon_stage":
                pos = ( room.world_width * ICE_DRAGON_EXIT_POS_RATIO[0], room.world_height * ICE_DRAGON_EXIT_POS_RATIO[1], )
            elif room.bg_key == "stage_20_16":
                pos = ( room.world_width * STAGE_20_16_EXIT_RATIO[0], room.world_height * STAGE_20_16_EXIT_RATIO[1], )
            else:
                pos = (room.world_width * 0.5, room.floor_top_y + 70)
        self.room_interactables.append(self.make_interactable(kind, pos, 95, label, prompt))
        self.message = text or "출구가 열렸습니다. 아래층 계단으로 이동하세요."
        self.message_timer = 2.0

    def start_floor_transition(self):
        if self.current_floor <= 1 or self.final_exit_ready:
            self.win_game()
            return
        self.pending_floor = self.current_floor - 1
        self.floor_transition_timer = 0.05
        self.state = "floor_transition"
        self.message = f"{self.current_floor}F -> {self.pending_floor}F"
        self.message_timer = 0.8

    def finish_reward_and_open_exit(self, text="출구가 열렸습니다. 아래층 계단으로 이동하세요."):
        self.state = "playing"
        self.open_floor_exit(text)

    def complete_room(self):
        room = self.current_room
        if not room or getattr(room, "reward_processed", False):
            return
        room.reward_processed = True
        room.cleared = False
        print(f"{room.floor}층 {room.room_type} 클리어")
        gained = 80 + (21 - room.floor) * 12
        if room.room_type in (ROOM_BOSS, ROOM_FINAL):
            gained += 350
        elif room.room_type == ROOM_ELITE:
            gained += 180
        self.score += gained
        self.player.gold += 18 + (21 - room.floor)
        self.player.heal(6 if any(name == "?묎툒 ?뚮났" for name in self.player.upgrades) else 0)
        if self.player.stage_clear_heal:
            self.player.heal(self.player.stage_clear_heal)
        self.sounds.play("clear")

        if room.room_type in (ROOM_BOSS, ROOM_FINAL):
            self.award_boss_ticket_reward(room)

        if room.room_type == ROOM_FINAL:
            self.final_exit_ready = True
            self.open_floor_exit("최종 보스 격파! 탈출 리프트가 열렸습니다.")
            return

        if room.room_type == ROOM_BOSS and not self.game_data.get("first_boss_pet_reward_taken", False):
            self.pet_choices = PetReward.random_choices(self.player)
            self.pending_boss_upgrade = self.should_give_upgrade(room)
            self.state = "pet_reward"
            return

        if room.room_type == ROOM_BOSS:
            if self.should_give_upgrade(room):
                self.upgrade_choices = Upgrade.random_choices()
                self.state = "upgrade"
                print("강적 처치 보상 발생")
            else:
                self.open_floor_exit("보스 격파! 아래층 통로가 열렸습니다.")
            return

        if self.should_give_upgrade(room):
            self.upgrade_choices = Upgrade.random_choices()
            self.state = "upgrade"
            print("일반 능력 강화 보상 발생")
        else:
            print("보상 없이 출구 개방")
            self.open_floor_exit()

    def interact_with(self, item):
        kind = item["kind"]
        if kind == "gacha_machine":
            self.menu_return_state = self.state
            self.state = "gacha"
            self.menu_message = ""
        elif kind == "character_terminal":
            self.menu_return_state = self.state
            self.state = "characters"
            self.menu_message = ""
        elif kind == "stairs_to_20f":
            self.begin_run()
        elif kind == "records_terminal":
            self.show_controls_overlay = True
        elif kind == "reward_chest":
            item["used"] = True
            self.special_choices = SpecialItem.random_choices(self.player)
            self.state = "special_reward"
        elif kind == "shop_terminal":
            self.state = "shop"
        elif kind == "rest_device":
            if not item.get("used"):
                item["used"] = True
                self.player.heal(28)
                self.message = "회복 캡슐을 사용했습니다. 체력 28 회복."
                self.message_timer = 1.6
        elif kind in ("exit_stairs", "exit_door"):
            self.start_floor_transition()

    def choose_pet_reward(self, idx):
        if idx < 0 or idx >= len(self.pet_choices):
            return
        choice = self.pet_choices[idx]
        choice.apply(self.player)
        self.game_data["selected_pet_type"] = choice.code
        self.game_data["first_boss_pet_reward_taken"] = True
        self.game_data = save_game_data(self.game_data)
        self.message = f"{choice.name} 동행 시작!"
        self.message_timer = 1.4
        if self.pending_boss_upgrade:
            self.pending_boss_upgrade = False
            self.upgrade_choices = Upgrade.random_choices()
            self.state = "upgrade"
        else:
            self.finish_reward_and_open_exit("보스 격파! 아래층 통로가 열렸습니다.")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.state == "title":
                    self.handle_title_click(event.pos)
                    continue
                if self.state == "gacha":
                    self.handle_gacha_click(event.pos)
                    continue
                if self.state == "characters":
                    self.handle_character_click(event.pos)
                    continue
                if self.state == "pet_reward":
                    for idx, rect in enumerate(self.pet_reward_rects):
                        if rect.collidepoint(event.pos):
                            self.choose_pet_reward(idx)
                            break
                    continue
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_ESCAPE and self.state == "title" and self.show_controls_overlay:
                self.show_controls_overlay = False
                continue
            if event.key == pygame.K_ESCAPE and self.state in ("gacha", "characters"):
                self.state = self.menu_return_state if self.menu_return_state in ("lab_lobby", "title") else "title"
                self.menu_message = ""
                continue
            if event.key == pygame.K_ESCAPE and self.state == "lab_lobby" and self.show_controls_overlay:
                self.show_controls_overlay = False
                continue
            if event.key == pygame.K_ESCAPE and self.state == "shop":
                self.state = "playing"
                continue
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_F3:
                self.debug_camera = not self.debug_camera
                continue
            if DEBUG_GACHA and event.key == pygame.K_F8:
                self.game_data["normal_tickets"] = self.game_data.get("normal_tickets", 0) + 1
                self.save_progress()
                self.menu_message = "디버그: 일반 뽑기권 +1"
                continue
            if DEBUG_GACHA and event.key == pygame.K_F9:
                self.game_data["premium_tickets"] = self.game_data.get("premium_tickets", 0) + 1
                self.save_progress()
                self.menu_message = "디버그: 프리미엄 뽑기권 +1"
                continue

            if self.state == "title":
                if event.key == pygame.K_RETURN:
                    self.enter_lobby()
                elif event.key == pygame.K_c:
                    self.show_controls_overlay = not self.show_controls_overlay
                elif event.key == pygame.K_g:
                    self.menu_return_state = "title"
                    self.state = "gacha"
                elif event.key == pygame.K_h:
                    self.menu_return_state = "title"
                    self.state = "characters"
            elif self.state == "lab_lobby":
                if self.show_controls_overlay:
                    if event.key in (pygame.K_RETURN, pygame.K_BACKSPACE):
                        self.show_controls_overlay = False
                    continue
                if event.key == pygame.K_RETURN:
                    item = self.nearest_interactable(self.lobby_interactables)
                    if item:
                        self.interact_with(item)
            elif self.state == "gacha":
                if event.key == pygame.K_1:
                    self.perform_gacha("normal")
                elif event.key == pygame.K_2:
                    self.perform_gacha("premium")
                elif event.key in (pygame.K_3, pygame.K_BACKSPACE):
                    self.state = self.menu_return_state if self.menu_return_state in ("lab_lobby", "title") else "title"
            elif self.state == "characters":
                if event.key in (pygame.K_1, pygame.K_2):
                    idx = event.key - pygame.K_1
                    if idx < len(CHARACTER_POOL):
                        self.select_character(CHARACTER_POOL[idx]["id"])
                elif event.key in (pygame.K_RETURN, pygame.K_BACKSPACE):
                    self.state = self.menu_return_state if self.menu_return_state in ("lab_lobby", "title") else "title"
            elif self.state == "playing":
                if not self.room_started:
                    continue
                if event.key == pygame.K_RETURN:
                    item = self.nearest_interactable(self.room_interactables)
                    if item:
                        self.interact_with(item)
                elif event.key == pygame.K_j:
                    self.player.melee_attack(self.current_room.enemies, self.current_room.boss, self.current_room.effects, self.sounds, self.current_room.projectiles, self.effect_sprites)
                elif event.key == pygame.K_SPACE:
                    self.player.dash(self.current_room.effects, self.sounds, self.current_room.traps, self.current_room.arena_rect, self.current_room.walkable_polygon)
                elif event.key == pygame.K_k:
                    self.player.special(self.current_room.projectiles, self.current_room.effects, self.sounds, self.current_room.enemies, self.current_room.boss, self.effect_sprites)
                elif event.key == pygame.K_l:
                    elite_floor = self.current_room.room_type == ROOM_ELITE and (7 <= self.current_room.floor <= 9 or 2 <= self.current_room.floor <= 4)
                    self.player.ultimate_attack(self.current_room.enemies, self.current_room.boss, self.current_room.effects, self.sounds, self.effect_sprites, 0.5 if elite_floor else 1.0)
            elif self.state == "upgrade":
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    idx = event.key - pygame.K_1
                    if idx < len(self.upgrade_choices):
                        self.upgrade_choices[idx].apply(self.player)
                        self.message = f"{self.upgrade_choices[idx].name} 획득"
                        self.message_timer = 1.4
                        self.finish_reward_and_open_exit()
            elif self.state == "special_reward":
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    idx = event.key - pygame.K_1
                    if idx < len(self.special_choices):
                        self.special_choices[idx].apply(self.player)
                        self.message = f"{self.special_choices[idx].name} 획득!"
                        self.message_timer = 1.4
                        self.finish_reward_and_open_exit("상자가 열렸습니다. 아래층 통로가 개방되었습니다.")
            elif self.state == "pet_reward":
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    idx = event.key - pygame.K_1
                    self.choose_pet_reward(idx)
                elif event.key == pygame.K_RETURN:
                    self.choose_pet_reward(0)
            elif self.state == "shop":
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    idx = event.key - pygame.K_1
                    if idx < len(self.shop_items):
                        if Shop.buy(self.shop_items[idx], self.player):
                            self.message = f"{self.shop_items[idx][0]} 구매 완료"
                            self.message_timer = 1.2
                            self.state = "playing"
                        else:
                            self.message = "골드가 부족합니다."
                            self.message_timer = 1.2
                elif event.key in (pygame.K_RETURN, pygame.K_BACKSPACE):
                    self.state = "playing"
            elif self.state in ("game_over", "win"):
                if event.key in (pygame.K_RETURN, pygame.K_r):
                    self.enter_lobby()

    def handle_title_click(self, pos):
        if self.show_controls_overlay:
            if self.title_buttons["close_controls"].collidepoint(pos):
                self.show_controls_overlay = False
            return
        if self.title_buttons["start"].collidepoint(pos):
            self.enter_lobby()
        elif self.title_buttons["characters"].collidepoint(pos):
            self.menu_return_state = "title"
            self.state = "characters"
            self.menu_message = ""
        elif self.title_buttons["gacha"].collidepoint(pos):
            self.menu_return_state = "title"
            self.state = "gacha"
            self.menu_message = ""
        elif self.title_buttons["controls"].collidepoint(pos):
            self.show_controls_overlay = True
        elif self.title_buttons["quit"].collidepoint(pos):
            pygame.quit()
            sys.exit()

    def handle_gacha_click(self, pos):
        if self.gacha_buttons["normal"].collidepoint(pos):
            self.perform_gacha("normal")
        elif self.gacha_buttons["premium"].collidepoint(pos):
            self.perform_gacha("premium")
        elif self.gacha_buttons["back"].collidepoint(pos):
            self.state = self.menu_return_state if self.menu_return_state in ("lab_lobby", "title") else "title"
            self.menu_message = ""

    def handle_character_click(self, pos):
        for character_id, rect in self.character_card_rects:
            if rect.collidepoint(pos):
                self.select_character(character_id)
                return
        back_rect = pygame.Rect(WIDTH // 2 - 105, HEIGHT - 76, 210, 44)
        if back_rect.collidepoint(pos):
            self.state = self.menu_return_state if self.menu_return_state in ("lab_lobby", "title") else "title"
            self.menu_message = ""

    def update(self, dt):
        self.announcement_timer = max(0, self.announcement_timer - dt)
        self.message_timer = max(0, self.message_timer - dt)
        self.update_environment_particles(dt)

        if self.state == "floor_transition":
            self.floor_transition_timer -= dt
            if self.floor_transition_timer <= 0:
                self.enter_floor(self.pending_floor)
            return

        if self.state == "lab_lobby":
            keys = pygame.key.get_pressed()
            self.player.update(dt, keys, None, self.lobby_walkable_polygon())
            self.active_prompt = self.nearest_interactable(self.lobby_interactables)
            if self.player_in_lobby_auto_entry():
                self.begin_run()
            return

        if self.state == "playing":
            keys = pygame.key.get_pressed()
            self.player.update(dt, keys, self.current_room.arena_rect, self.current_room.walkable_polygon)
            camera_target = self.player.pos
            if self.current_room.boss and not self.current_room.boss.dead:
                if self.current_room.bg_key in ("boss_stage_15", "ice_dragon_stage"):
                    camera_target = self.player.pos * 0.78 + self.current_room.boss.visual_pos * 0.22
                else:
                    camera_target = self.player.pos * 0.78 + self.current_room.boss.pos * 0.22
            self.camera.update(camera_target, self.current_room.world_width, self.current_room.world_height, dt, self.current_room)
            self.active_prompt = self.nearest_interactable(self.room_interactables)
            if not self.room_started:
                self.player.invuln = max(self.player.invuln, self.announcement_timer + 0.45)
                if self.announcement_timer <= 0:
                    self.current_room.setup()
                    self.current_room.reward_processed = False
                    self.room_started = True
                    self.camera.reset(self.player.pos, self.current_room.world_width, self.current_room.world_height, self.current_room)
                    self.player.invuln = max(self.player.invuln, 0.55)
                    self.message = "전투 시작!"
                    self.message_timer = 0.45
                return
            if keys[pygame.K_j]:
                self.player.melee_attack( self.current_room.enemies, self.current_room.boss, self.current_room.effects, self.sounds, self.current_room.projectiles, self.effect_sprites, )
            self.current_room.update(dt, self.player, self.sounds)
            if self.player.just_dodge_event:
                self.slow_timer = 0.32
                self.message = "저스트 회피! 반격 피해 증가"
                self.message_timer = 0.9
                self.player.just_dodge_event = False
            if self.player.hp <= 0:
                self.game_over()
                return
            if self.current_room.cleared and not getattr(self.current_room, "reward_processed", False):
                if self.clear_timer <= 0:
                    self.clear_timer = 1.1
                    self.message = "방 클리어!"
                    self.message_timer = 1.1
                else:
                    self.clear_timer -= dt
                    if self.clear_timer <= 0:
                        self.complete_room()

    def draw_hud(self):
        draw_hud_backdrop(self.screen, 108)
        room = self.current_room
        room_name = room.room_type if room else "연구소 로비"
        zone_name = room.zone_name if room else "시작 준비 구역"
        zone_color = room.zone_color if room else CYAN
        draw_text(self.screen, self.font, f"현재 위치: {self.current_floor}F - {room_name}", 18, 12, WHITE)
        draw_text(self.screen, self.font_sm, f"구역: {zone_name}", 18, 42, zone_color)
        if self.room_interactables:
            objective = "목표: 출구/장치 근처에서 Enter"
        elif room and room.room_type == ROOM_REWARD:
            objective = "목표: 상자를 열고 보상을 받으세요"
        elif room and room.room_type in (ROOM_SHOP, ROOM_REST):
            objective = "목표: 장치를 이용하거나 아래층 통로로 이동"
        elif getattr(room, "reward_processed", False):
            objective = "목표: 아래층 계단 찾기"
        else:
            objective = "목표: 적을 처치하고 아래층 계단 찾기"
        draw_text(self.screen, self.font_sm, objective, 18, 70, (215, 228, 232))

        draw_hud_bar(self.screen, 330, 14, 190, 14, self.player.hp, self.player.max_hp, (245, 85, 115))
        draw_text(self.screen, self.font_sm, f"체력 {int(self.player.hp)}/{self.player.max_hp}", 336, 36, WHITE)
        draw_text(self.screen, self.font_sm, f"점수 {self.score}", 550, 12, WHITE)
        draw_text(self.screen, self.font_sm, f"골드 {self.player.gold}", 550, 38, YELLOW)
        dash_ready = self.player.dash_cooldown <= 0
        dash_color = CYAN if dash_ready else BLUE
        draw_hud_bar(self.screen, 660, 14, 130, 12, self.player.dash_cooldown_max - self.player.dash_cooldown, self.player.dash_cooldown_max, dash_color, dash_ready)
        draw_text(self.screen, self.font_sm, "대시 READY" if dash_ready else f"대시 {self.player.dash_cooldown:.1f}s", 675, 35, CYAN if dash_ready else WHITE)
        skill_ready = self.player.special_cooldown <= 0
        skill_color = (190, 105, 255) if skill_ready else (115, 100, 205)
        draw_hud_bar(self.screen, 810, 14, 130, 12, self.player.special_cooldown_max - self.player.special_cooldown, self.player.special_cooldown_max, skill_color, skill_ready)
        draw_text(self.screen, self.font_sm, "스킬", 850, 35, WHITE)
        draw_hud_bar(self.screen, 960, 14, 160, 12, self.player.ultimate, 100, ORANGE)
        draw_text(self.screen, self.font_sm, "궁극기", 1014, 35, WHITE)
        if self.player.selected_pet_type in PET_DEFS:
            pet = PET_DEFS[self.player.selected_pet_type]
            icon = load_pet_image(self.player.selected_pet_type, (28, 28))
            if icon:
                self.screen.blit(icon, (1130, 20))
                text_x = 1162
            else:
                pygame.draw.circle(self.screen, pet["color"], (1144, 34), 12)
                text_x = 1162
            draw_text(self.screen, self.font_sm, pet["name"], text_x, 18, WHITE)
            draw_text(self.screen, self.font_sm, pet["short"], text_x, 40, pet["color"])

    def draw_interactable(self, surface, item, offset=(0, 0)):
        pos = item["pos"]
        ox, oy = offset
        x, y = int(pos.x - ox), int(pos.y - oy)
        kind = item["kind"]
        color = CYAN
        if "gacha" in kind:
            color = YELLOW
        elif "character" in kind:
            color = PURPLE
        elif "exit" in kind or "stairs" in kind:
            color = GREEN
        elif "reward" in kind:
            color = ORANGE
        elif "shop" in kind:
            color = (255, 190, 90)
        pygame.draw.ellipse(surface, (0, 0, 0, 105), (x - 48, y + 24, 96, 24))
        if kind in ("exit_stairs", "stairs_to_20f"):
            for step in range(4):
                pygame.draw.rect(surface, (22, 32, 38), (x - 68 + step * 13, y + 30 - step * 12, 136 - step * 26, 12), border_radius=3)
                pygame.draw.rect(surface, color, (x - 68 + step * 13, y + 30 - step * 12, 136 - step * 26, 12), 1, border_radius=3)
        elif kind == "reward_chest":
            pygame.draw.rect(surface, (68, 42, 22), (x - 42, y - 22, 84, 48), border_radius=6)
            pygame.draw.rect(surface, color, (x - 42, y - 22, 84, 48), 2, border_radius=6)
            pygame.draw.rect(surface, (255, 230, 130), (x - 8, y - 4, 16, 20), border_radius=3)
        else:
            pygame.draw.rect(surface, (18, 27, 34), (x - 44, y - 52, 88, 78), border_radius=8)
            pygame.draw.rect(surface, color, (x - 44, y - 52, 88, 78), 2, border_radius=8)
            pygame.draw.rect(surface, (*color, 80), (x - 28, y - 38, 56, 32), border_radius=4)
        draw_text(surface, self.font_sm, item["label"], x, y - 80, WHITE, center=True)

    def draw_lobby(self):
        self.screen.fill((7, 10, 14))
        floor = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(floor, (13, 22, 28), (0, 0, WIDTH, HEIGHT))
        for i in range(18):
            alpha = int(18 + i * 4)
            pygame.draw.rect(floor, (0, 0, 0, alpha), (0, i * 16, WIDTH, 16))
        pygame.draw.rect(floor, (18, 38, 44), (90, 250, WIDTH - 180, 375), border_radius=18)
        pygame.draw.rect(floor, (80, 220, 210), (90, 250, WIDTH - 180, 375), 2, border_radius=18)
        for x in range(120, WIDTH - 100, 92):
            pygame.draw.line(floor, (90, 135, 138, 48), (x, 260), (x - 60, 620), 1)
        for y in range(294, 624, 54):
            pygame.draw.line(floor, (90, 135, 138, 44), (100, y), (WIDTH - 100, y), 1)
        pygame.draw.rect(floor, (18, 24, 31), (WIDTH // 2 - 120, 205, 240, 96), border_radius=8)
        pygame.draw.rect(floor, GREEN, (WIDTH // 2 - 120, 205, 240, 96), 2, border_radius=8)
        pygame.draw.rect(floor, (8, 13, 18), (145, 360, 170, 140), border_radius=10)
        pygame.draw.rect(floor, (8, 13, 18), (960, 360, 170, 140), border_radius=10)
        self.screen.blit(floor, (0, 0))

        for item in self.lobby_interactables:
            self.draw_interactable(self.screen, item)
        draw_ellipse_shadow(self.screen, self.player.pos, self.player.radius)
        self.player.draw(self.screen)

        hud = pygame.Surface((WIDTH, 96), pygame.SRCALPHA)
        hud.fill((5, 8, 12, 190))
        self.screen.blit(hud, (0, 0))
        draw_text(self.screen, self.font_md, "시연구소 로비", 24, 14, CYAN)
        draw_text(self.screen, self.font_sm, "목표: 격리구역 진입문에서 Enter를 눌러 20F로 내려가기", 26, 56, WHITE)
        draw_text(self.screen, self.font_sm, f"일반권 {self.game_data.get('normal_tickets', 0)} / 프리미엄권 {self.game_data.get('premium_tickets', 0)}", WIDTH - 330, 18, YELLOW)
        draw_text(self.screen, self.font_sm, f"최고 기록 {self.high_score}", WIDTH - 330, 46, WHITE)
        if self.active_prompt:
            draw_text(self.screen, self.font_md, self.active_prompt["prompt"], WIDTH // 2, HEIGHT - 74, YELLOW, center=True)
        self.draw_message()
        if self.show_controls_overlay:
            self.draw_controls_overlay(pygame.mouse.get_pos())

    def draw_room_interactables(self, surface):
        for item in self.room_interactables:
            if item.get("active") and not item.get("used"):
                self.draw_interactable(surface, item)

    def draw_playing(self):
        room = self.current_room
        world = pygame.Surface((room.world_width, room.world_height))
        self.draw_world_background(world, room)
        self.draw_world_combat_floor(world, room)
        self.draw_room_interactables(world)
        room.draw_entities(world, self.font_sm, self.player)
        self.draw_just_dodge_text(world)
        camera_pos = self.camera.offset()
        if room.bg_key == "boss_stage_15":
            rear_depth = 0.0
        elif room.floor_bottom_y > room.floor_top_y:
            rear_depth = clamp((room.floor_bottom_y - self.player.pos.y) / (room.floor_bottom_y - room.floor_top_y), 0.0, 1.0)
        else:
            rear_depth = 0.0
        zoom = 1.0 if room.bg_key == "boss_stage_15" else 1.0 + rear_depth * 0.045
        view_w = max(1, min(room.world_width, int(WIDTH / zoom)))
        view_h = max(1, min(room.world_height, int(HEIGHT / zoom)))
        view_x = int(clamp(camera_pos.x + (WIDTH - view_w) * 0.5, 0, max(0, room.world_width - view_w)))
        view_y = int(clamp(camera_pos.y + (HEIGHT - view_h) * 0.5, 0, max(0, room.world_height - view_h)))
        view_rect = pygame.Rect(view_x, view_y, view_w, view_h)
        self.last_view_rect = view_rect
        self.last_view_zoom = WIDTH / view_w
        if zoom > 1.003:
            self.screen.blit(pygame.transform.smoothscale(world.subsurface(view_rect), (WIDTH, HEIGHT)), (0, 0))
        else:
            self.screen.blit(world, (-int(camera_pos.x), -int(camera_pos.y)))
        self.draw_scene_color_grade()
        self.draw_hud()
        if self.current_room.room_type == ROOM_SURVIVAL:
            left = max(0, self.current_room.survival_goal - self.current_room.timer)
            draw_text(self.screen, self.font_md, f"버티기 {left:.1f}초", WIDTH // 2, 96, YELLOW, center=True)
        if self.active_prompt:
            draw_text(self.screen, self.font_md, self.active_prompt["prompt"], WIDTH // 2, HEIGHT - 74, YELLOW, center=True)
        self.draw_camera_debug()
        self.draw_announcement()
        self.draw_message()

    def draw_end_screen(self, title, subtitle, color):
        self.draw_background()
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        draw_text(self.screen, self.font_lg, title, WIDTH // 2, 150, color, center=True)
        draw_text(self.screen, self.font_md, subtitle, WIDTH // 2, 225, WHITE, center=True)
        draw_text(self.screen, self.font, f"최종 점수: {self.score}", WIDTH // 2, 300, WHITE, center=True)
        draw_text(self.screen, self.font, f"최고 기록: {self.high_score}", WIDTH // 2, 340, YELLOW, center=True)
        y = 386
        if self.best_updated:
            draw_text(self.screen, self.font, "최고 기록 갱신", WIDTH // 2, y, CYAN, center=True)
            y += 42
        if self.run_reward_log:
            draw_text(self.screen, self.font_sm, "이번 런 티켓 보상", WIDTH // 2, y, CYAN, center=True)
            y += 28
            for reward in self.run_reward_log[-4:]:
                draw_text(self.screen, self.font_sm, reward, WIDTH // 2, y, WHITE, center=True)
                y += 24
        draw_text(self.screen, self.font_md, "Enter 로비로 돌아가기    ESC 종료", WIDTH // 2, 590, WHITE, center=True)

    def draw_floor_transition(self):
        self.screen.fill((0, 0, 0))
        draw_text(self.screen, self.font_lg, f"{self.current_floor}F -> {self.pending_floor}F", WIDTH // 2, HEIGHT // 2 - 35, CYAN, center=True)
        draw_text(self.screen, self.font, "아래층으로 이동 중...", WIDTH // 2, HEIGHT // 2 + 40, WHITE, center=True)

    def draw(self):
        self.update_music()
        if self.state == "title":
            self.draw_title()
        elif self.state == "lab_lobby":
            self.draw_lobby()
        elif self.state == "floor_transition":
            self.draw_floor_transition()
        elif self.state == "gacha":
            self.draw_gacha()
        elif self.state == "characters":
            self.draw_characters()
        elif self.state == "upgrade":
            self.draw_upgrade()
            self.draw_announcement()
        elif self.state == "special_reward":
            self.draw_special_reward()
            self.draw_announcement()
        elif self.state == "pet_reward":
            self.draw_pet_reward()
            self.draw_announcement()
        elif self.state == "shop":
            self.draw_shop()
            self.draw_announcement()
            self.draw_message()
        elif self.state == "game_over":
            self.draw_end_screen("게임 오버", f"도달한 최저 층: {self.current_floor}층", RED)
        elif self.state == "win":
            self.draw_end_screen("탈출 성공", "20층 격리구역을 돌파했습니다.", CYAN)
        else:
            self.draw_playing()
        pygame.display.flip()

    def load_lobby_image(self):
        path = find_asset_path(os.path.join("assets", "lobby.png"), "assets/lobby.png", "lobby.png")
        if not path:
            print("lobby.png 없음: 임시 로비 배경 사용")
            return None
        try:
            image = pygame.image.load(path).convert()
            print("로비 배경 로드 성공:", path)
            return pygame.transform.smoothscale(image, (WIDTH, HEIGHT))
        except (pygame.error, OSError) as exc:
            print("lobby.png 로드 실패: 임시 로비 배경 사용", exc)
            return None

    def enter_lobby(self):
        self.state = "lab_lobby"
        self.menu_return_state = "lab_lobby"
        self.current_floor = 20
        self.current_room = None
        self.player = Player(self.game_data.get("selected_character_id", STARTER_CHARACTER_ID))
        self.apply_selected_character_bonus()
        self.player.pos = self.lobby_point(0.50, 0.78)
        self.player.hp = self.player.max_hp
        self.lobby_interactables = [ self.make_interactable( "gacha_machine", self.lobby_point(*LOBBY_INTERACTABLE_RATIOS["gacha_machine"]), 120, "실험 뽑기기계", "ENTER: 뽑기기계 사용", ), self.make_interactable( "stairs_to_20f", self.lobby_point(*LOBBY_INTERACTABLE_RATIOS["stairs_to_20f"]), 155, "20층 진입 계단", "ENTER: 20층으로 내려가기", ), self.make_interactable( "character_terminal", self.lobby_point(*LOBBY_INTERACTABLE_RATIOS["character_terminal"]), 115, "캐릭터 관리 단말기", "ENTER: 캐릭터 선택", ), ]
        self.message = "시연구소 로비입니다. 중앙 계단에서 20층으로 내려갈 수 있습니다."
        self.message_timer = 2.2
        self.active_prompt = None
        self.gacha_result = None
        self.show_controls_overlay = False

    def draw_lobby_interactable_marker(self, surface, item):
        pos = item["pos"]
        x, y = int(pos.x), int(pos.y)
        kind = item["kind"]
        if kind == "gacha_machine":
            color = YELLOW
        elif kind == "character_terminal":
            color = PURPLE
        else:
            color = GREEN
        pulse = 0.58 + 0.22 * math.sin(pygame.time.get_ticks() * 0.006)
        marker = pygame.Surface((150, 70), pygame.SRCALPHA)
        pygame.draw.ellipse(marker, (*color, int(70 + pulse * 55)), (18, 28, 114, 28), 2)
        pygame.draw.circle(marker, (*color, 150), (75, 18), 8)
        pygame.draw.circle(marker, WHITE, (75, 18), 3)
        surface.blit(marker, (x - 75, y - 35))
        draw_text(surface, self.font_sm, item["label"], x, y - 54, WHITE, center=True)

    def draw_lobby_fallback_background(self):
        self.screen.fill((7, 10, 14))
        floor = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(floor, (13, 22, 28), (0, 0, WIDTH, HEIGHT))
        for i in range(18):
            alpha = int(18 + i * 4)
            pygame.draw.rect(floor, (0, 0, 0, alpha), (0, i * 16, WIDTH, 16))
        pygame.draw.polygon(floor, (18, 38, 44), self.lobby_walkable_polygon())
        pygame.draw.polygon(floor, (80, 220, 210), self.lobby_walkable_polygon(), 2)
        for x in range(120, WIDTH - 100, 92):
            pygame.draw.line(floor, (90, 135, 138, 48), (x, HEIGHT * 0.48), (x - 60, HEIGHT * 0.91), 1)
        pygame.draw.rect(floor, (18, 24, 31), (WIDTH // 2 - 120, 205, 240, 96), border_radius=8)
        pygame.draw.rect(floor, GREEN, (WIDTH // 2 - 120, 205, 240, 96), 2, border_radius=8)
        self.screen.blit(floor, (0, 0))

    def draw_lobby(self):
        if self.lobby_image:
            self.screen.blit(self.lobby_image, (0, 0))
        else:
            self.draw_lobby_fallback_background()

        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(shade, (0, 0, 0, 70), (0, 0, WIDTH, 96))
        pygame.draw.rect(shade, (0, 0, 0, 76), (0, HEIGHT - 112, WIDTH, 112))
        self.screen.blit(shade, (0, 0))

        for item in self.lobby_interactables:
            self.draw_lobby_interactable_marker(self.screen, item)
        draw_ellipse_shadow(self.screen, self.player.pos, self.player.radius)
        self.player.draw(self.screen)

        draw_text(self.screen, self.font_md, "시연구소 로비", 24, 14, CYAN)
        draw_text(self.screen, self.font_sm, "목표: 중앙 계단에서 Enter를 눌러 20F 격리구역으로 내려가기", 26, 56, WHITE)
        draw_text(self.screen, self.font_sm, f"일반권 {self.game_data.get('normal_tickets', 0)} / 프리미엄권 {self.game_data.get('premium_tickets', 0)}", WIDTH - 330, 18, YELLOW)
        draw_text(self.screen, self.font_sm, f"최고 기록 {self.high_score}", WIDTH - 330, 46, WHITE)
        if self.active_prompt:
            prompt_panel = pygame.Surface((560, 52), pygame.SRCALPHA)
            pygame.draw.rect(prompt_panel, (0, 0, 0, 172), prompt_panel.get_rect(), border_radius=8)
            pygame.draw.rect(prompt_panel, (*YELLOW, 210), prompt_panel.get_rect(), 2, border_radius=8)
            self.screen.blit(prompt_panel, (WIDTH // 2 - 280, HEIGHT - 86))
            draw_text(self.screen, self.font, self.active_prompt["prompt"], WIDTH // 2, HEIGHT - 75, YELLOW, center=True)
        self.draw_message()
        if self.show_controls_overlay:
            self.draw_controls_overlay(pygame.mouse.get_pos())

    def enter_lobby(self):
        self.state = "lab_lobby"
        self.menu_return_state = "lab_lobby"
        self.current_floor = 20
        self.current_room = None
        self.player = Player(self.game_data.get("selected_character_id", STARTER_CHARACTER_ID))
        self.apply_selected_character_bonus()
        self.player.pos = self.lobby_point(0.50, 0.78)
        self.player.hp = self.player.max_hp
        self.lobby_interactables = [ self.make_interactable( "gacha_machine", self.lobby_point(*LOBBY_INTERACTABLE_RATIOS["gacha_machine"]), 120, "실험 뽑기기계", "ENTER: 뽑기기계 사용", ), self.make_interactable( "stairs_to_20f", self.lobby_point(*LOBBY_INTERACTABLE_RATIOS["stairs_to_20f"]), 155, "20층 진입 계단", "안쪽으로 들어가면 20층 자동 진입", ), self.make_interactable( "character_terminal", self.lobby_point(*LOBBY_INTERACTABLE_RATIOS["character_terminal"]), 115, "캐릭터 관리 단말기", "ENTER: 캐릭터 선택", ), ]
        self.message = "시연구소 로비입니다. 중앙 계단 안쪽으로 들어가면 20층으로 내려갑니다."
        self.message_timer = 2.2
        self.active_prompt = None
        self.gacha_result = None
        self.show_controls_overlay = False

    def draw_lobby(self):
        if self.lobby_image:
            self.screen.blit(self.lobby_image, (0, 0))
        else:
            self.draw_lobby_fallback_background()

        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(shade, (0, 0, 0, 70), (0, 0, WIDTH, 96))
        pygame.draw.rect(shade, (0, 0, 0, 76), (0, HEIGHT - 112, WIDTH, 112))
        self.screen.blit(shade, (0, 0))

        for item in self.lobby_interactables:
            self.draw_lobby_interactable_marker(self.screen, item)
        draw_ellipse_shadow(self.screen, self.player.pos, self.player.radius)
        self.player.draw(self.screen)

        draw_text(self.screen, self.font_md, "시연구소 로비", 24, 14, CYAN)
        draw_text(self.screen, self.font_sm, "목표: 중앙 계단 안쪽으로 들어가 20F 격리구역으로 내려가기", 26, 56, WHITE)
        draw_text(self.screen, self.font_sm, f"일반권 {self.game_data.get('normal_tickets', 0)} / 프리미엄권 {self.game_data.get('premium_tickets', 0)}", WIDTH - 330, 18, YELLOW)
        draw_text(self.screen, self.font_sm, f"최고 기록 {self.high_score}", WIDTH - 330, 46, WHITE)
        if self.active_prompt:
            prompt_panel = pygame.Surface((620, 52), pygame.SRCALPHA)
            pygame.draw.rect(prompt_panel, (0, 0, 0, 172), prompt_panel.get_rect(), border_radius=8)
            pygame.draw.rect(prompt_panel, (*YELLOW, 210), prompt_panel.get_rect(), 2, border_radius=8)
            self.screen.blit(prompt_panel, (WIDTH // 2 - 310, HEIGHT - 86))
            draw_text(self.screen, self.font, self.active_prompt["prompt"], WIDTH // 2, HEIGHT - 75, YELLOW, center=True)
        self.draw_message()
        if self.show_controls_overlay:
            self.draw_controls_overlay(pygame.mouse.get_pos())

    def get_world_background(self, room):
        if room.room_type in (ROOM_REWARD, ROOM_REST):
            forced_key = get_normal_stage_background_key_for_floor(room.floor)
            if room.bg_key != forced_key:
                print("reward/rest 배경 강제:", room.bg_key, "->", forced_key)
                room.bg_key = forced_key
        if not is_valid_background_filename(room.bg_key, allow_boss_stage=room.room_type in (ROOM_BOSS, ROOM_FINAL)):
            fallback_key = get_normal_stage_background_key_for_floor(room.floor)
            print("잘못된 배경 키 차단:", room.bg_key, "->", fallback_key)
            room.bg_key = fallback_key
        if not is_valid_background_filename(room.bg_key):
            fallback_key = get_background_key(room.floor)
            print("잘못된 배경 키 차단:", room.bg_key, "->", fallback_key)
            room.bg_key = fallback_key
        key = (room.bg_key, room.world_width, room.world_height)
        if key in self.world_backgrounds:
            return self.world_backgrounds[key]
        base = self.backgrounds.get(room.bg_key)
        if not base and room.bg_key == "ice_dragon_stage":
            print("ice_dragon_stage 배경 없음: 얼음 드래곤 fallback 배경 사용")
            bg = self.create_ice_dragon_fallback_background(room.world_width, room.world_height)
            self.world_backgrounds[key] = bg
            return bg
        if not base and room.bg_key == "boss_stage_15":
            print("boss_stage_15 배경 없음: 15층 fallback 배경 사용")
            bg = self.create_boss15_fallback_background(room.world_width, room.world_height)
            self.world_backgrounds[key] = bg
            return bg
        if not base and room.bg_key == "boss_stage_15":
            print("15층 보스방 배경 없음: 기존 보스방 배경 사용")
            base = self.backgrounds.get("15_11")
        if not base and room.bg_key == "stage_20_16":
            print("20~16층 배경 없음: 기존 배경 사용")
            base = self.backgrounds.get("20_16")
        if not base:
            base = self.lab_arena_image
        if base:
            bg = pygame.transform.smoothscale(base, (room.world_width, room.world_height))
        else:
            bg = pygame.Surface((room.world_width, room.world_height))
            old_screen = self.screen
            temp_screen = pygame.Surface((WIDTH, HEIGHT))
            self.screen = temp_screen
            self.draw_fallback_background(room.bg_key)
            self.screen = old_screen
            bg = pygame.transform.smoothscale(temp_screen, (room.world_width, room.world_height))
        self.world_backgrounds[key] = bg
        return bg

    def enter_floor(self, floor):
        self.current_floor = floor
        self.current_room = self.rooms[floor]
        self.current_room.reward_processed = False
        self.room_interactables = []
        self.active_prompt = None
        self.announcement_timer = 0.0
        self.room_started = False
        self.clear_timer = 0
        self.message = ""
        self.message_timer = 0
        if self.current_room.bg_key == "ice_dragon_stage":
            start = pygame.Vector2( self.current_room.world_width * 0.50, self.current_room.floor_bottom_y - 110, )
        elif self.current_room.bg_key == "boss_stage_15":
            start = pygame.Vector2( self.current_room.world_width * 0.50, self.current_room.world_height * 0.70, )
        elif self.current_room.bg_key == "stage_20_16":
            start = pygame.Vector2( self.current_room.world_width * STAGE_20_16_PLAYER_START_RATIO[0], self.current_room.world_height * STAGE_20_16_PLAYER_START_RATIO[1], )
        else:
            start = pygame.Vector2(self.current_room.world_width // 2, self.current_room.floor_bottom_y - 120)
        self.player.pos = clamp_point_to_polygon(start, self.current_room.walkable_polygon, self.player.radius)
        self.camera.reset(self.player.pos, self.current_room.world_width, self.current_room.world_height, self.current_room)

        if self.current_room.room_type == ROOM_REWARD:
            self.current_room.setup()
            self.room_started = True
            self.state = "playing"
            self.room_interactables.append(self.make_interactable("reward_chest", (self.current_room.world_width // 2, self.current_room.floor_top_y + 160), 82, "보상 상자", "ENTER: 상자 열기"))
            self.message = "보상 상자가 있습니다."
            self.message_timer = 1.5
        elif self.current_room.room_type == ROOM_SHOP:
            self.current_room.setup()
            self.room_started = True
            self.state = "playing"
            self.shop_items = Shop.random_items()
            self.room_interactables.append(self.make_interactable("shop_terminal", (self.current_room.arena_rect.centerx - 220, self.current_room.arena_rect.centery), 80, "상점 단말기", "ENTER: 상점 이용"))
            self.open_floor_exit("상점 이용 후 아래층 통로로 이동하세요.")
        elif self.current_room.room_type == ROOM_REST:
            self.current_room.setup()
            self.room_started = True
            self.state = "playing"
            self.room_interactables.append(self.make_interactable("rest_device", (self.current_room.arena_rect.centerx - 220, self.current_room.arena_rect.centery), 80, "회복 캡슐", "ENTER: 회복 장치 사용"))
            self.open_floor_exit("회복 후 아래층 통로로 이동하세요.")
        else:
            self.state = "playing"

    def open_floor_exit(self, text=None):
        if any(item["kind"] in ("exit_stairs", "exit_door") and item.get("active") for item in self.room_interactables):
            return
        room = self.current_room
        if not room:
            return
        if room.room_type == ROOM_FINAL:
            kind = "exit_door"
            label = "탈출 리프트"
            prompt = "ENTER: 결과 화면으로 이동"
            pos = (room.world_width * 0.5, room.floor_top_y + 88)
        elif room.room_type in (ROOM_REWARD, ROOM_SHOP, ROOM_REST):
            kind = "exit_stairs"
            label = "아래층 통로"
            prompt = "ENTER: 다음 층으로 이동"
            pos = (room.arena_rect.right - 130, room.arena_rect.top + 92)
        else:
            kind = "exit_stairs"
            label = "아래층 계단"
            prompt = "ENTER: 다음 층으로 이동"
            if room.floor == ICE_DRAGON_FLOOR and room.room_type == ROOM_BOSS:
                if room.bg_key == "ice_dragon_stage":
                    pos = ( room.world_width * ICE_DRAGON_EXIT_POS_RATIO[0], room.world_height * ICE_DRAGON_EXIT_POS_RATIO[1], )
                else:
                    pos = ( room.world_width * BOSS15_EXIT_POS_RATIO[0], room.world_height * BOSS15_EXIT_POS_RATIO[1], )
            elif room.bg_key == "stage_20_16":
                pos = ( room.world_width * STAGE_20_16_EXIT_RATIO[0], room.world_height * STAGE_20_16_EXIT_RATIO[1], )
            else:
                pos = (room.world_width * 0.5, room.floor_top_y + 70)
        self.room_interactables.append(self.make_interactable(kind, pos, 95, label, prompt))
        self.message = text or "출구가 열렸습니다. 아래층 계단으로 이동하세요."
        self.message_timer = 2.0

    def draw_world_background(self, surface, room):
        background = self.get_world_background(room)
        if room.bg_key in ("boss_stage_15", "ice_dragon_stage"):
            room.background_surface = background
        surface.blit(background, (0, 0))
        if room.bg_key not in ("stage_20_16", "boss_stage_15", "ice_dragon_stage"):
            self.draw_world_decorations(surface, room)

    def draw_world_combat_floor(self, surface, room):
        if room.bg_key == "ice_dragon_stage":
            if DEBUG_BOSS15_AREA or DEBUG_BOSS15_FLOOR or DEBUG_ICE_ARENA_BOUNDS:
                floor = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
                pygame.draw.polygon(floor, (80, 255, 255, 70), room.walkable_polygon)
                pygame.draw.polygon(floor, (80, 255, 255, 160), room.walkable_polygon, 3)
                pygame.draw.line(floor, (255, 240, 120, 170), (room.arena_rect.left, room.floor_top_y), (room.arena_rect.right, room.floor_top_y), 2)
                if DEBUG_ICE_ARENA_BOUNDS:
                    cx, cy, (rx, ry) = get_ice_dragon_arena_values(room.world_width, room.world_height)
                    arena_rect = pygame.Rect(int(cx - rx), int(cy - ry), int(rx * 2), int(ry * 2))
                    pygame.draw.ellipse(floor, (255, 255, 255, 180), arena_rect, 2)
                    pygame.draw.circle(floor, (255, 240, 120, 210), (int(cx), int(cy)), 8)
                    if DEBUG_BREATH_SECTORS:
                        for index in range(5):
                            polygon = ice_dragon_sector_polygon((cx, cy), rx, ry, index)
                            pygame.draw.polygon(floor, (255, 255, 255, 90), polygon, 1)
                surface.blit(floor, (0, 0))
            return

        if room.bg_key == "boss_stage_15":
            floor = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            if DEBUG_BOSS15_AREA or DEBUG_BOSS15_FLOOR:
                pygame.draw.polygon(floor, (80, 255, 120, 62), room.walkable_polygon)
                pygame.draw.polygon(floor, (80, 255, 120, 150), room.walkable_polygon, 3)
                pygame.draw.line(floor, (255, 230, 80, 160), (room.arena_rect.left, room.floor_top_y), (room.arena_rect.right, room.floor_top_y), 2)
                melee_zone = pygame.Rect( int(room.world_width * BOSS15_MELEE_ZONE_RATIO[0]), int(room.world_height * BOSS15_MELEE_ZONE_RATIO[1]), int(room.world_width * BOSS15_MELEE_ZONE_RATIO[2]), int(room.world_height * BOSS15_MELEE_ZONE_RATIO[3]), )
                pygame.draw.rect(floor, (80, 220, 255, 150), melee_zone, 2)
                exit_pos = ( room.world_width * BOSS15_EXIT_POS_RATIO[0], room.world_height * BOSS15_EXIT_POS_RATIO[1], )
                pygame.draw.circle(floor, (255, 240, 80, 180), (int(exit_pos[0]), int(exit_pos[1])), 18, 2)
            surface.blit(floor, (0, 0))
            return

        if room.bg_key == "stage_20_16":
            floor = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            pygame.draw.polygon(floor, (0, 0, 0, 22), room.walkable_polygon)
            pygame.draw.polygon(floor, (70, 230, 210, 18), room.walkable_polygon)
            if DEBUG_WALKABLE:
                pygame.draw.polygon(floor, (80, 255, 120, 110), room.walkable_polygon, 3)
                exit_pos = ( room.world_width * STAGE_20_16_EXIT_RATIO[0], room.world_height * STAGE_20_16_EXIT_RATIO[1], )
                pygame.draw.circle(floor, (255, 240, 80, 180), (int(exit_pos[0]), int(exit_pos[1])), 18, 2)
            surface.blit(floor, (0, 0))
            return

        floor = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        arena = room.arena_rect
        key = room.bg_key
        if key == "20_16":
            tint = (70, 205, 195)
        elif key == "15_11":
            tint = (160, 185, 45)
        elif key == "10_6":
            tint = (75, 120, 215)
        else:
            tint = (195, 60, 65)

        pygame.draw.polygon(floor, (4, 7, 9, 24), room.walkable_polygon)
        for i in range(22):
            t = i / 21
            y = int(room.floor_top_y + t * (room.floor_bottom_y - room.floor_top_y))
            alpha = int(12 + t * 38)
            left, right = polygon_x_bounds(y, room.walkable_polygon)
            pygame.draw.rect(floor, (0, 0, 0, alpha), (left, y, right - left, 16))
        pygame.draw.ellipse(floor, (*tint, 18), (arena.centerx - 460, room.floor_top_y + 120, 920, 260))
        pygame.draw.rect(floor, (0, 0, 0, 58), (arena.left, room.floor_bottom_y - 8, arena.width, 62), border_radius=14)
        pygame.draw.polygon(floor, (*tint, 26), room.walkable_polygon)
        surface.blit(floor, (0, 0))

    def run(self):
        while True:
            raw_dt = self.clock.tick(FPS) / 1000.0
            if self.slow_timer > 0:
                self.slow_timer = max(0, self.slow_timer - raw_dt)
                dt = raw_dt * 0.34
            else:
                dt = raw_dt
            self.handle_events()
            self.update(dt)
            self.draw()

def boss15_asset_candidates(filename):
    stem, ext = os.path.splitext(filename)
    return [ os.path.join("assets", filename), filename, os.path.join("assets", f"{filename}.png") if not filename.endswith(".png") else os.path.join("assets", f"{filename}.png"), os.path.join("assets", f"{stem}.png.png"), f"{stem}.png.png", os.path.join("assets", f"assets{stem}.png.png"), ]

def boss15_sheet_rects(sheet, frame_count, motion_key):
    width, height = sheet.get_size()
    if motion_key == "idle":
        rect = pygame.Rect( int(width * 0.000), int(height * 0.018), int(width * 0.180), int(height * 0.40), )
        return [rect.clip(sheet.get_rect())]

    if motion_key == "telegraph":
        cols, rows = 3, 2
        frame_w = width // cols
        frame_h = height // rows
        return [ pygame.Rect( (index % cols) * frame_w, (index // cols) * frame_h, frame_w, frame_h, ) for index in range(min(frame_count, cols * rows)) ]

    pose_index = { "skill1": 1, "skill2": 6, "groggy": 4, "defeat": 7, }.get(motion_key, 0)
    cols, rows = 4, 2
    cell_w = width / cols
    cell_h = height / rows
    col = pose_index % cols
    row = pose_index // cols
    rect = pygame.Rect( int(cell_w * col + cell_w * 0.03), int(cell_h * row + cell_h * 0.03), int(cell_w * 0.94), int(cell_h * 0.90), )
    return [rect.clip(sheet.get_rect())]

def remove_boss15_sheet_background(surface):
    image = remove_neutral_edge_background(surface, tolerance=120)
    image = remove_white_background(image)
    width, height = image.get_size()
    for y in range(height):
        for x in range(width):
            color = image.get_at((x, y))
            if color.a <= 0:
                continue
            maximum = max(color.r, color.g, color.b)
            minimum = min(color.r, color.g, color.b)
            average = (color.r + color.g + color.b) / 3
            if maximum - minimum < 46 and average > 132:
                image.set_at((x, y), (color.r, color.g, color.b, 0))
    return image

def apply_boss15_scene_tone(surface):
    image = surface.copy().convert_alpha()
    image.fill((198, 218, 245, 216), special_flags=pygame.BLEND_RGBA_MULT)
    return image

def prepare_boss15_frame(frame, motion_key):
    if motion_key == "telegraph":
        return trim_transparent(remove_boss15_sheet_background(frame), padding=4)
    cleaned = remove_boss15_sheet_background(frame)
    cleaned = keep_significant_alpha_components(cleaned, min_alpha=16)
    cleaned = trim_transparent(cleaned, padding=7)
    visible_h = max(1, int(cleaned.get_height() * BOSS15_BODY_CROP_BOTTOM_RATIO))
    cleaned = cleaned.subsurface(pygame.Rect(0, 0, cleaned.get_width(), visible_h)).copy()
    cleaned = apply_edge_fade(cleaned, margin_ratio=0.025)
    return apply_boss15_scene_tone(cleaned)

def slice_boss15_sheet(sheet, frame_count, target_height, motion_key="idle"):
    raw_frames = []
    for frame_rect in boss15_sheet_rects(sheet, max(1, int(frame_count)), motion_key):
        frame = sheet.subsurface(frame_rect.clip(sheet.get_rect())).copy()
        try:
            frame = prepare_boss15_frame(frame, motion_key)
        except (pygame.error, ValueError):
            pass
        if frame.get_width() <= 2 or frame.get_height() <= 2:
            continue
        height = max(24, int(target_height))
        width = max(24, int(frame.get_width() * height / max(1, frame.get_height())))
        raw_frames.append(pygame.transform.smoothscale(frame, (width, height)))

    if not raw_frames:
        return []

    canvas_w = max(frame.get_width() for frame in raw_frames)
    canvas_h = max(frame.get_height() for frame in raw_frames)
    frames = []
    for frame in raw_frames:
        canvas = pygame.Surface((canvas_w, canvas_h), pygame.SRCALPHA)
        canvas.blit(frame, ((canvas_w - frame.get_width()) // 2, canvas_h - frame.get_height()))
        frames.append(canvas)
    return frames

def load_boss15_motion_resources(self):
    cached_frames = BOSS15_ASSET_CACHE.get("frames")
    if cached_frames:
        return {key: list(value) for key, value in cached_frames.items()}

    resource_defs = { "idle": ("boss15_idle.png", BOSS15_FRAME_COUNTS["idle"], HEIGHT * BOSS15_VISUAL_HEIGHT_RATIO), "skill1": ("boss15_skill1.png", BOSS15_FRAME_COUNTS["skill1"], HEIGHT * BOSS15_VISUAL_HEIGHT_RATIO), "skill2": ("boss15_skill2.png", BOSS15_FRAME_COUNTS["skill2"], HEIGHT * BOSS15_VISUAL_HEIGHT_RATIO), "groggy": ("boss15_groggy.png", BOSS15_FRAME_COUNTS["groggy"], HEIGHT * BOSS15_VISUAL_HEIGHT_RATIO), "defeat": ("boss15_defeat.png", BOSS15_FRAME_COUNTS["defeat"], HEIGHT * BOSS15_VISUAL_HEIGHT_RATIO), "telegraph": ("boss15_telegraph.png", BOSS15_FRAME_COUNTS["telegraph"], 118), }
    frames = {}
    for key, (filename, frame_count, target_height) in resource_defs.items():
        path = find_asset_path(*boss15_asset_candidates(filename))
        if not path:
            if key != "skill2":
                print(f"{filename} 없음: 15층 보스 fallback 사용")
            frames[key] = []
            continue
        try:
            sheet = pygame.image.load(path)
            sheet = sheet.convert_alpha() if pygame.display.get_surface() else sheet.copy()
            frames[key] = slice_boss15_sheet(sheet, frame_count, target_height, key)
            if frames[key]:
                print("15층 보스 리소스 로드 성공:", os.path.basename(path))
            if not frames[key]:
                print(f"{filename} 프레임 추출 실패: 15층 보스 fallback 사용")
        except (pygame.error, OSError, FileNotFoundError, ValueError) as exc:
            print(f"{filename} 로드 실패: 15층 보스 fallback 사용", exc)
            frames[key] = []

    fallback = frames.get("idle")
    if not fallback:
        print("boss15_idle 이미지 없음: 도형 fallback 보스를 사용합니다.")
    if fallback:
        frames["idle"] = frames.get("idle") or fallback
        frames["skill1"] = frames.get("skill1") or frames["idle"]
        frames["skill2"] = frames.get("skill2") or frames.get("skill1") or frames["idle"]
        frames["groggy"] = frames.get("groggy") or frames["idle"]
        frames["defeat"] = frames.get("defeat") or frames["groggy"]
    else:
        frames["idle"] = []
        frames["skill1"] = []
        frames["skill2"] = []
        frames["groggy"] = []
        frames["defeat"] = []
    frames["telegraph"] = frames.get("telegraph") or []
    BOSS15_ASSET_CACHE["frames"] = {key: list(value) for key, value in frames.items()}
    return frames

def preload_boss15_assets():
    frames = load_boss15_motion_resources(None)
    BOSS15_ASSET_CACHE["frames"] = {key: list(value) for key, value in frames.items()}
    BOSS15_ASSET_CACHE["loaded"] = {key: bool(value) for key, value in frames.items()}
    print("15층 보스 모션 캐싱 완료:", BOSS15_ASSET_CACHE["loaded"])
    return BOSS15_ASSET_CACHE

def ensure_boss15_anim_attrs(self):
    if not hasattr(self, "floor15_anim_state"):
        self.floor15_anim_state = "idle"
        self.floor15_anim_timer = 0.0
        self.floor15_defeat_timer = 0.0
        self.floor15_groggy_flags = set()
        self.floor15_last_pattern = None
        self.floor15_state_locked = False
        self.floor15_ai_state = "idle"
        self.floor15_state_timer = 0.0
        self.floor15_attack_cooldown = BOSS15_ATTACK_INTERVAL
        self.floor15_current_pattern = None
        self.floor15_telegraph_spawned = False

def set_boss15_anim_state(self, state, restart=False):
    ensure_boss15_anim_attrs(self)
    if restart or self.floor15_anim_state != state:
        self.floor15_anim_state = state
        self.floor15_anim_timer = 0.0

def get_floor15_frame_from_state(self):
    ensure_boss15_anim_attrs(self)
    if not self.floor15_frames:
        return None
    if self.dead:
        state_key = "defeat"
    elif self.hp <= 0 or self.floor15_anim_state == "defeat":
        state_key = "defeat"
    elif self.vulnerable_timer > 0 or self.floor15_anim_state == "groggy":
        state_key = "groggy"
    elif self.floor15_anim_state in ("skill1_windup", "skill1_attack"):
        state_key = "skill1"
    elif self.floor15_anim_state in ("skill2_windup", "skill2_attack"):
        state_key = "skill2"
    else:
        state_key = "idle"

    frames = self.floor15_frames.get(state_key) or self.floor15_frames.get("idle")
    if not frames:
        return None
    fps = BOSS15_ANIM_FPS.get(state_key, 8)
    index = int(self.floor15_anim_timer * fps)
    if state_key in ("skill1", "skill2", "defeat"):
        index = min(index, len(frames) - 1)
    else:
        index %= len(frames)
    return frames[index]

def take_damage_boss15_stateful(self, amount):
    if self.floor != ICE_DRAGON_FLOOR:
        if self.floor == ICE_DRAGON_FLOOR and self.vulnerable_timer > 0:
            amount *= 1.35
        self.hp -= amount
        if self.hp <= self.max_hp * 0.5 and self.floor in (1, ICE_DRAGON_FLOOR):
            if self.floor == ICE_DRAGON_FLOOR and not self.phase2:
                self.floor15_phase_text = True
            self.phase2 = True
        if self.hp <= 0:
            self.dead = True
        return

    ensure_boss15_anim_attrs(self)
    if self.floor15_anim_state == "defeat" or self.dead:
        return
    if self.vulnerable_timer > 0:
        amount *= 1.35
    old_hp = self.hp
    self.hp = max(0, self.hp - amount)
    if self.hp <= self.max_hp * 0.5 and not self.phase2:
        self.phase2 = True
        self.floor15_phase_text = True
    for threshold in (0.70, 0.40):
        if old_hp > self.max_hp * threshold >= self.hp and threshold not in self.floor15_groggy_flags and self.hp > 0:
            self.floor15_groggy_flags.add(threshold)
            self.warning_attacks.clear()
            self.floor15_ai_state = "groggy"
            self.floor15_state_timer = 3.0
            self.floor15_current_pattern = None
            self.floor15_telegraph_spawned = False
            self.vulnerable_timer = 3.0
            self.pattern_cd = 3.1
            set_boss15_anim_state(self, "groggy", restart=True)
            break
    if self.hp <= 0:
        self.hp = 0
        self.warning_attacks.clear()
        self.floor15_summon_queue.clear()
        self.vulnerable_timer = 0
        self.pattern_cd = 999
        self.floor15_ai_state = "defeat"
        self.floor15_defeat_timer = 0.0
        set_boss15_anim_state(self, "defeat", restart=True)

def choose_boss15_pattern(self, player):
    melee_zone = self.get_floor15_melee_zone()
    near = melee_zone.collidepoint(player.pos.x, player.pos.y)
    patterns = ["sweep", "capsule_drop", "laser"]
    weights = [0.62, 0.28, 0.10] if near else [0.25, 0.58, 0.17]
    return random.choices(patterns, weights=weights, k=1)[0]

def spawn_boss15_telegraph(self, player):
    self.warning_attacks.clear()
    pattern = self.floor15_current_pattern
    if pattern == "sweep":
        y = clamp(player.pos.y, self.floor_top_y + 38, self.floor_bottom_y - 70)
        left, right = polygon_x_bounds(y, self.walkable_polygon)
        pos = ((left + right) * 0.5, y)
        self.warning_attacks.append( BossWarning( "ellipse", pos, (max(150, (right - left) * 0.42), 46), BOSS15_TELEGRAPH_TIME, BOSS15_ATTACK_ACTIVE_TIME, 24 if self.phase2 else 20, (205, 80, 255), "sweep", ) )
    elif pattern == "laser":
        y = clamp(player.pos.y, self.floor_top_y + 55, self.floor_bottom_y - 80)
        left, right = polygon_x_bounds(y, self.walkable_polygon)
        origin = pygame.Vector2(left + 28, y)
        self.warning_attacks.append( BossWarning( "laser", origin, (max(220, right - left - 56), 10), BOSS15_TELEGRAPH_TIME, BOSS15_ATTACK_ACTIVE_TIME, 21 if self.phase2 else 17, (180, 80, 255), "laser", 0, ) )
    else:
        count = 6 if self.phase2 else 4
        for index in range(count):
            if index == 0:
                point = self.clamp_to_walkable(player.pos, 58)
                pos = (point.x, point.y)
            else:
                pos = self.random_walkable_point(68)
            self.warning_attacks.append( BossWarning( "circle", pos, 48 if self.phase2 else 42, BOSS15_TELEGRAPH_TIME, BOSS15_ATTACK_ACTIVE_TIME, 20 if self.phase2 else 16, (220, 80, 235), "capsule_drop", ) )

def update_floor15_stateful(self, dt, player, projectiles, traps, effects, spawn_enemy):
    ensure_boss15_anim_attrs(self)
    self.floor15_anim_timer += dt
    self.pos = self.clamp_to_walkable( pygame.Vector2(BOSS15_WORLD_WIDTH * BOSS15_CORE_POS_RATIO[0], BOSS15_WORLD_HEIGHT * BOSS15_CORE_POS_RATIO[1]), self.radius, )
    self.visual_pos = pygame.Vector2(BOSS15_WORLD_WIDTH * BOSS15_ANCHOR_POS_RATIO[0], BOSS15_WORLD_HEIGHT * BOSS15_ANCHOR_POS_RATIO[1])
    self.warning_lines = []

    if self.floor15_anim_state == "defeat" or self.hp <= 0:
        set_boss15_anim_state(self, "defeat")
        self.warning_attacks.clear()
        self.floor15_summon_queue.clear()
        self.floor15_defeat_timer += dt
        defeat_frames = self.floor15_frames.get("defeat") or self.floor15_frames.get("idle") or []
        defeat_duration = max(0.9, len(defeat_frames) / max(1, BOSS15_ANIM_FPS["defeat"]))
        if self.floor15_defeat_timer >= defeat_duration:
            self.dead = True
        return

    for warning in self.warning_attacks:
        was_triggered = warning.triggered
        result = warning.update(dt, player)
        if warning.triggered and not was_triggered:
            effects.append(Effect(warning.pos.x, warning.pos.y, 70, warning.color[:3], 0.26))
            if self.floor15_anim_state.endswith("windup"):
                next_state = "skill1_attack" if self.floor15_anim_state.startswith("skill1") else "skill2_attack"
                set_boss15_anim_state(self, next_state, restart=True)
        if result == "dodged":
            effects.append(Effect(player.pos.x, player.pos.y, 64, YELLOW, 0.26))
        elif result == "shield":
            effects.append(Effect(player.pos.x, player.pos.y, 58, CYAN, 0.24))
        elif result == "hit":
            effects.append(Effect(player.pos.x, player.pos.y, 42, RED, 0.18))
    self.warning_attacks = [warning for warning in self.warning_attacks if not warning.done]

    ready_summons = []
    for summon in self.floor15_summon_queue:
        summon["timer"] -= dt
        if summon["timer"] <= 0:
            ready_summons.append(summon)
    self.floor15_summon_queue = [summon for summon in self.floor15_summon_queue if summon not in ready_summons]
    for summon in ready_summons:
        for _ in range(summon["count"]):
            spawn_enemy(random.choice(["媛먯뿼泥?", "媛먯뿼泥?", "?뚯쭊 ?ㅽ뿕泥?"]))
        effects.append(Effect(summon["pos"][0], summon["pos"][1], 88, PURPLE, 0.38))

    if self.vulnerable_timer > 0:
        set_boss15_anim_state(self, "groggy")
        if self.vulnerable_timer <= 0:
            set_boss15_anim_state(self, "idle", restart=True)
        return

    if self.pattern_cd > 0 or self.warning_attacks:
        if not self.warning_attacks and self.pattern_cd <= 0.12 and "attack" in self.floor15_anim_state:
            set_boss15_anim_state(self, "idle")
        return

    if self.floor15_phase_text:
        effects.append(Effect(self.arena_rect.centerx, self.arena_rect.top + 70, 180, (230, 95, 255), 0.6))
        self.floor15_phase_text = False

    self.pattern_count += 1
    pattern = random.choices( ["stomp", "fall", "laser", "rune", "summon"], weights=[4, 4, 3, 3 if self.phase2 else 2, 2], k=1, )[0]
    self.floor15_last_pattern = pattern
    if pattern in ("stomp", "laser"):
        set_boss15_anim_state(self, "skill1_windup", restart=True)
    else:
        set_boss15_anim_state(self, "skill2_windup", restart=True)

    if pattern == "stomp":
        self.floor15_stomp(player)
        self.pattern_cd = 1.35 if not self.phase2 else 1.05
    elif pattern == "fall":
        self.floor15_fall(player)
        self.pattern_cd = 1.6 if not self.phase2 else 1.2
    elif pattern == "laser":
        self.floor15_laser()
        self.pattern_cd = 1.55 if not self.phase2 else 1.15
    elif pattern == "rune":
        self.floor15_runes(player)
        self.pattern_cd = 1.5 if not self.phase2 else 1.12
    else:
        self.floor15_summon(player)
        self.pattern_cd = 1.9 if not self.phase2 else 1.45

def update_floor15_state_machine(self, dt, player, projectiles, traps, effects, spawn_enemy):
    ensure_boss15_anim_attrs(self)
    self.floor15_anim_timer += dt
    self.pos = self.clamp_to_walkable( pygame.Vector2(BOSS15_WORLD_WIDTH * BOSS15_CORE_POS_RATIO[0], BOSS15_WORLD_HEIGHT * BOSS15_CORE_POS_RATIO[1]), self.radius, )
    self.visual_pos = pygame.Vector2(BOSS15_WORLD_WIDTH * BOSS15_ANCHOR_POS_RATIO[0], BOSS15_WORLD_HEIGHT * BOSS15_ANCHOR_POS_RATIO[1])
    self.warning_lines = []

    if self.floor15_ai_state == "defeat" or self.floor15_anim_state == "defeat" or self.hp <= 0:
        self.floor15_ai_state = "defeat"
        set_boss15_anim_state(self, "defeat")
        self.warning_attacks.clear()
        self.floor15_summon_queue.clear()
        self.floor15_defeat_timer += dt
        defeat_frames = self.floor15_frames.get("defeat") or self.floor15_frames.get("idle") or []
        defeat_duration = max(0.9, len(defeat_frames) / max(1, BOSS15_ANIM_FPS["defeat"]))
        if self.floor15_defeat_timer >= defeat_duration:
            self.dead = True
        return

    if self.vulnerable_timer > 0 or self.floor15_ai_state == "groggy":
        self.floor15_ai_state = "groggy"
        self.floor15_state_timer = max(0, self.floor15_state_timer - dt)
        set_boss15_anim_state(self, "groggy")
        self.warning_attacks.clear()
        if self.vulnerable_timer <= 0 and self.floor15_state_timer <= 0:
            self.floor15_ai_state = "idle"
            self.floor15_attack_cooldown = BOSS15_ATTACK_INTERVAL
            set_boss15_anim_state(self, "idle", restart=True)
        return

    for warning in self.warning_attacks:
        was_triggered = warning.triggered
        result = warning.update(dt, player)
        if warning.triggered and not was_triggered:
            effects.append(Effect(warning.pos.x, warning.pos.y, 70, warning.color[:3], 0.26))
            if self.floor15_ai_state == "telegraph":
                self.floor15_ai_state = "attack"
                self.floor15_state_timer = BOSS15_ATTACK_ACTIVE_TIME
                next_state = "skill1_attack" if self.floor15_current_pattern == "sweep" else "skill2_attack"
                set_boss15_anim_state(self, next_state, restart=True)
        if result == "dodged":
            effects.append(Effect(player.pos.x, player.pos.y, 64, YELLOW, 0.26))
        elif result == "shield":
            effects.append(Effect(player.pos.x, player.pos.y, 58, CYAN, 0.24))
        elif result == "hit":
            effects.append(Effect(player.pos.x, player.pos.y, 42, RED, 0.18))
    self.warning_attacks = [warning for warning in self.warning_attacks if not warning.done]

    if self.floor15_ai_state == "idle":
        set_boss15_anim_state(self, "idle")
        self.floor15_attack_cooldown = max(0, self.floor15_attack_cooldown - dt)
        if self.floor15_phase_text:
            effects.append(Effect(self.arena_rect.centerx, self.arena_rect.top + 70, 180, (230, 95, 255), 0.6))
            self.floor15_phase_text = False
        if self.floor15_attack_cooldown <= 0:
            self.floor15_ai_state = "choose_attack"
        return

    if self.floor15_ai_state == "choose_attack":
        self.pattern_count += 1
        if self.pattern_count % 5 == 0:
            self.floor15_ai_state = "groggy"
            self.floor15_state_timer = 3.0
            self.vulnerable_timer = max(self.vulnerable_timer, 3.0)
            self.floor15_current_pattern = None
            set_boss15_anim_state(self, "groggy", restart=True)
            return
        self.floor15_current_pattern = choose_boss15_pattern(self, player)
        self.floor15_last_pattern = self.floor15_current_pattern
        self.floor15_state_timer = BOSS15_WINDUP_TIME
        self.floor15_telegraph_spawned = False
        self.floor15_ai_state = "windup"
        set_boss15_anim_state(self, "skill1_windup" if self.floor15_current_pattern == "sweep" else "skill2_windup", restart=True)
        return

    if self.floor15_ai_state == "windup":
        self.floor15_state_timer = max(0, self.floor15_state_timer - dt)
        if self.floor15_state_timer <= 0:
            spawn_boss15_telegraph(self, player)
            self.floor15_telegraph_spawned = True
            self.floor15_ai_state = "telegraph"
            self.floor15_state_timer = BOSS15_TELEGRAPH_TIME
        return

    if self.floor15_ai_state == "telegraph":
        if not self.warning_attacks:
            self.floor15_ai_state = "recover"
            self.floor15_state_timer = BOSS15_RECOVER_TIME
        return

    if self.floor15_ai_state == "attack":
        self.floor15_state_timer = max(0, self.floor15_state_timer - dt)
        if self.floor15_state_timer <= 0 and not self.warning_attacks:
            self.floor15_ai_state = "recover"
            self.floor15_state_timer = BOSS15_RECOVER_TIME
        return

    if self.floor15_ai_state == "recover":
        self.floor15_state_timer = max(0, self.floor15_state_timer - dt)
        if self.floor15_state_timer <= 0:
            self.floor15_ai_state = "idle"
            self.floor15_current_pattern = None
            self.floor15_attack_cooldown = max(1.6, BOSS15_ATTACK_INTERVAL - (0.35 if self.phase2 else 0))
            set_boss15_anim_state(self, "idle", restart=True)

def draw_boss15_telegraph_sprite(self, surface, warning):
    frames = self.floor15_frames.get("telegraph") if self.floor15_frames else None
    if not frames:
        return
    frame = frames[int(self.floor15_anim_timer * BOSS15_ANIM_FPS["telegraph"]) % len(frames)]
    if warning.shape == "circle":
        target_w = target_h = max(34, int(warning.size * 2.1))
        angle = 0
    elif warning.shape == "ellipse":
        rx, ry = warning.size
        target_w = max(34, int(rx * 2.2))
        target_h = max(24, int(ry * 2.8))
        angle = 0
    elif warning.shape == "laser":
        length, laser_w = warning.size
        target_w = max(80, int(length))
        target_h = max(24, int(laser_w * 6))
        angle = -warning.angle
    else:
        return
    cache = getattr(self, "floor15_scaled_cache", {})
    cache_key = ("telegraph", id(frame), target_w, target_h, round(angle, 1))
    telegraph = cache.get(cache_key)
    if telegraph is None:
        telegraph = pygame.transform.smoothscale(frame, (target_w, target_h))
        if angle:
            telegraph = pygame.transform.rotate(telegraph, angle)
        if len(cache) > 24:
            cache.clear()
        cache[cache_key] = telegraph
        self.floor15_scaled_cache = cache
    rect = telegraph.get_rect(center=(int(warning.pos.x), int(warning.pos.y)))
    surface.blit(telegraph, rect)

def draw_floor15_warnings_with_telegraph(self, surface):
    for warning in self.warning_attacks:
        warning.draw(surface)
        if warning.warning_time > 0:
            draw_boss15_telegraph_sprite(self, surface, warning)

def draw_boss15_foreground_mask(surface, room):
    polygon = room.walkable_polygon
    background = getattr(room, "background_surface", None)
    if background:
        cached = getattr(room, "boss15_foreground_cache", None)
        if cached is None:
            cached = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            cached.blit(background, (0, 0))
            alpha = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            alpha.fill((255, 255, 255, 0))
            pygame.draw.polygon(alpha, (255, 255, 255, 255), polygon)
            cached.blit(alpha, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            room.boss15_foreground_cache = cached
        surface.blit(cached, (0, 0))
    else:
        mask = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        pygame.draw.polygon(mask, (10, 24, 31, 84), polygon)
        surface.blit(mask, (0, 0))

    lip = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    top_y = int(room.floor_top_y)
    left, right = polygon_x_bounds(top_y + 4, polygon)
    pygame.draw.line(lip, (90, 230, 230, 70), (int(left), top_y + 4), (int(right), top_y + 4), 2)
    surface.blit(lip, (0, 0))

def get_floor15_core_hitbox(self):
    x, y, w, h = BOSS15_CORE_HITBOX_RATIO
    return pygame.Rect( int(BOSS15_WORLD_WIDTH * x), int(BOSS15_WORLD_HEIGHT * y), int(BOSS15_WORLD_WIDTH * w), int(BOSS15_WORLD_HEIGHT * h), )

def get_floor15_melee_zone(self):
    x, y, w, h = BOSS15_MELEE_ZONE_RATIO
    return pygame.Rect( int(BOSS15_WORLD_WIDTH * x), int(BOSS15_WORLD_HEIGHT * y), int(BOSS15_WORLD_WIDTH * w), int(BOSS15_WORLD_HEIGHT * h), )

def get_floor15_head_focus_pos(self):
    return pygame.Vector2( BOSS15_WORLD_WIDTH * BOSS15_HEAD_FOCUS_RATIO[0], BOSS15_WORLD_HEIGHT * BOSS15_HEAD_FOCUS_RATIO[1], )

def draw_boss15_shape_fallback(self, surface):
    ensure_boss15_anim_attrs(self)
    x, y = self.visual_pos.x, self.visual_pos.y
    scale = max(0.85, (self.visual_height or HEIGHT * BOSS15_VISUAL_HEIGHT_RATIO) / 828)
    pulse = 0.5 + 0.5 * math.sin(self.timer * 4.2)
    state = self.floor15_anim_state
    is_skill1 = state in ("skill1_windup", "skill1_attack")
    is_skill2 = state in ("skill2_windup", "skill2_attack")
    is_groggy = state == "groggy" or self.vulnerable_timer > 0
    is_defeat = state == "defeat" or self.dead or self.hp <= 0

    gold = (210, 156, 45) if not is_defeat else (92, 78, 64)
    dark_gold = (112, 78, 34) if not is_defeat else (48, 44, 48)
    bone = (232, 206, 132) if not is_defeat else (105, 100, 96)
    purple = (205, 80, 255) if not is_groggy else (135, 100, 180)
    cyan = (90, 230, 230)
    bob = 0 if is_defeat else math.sin(self.timer * 2.8) * 5

    torso_y = y - 285 * scale + bob
    head_y = y - 470 * scale + bob
    core_pos = pygame.Vector2(x, torso_y + 54 * scale)
    arm_lift = 72 * scale if is_skill1 else 20 * scale
    hand_spread = 250 * scale

    aura = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    pygame.draw.ellipse(aura, (10, 6, 20, 120), (int(x - 410 * scale), int(y - 150 * scale), int(820 * scale), int(210 * scale)))
    pygame.draw.circle(aura, (*purple, 34), (int(core_pos.x), int(core_pos.y)), int((115 + pulse * 34) * scale))
    surface.blit(aura, (0, 0))

    spine_top = pygame.Vector2(x, head_y + 95 * scale)
    spine_bottom = pygame.Vector2(x, y - 92 * scale)
    pygame.draw.line(surface, dark_gold, spine_top, spine_bottom, max(8, int(15 * scale)))
    for i in range(7):
        rib_y = torso_y - 34 * scale + i * 34 * scale
        rib_w = (165 - i * 10) * scale
        pygame.draw.arc(surface, bone, (x - rib_w, rib_y - 18 * scale, rib_w, 44 * scale), math.pi * 0.98, math.pi * 1.92, max(4, int(7 * scale)))
        pygame.draw.arc(surface, bone, (x, rib_y - 18 * scale, rib_w, 44 * scale), math.pi * 1.08, math.pi * 2.02, max(4, int(7 * scale)))

    left_shoulder = pygame.Vector2(x - 145 * scale, torso_y - 56 * scale)
    right_shoulder = pygame.Vector2(x + 145 * scale, torso_y - 56 * scale)
    left_hand = pygame.Vector2(x - hand_spread, torso_y + 130 * scale - arm_lift)
    right_hand = pygame.Vector2(x + hand_spread, torso_y + 120 * scale - (arm_lift if is_skill1 else 0))
    for shoulder, hand, side in ((left_shoulder, left_hand, -1), (right_shoulder, right_hand, 1)):
        elbow = pygame.Vector2((shoulder.x + hand.x) * 0.5, shoulder.y + 66 * scale - arm_lift * 0.35)
        pygame.draw.line(surface, dark_gold, shoulder, elbow, max(10, int(18 * scale)))
        pygame.draw.line(surface, gold, elbow, hand, max(10, int(18 * scale)))
        pygame.draw.circle(surface, gold, shoulder, int(25 * scale))
        pygame.draw.circle(surface, dark_gold, elbow, int(20 * scale))
        pygame.draw.circle(surface, gold, hand, int(30 * scale))
        for claw in range(4):
            angle = (-55 + claw * 28) * side
            tip = hand + pygame.Vector2(side * 42 * scale, 0).rotate(angle)
            pygame.draw.line(surface, bone, hand, tip, max(3, int(5 * scale)))

    skull_rect = pygame.Rect(0, 0, int(230 * scale), int(180 * scale))
    skull_rect.center = (int(x), int(head_y))
    pygame.draw.ellipse(surface, gold, skull_rect)
    pygame.draw.ellipse(surface, dark_gold, skull_rect, max(5, int(8 * scale)))
    pygame.draw.polygon(surface, bone, [ (x - 72 * scale, head_y + 66 * scale), (x + 72 * scale, head_y + 66 * scale), (x + 38 * scale, head_y + 122 * scale), (x - 38 * scale, head_y + 122 * scale), ])
    pygame.draw.circle(surface, purple, (int(x - 48 * scale), int(head_y - 8 * scale)), int(22 * scale))
    pygame.draw.circle(surface, purple, (int(x + 48 * scale), int(head_y - 8 * scale)), int(22 * scale))
    pygame.draw.circle(surface, (40, 5, 65), (int(x - 48 * scale), int(head_y - 8 * scale)), int(12 * scale))
    pygame.draw.circle(surface, (40, 5, 65), (int(x + 48 * scale), int(head_y - 8 * scale)), int(12 * scale))
    for tooth in range(6):
        tx = x - 42 * scale + tooth * 17 * scale
        pygame.draw.line(surface, dark_gold, (tx, head_y + 70 * scale), (tx, head_y + 104 * scale), max(2, int(3 * scale)))

    core_radius = int((46 + pulse * 11) * scale)
    if is_groggy:
        core_radius = int(34 * scale)
    pygame.draw.circle(surface, purple, core_pos, core_radius)
    pygame.draw.circle(surface, (255, 225, 255), core_pos, max(5, int(core_radius * 0.28)))
    pygame.draw.circle(surface, cyan if is_skill2 else purple, core_pos, int(core_radius * 1.55), max(3, int(5 * scale)))

    if is_skill2:
        for i in range(8):
            angle = self.timer * 2.2 + i * math.tau / 8
            orb = core_pos + pygame.Vector2(math.cos(angle), math.sin(angle)) * (118 * scale)
            pygame.draw.circle(surface, (245, 210, 90), orb, int(15 * scale))
            pygame.draw.circle(surface, purple, orb, int(22 * scale), 3)
    if is_defeat:
        random.seed(15)
        for i in range(22):
            px = x + random.uniform(-260, 260) * scale
            py = torso_y + random.uniform(-210, 160) * scale
            pygame.draw.polygon(surface, (105, 85, 60), [ (px, py), (px + random.uniform(6, 18) * scale, py + random.uniform(-5, 9) * scale), (px + random.uniform(-8, 8) * scale, py + random.uniform(7, 20) * scale), ])

    self.visual_rect = pygame.Rect(int(x - 330 * scale), int(head_y - 115 * scale), int(660 * scale), int(y - head_y + 130 * scale))

def draw_floor15_background_boss(self, surface, font):
    x, y = self.visual_pos.x, self.visual_pos.y
    pulse = 0.5 + 0.5 * math.sin(self.timer * 5.0)
    aura_radius = int(96 + pulse * 18 + (24 if self.phase2 else 0))
    aura_center_y = y - max(180, int((self.visual_height or HEIGHT * BOSS15_VISUAL_HEIGHT_RATIO) * 0.48))

    ambient = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    pygame.draw.ellipse( ambient, (4, 10, 18, 104), ( int(x - 360), int(self.floor_top_y - 54), 720, 150, ), )
    pygame.draw.ellipse( ambient, (125, 55, 210, 34), ( int(x - 220), int(self.floor_top_y - 92), 440, 132, ), )
    surface.blit(ambient, (0, 0))

    aura = pygame.Surface((aura_radius * 2 + 8, aura_radius * 2 + 8), pygame.SRCALPHA)
    pygame.draw.circle(aura, (160, 60, 235, 48), (aura_radius + 4, aura_radius + 4), aura_radius, 5)
    pygame.draw.circle(aura, (120, 230, 80, 28), (aura_radius + 4, aura_radius + 4), max(8, aura_radius - 18), 2)
    surface.blit(aura, (x - aura_radius - 4, aura_center_y - aura_radius - 4))

    sprite = self.get_floor15_frame()
    if sprite:
        draw_sprite = sprite
        rect = draw_sprite.get_rect(midbottom=(x, y))
        self.visual_rect = rect
        surface.blit(draw_sprite, rect)
    else:
        draw_boss15_shape_fallback(self, surface)

    core_glow = pygame.Surface((220, 220), pygame.SRCALPHA)
    core_y = int(y - max(210, (self.visual_height or HEIGHT * BOSS15_VISUAL_HEIGHT_RATIO) * 0.42))
    pygame.draw.circle(core_glow, (200, 80, 255, 54), (110, 110), int(72 + pulse * 18))
    pygame.draw.circle(core_glow, (110, 230, 220, 24), (110, 110), int(96 + pulse * 12), 2)
    surface.blit(core_glow, (int(x - 110), core_y - 110), special_flags=pygame.BLEND_RGBA_ADD)

    for i in range(6 if self.phase2 else 4):
        angle = self.timer * (1.6 + i * 0.12) + i * math.tau / 6
        orb_pos = pygame.Vector2(x + math.cos(angle) * (100 + i * 5), aura_center_y + math.sin(angle * 1.4) * 28)
        pygame.draw.circle(surface, (120, 230, 80), orb_pos, 5)
        pygame.draw.circle(surface, (190, 85, 255), orb_pos, 9, 1)

    draw_bar(surface, WIDTH // 2 - 260, 82, 520, 16, self.hp, self.max_hp, self.color)
    draw_text(surface, font, f"15층 보스 - {self.name}", WIDTH // 2, 54, WHITE, center=True)
    if self.phase2:
        draw_text(surface, font, "격리 관리자 G가 폭주합니다!", WIDTH // 2, 106, (230, 95, 255), center=True)

    if DEBUG_BOSS15 or DEBUG_BOSS15_AREA or DEBUG_BOSS15_FLOOR:
        pygame.draw.rect(surface, (255, 220, 80), self.visual_rect, 2)
        pygame.draw.circle(surface, (255, 80, 80), (int(self.pos.x), int(self.pos.y)), int(self.radius), 2)
        pygame.draw.polygon(surface, (80, 255, 120), self.walkable_polygon, 2)
        pygame.draw.rect(surface, (255, 80, 120), self.get_floor15_core_hitbox(), 2)
        pygame.draw.rect(surface, (80, 220, 255), self.get_floor15_melee_zone(), 2)
        pygame.draw.circle(surface, (255, 240, 80), (int(self.visual_pos.x), int(self.visual_pos.y)), 7)
        head_focus = self.get_floor15_head_focus_pos()
        pygame.draw.circle(surface, (255, 160, 60), (int(head_focus.x), int(head_focus.y)), 7)
        draw_text(surface, font, self.floor15_anim_state, int(self.visual_pos.x), int(self.visual_pos.y) + 24, YELLOW, center=True)
        for warning in self.warning_attacks:
            if hasattr(warning, "rect"):
                pygame.draw.rect(surface, (255, 90, 90), warning.rect, 1)

def draw_entities_with_boss15_order(self, surface, font, player=None):
    boss15 = self.boss and self.boss.floor == ICE_DRAGON_FLOOR
    if boss15:
        self.boss.draw(surface, font)
        draw_boss15_foreground_mask(surface, self)
        self.boss.draw_warnings(surface)
        if DEBUG_BOSS15_FLOOR and player:
            diagonal = player.radius * 0.7
            points = [ player.pos, player.pos + pygame.Vector2(player.radius, 0), player.pos + pygame.Vector2(-player.radius, 0), player.pos + pygame.Vector2(0, player.radius), player.pos + pygame.Vector2(0, -player.radius), player.pos + pygame.Vector2(diagonal, diagonal), player.pos + pygame.Vector2(-diagonal, diagonal), player.pos + pygame.Vector2(diagonal, -diagonal), player.pos + pygame.Vector2(-diagonal, -diagonal), ]
            for point in points:
                pygame.draw.circle(surface, (255, 240, 80), (int(point.x), int(point.y)), 4)
    elif self.boss and hasattr(self.boss, "draw_warnings"):
        self.boss.draw_warnings(surface)

    for trap in self.traps:
        trap.draw(surface)
    for projectile in self.projectiles:
        projectile.draw(surface)

    actors = []
    for enemy in self.enemies:
        actors.append((enemy.pos.y, enemy.draw))
    if self.boss and not boss15:
        actors.append((self.boss.pos.y, lambda target_surface, boss=self.boss: boss.draw(target_surface, font)))
    if player:
        for pet in player.pets:
            actors.append((pet.pos.y, pet.draw))
        actors.append((player.pos.y, player.draw))
    for _, draw_actor in sorted(actors, key=lambda item: item[0]):
        draw_actor(surface)

    for effect in self.effects:
        effect.draw(surface)

class IceDragonHazard:
    def __init__(self, kind, arena_center, arena_radius, warning_time, active_time, damage, sector_index=None, pos=None, velocity=None, radius=58):
        self.kind = kind
        self.arena_center = pygame.Vector2(arena_center)
        self.arena_radius = arena_radius
        if isinstance(arena_radius, (tuple, list, pygame.Vector2)):
            self.arena_rx = max(1, float(arena_radius[0]))
            self.arena_ry = max(1, float(arena_radius[1]))
        else:
            self.arena_rx = max(1, float(arena_radius))
            self.arena_ry = max(1, float(arena_radius))
        self.warning_time = warning_time
        self.active_time = active_time
        self.damage = damage
        self.sector_index = sector_index
        self.pos = pygame.Vector2(pos) if pos is not None else pygame.Vector2(arena_center)
        self.velocity = pygame.Vector2(velocity) if velocity is not None else pygame.Vector2(0, 0)
        self.radius = radius
        self.color = (105, 220, 255)
        self.kind_label = kind
        self.done = False
        self.triggered = False
        self.hit_cooldown = 0.0
        self.visual_rect = pygame.Rect(0, 0, 0, 0)
        self.footprint_rect = pygame.Rect(0, 0, 0, 0)

    @property
    def active(self):
        return self.warning_time <= 0 and self.active_time > 0

    def update(self, dt, player):
        if self.done:
            return None
        self.hit_cooldown = max(0, self.hit_cooldown - dt)
        if self.warning_time > 0:
            self.warning_time -= dt
            if self.warning_time <= 0:
                self.triggered = True
            return None

        self.active_time -= dt
        if self.kind == "blizzard":
            self.pos += self.velocity * dt
            rel = self.pos - self.arena_center
            if self.pos.y < self.arena_center.y + self.radius:
                self.pos.y = self.arena_center.y + self.radius
                self.velocity.y = abs(self.velocity.y)
            rx = max(1, self.arena_rx - self.radius)
            ry = max(1, self.arena_ry - self.radius)
            nx = rel.x / rx
            ny = rel.y / ry
            if nx * nx + ny * ny > 1.0:
                angle = math.atan2(ny, nx)
                self.pos = pygame.Vector2( self.arena_center.x + math.cos(angle) * rx, self.arena_center.y + math.sin(angle) * ry, )
                normal = pygame.Vector2(math.cos(angle) / rx, math.sin(angle) / ry)
                if normal.length_squared() > 0:
                    normal = normal.normalize()
                    self.velocity = self.velocity.reflect(normal)

        result = None
        if self.damage > 0 and self.hit_cooldown <= 0 and self.hits_player(player):
            if hasattr(player, "take_ice_hazard_damage"):
                result = player.take_ice_hazard_damage(self.damage, self.kind)
            else:
                result = player.take_damage(self.damage)
            if self.kind == "blizzard" and result in ("hit", "blocked", "shield"):
                player.frost_slow_timer = max(getattr(player, "frost_slow_timer", 0), 1.15)
            self.hit_cooldown = 0.45
        if self.active_time <= 0:
            self.done = True
        return result

    def sector_polygon(self):
        return ice_dragon_sector_polygon(self.arena_center, self.arena_rx, self.arena_ry, self.sector_index)

    def hits_player(self, player):
        if self.kind == "breath":
            sector = ice_dragon_sector_from_point(player.pos, self.arena_center, self.arena_rx, self.arena_ry, player.radius)
            return sector == self.sector_index
        if self.kind == "blizzard":
            return self.hits_blizzard_footprint(player)
        return False

    def blizzard_footprint_radii(self):
        return max(28, self.radius * 0.68), max(14, self.radius * 0.34)

    def hits_blizzard_footprint(self, player):
        rx, ry = self.blizzard_footprint_radii()
        self.footprint_rect = pygame.Rect( int(self.pos.x - rx), int(self.pos.y - ry), int(rx * 2), int(ry * 2), )
        foot = pygame.Vector2(player.pos.x, player.pos.y + player.radius * 0.65)
        dx = (foot.x - self.pos.x) / max(1, rx + player.radius * 0.35)
        dy = (foot.y - self.pos.y) / max(1, ry + player.radius * 0.20)
        return dx * dx + dy * dy <= 1.0

    def draw(self, surface):
        temp = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        pulse = 0.45 + 0.55 * abs(math.sin(pygame.time.get_ticks() * 0.012))
        effect_frames = load_ice_dragon_effect_resources()
        if self.kind == "breath":
            polygon = self.sector_polygon()
            if polygon:
                sprite = effect_frames.get("breath_warning" if self.warning_time > 0 else "breath_effect")
                if self.warning_time > 0:
                    if not draw_sprite_clipped_to_polygon(temp, sprite, polygon, int(100 + pulse * 70)):
                        color = (90, 225, 255, int(48 + pulse * 74))
                        pygame.draw.polygon(temp, color, polygon)
                    pygame.draw.polygon(temp, (210, 250, 255, 130), polygon, 2)
                else:
                    if not draw_sprite_clipped_to_polygon(temp, sprite, polygon, 205):
                        pygame.draw.polygon(temp, (120, 235, 255, 132), polygon)
                    pygame.draw.polygon(temp, (235, 255, 255, 150), polygon, 1)
        elif self.kind == "blizzard":
            if self.warning_time > 0:
                sprite = effect_frames.get("blizzard_warning")
                size = int(self.radius * 2.25)
                if sprite:
                    glyph = pygame.transform.smoothscale(sprite, (size, int(size * 0.66)))
                    glyph.set_alpha(int(90 + pulse * 95))
                    temp.blit(glyph, glyph.get_rect(center=(int(self.pos.x), int(self.pos.y))))
                else:
                    rx, ry = self.blizzard_footprint_radii()
                    pygame.draw.ellipse(temp, (115, 230, 255, int(55 + pulse * 80)), pygame.Rect(int(self.pos.x - rx), int(self.pos.y - ry), int(rx * 2), int(ry * 2)), 3)
            else:
                sprite = effect_frames.get("blizzard_tornado")
                if sprite:
                    height = int(self.radius * 3.9 * ICE_DRAGON_TORNADO_VISUAL_SCALE)
                    width = max(1, int(sprite.get_width() * height / max(1, sprite.get_height())))
                    tornado = pygame.transform.smoothscale(sprite, (width, height))
                    tornado.set_alpha(218)
                    self.visual_rect = tornado.get_rect(midbottom=(int(self.pos.x), int(self.pos.y + self.radius * 0.28)))
                    temp.blit(tornado, self.visual_rect)
                else:
                    rx, ry = self.blizzard_footprint_radii()
                    self.visual_rect = pygame.Rect( int(self.pos.x - rx * ICE_DRAGON_TORNADO_VISUAL_SCALE), int(self.pos.y - ry * 4.0 * ICE_DRAGON_TORNADO_VISUAL_SCALE), int(rx * 2 * ICE_DRAGON_TORNADO_VISUAL_SCALE), int(ry * 4.0 * ICE_DRAGON_TORNADO_VISUAL_SCALE), )
                    layers = 7
                    for index in range(layers):
                        t = index / max(1, layers - 1)
                        layer_y = self.pos.y - t * self.visual_rect.height * 0.72
                        layer_rx = rx * ICE_DRAGON_TORNADO_VISUAL_SCALE * (1.0 - t * 0.58)
                        layer_ry = max(7, ry * (0.86 - t * 0.38))
                        alpha = int(118 - t * 52)
                        layer_rect = pygame.Rect( int(self.pos.x - layer_rx), int(layer_y - layer_ry), int(layer_rx * 2), int(layer_ry * 2), )
                        pygame.draw.ellipse(temp, (115, 230, 255, alpha), layer_rect, 3)
                    pygame.draw.ellipse( temp, (205, 250, 255, 132), pygame.Rect(int(self.pos.x - rx), int(self.pos.y - ry), int(rx * 2), int(ry * 2)), 2, )
        surface.blit(temp, (0, 0))

def load_ice_dragon_motion_resources(self):
    cached = BOSS15_ASSET_CACHE.get("ice_dragon_frames")
    if cached is not None:
        return cached
    path = find_asset_path( os.path.join("assets", ICE_DRAGON_SHEET), os.path.join("assets", "ice_dragon_sheet.png.png"), ICE_DRAGON_SHEET, "ice_dragon_sheet.png.png", )
    frames = {}
    if path:
        try:
            sheet = pygame.image.load(path)
            sheet = sheet.convert_alpha() if pygame.display.get_surface() else sheet.copy()
            crop_defs = { "idle": (5, 10, 350, 325, 350), "breath_prepare": (1245, 380, 1445, 560, 300), "breath_cast": (350, 25, 610, 320, 350), "tornado_prepare": (5, 10, 350, 325, 350), "tornado_cast": (665, 15, 925, 325, 360), "damaged": (920, 35, 1150, 325, 300), "dead": (1140, 135, 1445, 325, 245), }
            body_frames = {}
            for name, (x1, y1, x2, y2, target_h) in crop_defs.items():
                rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1).clip(sheet.get_rect())
                frame = sheet.subsurface(rect).copy()
                frame = remove_ice_dragon_body_background(frame)
                if name == "dead":
                    frame = remove_ice_dragon_death_background(frame)
                if name == "breath_cast":
                    frame = remove_ice_dragon_body_effect_pixels(frame, "breath")
                frame = trim_transparent(frame, padding=8)
                frame = keep_largest_alpha_component(frame)
                body_frames[name] = prepare_ice_dragon_body_frame(frame, target_h)

            idle = body_frames["idle"]
            breath_prepare = body_frames["breath_prepare"]
            breath_right = body_frames["breath_cast"]
            breath_left = pygame.transform.flip(breath_right, True, False)
            tornado_prepare = body_frames["tornado_prepare"]
            tornado_cast = body_frames["tornado_cast"]
            frames = { "idle": [idle], "breath": [breath_prepare, breath_right], "breath_left": [breath_prepare, breath_left], "breath_left_diagonal": [breath_prepare, breath_left], "breath_center": [breath_prepare, breath_right], "breath_right_diagonal": [breath_prepare, breath_right], "breath_right": [breath_prepare, breath_right], "tornado": [tornado_prepare, tornado_cast], "damaged": [body_frames["damaged"]], "dead": [body_frames["dead"]], }
            print("ice_dragon_sheet 로드 성공:", path)
        except (pygame.error, OSError, ValueError) as exc:
            print("ice_dragon_sheet 로드 실패: fallback 사용", exc)
            frames = {}
    BOSS15_ASSET_CACHE["ice_dragon_frames"] = frames
    return frames

def remove_ice_dragon_body_background(frame):
    image = remove_white_background(frame)
    for y in range(image.get_height()):
        for x in range(image.get_width()):
            color = image.get_at((x, y))
            if color.a <= 0:
                continue
            saturation = max(color.r, color.g, color.b) - min(color.r, color.g, color.b)
            if min(color.r, color.g, color.b) > 244 or ( min(color.r, color.g, color.b) > 226 and saturation < 20 ):
                image.set_at((x, y), (color.r, color.g, color.b, 0))
    return image

def remove_ice_dragon_death_background(frame):
    image = frame.copy().convert_alpha()
    width, height = image.get_size()

    def is_death_background(color):
        if color.a <= 8:
            return True
        saturation = max(color.r, color.g, color.b) - min(color.r, color.g, color.b)
        return (
            min(color.r, color.g, color.b) > 238
            or (min(color.r, color.g, color.b) > 215 and saturation < 28)
        )

    stack = []
    visited = set()
    for x in range(width):
        stack.append((x, 0))
        stack.append((x, height - 1))
    for y in range(height):
        stack.append((0, y))
        stack.append((width - 1, y))

    while stack:
        x, y = stack.pop()
        if (x, y) in visited or x < 0 or y < 0 or x >= width or y >= height:
            continue
        visited.add((x, y))
        color = image.get_at((x, y))
        if not is_death_background(color):
            continue
        image.set_at((x, y), (color.r, color.g, color.b, 0))
        stack.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))

    # Remove the pale halo left by antialiasing at the former white edge.
    original = image.copy()
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            color = original.get_at((x, y))
            if color.a <= 0 or not is_death_background(color):
                continue
            if any(
                original.get_at((x + dx, y + dy)).a == 0
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
            ):
                image.set_at((x, y), (color.r, color.g, color.b, 0))
    return image

def sanitize_ice_dragon_transparency(frame):
    image = frame.copy()
    for y in range(image.get_height()):
        for x in range(image.get_width()):
            color = image.get_at((x, y))
            saturation = max(color.r, color.g, color.b) - min(color.r, color.g, color.b)
            if color.a <= 0:
                image.set_at((x, y), (0, 0, 0, 0))
            elif min(color.r, color.g, color.b) > 236 and saturation < 18:
                image.set_at((x, y), (color.r, color.g, color.b, 0))
    return image

def remove_ice_dragon_body_effect_pixels(frame, effect_kind):
    image = frame.copy()
    width, height = image.get_size()
    for y in range(height):
        for x in range(width):
            color = image.get_at((x, y))
            if color.a <= 0:
                continue
            icy_glow = color.b > 190 and color.g > 145 and color.r < 235
            if effect_kind == "breath" and x > width * 0.73 and y > height * 0.30 and icy_glow:
                image.set_at((x, y), (color.r, color.g, color.b, 0))
            elif effect_kind == "tornado":
                orb_region = x < width * 0.38 and y < height * 0.42
                floor_effect_region = y > height * 0.70
                if icy_glow and (orb_region or floor_effect_region):
                    image.set_at((x, y), (color.r, color.g, color.b, 0))
    return image

def keep_largest_alpha_component(frame):
    mask = pygame.mask.from_surface(frame, 10)
    components = mask.connected_components(24)
    if not components:
        return frame
    largest = max(components, key=lambda component: component.count())
    rects = largest.get_bounding_rects()
    if not rects:
        return frame
    rect = rects[0].inflate(12, 12).clip(frame.get_rect())
    return frame.subsurface(rect).copy()

def normalize_ice_dragon_frame(frame, target_w, target_h):
    canvas = pygame.Surface((target_w, target_h), pygame.SRCALPHA)
    rect = frame.get_rect(midbottom=(target_w // 2, target_h))
    canvas.blit(frame, rect)
    return canvas

def prepare_ice_dragon_body_frame(frame, target_h):
    target_w, canvas_h = ICE_DRAGON_BODY_FRAME_SIZE
    frame = sanitize_ice_dragon_transparency(frame)
    scale = min(target_w / max(1, frame.get_width()), target_h / max(1, frame.get_height()))
    width = max(1, int(frame.get_width() * scale))
    height = max(1, int(frame.get_height() * scale))
    scaled = pygame.transform.smoothscale(frame, (width, height))
    scaled = sanitize_ice_dragon_transparency(scaled)
    scaled = apply_edge_fade(scaled, 0.025)
    canvas = pygame.Surface(ICE_DRAGON_BODY_FRAME_SIZE, pygame.SRCALPHA)
    canvas.blit(scaled, scaled.get_rect(midbottom=(target_w // 2, canvas_h - 4)))
    return canvas

def normalize_ice_effect_frame(frame, target_w, target_h, anchor="center"):
    cleaned = trim_transparent(remove_white_background(frame), padding=8)
    if cleaned.get_width() <= 2 or cleaned.get_height() <= 2:
        return None
    scale = min(target_w / max(1, cleaned.get_width()), target_h / max(1, cleaned.get_height()))
    width = max(1, int(cleaned.get_width() * scale))
    height = max(1, int(cleaned.get_height() * scale))
    scaled = pygame.transform.smoothscale(cleaned, (width, height))
    canvas = pygame.Surface((target_w, target_h), pygame.SRCALPHA)
    if anchor == "midbottom":
        rect = scaled.get_rect(midbottom=(target_w // 2, target_h))
    else:
        rect = scaled.get_rect(center=(target_w // 2, target_h // 2))
    canvas.blit(scaled, rect)
    return apply_edge_fade(canvas, 0.025)

def load_ice_dragon_effect_resources():
    cached = BOSS15_ASSET_CACHE.get("ice_dragon_effects")
    if cached is not None:
        return cached
    path = find_asset_path( os.path.join("assets", ICE_DRAGON_SHEET), os.path.join("assets", "ice_dragon_sheet.png.png"), ICE_DRAGON_SHEET, "ice_dragon_sheet.png.png", )
    effects = {}
    if path:
        try:
            sheet = pygame.image.load(path)
            sheet = sheet.convert_alpha() if pygame.display.get_surface() else sheet.copy()
            crop_defs = { "breath_warning": (0.000, 0.805, 0.245, 0.995, 260, 170, "center"), "breath_effect": (0.000, 0.555, 0.260, 0.790, 340, 210, "center"), "blizzard_warning": (0.735, 0.795, 0.995, 0.995, 180, 118, "center"), "blizzard_tornado": (0.610, 0.545, 0.805, 0.805, 168, 230, "midbottom"), }
            for name, (x1, y1, x2, y2, target_w, target_h, anchor) in crop_defs.items():
                frame = crop_by_ratio(sheet, x1, y1, x2, y2)
                normalized = normalize_ice_effect_frame(frame, target_w, target_h, anchor)
                if normalized:
                    effects[name] = normalized
        except (pygame.error, OSError, ValueError) as exc:
            print("ice_dragon effect sheet 로드 실패: fallback 사용", exc)
            effects = {}
    BOSS15_ASSET_CACHE["ice_dragon_effects"] = effects
    return effects

def draw_sprite_clipped_to_polygon(surface, sprite, polygon, alpha=180):
    if not sprite or not polygon:
        return False
    min_x = int(max(0, min(point[0] for point in polygon)))
    min_y = int(max(0, min(point[1] for point in polygon)))
    max_x = int(min(surface.get_width(), max(point[0] for point in polygon)))
    max_y = int(min(surface.get_height(), max(point[1] for point in polygon)))
    width = max(1, max_x - min_x)
    height = max(1, max_y - min_y)
    scaled = pygame.transform.smoothscale(sprite, (width, height))
    temp = pygame.Surface((width, height), pygame.SRCALPHA)
    temp.blit(scaled, (0, 0))
    mask = pygame.Surface((width, height), pygame.SRCALPHA)
    local_polygon = [(point[0] - min_x, point[1] - min_y) for point in polygon]
    pygame.draw.polygon(mask, (255, 255, 255, alpha), local_polygon)
    temp.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    surface.blit(temp, (min_x, min_y))
    return True

def get_ice_dragon_breath_direction_from_sector(sector):
    if sector == 0:
        return "left"
    if sector == 1:
        return "left_diagonal"
    if sector == 2:
        return "center"
    if sector == 3:
        return "right_diagonal"
    if sector == 4:
        return "right"
    return "center"

def get_ice_dragon_representative_breath_direction(sectors):
    if not sectors:
        return "center"
    avg = sum(sectors) / len(sectors)
    if avg < 0.75:
        return "left"
    if avg < 1.75:
        return "left_diagonal"
    if avg < 2.75:
        return "center"
    if avg < 3.75:
        return "right_diagonal"
    return "right"

def set_ice_dragon_animation(self, animation, force=False, frame_index=None, locked=None):
    if getattr(self, "ice_dragon_animation_locked", False) and not force:
        return
    if getattr(self, "ice_dragon_animation", None) != animation:
        self.ice_dragon_animation = animation
        self.ice_dragon_anim_timer = 0.0
        self.ice_dragon_frame_index = 0
    if frame_index is not None:
        frames = self.floor15_frames.get(animation) or self.floor15_frames.get("idle") or []
        max_index = max(0, len(frames) - 1) if isinstance(frames, (list, tuple)) else 0
        self.ice_dragon_frame_index = int(clamp(frame_index, 0, max_index))
    if locked is not None:
        self.ice_dragon_animation_locked = bool(locked)

def update_ice_dragon_animation(self, dt):
    state = getattr(self, "ice_dragon_ai_state", "idle")
    if self.dead or state == "dead":
        animation = "dead"
        frame_index = 0
        locked = False
    elif state == "death":
        animation = "dead"
        frame_index = 0
        locked = True
    elif state == "damaged":
        animation = "damaged"
        frame_index = 0
        locked = False
    elif state == "telegraph_breath":
        animation = f"breath_{getattr(self, 'breath_direction', 'center')}"
        frame_index = 0
        locked = True
    elif state == "execute_breath":
        animation = f"breath_{getattr(self, 'breath_direction', 'center')}"
        frame_index = 1
        locked = True
    elif state == "telegraph_blizzard":
        animation = "tornado"
        frame_index = 0
        locked = True
    elif state == "execute_blizzard":
        animation = "tornado"
        frame_index = 1
        locked = True
    else:
        animation = "idle"
        frame_index = 0
        locked = False
    if animation not in self.floor15_frames:
        animation = "breath" if animation.startswith("breath_") else "idle"
    set_ice_dragon_animation(self, animation, force=True, frame_index=frame_index, locked=locked)
    self.ice_dragon_anim_timer += dt

def get_ice_dragon_frame(self):
    if not self.floor15_frames:
        return None
    animation = getattr(self, "ice_dragon_animation", "idle")
    frames = self.floor15_frames.get(animation)
    if not frames and animation.startswith("breath_"):
        frames = self.floor15_frames.get("breath")
    frames = frames or self.floor15_frames.get("idle") or []
    if not isinstance(frames, (list, tuple)):
        return frames
    if not frames:
        return None
    index = int(clamp(getattr(self, "ice_dragon_frame_index", 0), 0, len(frames) - 1))
    return frames[index]

def take_damage_ice_dragon(self, amount):
    if self.floor == INFERNO_LIGER_FLOOR and getattr(self, "liger_death_state", "") in ("dying", "dead"):
        return
    if self.floor == FOREST_GUARDIAN_FLOOR and getattr(self, "forest_death_state", "") in ("dying", "dead"):
        return
    if self.floor == FINAL_CORE_PATTERN_FLOOR and getattr(self, "final_core_death_state", "") in ("dying", "dead"):
        return
    if self.floor == ICE_DRAGON_FLOOR:
        if getattr(self, "is_dying", False) or getattr(self, "ready_to_clear", False):
            return
        if getattr(self, "ice_dragon_ai_state", "idle") == "damaged" or self.vulnerable_timer > 0:
            amount *= 1.25
        self.ice_dragon_hurt_flash = 0.18
        if not self.warning_attacks and getattr(self, "ice_dragon_ai_state", "idle") in ("idle", "choose_pattern"):
            self.ice_dragon_ai_state = "damaged"
            self.ice_dragon_state_timer = 0.18
    self.hp -= amount
    if self.hp <= self.max_hp * 0.5:
        if self.floor == ICE_DRAGON_FLOOR and not self.phase2:
            self.phase2 = True
            self.floor15_phase_text = True
        elif self.floor == 1:
            self.phase2 = True
    if self.hp <= 0:
        self.hp = 0
        if self.floor == ICE_DRAGON_FLOOR:
            start_ice_dragon_death(self)
        elif self.floor == INFERNO_LIGER_FLOOR:
            start_liger_death(self)
        elif self.floor == FOREST_GUARDIAN_FLOOR:
            start_forest_guardian_death(self)
        elif self.floor == FINAL_CORE_PATTERN_FLOOR:
            start_final_core_death(self)
        else:
            self.dead = True

def start_final_core_death(self):
    if getattr(self, "final_core_death_state", "") in ("dying", "dead"):
        return
    self.hp = 0
    self.dead = False
    self.final_core_death_state = "dying"
    self.final_core_death_timer = 0.0
    self.state = "defeat"
    self.attack_timer = 0.0
    self.pattern_cd = 999.0
    self.warning_lines = []
    self.warning_attacks.clear()
    self.final_core_last_pattern = "defeat"
    self.final_core_move_target = None

def start_forest_guardian_death(self):
    if getattr(self, "forest_death_state", "") in ("dying", "dead"):
        return
    self.hp = 0
    self.dead = False
    self.forest_death_state = "dying"
    self.forest_death_timer = 0.0
    self.state = "defeat"
    self.attack_timer = 0.0
    self.pattern_cd = 999.0
    self.warning_lines = []
    self.warning_attacks.clear()
    self.forest_guard_timer = 0.0
    self.forest_last_pattern = "defeat"

def start_liger_death(self):
    if getattr(self, "liger_death_state", "") in ("dying", "dead"):
        return
    self.hp = 0
    self.dead = False
    self.liger_death_state = "dying"
    self.liger_death_timer = 0.0
    self.state = "defeat"
    self.attack_timer = 0.0
    self.pattern_cd = 999.0
    self.warning_lines = []
    self.warning_attacks.clear()
    self.liger_last_pattern = "defeat"
    self.liger_roar_opening = 0.0

def start_ice_dragon_death(self):
    if getattr(self, "is_dying", False) or getattr(self, "ready_to_clear", False):
        return
    self.hp = 0
    self.dead = False
    self.is_dying = True
    self.ready_to_clear = False
    self.ice_dragon_ai_state = "death"
    self.ice_dragon_death_timer = 0.0
    self.ice_dragon_state_timer = ICE_DRAGON_DEATH_ANIM_TIME
    self.ice_dragon_current_pattern = None
    self.pattern_cd = 999.0
    self.attack_timer = 0.0
    self.ice_dragon_hurt_flash = 0.0
    self.warning_lines = []
    self.warning_attacks.clear()
    self.active_tornadoes.clear()
    self.current_breath_sector = None
    self.active_breath_sectors = []
    self.breath_direction = "center"
    set_ice_dragon_animation(self, "dead", force=True, frame_index=0, locked=True)

def ensure_ice_dragon_attrs(self):
    if not hasattr(self, "ice_dragon_ai_state"):
        self.ice_dragon_ai_state = "idle"
    if not hasattr(self, "ice_dragon_state_timer"):
        self.ice_dragon_state_timer = 0.0
    if not hasattr(self, "ice_dragon_current_pattern"):
        self.ice_dragon_current_pattern = None
    if not hasattr(self, "ice_dragon_hurt_flash"):
        self.ice_dragon_hurt_flash = 0.0
    if not hasattr(self, "current_breath_sector"):
        self.current_breath_sector = None
    if not hasattr(self, "active_breath_sectors"):
        self.active_breath_sectors = []
    if not hasattr(self, "breath_direction"):
        self.breath_direction = "center"
    if not hasattr(self, "active_tornadoes"):
        self.active_tornadoes = []
    if not hasattr(self, "ice_dragon_animation"):
        self.ice_dragon_animation = "idle"
    if not hasattr(self, "ice_dragon_animation_locked"):
        self.ice_dragon_animation_locked = False
    if not hasattr(self, "ice_dragon_anim_timer"):
        self.ice_dragon_anim_timer = 0.0
    if not hasattr(self, "ice_dragon_frame_index"):
        self.ice_dragon_frame_index = 0
    if not hasattr(self, "ice_dragon_death_timer"):
        self.ice_dragon_death_timer = 0.0
    if not hasattr(self, "is_dying"):
        self.is_dying = False
    if not hasattr(self, "ready_to_clear"):
        self.ready_to_clear = False

def start_ice_dragon_pattern(self, player):
    self.warning_attacks.clear()
    cx, cy, radius = get_ice_dragon_arena_values(ICE_DRAGON_WORLD_WIDTH, ICE_DRAGON_WORLD_HEIGHT)
    center = (cx, cy)
    pattern = self.ice_dragon_current_pattern
    if pattern == "breath":
        arena_rx = radius[0] if isinstance(radius, (tuple, list, pygame.Vector2)) else radius
        arena_ry = radius[1] if isinstance(radius, (tuple, list, pygame.Vector2)) else radius
        target_sector = ice_dragon_sector_from_point(player.pos, center, arena_rx, arena_ry, player.radius)
        if target_sector is None:
            dx = player.pos.x - cx
            dy = max(0, player.pos.y - cy)
            angle = math.atan2(dy / max(1, arena_ry), dx / max(1, arena_rx))
            target_sector = int(clamp((math.pi - angle) / (math.pi / 5), 0, 4.999))
        phase2 = self.hp <= self.max_hp * 0.5
        self.phase2 = self.phase2 or phase2
        if phase2:
            matching_combos = [combo for combo in ICE_DRAGON_PHASE2_BREATH_COMBOS if target_sector in combo]
            sectors = list(random.choice(matching_combos or ICE_DRAGON_PHASE2_BREATH_COMBOS))
        else:
            sectors = [target_sector]
        self.current_breath_sector = target_sector
        self.active_breath_sectors = sectors
        self.breath_direction = get_ice_dragon_representative_breath_direction(sectors)
        for sector in sectors:
            self.warning_attacks.append( IceDragonHazard( "breath", center, radius, ICE_DRAGON_TELEGRAPH_TIME, ICE_DRAGON_BREATH_ACTIVE_TIME, 24 if self.phase2 else 20, sector_index=sector, ) )
        self.ice_dragon_ai_state = "telegraph_breath"
        self.ice_dragon_state_timer = ICE_DRAGON_TELEGRAPH_TIME + ICE_DRAGON_BREATH_ACTIVE_TIME
        set_ice_dragon_animation( self, f"breath_{self.breath_direction}", force=True, frame_index=0, locked=True, )
    else:
        self.current_breath_sector = None
        self.active_breath_sectors = []
        self.breath_direction = "center"
        available_slots = max(0, ICE_DRAGON_MAX_ACTIVE_TORNADOES - len(self.active_tornadoes))
        count = min(4 if self.phase2 else 3, available_slots)
        if count <= 0:
            self.ice_dragon_current_pattern = "breath"
            start_ice_dragon_pattern(self, player)
            return
        for _ in range(count):
            x, y = get_random_point_in_walkable_polygon(self.walkable_polygon, self.floor_top_y, self.floor_bottom_y, 92)
            velocity = pygame.Vector2(random.uniform(-90, 90), random.uniform(-45, 80))
            if velocity.length_squared() < 900:
                velocity = pygame.Vector2(70, 45).rotate(random.randrange(0, 360))
            self.active_tornadoes.append( IceDragonHazard( "blizzard", center, radius, ICE_DRAGON_BLIZZARD_TELEGRAPH_TIME, ICE_DRAGON_BLIZZARD_ACTIVE_TIME, 11 if self.phase2 else 9, pos=(x, y), velocity=velocity, radius=62 if self.phase2 else 54, ) )
        self.ice_dragon_ai_state = "telegraph_blizzard"
        self.ice_dragon_state_timer = ICE_DRAGON_BLIZZARD_TELEGRAPH_TIME
        set_ice_dragon_animation(self, "tornado", force=True, frame_index=0, locked=True)

def update_ice_dragon_state_machine(self, dt, player, projectiles, traps, effects, spawn_enemy):
    ensure_ice_dragon_attrs(self)
    self.timer += dt
    self.ice_dragon_hurt_flash = max(0, self.ice_dragon_hurt_flash - dt)
    update_ice_dragon_animation(self, dt)
    self.pos = pygame.Vector2( ICE_DRAGON_WORLD_WIDTH * ICE_DRAGON_CORE_POS_RATIO[0], ICE_DRAGON_WORLD_HEIGHT * ICE_DRAGON_CORE_POS_RATIO[1], )
    self.visual_pos = pygame.Vector2( ICE_DRAGON_WORLD_WIDTH * ICE_DRAGON_VISUAL_ANCHOR_RATIO[0], ICE_DRAGON_WORLD_HEIGHT * ICE_DRAGON_VISUAL_ANCHOR_RATIO[1], )
    self.visual_height = int(HEIGHT * ICE_DRAGON_VISUAL_HEIGHT_RATIO)
    self.warning_lines = []

    if self.hp <= 0 and not self.is_dying and not self.ready_to_clear:
        start_ice_dragon_death(self)

    if self.ice_dragon_ai_state == "death":
        self.ice_dragon_death_timer += dt
        self.ice_dragon_state_timer = max(
            0.0, ICE_DRAGON_DEATH_ANIM_TIME - self.ice_dragon_death_timer
        )
        self.warning_attacks.clear()
        self.active_tornadoes.clear()
        self.current_breath_sector = None
        self.active_breath_sectors = []
        self.breath_direction = "center"
        projectiles[:] = [
            projectile
            for projectile in projectiles
            if getattr(projectile, "owner", None) != "enemy"
        ]
        shard_step = int(self.ice_dragon_death_timer * 8)
        if shard_step != getattr(self, "_ice_dragon_last_death_shard_step", -1):
            self._ice_dragon_last_death_shard_step = shard_step
            angle = (shard_step * 137.5) % 360
            offset = pygame.Vector2(110, 0).rotate(angle)
            effects.append(
                Effect(
                    self.visual_pos.x + offset.x,
                    self.visual_pos.y - 170 + offset.y * 0.45,
                    34,
                    (185, 245, 255),
                    0.42,
                )
            )
        if self.ice_dragon_death_timer >= ICE_DRAGON_DEATH_ANIM_TIME:
            self.ice_dragon_ai_state = "dead"
            self.is_dying = False
            self.ready_to_clear = True
            self.dead = True
            self.ice_dragon_animation_locked = False
        return

    if self.dead or self.ice_dragon_ai_state == "dead":
        self.ready_to_clear = True
        return

    for warning in self.warning_attacks:
        was_triggered = warning.triggered
        result = warning.update(dt, player)
        if warning.triggered and not was_triggered:
            effects.append(Effect(warning.pos.x, warning.pos.y, 78, (120, 230, 255), 0.28))
        if result == "dodged":
            effects.append(Effect(player.pos.x, player.pos.y, 64, YELLOW, 0.26))
        elif result == "shield":
            effects.append(Effect(player.pos.x, player.pos.y, 58, CYAN, 0.24))
        elif result == "hit":
            effects.append(Effect(player.pos.x, player.pos.y, 42, (120, 230, 255), 0.18))
    self.warning_attacks = [warning for warning in self.warning_attacks if not warning.done]

    for tornado in self.active_tornadoes:
        was_triggered = tornado.triggered
        result = tornado.update(dt, player)
        if tornado.triggered and not was_triggered:
            effects.append(Effect(tornado.pos.x, tornado.pos.y, 78, (120, 230, 255), 0.28))
        if result == "dodged":
            effects.append(Effect(player.pos.x, player.pos.y, 64, YELLOW, 0.26))
        elif result == "shield":
            effects.append(Effect(player.pos.x, player.pos.y, 58, CYAN, 0.24))
        elif result == "hit":
            effects.append(Effect(player.pos.x, player.pos.y, 42, (120, 230, 255), 0.18))
    self.active_tornadoes = [tornado for tornado in self.active_tornadoes if not tornado.done]

    if self.floor15_phase_text:
        effects.append(Effect(self.arena_rect.centerx, self.arena_rect.top + 70, 160, (120, 230, 255), 0.6))
        self.floor15_phase_text = False

    state = self.ice_dragon_ai_state
    if state == "damaged":
        self.ice_dragon_state_timer -= dt
        if self.ice_dragon_state_timer <= 0:
            self.ice_dragon_ai_state = "idle"
            set_ice_dragon_animation(self, "idle", force=True, frame_index=0, locked=False)
            self.pattern_cd = min(self.pattern_cd, 0.65)
        return

    if state == "choose_pattern":
        self.ice_dragon_state_timer -= dt
        if self.ice_dragon_state_timer <= 0:
            start_ice_dragon_pattern(self, player)
        return

    if state == "telegraph_blizzard":
        self.ice_dragon_state_timer -= dt
        if self.ice_dragon_state_timer <= 0:
            self.ice_dragon_ai_state = "execute_blizzard"
            self.ice_dragon_state_timer = ICE_DRAGON_TORNADO_CAST_ANIM_TIME
            set_ice_dragon_animation(self, "tornado", force=True, frame_index=1, locked=True)
        return
    if state == "execute_blizzard":
        self.ice_dragon_state_timer -= dt
        if self.ice_dragon_state_timer <= 0:
            self.ice_dragon_ai_state = "recover_blizzard"
            self.ice_dragon_state_timer = ICE_DRAGON_TORNADO_RECOVER_TIME
            set_ice_dragon_animation(self, "idle", force=True, frame_index=0, locked=False)
        return
    if state == "telegraph_breath" and any(w.active for w in self.warning_attacks):
        self.ice_dragon_ai_state = "execute_breath"
        set_ice_dragon_animation( self, f"breath_{self.breath_direction}", force=True, frame_index=1, locked=True, )
    if state == "execute_breath" and not self.warning_attacks:
        self.ice_dragon_ai_state = "recover_breath"
        self.ice_dragon_state_timer = ICE_DRAGON_BREATH_RECOVER_TIME
        set_ice_dragon_animation(self, "idle", force=True, frame_index=0, locked=False)
        return
    if state.startswith("recover_"):
        self.ice_dragon_state_timer -= dt
        if self.ice_dragon_state_timer <= 0:
            self.ice_dragon_ai_state = "idle"
            set_ice_dragon_animation(self, "idle", force=True, frame_index=0, locked=False)
            self.pattern_cd = 1.0 if self.phase2 else 1.25
            self.current_breath_sector = None
            self.active_breath_sectors = []
            self.breath_direction = "center"
        return
    if self.warning_attacks:
        return

    self.pattern_cd -= dt
    if self.pattern_cd > 0:
        return
    self.pattern_count += 1
    self.ice_dragon_ai_state = "choose_pattern"
    self.ice_dragon_state_timer = 0.12
    if len(self.active_tornadoes) >= ICE_DRAGON_MAX_ACTIVE_TORNADOES:
        self.ice_dragon_current_pattern = "breath"
    else:
        self.ice_dragon_current_pattern = random.choices( ["breath", "blizzard"], weights=[0.62, 0.38 if not self.phase2 else 0.52], k=1, )[0]

def draw_ice_dragon_warnings(self, surface):
    for tornado in getattr(self, "active_tornadoes", []):
        tornado.draw(surface)
    for warning in self.warning_attacks:
        warning.draw(surface)

def get_ice_dragon_core_hitbox(self):
    return pygame.Rect( int(ICE_DRAGON_WORLD_WIDTH * 0.43), int(ICE_DRAGON_WORLD_HEIGHT * 0.31), int(ICE_DRAGON_WORLD_WIDTH * 0.14), int(ICE_DRAGON_WORLD_HEIGHT * 0.16), )

def get_ice_dragon_melee_zone(self):
    cx, cy, (rx, ry) = get_ice_dragon_arena_values(ICE_DRAGON_WORLD_WIDTH, ICE_DRAGON_WORLD_HEIGHT)
    width = 140
    height = 60
    center_y = cy + ry * 0.06
    return pygame.Rect( int(cx - width * 0.5), int(center_y - height * 0.5), int(width), int(height), )

def get_ice_dragon_head_focus_pos(self):
    return pygame.Vector2( ICE_DRAGON_WORLD_WIDTH * ICE_DRAGON_HEAD_FOCUS_RATIO[0], ICE_DRAGON_WORLD_HEIGHT * ICE_DRAGON_HEAD_FOCUS_RATIO[1], )

def draw_ice_dragon_fallback(self, surface):
    anchor_x, anchor_y = self.visual_pos.x, self.visual_pos.y
    direction = getattr(self, "breath_direction", "center")
    direction_offset = { "left": -80, "left_diagonal": -42, "center": 0, "right_diagonal": 42, "right": 80, }.get(direction, 0)
    x = anchor_x
    y = anchor_y - 116
    scale = 1.0
    body = pygame.Rect(0, 0, int(320 * scale), int(150 * scale))
    body.center = (int(x), int(y))
    draw_ellipse_shadow(surface, pygame.Vector2(anchor_x, anchor_y), 140, 110, 2.8, 0.35)
    pygame.draw.ellipse(surface, (24, 86, 140), body)
    pygame.draw.ellipse(surface, (130, 230, 255), body, 5)
    head = pygame.Rect(0, 0, int(120 * scale), int(95 * scale))
    head.center = (int(x + direction_offset), int(y - 90))
    pygame.draw.ellipse(surface, (30, 110, 175), head)
    pygame.draw.ellipse(surface, (170, 245, 255), head, 4)
    for side in (-1, 1):
        wing = [ (x + side * 80 * scale, y - 20 * scale), (x + side * 250 * scale, y - 130 * scale), (x + side * 210 * scale, y + 50 * scale), ]
        pygame.draw.polygon(surface, (28, 92, 150), wing)
        pygame.draw.polygon(surface, (120, 220, 255), wing, 4)
        pygame.draw.polygon(surface, (220, 250, 255), [ (x + side * 20 * scale, y - 150 * scale), (x + side * 42 * scale, y - 220 * scale), (x + side * 64 * scale, y - 150 * scale), ])
    eye_y = int(y - 100)
    pygame.draw.circle(surface, (230, 255, 255), (int(x + direction_offset - 25), eye_y), 7)
    pygame.draw.circle(surface, (230, 255, 255), (int(x + direction_offset + 25), eye_y), 7)
    self.visual_rect = pygame.Rect(int(anchor_x - 280), int(anchor_y - 360), 560, 380)

def draw_ice_dragon_breath_direction_cue(self, surface):
    state = getattr(self, "ice_dragon_ai_state", "idle")
    if state not in ("telegraph_breath", "execute_breath"):
        return
    direction = getattr(self, "breath_direction", "center")
    vectors = { "left": pygame.Vector2(-1.0, 0.12), "left_diagonal": pygame.Vector2(-0.72, 0.44), "center": pygame.Vector2(0.0, 1.0), "right_diagonal": pygame.Vector2(0.72, 0.44), "right": pygame.Vector2(1.0, 0.12), }
    aim = vectors.get(direction, pygame.Vector2(0, 1))
    if aim.length_squared() > 0:
        aim = aim.normalize()
    origin = pygame.Vector2(self.visual_pos.x, self.visual_pos.y - 245)
    pulse = 0.45 + 0.55 * abs(math.sin(pygame.time.get_ticks() * 0.018))
    length = 92 if state == "telegraph_breath" else 145
    width = 12 if state == "telegraph_breath" else 22
    end = origin + aim * length
    color = (145, 235, 255, int(74 + pulse * 70))
    glow = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    pygame.draw.line(glow, color, origin, end, width)
    pygame.draw.circle(glow, (230, 255, 255, int(70 + pulse * 60)), end, max(8, width))
    surface.blit(glow, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

def draw_ice_dragon_boss(self, surface, font):
    pulse = 0.5 + 0.5 * math.sin(self.timer * 4.0)
    x, y = self.visual_pos.x, self.visual_pos.y
    death_progress = clamp(
        getattr(self, "ice_dragon_death_timer", 0.0) / ICE_DRAGON_DEATH_ANIM_TIME,
        0.0,
        1.0,
    )
    death_offset_y = int(54 * death_progress)
    death_alpha = int(255 * (1.0 - max(0.0, death_progress - 0.45) / 0.55))
    aura = pygame.Surface((620, 420), pygame.SRCALPHA)
    aura_alpha = int((32 + pulse * 30) * (1.0 - death_progress))
    pygame.draw.ellipse(aura, (90, 220, 255, aura_alpha), (40, 120, 540, 210), 6)
    pygame.draw.ellipse(aura, (230, 255, 255, int(26 * (1.0 - death_progress))), (90, 150, 440, 150), 2)
    surface.blit(aura, (int(x - 310), int(y - 330)), special_flags=pygame.BLEND_RGBA_ADD)

    sprite = self.get_floor15_frame()
    if sprite:
        draw_sprite = sprite
        if getattr(self, "ice_dragon_ai_state", "idle") in ("death", "dead"):
            draw_sprite = sprite.copy()
            draw_sprite.set_alpha(death_alpha)
        rect = draw_sprite.get_rect(midbottom=(int(x), int(y + death_offset_y)))
        self.visual_rect = rect
        surface.blit(draw_sprite, rect)
    else:
        draw_ice_dragon_fallback(self, surface)
    if getattr(self, "ice_dragon_ai_state", "idle") not in ("death", "dead"):
        draw_ice_dragon_breath_direction_cue(self, surface)

    draw_bar(surface, WIDTH // 2 - 260, 82, 520, 16, self.hp, self.max_hp, self.color)
    draw_text(surface, font, "16층 보스 - Ice Dragon", WIDTH // 2, 54, WHITE, center=True)
    if self.phase2:
        draw_text(surface, font, "빙룡의 냉기가 거세집니다!", WIDTH // 2, 106, (150, 235, 255), center=True)

    if DEBUG_BOSS15 or DEBUG_BOSS15_AREA or DEBUG_BOSS15_FLOOR:
        pygame.draw.rect(surface, (255, 220, 80), self.visual_rect, 2)
        pygame.draw.polygon(surface, (80, 255, 255), self.walkable_polygon, 2)
        pygame.draw.rect(surface, (255, 80, 120), self.get_floor15_core_hitbox(), 2)
        pygame.draw.rect(surface, (80, 220, 255), self.get_floor15_melee_zone(), 2)

def draw_entities_with_ice_dragon_order(self, surface, font, player=None):
    if player:
        draw_lumizone_aura(surface, player)
    ice_dragon = self.boss and self.boss.floor == ICE_DRAGON_FLOOR
    if ice_dragon:
        self.boss.draw(surface, font)
        self.boss.draw_warnings(surface)
    elif self.boss and hasattr(self.boss, "draw_warnings"):
        self.boss.draw_warnings(surface)

    for trap in self.traps:
        trap.draw(surface)
    for projectile in self.projectiles:
        projectile.draw(surface)

    actors = []
    for enemy in self.enemies:
        actors.append((enemy.pos.y, enemy.draw))
    if self.boss and not ice_dragon:
        actors.append((self.boss.pos.y, lambda target_surface, boss=self.boss: boss.draw(target_surface, font)))
    if player:
        for pet in player.pets:
            actors.append((pet.pos.y, pet.draw))
        actors.append((player.pos.y, player.draw))
    for _, draw_actor in sorted(actors, key=lambda item: item[0]):
        draw_actor(surface)

    for effect in self.effects:
        effect.draw(surface)

if not hasattr(Boss, "load_floor15_motion_frames_original"):
    Boss.load_floor15_motion_frames_original = Boss.load_floor15_motion_frames
Boss.load_floor15_motion_frames = load_ice_dragon_motion_resources
Boss.get_floor15_frame = get_ice_dragon_frame
Boss.take_damage = take_damage_ice_dragon
Boss.update_floor15 = update_ice_dragon_state_machine
Boss.draw_warnings = draw_ice_dragon_warnings
Boss.get_floor15_core_hitbox = get_ice_dragon_core_hitbox
Boss.get_floor15_melee_zone = get_ice_dragon_melee_zone
Boss.get_floor15_head_focus_pos = get_ice_dragon_head_focus_pos
Boss.draw_floor15 = draw_ice_dragon_boss
Room.draw_entities = draw_entities_with_ice_dragon_order

# -----------------------------------------------------------------------------
# 11F LIGER-X11 Inferno visibility/camera/background fix
# -----------------------------------------------------------------------------
INFERNO_LIGER_ASSET_ALIASES = {
    "idle": ("inferno_idle(2).png", "inferno_idle.png"),
    "attack": ("inferno_attack(2).png", "inferno_attack.png"),
    "phase2": ("inferno_phase2(2).png", "inferno_phase2.png"),
    "dash": ("inferno_dash(2).png", "inferno_dash.png"),
    "roar": ("inferno_roar.png",),
    "defeat": ("inferno_defeat.png",),
}

def _liger_load_surface_from_aliases(names):
    for name in names:
        image = load_image_optional(name)
        if image is not None:
            try:
                return trim_transparent(remove_neutral_edge_background(image, tolerance=42), padding=2)
            except Exception:
                return image
    return None

def _liger_ensure_assets(self):
    if getattr(self, "floor", None) != INFERNO_LIGER_FLOOR:
        return
    if getattr(self, "_liger_assets_ready", False):
        return
    self.skin_images = {}
    for key, aliases in INFERNO_LIGER_ASSET_ALIASES.items():
        image = _liger_load_surface_from_aliases(aliases)
        if image is not None:
            self.skin_images[key] = image
    self.has_image_skin = any(self.skin_images.values())
    self.skin_scaled_cache = {}
    self._liger_assets_ready = True
    if not self.has_image_skin:
        print("[WARN] LIGER-X11 이미지가 없어 코드 그림으로 표시합니다. assets 폴더에 inferno_*.png를 넣어주세요.")

def _liger_current_image(self):
    _liger_ensure_assets(self)
    if getattr(self, "liger_death_state", "") == "dead":
        return None
    if self.dead or getattr(self, "liger_death_state", "") == "dying":
        return self.skin_images.get("defeat") or self.skin_images.get("idle")
    last = getattr(self, "liger_last_pattern", None)
    if getattr(self, "liger_roar_opening", 0) > 0:
        return self.skin_images.get("roar") or self.skin_images.get("phase2") or self.skin_images.get("idle")
    if self.attack_timer > 0:
        if last == "dash":
            return self.skin_images.get("dash") or self.skin_images.get("attack") or self.skin_images.get("idle")
        if last == "roar":
            return self.skin_images.get("roar") or self.skin_images.get("attack") or self.skin_images.get("idle")
        return self.skin_images.get("attack") or self.skin_images.get("phase2") or self.skin_images.get("idle")
    if self.phase2:
        return self.skin_images.get("phase2") or self.skin_images.get("idle")
    return self.skin_images.get("idle")

def _liger_draw_image_boss(self, surface, image):
    scale = depth_scale(self.pos.y)
    target_h = max(220, int(270 * scale))
    target_w = max(300, int(image.get_width() * target_h / max(1, image.get_height())))
    cache_key = (id(image), target_w, target_h, getattr(self, "liger_direction", 1) < 0)
    draw_image = self.skin_scaled_cache.get(cache_key)
    if draw_image is None:
        draw_image = pygame.transform.smoothscale(image, (target_w, target_h))
        if getattr(self, "liger_direction", 1) < 0:
            draw_image = pygame.transform.flip(draw_image, True, False)
        if len(self.skin_scaled_cache) > 18:
            self.skin_scaled_cache.clear()
        self.skin_scaled_cache[cache_key] = draw_image
    death_progress = 0.0
    if getattr(self, "liger_death_state", "") == "dying":
        death_progress = clamp(getattr(self, "liger_death_timer", 0.0) / INFERNO_LIGER_DEATH_ANIM_TIME, 0.0, 1.0)
        draw_image = draw_image.copy()
        fade_start = 0.45
        if death_progress > fade_start:
            draw_image.set_alpha(int(255 * (1.0 - (death_progress - fade_start) / (1.0 - fade_start))))
    bob = 0 if death_progress else math.sin(self.timer * 4.0) * 4
    death_offset_y = int(42 * death_progress)
    rect = draw_image.get_rect(midbottom=(int(self.pos.x), int(self.pos.y + 72 * scale + bob + death_offset_y)))
    self.visual_rect = rect
    draw_ellipse_shadow(surface, self.pos, self.radius, 150, 3.1, 0.50)
    surface.blit(draw_image, rect)

def _liger_draw_code_boss(self, surface):
    scale = depth_scale(self.pos.y)
    x, y = self.pos.x, self.pos.y
    r = int(self.radius * scale)
    bob = math.sin(self.timer * 5.0) * 4
    draw_ellipse_shadow(surface, self.pos, self.radius, 155, 3.0, 0.55)
    body = pygame.Rect(0, 0, int(r * 3.0), int(r * 1.35))
    body.center = (int(x), int(y + bob))
    pygame.draw.ellipse(surface, (35, 22, 18), body)
    pygame.draw.ellipse(surface, (255, 86, 30), body, max(4, int(5 * scale)))
    head = pygame.Rect(0, 0, int(r * 1.35), int(r * 1.00))
    head.center = (int(x + r * 1.05), int(y - r * 0.34 + bob))
    pygame.draw.ellipse(surface, (45, 28, 20), head)
    pygame.draw.circle(surface, (255, 210, 80), (int(x + r * 1.28), int(y - r * 0.46 + bob)), max(4, int(6 * scale)))
    for i in range(9):
        px = x - r * 1.25 + i * r * 0.34
        pygame.draw.line(surface, (255, 92, 24), (px, y - r * 0.72 + bob), (px + r * 0.25, y - r * 1.15 - random.random() * 16 + bob), max(3, int(5 * scale)))
    for side in (-1, 1):
        pygame.draw.line(surface, (255, 110, 30), (x - r * 0.4, y + side * r * 0.18 + bob), (x + r * 1.75, y + side * r * 0.18 + bob), max(3, int(5 * scale)))

def _liger_draw(self, surface, font):
    if self.floor != INFERNO_LIGER_FLOOR:
        return _ORIGINAL_BOSS_DRAW(self, surface, font)
    if getattr(self, "liger_death_state", "") == "dead":
        return
    _liger_ensure_assets(self)
    current_img = _liger_current_image(self)
    if current_img is not None:
        _liger_draw_image_boss(self, surface, current_img)
    else:
        _liger_draw_code_boss(self, surface)

def _liger_camera_update(self, target_pos, world_width, world_height, dt, room=None):
    if room and getattr(room, "bg_key", "") == "inferno_stage_11":
        focus = pygame.Vector2(target_pos)
        if getattr(room, "boss", None) and not room.boss.dead:
            focus = focus.lerp(room.boss.pos, 0.30)
        target_x = clamp(focus.x - WIDTH * 0.5, 0, max(0, world_width - WIDTH))
        target_y = clamp(focus.y - HEIGHT * 0.54, 0, max(0, world_height - HEIGHT))
        self.pos.x += (target_x - self.pos.x) * min(1.0, dt * 6.0)
        self.pos.y += (target_y - self.pos.y) * min(1.0, dt * 5.0)
        return
    return _ORIGINAL_CAMERA_UPDATE(self, target_pos, world_width, world_height, dt, room)

def _liger_camera_reset(self, target_pos, world_width, world_height, room=None):
    if room and getattr(room, "bg_key", "") == "inferno_stage_11":
        focus = pygame.Vector2(target_pos)
        if getattr(room, "boss", None) and not room.boss.dead:
            focus = focus.lerp(room.boss.pos, 0.30)
        self.pos.x = clamp(focus.x - WIDTH * 0.5, 0, max(0, world_width - WIDTH))
        self.pos.y = clamp(focus.y - HEIGHT * 0.54, 0, max(0, world_height - HEIGHT))
        self.shake_timer = 0
        self.shake_strength = 0
        return
    return _ORIGINAL_CAMERA_RESET(self, target_pos, world_width, world_height, room)

def _liger_game_get_world_background(self, room):
    if getattr(room, "bg_key", "") == "inferno_stage_11":
        key = (room.bg_key, room.world_width, room.world_height)
        if key in self.world_backgrounds:
            return self.world_backgrounds[key]
        base = self.backgrounds.get("inferno_stage_11") or load_image_optional("inferno_stage_11.png", alpha=False)
        if base:
            bg = scale_cover(base, (room.world_width, room.world_height))
        else:
            bg = pygame.Surface((room.world_width, room.world_height))
            bg.fill((16, 18, 24))
        self.world_backgrounds[key] = bg
        return bg
    return _ORIGINAL_GAME_GET_WORLD_BACKGROUND(self, room)

def _liger_game_draw_world_background(self, surface, room):
    if getattr(room, "bg_key", "") == "inferno_stage_11":
        surface.blit(self.get_world_background(room), (0, 0))
        return
    return _ORIGINAL_GAME_DRAW_WORLD_BACKGROUND(self, surface, room)

def _liger_game_draw_world_combat_floor(self, surface, room):
    if getattr(room, "bg_key", "") == "inferno_stage_11":
        if DEBUG_WALKABLE:
            floor = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            pygame.draw.polygon(floor, (255, 120, 35, 80), room.walkable_polygon)
            pygame.draw.polygon(floor, (255, 220, 80, 170), room.walkable_polygon, 3)
            surface.blit(floor, (0, 0))
        return
    return _ORIGINAL_GAME_DRAW_WORLD_COMBAT_FLOOR(self, surface, room)

def _liger_enter_floor(self, floor):
    _ORIGINAL_GAME_ENTER_FLOOR(self, floor)
    if getattr(self.current_room, "bg_key", "") == "inferno_stage_11":
        start = pygame.Vector2(self.current_room.world_width * 0.50, self.current_room.floor_bottom_y - 105)
        self.player.pos = clamp_point_to_polygon(start, self.current_room.walkable_polygon, self.player.radius)
        if getattr(self.current_room, "boss", None):
            self.current_room.boss.set_arena(self.current_room.arena_rect, self.current_room.walkable_polygon, self.current_room.floor_top_y, self.current_room.floor_bottom_y)
            self.current_room.boss.warning_lines = []
            self.current_room.boss.warning_attacks.clear()
            self.current_room.boss.pattern_cd = 0.0
            self.current_room.boss.attack_timer = 0.0
        self.camera.reset(self.player.pos, self.current_room.world_width, self.current_room.world_height, self.current_room)

_ORIGINAL_BOSS_DRAW = Boss.draw
Boss.draw = _liger_draw
_ORIGINAL_CAMERA_UPDATE = Camera.update
_ORIGINAL_CAMERA_RESET = Camera.reset
Camera.update = _liger_camera_update
Camera.reset = _liger_camera_reset
_ORIGINAL_GAME_GET_WORLD_BACKGROUND = Game.get_world_background
_ORIGINAL_GAME_DRAW_WORLD_BACKGROUND = Game.draw_world_background
_ORIGINAL_GAME_DRAW_WORLD_COMBAT_FLOOR = Game.draw_world_combat_floor
_ORIGINAL_GAME_ENTER_FLOOR = Game.enter_floor
Game.get_world_background = _liger_game_get_world_background
Game.draw_world_background = _liger_game_draw_world_background
Game.draw_world_combat_floor = _liger_game_draw_world_combat_floor
Game.enter_floor = _liger_enter_floor

def boss_should_draw_after_death_state(boss):
    if not boss:
        return False
    if not boss.dead:
        return True
    return any(
        getattr(boss, attr, "") == "dying"
        for attr in ("liger_death_state", "forest_death_state", "final_core_death_state")
    ) or getattr(boss, "ice_dragon_ai_state", "") == "death"

def draw_entities_with_liger_and_ice_dragon_order(self, surface, font, player=None):
    if player:
        draw_lumizone_aura(surface, player)
    draw_boss = boss_should_draw_after_death_state(self.boss)
    special_large_boss = draw_boss and self.boss and self.boss.floor == ICE_DRAGON_FLOOR
    if special_large_boss:
        self.boss.draw(surface, font)
        self.boss.draw_warnings(surface)
    elif draw_boss and self.boss and hasattr(self.boss, "draw_warnings"):
        self.boss.draw_warnings(surface)
    for trap in self.traps:
        trap.draw(surface)
    for projectile in self.projectiles:
        projectile.draw(surface)
    actors = []
    for enemy in self.enemies:
        actors.append((enemy.pos.y, enemy.draw))
    if draw_boss and self.boss and not special_large_boss:
        actors.append((self.boss.pos.y, lambda target_surface, boss=self.boss: boss.draw(target_surface, font)))
    if player:
        for pet in player.pets:
            actors.append((pet.pos.y, pet.draw))
        actors.append((player.pos.y, player.draw))
    for _, draw_actor in sorted(actors, key=lambda item: item[0]):
        draw_actor(surface)
    for effect in self.effects:
        effect.draw(surface)
Room.draw_entities = draw_entities_with_liger_and_ice_dragon_order

# Final floor/boss patch: 10F and 5F are normal combat rooms, 6F is Forest Guardian.
FOREST_GUARDIAN_FLOOR = 6
FOREST_GUARDIAN_STAGE_BACKGROUND = "forest_guardian_stage.png"
FOREST_GUARDIAN_IMAGE_IDLE = "forest_guardian_idle.jpg"
FOREST_GUARDIAN_IMAGE_BEAM = "forest_guardian_beam.jpg"
FOREST_GUARDIAN_IMAGE_GROUND = "forest_guardian_ground.jpg"
FOREST_GUARDIAN_IMAGE_DEFEAT = "forest_guardian_defeat.jpg"
FOREST_GUARDIAN_WORLD_WIDTH = 2200
FOREST_GUARDIAN_WORLD_HEIGHT = 1250
FOREST_GUARDIAN_WALKABLE_POLYGON_RATIO = [(0.08, 0.84), (0.92, 0.84), (0.84, 0.50), (0.64, 0.37), (0.36, 0.37), (0.16, 0.50)]
FOREST_GUARDIAN_CORE_POS_RATIO = (0.50, 0.43)
FOREST_GUARDIAN_VISUAL_ANCHOR_RATIO = (0.50, 0.60)
FOREST_GUARDIAN_FRAME_HEIGHTS = {"idle": 395, "beam": 395, "ground": 395, "defeat": 395}
FOREST_GUARDIAN_MAX_HP = 3000
FOREST_GUARDIAN_DEATH_ANIM_TIME = 1.35
FINAL_CORE_PATTERN_FLOOR = 1
FINAL_CORE_STAGE_BACKGROUND = "final_core_stage.png"
FINAL_CORE_IMAGE_IDLE = "final_core_idle.png"
FINAL_CORE_IMAGE_BEAM = "final_core_beam.png"
FINAL_CORE_IMAGE_CRYSTAL = "final_core_crystal.png"
FINAL_CORE_IMAGE_ULTIMATE = "final_core_ultimate.png"
FINAL_CORE_IMAGE_EFFECTS = "final_core_effects.png"
FINAL_CORE_WORLD_WIDTH = 2200
FINAL_CORE_WORLD_HEIGHT = 1250
FINAL_CORE_WALKABLE_POLYGON_RATIO = [(0.08, 0.84), (0.92, 0.84), (0.84, 0.50), (0.64, 0.37), (0.36, 0.37), (0.16, 0.50)]
FINAL_CORE_FRAME_HEIGHT = 410
FINAL_CORE_DEATH_ANIM_TIME = 1.35
FINAL_CORE_MAX_HP = 5000
BACKGROUND_IMAGES["forest_guardian_stage"] = FOREST_GUARDIAN_STAGE_BACKGROUND
BACKGROUND_IMAGE_ALIASES["forest_guardian_stage"] = [FOREST_GUARDIAN_STAGE_BACKGROUND, os.path.join("assets", FOREST_GUARDIAN_STAGE_BACKGROUND)]
BACKGROUND_IMAGES["final_core_stage"] = FINAL_CORE_STAGE_BACKGROUND
BACKGROUND_IMAGE_ALIASES["final_core_stage"] = [FINAL_CORE_STAGE_BACKGROUND, os.path.join("assets", FINAL_CORE_STAGE_BACKGROUND)]
BOSS_CONFIGS[FOREST_GUARDIAN_FLOOR] = {"boss_id": "forest_guardian_6", "name": "Forest Guardian", "fallback_type": "forest_guardian", "hitbox": (170, 150), "skins": {"idle": FOREST_GUARDIAN_IMAGE_IDLE, "attack": FOREST_GUARDIAN_IMAGE_BEAM, "phase2": FOREST_GUARDIAN_IMAGE_GROUND, "defeat": FOREST_GUARDIAN_IMAGE_DEFEAT}}
Boss.DATA[FOREST_GUARDIAN_FLOOR] = ("Forest Guardian", (90, 215, 125), FOREST_GUARDIAN_MAX_HP)
BOSS_CONFIGS[FINAL_CORE_PATTERN_FLOOR] = {"boss_id": "final_core_1", "name": "Final Core", "fallback_type": "final_core", "hitbox": (190, 170), "skins": {"idle": FINAL_CORE_IMAGE_IDLE, "attack": FINAL_CORE_IMAGE_BEAM, "phase2": FINAL_CORE_IMAGE_ULTIMATE, "defeat": FINAL_CORE_IMAGE_CRYSTAL}}

_ORIGINAL_FINAL_ROOM_INIT = Room.__init__
def _final_room_init(self, floor, room_type):
    _ORIGINAL_FINAL_ROOM_INIT(self, floor, room_type)
    if floor == FOREST_GUARDIAN_FLOOR and room_type == ROOM_BOSS:
        self.bg_key = "forest_guardian_stage"
        self.world_width = FOREST_GUARDIAN_WORLD_WIDTH
        self.world_height = FOREST_GUARDIAN_WORLD_HEIGHT
        self.walkable_polygon = make_ratio_polygon(self.world_width, self.world_height, FOREST_GUARDIAN_WALKABLE_POLYGON_RATIO)
        ys = [point[1] for point in self.walkable_polygon]
        self.floor_top_y = min(ys)
        self.floor_bottom_y = max(ys)
        xs = [point[0] for point in self.walkable_polygon]
        self.arena_rect = pygame.Rect(min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))
        self.movement_mode = "floor_depth"
        self.stair_zones = []
    elif floor == FINAL_CORE_PATTERN_FLOOR and room_type == ROOM_FINAL:
        self.bg_key = "final_core_stage"
        self.world_width = FINAL_CORE_WORLD_WIDTH
        self.world_height = FINAL_CORE_WORLD_HEIGHT
        self.walkable_polygon = make_ratio_polygon(self.world_width, self.world_height, FINAL_CORE_WALKABLE_POLYGON_RATIO)
        ys = [point[1] for point in self.walkable_polygon]
        self.floor_top_y = min(ys)
        self.floor_bottom_y = max(ys)
        xs = [point[0] for point in self.walkable_polygon]
        self.arena_rect = pygame.Rect(min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))
        self.movement_mode = "floor_depth"
        self.stair_zones = []
Room.__init__ = _final_room_init

_ORIGINAL_FINAL_ROOM_SETUP = Room.setup
def _final_room_setup(self):
    if self.floor == FOREST_GUARDIAN_FLOOR and self.room_type == ROOM_BOSS:
        self.boss = Boss(self.floor)
        self.boss.set_arena(self.arena_rect, self.walkable_polygon, self.floor_top_y, self.floor_bottom_y)
        return
    if self.floor == FINAL_CORE_PATTERN_FLOOR and self.room_type == ROOM_FINAL:
        self.boss = Boss(self.floor)
        self.boss.set_arena(self.arena_rect, self.walkable_polygon, self.floor_top_y, self.floor_bottom_y)
        return
    return _ORIGINAL_FINAL_ROOM_SETUP(self)
Room.setup = _final_room_setup

_ORIGINAL_FINAL_BOSS_INIT = Boss.__init__
def _final_boss_init(self, floor):
    _ORIGINAL_FINAL_BOSS_INIT(self, floor)
    if floor == FOREST_GUARDIAN_FLOOR:
        self.name = "Forest Guardian"
        self.boss_id = "forest_guardian_6"
        self.fallback_type = "forest_guardian"
        self.color = (90, 215, 125)
        self.max_hp = FOREST_GUARDIAN_MAX_HP
        self.hp = self.max_hp
        self.radius = 74
        self.hitbox_w, self.hitbox_h = 170, 150
        self.pattern_cd = 1.3
        self.forest_frames = {}
        self.forest_last_pattern = "idle"
        self.forest_guard_timer = 0
    elif floor == FINAL_CORE_PATTERN_FLOOR:
        self.name = "Final Core"
        self.color = (190, 95, 255)
        self.max_hp = FINAL_CORE_MAX_HP
        self.hp = self.max_hp
        self.radius = 82
        self.hitbox_w, self.hitbox_h = 190, 170
        self.pattern_cd = 1.25
        self.final_core_last_pattern = "idle"
        self.final_core_frames = {}
        self.final_core_direction = 1
        self.final_core_move_target = None
Boss.__init__ = _final_boss_init

_ORIGINAL_FINAL_BOSS_SET_ARENA = Boss.set_arena
def _final_boss_set_arena(self, arena_rect, walkable_polygon=None, floor_top_y=None, floor_bottom_y=None):
    _ORIGINAL_FINAL_BOSS_SET_ARENA(self, arena_rect, walkable_polygon, floor_top_y, floor_bottom_y)
    if self.floor == INFERNO_LIGER_FLOOR:
        self.pos = self.clamp_to_walkable(pygame.Vector2(self.arena_rect.centerx, self.floor_top_y + self.arena_rect.height * 0.08), self.radius)
        self.visual_pos = pygame.Vector2(self.pos)
        self.liger_direction = 1
    elif self.floor == FOREST_GUARDIAN_FLOOR:
        self.pos = pygame.Vector2(FOREST_GUARDIAN_WORLD_WIDTH * FOREST_GUARDIAN_CORE_POS_RATIO[0], FOREST_GUARDIAN_WORLD_HEIGHT * FOREST_GUARDIAN_CORE_POS_RATIO[1])
        self.visual_pos = pygame.Vector2(FOREST_GUARDIAN_WORLD_WIDTH * FOREST_GUARDIAN_VISUAL_ANCHOR_RATIO[0], FOREST_GUARDIAN_WORLD_HEIGHT * FOREST_GUARDIAN_VISUAL_ANCHOR_RATIO[1])
        self.visual_height = FOREST_GUARDIAN_FRAME_HEIGHTS["idle"]
    elif self.floor == FINAL_CORE_PATTERN_FLOOR:
        self.pos = self.clamp_to_walkable(pygame.Vector2(self.arena_rect.centerx, self.floor_top_y + self.arena_rect.height * 0.36), self.radius)
        self.visual_pos = pygame.Vector2(self.pos)
Boss.set_arena = _final_boss_set_arena

def _forest_clean_sprite(frame):
    frame = frame.convert_alpha()
    max_clean_h = 520
    if frame.get_height() > max_clean_h:
        scaled_w = max(1, int(frame.get_width() * max_clean_h / frame.get_height()))
        frame = pygame.transform.smoothscale(frame, (scaled_w, max_clean_h))
    bg_removed = remove_neutral_edge_background(frame, tolerance=72)
    width, height = bg_removed.get_size()
    pixels = pygame.PixelArray(bg_removed)
    for y in range(0, height, 1):
        for x in range(0, width, 1):
            color = bg_removed.unmap_rgb(pixels[x, y])
            if color.a < 18:
                pixels[x, y] = (0, 0, 0, 0)
            else:
                neutral = max(color.r, color.g, color.b) - min(color.r, color.g, color.b) < 34
                checker_gray = neutral and color.r > 126 and color.g > 126 and color.b > 126
                if checker_gray:
                    pixels[x, y] = (color.r, color.g, color.b, 0)
    del pixels
    return trim_transparent(bg_removed, padding=2)

def _forest_load_frames(self):
    if getattr(self, "forest_frames", None):
        return self.forest_frames
    frames = {}
    sources = { "idle": FOREST_GUARDIAN_IMAGE_IDLE, "beam": FOREST_GUARDIAN_IMAGE_BEAM, "ground": FOREST_GUARDIAN_IMAGE_GROUND, "defeat": FOREST_GUARDIAN_IMAGE_DEFEAT, }
    for key, filename in sources.items():
        path = find_asset_path(os.path.join("assets", filename), filename)
        if not path:
            continue
        try:
            frame = pygame.image.load(path)
            frame = frame.convert_alpha() if pygame.display.get_surface() else frame.copy()
            frame = _forest_clean_sprite(frame)
            h = FOREST_GUARDIAN_FRAME_HEIGHTS.get(key, 470)
            w = max(260, int(frame.get_width() * h / max(1, frame.get_height())))
            frames[key] = pygame.transform.smoothscale(frame, (w, h))
        except (pygame.error, OSError, ValueError):
            pass
    self.forest_frames = frames
    return frames

def _forest_current_frame(self):
    frames = _forest_load_frames(self)
    if getattr(self, "forest_death_state", "") == "dead":
        return None
    if self.dead or getattr(self, "forest_death_state", "") == "dying":
        return frames.get("defeat") or frames.get("idle")
    if self.attack_timer > 0:
        if self.forest_last_pattern == "ranged":
            return frames.get("beam") or frames.get("idle")
        if self.forest_last_pattern in ("melee", "guard", "fury"):
            return frames.get("ground") or frames.get("idle")
        return frames.get("ground") or frames.get("idle")
    if self.forest_guard_timer > 0:
        return frames.get("ground") or frames.get("idle")
    return frames.get("idle")

def _final_core_load_frames(self):
    if getattr(self, "final_core_frames", None):
        return self.final_core_frames
    frames = {}
    sources = { "idle": FINAL_CORE_IMAGE_IDLE, "beam": FINAL_CORE_IMAGE_BEAM, "crystal": FINAL_CORE_IMAGE_CRYSTAL, "ultimate": FINAL_CORE_IMAGE_ULTIMATE, }
    for key, filename in sources.items():
        path = find_asset_path(os.path.join("assets", filename), filename)
        if not path:
            continue
        try:
            frame = pygame.image.load(path)
            frame = frame.convert_alpha() if pygame.display.get_surface() else frame.copy()
            frame = _forest_clean_sprite(frame)
            h = FINAL_CORE_FRAME_HEIGHT
            w = max(280, int(frame.get_width() * h / max(1, frame.get_height())))
            frames[key] = pygame.transform.smoothscale(frame, (w, h))
        except (pygame.error, OSError, ValueError):
            pass
    self.final_core_frames = frames
    return frames

def _final_core_current_frame(self):
    frames = _final_core_load_frames(self)
    pattern = getattr(self, "final_core_last_pattern", "idle")
    if getattr(self, "final_core_death_state", "") == "dead":
        return None
    if self.dead or getattr(self, "final_core_death_state", "") == "dying":
        return frames.get("crystal") or frames.get("idle")
    if self.attack_timer > 0:
        if pattern == "core_beam":
            return frames.get("beam") or frames.get("idle")
        if pattern == "collapse":
            return frames.get("crystal") or frames.get("idle")
        if pattern in ("death_ring", "summon_burst"):
            return frames.get("ultimate") or frames.get("beam") or frames.get("idle")
    return frames.get("idle")

def _draw_final_core_image_boss(self, surface):
    frame = _final_core_current_frame(self)
    if not frame:
        self.draw_final_core_boss(surface)
        return
    draw_frame = frame
    if getattr(self, "final_core_direction", 1) < 0:
        cache_key = ("flip", id(frame))
        cached = self.skin_scaled_cache.get(cache_key)
        if cached is None:
            cached = pygame.transform.flip(frame, True, False)
            self.skin_scaled_cache[cache_key] = cached
        draw_frame = cached
    bob = math.sin(self.timer * 3.2) * 6
    death_progress = 0.0
    if getattr(self, "final_core_death_state", "") == "dying":
        death_progress = clamp(getattr(self, "final_core_death_timer", 0.0) / FINAL_CORE_DEATH_ANIM_TIME, 0.0, 1.0)
        draw_frame = draw_frame.copy()
        fade_start = 0.45
        if death_progress > fade_start:
            draw_frame.set_alpha(int(255 * (1.0 - (death_progress - fade_start) / (1.0 - fade_start))))
    bob = 0 if death_progress else bob
    death_offset_y = int(44 * death_progress)
    rect = draw_frame.get_rect(midbottom=(int(self.visual_pos.x), int(self.visual_pos.y + 70 + bob + death_offset_y)))
    self.visual_rect = rect
    draw_ellipse_shadow(surface, self.pos, self.radius, 185, 3.4, 0.46)
    surface.blit(draw_frame, rect)

def _forest_update(self, dt, player, projectiles, traps, effects, spawn_enemy):
    self.warning_lines = []
    fixed = pygame.Vector2(FOREST_GUARDIAN_WORLD_WIDTH * FOREST_GUARDIAN_CORE_POS_RATIO[0], FOREST_GUARDIAN_WORLD_HEIGHT * FOREST_GUARDIAN_CORE_POS_RATIO[1])
    self.pos = self.clamp_to_walkable(fixed, self.radius)
    self.visual_pos = pygame.Vector2(FOREST_GUARDIAN_WORLD_WIDTH * FOREST_GUARDIAN_VISUAL_ANCHOR_RATIO[0], FOREST_GUARDIAN_WORLD_HEIGHT * FOREST_GUARDIAN_VISUAL_ANCHOR_RATIO[1])
    self.forest_guard_timer = max(0, self.forest_guard_timer - dt)
    for warning in self.warning_attacks:
        was_triggered = warning.triggered
        result = warning.update(dt, player)
        if warning.triggered and not was_triggered:
            if get_boss_skill_image(warning.kind) is None:
                effects.append(Effect(warning.pos.x, warning.pos.y, 82, warning.color[:3], 0.30))
        if result == "hit":
            effects.append(Effect(player.pos.x, player.pos.y, 48, RED, 0.20))
        elif result == "dodged":
            effects.append(Effect(player.pos.x, player.pos.y, 62, YELLOW, 0.22))
        elif result == "shield":
            effects.append(Effect(player.pos.x, player.pos.y, 58, CYAN, 0.22))
    self.warning_attacks = [warning for warning in self.warning_attacks if not warning.done]
    if self.pattern_cd > 0 or self.warning_attacks:
        return
    direction = player.pos - self.pos
    if direction.length_squared() == 0:
        direction = pygame.Vector2(0, 1)
    angle = math.degrees(math.atan2(direction.y, direction.x))
    pattern = random.choices(["melee", "ranged", "guard", "fury"], weights=[4, 4, 2, 1.4 if self.phase2 else 0.7], k=1)[0]
    self.forest_last_pattern = pattern
    self.state = "attack"
    self.attack_timer = 0.62
    if pattern == "melee":
        self.warning_attacks.append(BossWarning("ellipse", (player.pos.x, player.pos.y), (118, 46), 0.72, 0.28, 22 if self.phase2 else 18, (115, 225, 105), "forest_thorns"))
        self.warning_attacks.append(BossWarning("laser", self.pos, (520, 18), 0.70, 0.24, 18 if self.phase2 else 14, (120, 210, 95), "forest_root_swing", angle))
        self.pattern_cd = 1.65 if not self.phase2 else 1.32
    elif pattern == "ranged":
        spreads = (-22, 0, 22) if not self.phase2 else (-32, -16, 0, 16, 32)
        for spread in spreads:
            d = pygame.Vector2(1, 0).rotate(angle + spread)
            projectiles.append(Projectile(self.pos.x, self.pos.y - 18, d.x * 280, d.y * 280, 11, 15 if self.phase2 else 12, "enemy", (85, 220, 110), 3.2))
        self.warning_attacks.append(BossWarning("circle", self.clamp_to_walkable(player.pos, 70), 72 if self.phase2 else 58, 0.85, 0.44, 20 if self.phase2 else 15, (70, 190, 95), "forest_poison"))
        self.pattern_cd = 1.85 if not self.phase2 else 1.45
    elif pattern == "guard":
        self.forest_guard_timer = 1.4
        self.warning_attacks.append(BossWarning("circle", self.pos, 210 if self.phase2 else 170, 0.72, 0.32, 18 if self.phase2 else 12, (95, 235, 140), "forest_guard"))
        self.pattern_cd = 2.15 if not self.phase2 else 1.75
    else:
        for i in range(7 if self.phase2 else 5):
            pos = self.clamp_to_walkable(player.pos if i == 0 else pygame.Vector2(*self.random_walkable_point(76)), 76)
            self.warning_attacks.append(BossWarning("circle", pos, 62 if self.phase2 else 52, 0.95 + i * 0.04, 0.32, 24 if self.phase2 else 18, (120, 245, 145), "forest_fury"))
        self.pattern_cd = 2.35 if not self.phase2 else 1.85
    effects.append(Effect(self.pos.x, self.pos.y, 104, (90, 215, 125), 0.30))

def _process_boss_warning_attacks(self, dt, player, effects, flash_color):
    for warning in self.warning_attacks:
        was_triggered = warning.triggered
        result = warning.update(dt, player)
        if warning.triggered and not was_triggered:
            if get_boss_skill_image(warning.kind) is None:
                effects.append(Effect(warning.pos.x, warning.pos.y, 82, flash_color, 0.28))
        if result == "hit":
            effects.append(Effect(player.pos.x, player.pos.y, 48, RED, 0.18))
        elif result == "dodged":
            effects.append(Effect(player.pos.x, player.pos.y, 60, YELLOW, 0.20))
        elif result == "shield":
            effects.append(Effect(player.pos.x, player.pos.y, 56, CYAN, 0.20))
    self.warning_attacks = [warning for warning in self.warning_attacks if not warning.done]

def _final_core_update(self, dt, player, projectiles, traps, effects, spawn_enemy):
    self.warning_lines = []
    self.final_core_move_timer = getattr(self, "final_core_move_timer", 0.0) - dt
    if self.final_core_move_target is None or distance(self.pos, self.final_core_move_target) < 34 or self.final_core_move_timer <= 0:
        angle = random.uniform(0, 360)
        step_distance = random.uniform(180, 460)
        target = self.pos + pygame.Vector2(1, 0).rotate(angle) * step_distance
        self.final_core_move_target = self.clamp_to_walkable(target, self.radius)
        self.final_core_move_timer = random.uniform(0.75, 1.55)
    move_vec = self.final_core_move_target - self.pos
    if move_vec.length_squared() > 0:
        self.final_core_direction = 1 if move_vec.x >= 0 else -1
        speed = 120 if not self.phase2 else 155
        step = move_vec.normalize() * min(move_vec.length(), speed * dt)
        self.pos = self.clamp_to_walkable(self.pos + step, self.radius)
    self.visual_pos = pygame.Vector2(self.pos)
    _process_boss_warning_attacks(self, dt, player, effects, (245, 70, 95))
    if self.pattern_cd > 0 or self.warning_attacks:
        return
    direction = player.pos - self.pos
    if direction.length_squared() == 0:
        direction = pygame.Vector2(0, 1)
    angle = math.degrees(math.atan2(direction.y, direction.x))
    pattern = random.choices( ["core_beam", "death_ring", "collapse", "summon_burst"], weights=[4, 3, 3, 2 if self.phase2 else 1], k=1, )[0]
    self.final_core_last_pattern = pattern
    self.state = "attack"
    self.attack_timer = 0.65
    if pattern == "core_beam":
        spreads = (-24, 0, 24) if not self.phase2 else (-36, -18, 0, 18, 36)
        for spread in spreads:
            self.warning_attacks.append(BossWarning("laser", self.pos, (780 if self.phase2 else 650, 18), 0.72, 0.28, 24 if self.phase2 else 18, (255, 80, 110), "final_beam", angle + spread))
        self.pattern_cd = 1.75 if not self.phase2 else 1.32
    elif pattern == "death_ring":
        self.warning_attacks.append(BossWarning("circle", self.pos, 250 if self.phase2 else 205, 0.78, 0.34, 26 if self.phase2 else 20, (245, 70, 95), "final_ring"))
        shots = 12 if self.phase2 else 8
        for i in range(shots):
            d = pygame.Vector2(1, 0).rotate(i * 360 / shots + self.timer * 18)
            projectiles.append(Projectile(self.pos.x, self.pos.y, d.x * 330, d.y * 330, 9, 14 if self.phase2 else 10, "enemy", (245, 70, 95), 3.0))
        self.pattern_cd = 2.0 if not self.phase2 else 1.55
    elif pattern == "collapse":
        count = 7 if self.phase2 else 5
        for i in range(count):
            point = self.clamp_to_walkable(player.pos if i == 0 else pygame.Vector2(*self.random_walkable_point(78)), 74)
            self.warning_attacks.append(BossWarning("circle", point, 62 if self.phase2 else 52, 0.92 + i * 0.04, 0.34, 25 if self.phase2 else 18, (255, 105, 130), "final_collapse"))
        self.pattern_cd = 2.2 if not self.phase2 else 1.72
    else:
        for i in range(3 if self.phase2 else 2):
            pos = self.random_walkable_point(82)
            self.warning_attacks.append(BossWarning("ellipse", pos, (92, 40), 0.82 + i * 0.08, 0.45, 18 if self.phase2 else 14, (210, 55, 120), "final_burst"))
        for spread in (-14, 14) if not self.phase2 else (-24, -8, 8, 24):
            d = pygame.Vector2(1, 0).rotate(angle + spread)
            projectiles.append(Projectile(self.pos.x, self.pos.y, d.x * 300, d.y * 300, 10, 13 if self.phase2 else 10, "enemy", (255, 90, 125), 3.2))
        self.pattern_cd = 2.1 if not self.phase2 else 1.65
    effects.append(Effect(self.pos.x, self.pos.y, 110, (245, 70, 95), 0.30))

_ORIGINAL_FINAL_BOSS_UPDATE = Boss.update
def _final_boss_update(self, dt, player, projectiles, traps, effects, spawn_enemy):
    if self.dead:
        self.state = "defeat"
        self.attack_timer = 0
        self.pattern_cd = 999
        self.warning_lines = []
        self.warning_attacks.clear()
        if hasattr(self, "floor15_summon_queue"):
            self.floor15_summon_queue.clear()
        if hasattr(self, "active_tornadoes"):
            self.active_tornadoes.clear()
        return
    if self.floor == FOREST_GUARDIAN_FLOOR:
        self.timer += dt
        self.attack_timer = max(0, self.attack_timer - dt)
        self.pattern_cd -= dt
        self.vulnerable_timer = max(0, self.vulnerable_timer - dt)
        if getattr(self, "forest_death_state", "") == "dying":
            self.forest_death_timer = getattr(self, "forest_death_timer", 0.0) + dt
            self.state = "defeat"
            self.attack_timer = 0.0
            self.pattern_cd = 999.0
            self.warning_lines = []
            self.warning_attacks.clear()
            self.forest_guard_timer = 0.0
            fixed = pygame.Vector2(FOREST_GUARDIAN_WORLD_WIDTH * FOREST_GUARDIAN_CORE_POS_RATIO[0], FOREST_GUARDIAN_WORLD_HEIGHT * FOREST_GUARDIAN_CORE_POS_RATIO[1])
            self.pos = self.clamp_to_walkable(fixed, self.radius)
            self.visual_pos = pygame.Vector2(FOREST_GUARDIAN_WORLD_WIDTH * FOREST_GUARDIAN_VISUAL_ANCHOR_RATIO[0], FOREST_GUARDIAN_WORLD_HEIGHT * FOREST_GUARDIAN_VISUAL_ANCHOR_RATIO[1])
            if self.forest_death_timer >= FOREST_GUARDIAN_DEATH_ANIM_TIME:
                self.forest_death_state = "dead"
                self.dead = True
            return
        if self.hp <= self.max_hp * 0.5 and not self.phase2:
            self.phase2 = True
            self.pattern_cd = max(self.pattern_cd, 1.0)
        return _forest_update(self, dt, player, projectiles, traps, effects, spawn_enemy)
    if self.floor == FINAL_CORE_PATTERN_FLOOR:
        self.timer += dt
        self.attack_timer = max(0, self.attack_timer - dt)
        self.pattern_cd -= dt
        self.vulnerable_timer = max(0, self.vulnerable_timer - dt)
        if getattr(self, "final_core_death_state", "") == "dying":
            self.final_core_death_timer = getattr(self, "final_core_death_timer", 0.0) + dt
            self.state = "defeat"
            self.attack_timer = 0.0
            self.pattern_cd = 999.0
            self.warning_lines = []
            self.warning_attacks.clear()
            if self.final_core_death_timer >= FINAL_CORE_DEATH_ANIM_TIME:
                self.final_core_death_state = "dead"
                self.dead = True
            return
        if self.hp <= self.max_hp * 0.5 and not self.phase2:
            self.phase2 = True
            self.pattern_cd = max(self.pattern_cd, 1.0)
        return _final_core_update(self, dt, player, projectiles, traps, effects, spawn_enemy)
    if self.floor == INFERNO_LIGER_FLOOR:
        self.timer += dt
        self.attack_timer = max(0, self.attack_timer - dt)
        self.pattern_cd -= dt
        self.vulnerable_timer = max(0, self.vulnerable_timer - dt)
        fixed = pygame.Vector2(self.arena_rect.centerx, self.floor_top_y + self.arena_rect.height * 0.08)
        self.pos = self.clamp_to_walkable(fixed, self.radius)
        self.visual_pos = pygame.Vector2(self.pos)
        self.warning_lines = []
        if getattr(self, "liger_death_state", "") == "dying":
            self.liger_death_timer = getattr(self, "liger_death_timer", 0.0) + dt
            self.state = "defeat"
            self.attack_timer = 0.0
            self.pattern_cd = 999.0
            self.warning_attacks.clear()
            if self.liger_death_timer >= INFERNO_LIGER_DEATH_ANIM_TIME:
                self.liger_death_state = "dead"
                self.dead = True
            return
        if getattr(self, "liger_roar_opening", 0) > 0:
            self.liger_roar_opening -= dt
            self.state = "roar"
            self.liger_last_pattern = "roar"
            return
        for warning in self.warning_attacks:
            was_triggered = warning.triggered
            result = warning.update(dt, player)
            if warning.triggered and not was_triggered:
                if get_boss_skill_image(warning.kind) is None:
                    effects.append(Effect(warning.pos.x, warning.pos.y, 78, (255, 95, 35), 0.25))
            if result == "hit":
                effects.append(Effect(player.pos.x, player.pos.y, 48, RED, 0.18))
            elif result == "dodged":
                effects.append(Effect(player.pos.x, player.pos.y, 58, YELLOW, 0.20))
            elif result == "shield":
                effects.append(Effect(player.pos.x, player.pos.y, 54, CYAN, 0.20))
        self.warning_attacks = [warning for warning in self.warning_attacks if not warning.done]
        if self.pattern_cd > 0 or self.warning_attacks:
            return
        direction = player.pos - self.pos
        if direction.length_squared() == 0:
            direction = pygame.Vector2(1, 0)
        angle = math.degrees(math.atan2(direction.y, direction.x))
        pattern = random.choices(["breath", "claw", "roar", "meteors"], weights=[4, 3, 2, 2 if self.phase2 else 1], k=1)[0]
        self.liger_last_pattern = pattern
        self.state = "attack"
        self.attack_timer = 0.55
        if pattern == "breath":
            for spread in ((-18, 0, 18) if not self.phase2 else (-26, -13, 0, 13, 26)):
                d = pygame.Vector2(1, 0).rotate(angle + spread)
                projectiles.append(Projectile(self.pos.x, self.pos.y - 20, d.x * 330, d.y * 330, 11, 13 if self.phase2 else 10, "enemy", ORANGE, 2.7))
            self.warning_attacks.append(BossWarning("laser", self.pos, (590 if not self.phase2 else 690, 28), 0.52, 0.22, 16 if self.phase2 else 12, (255, 135, 35), "inferno_breath", angle))
            self.pattern_cd = 1.75 if not self.phase2 else 1.35
        elif pattern == "claw":
            for spread in (-15, 15):
                self.warning_attacks.append(BossWarning("laser", self.pos, (460, 14), 0.55, 0.22, 15 if self.phase2 else 12, (255, 145, 45), "inferno_claw", angle + spread))
            self.pattern_cd = 1.65 if not self.phase2 else 1.28
        elif pattern == "roar":
            self.warning_attacks.append(BossWarning("circle", self.pos, 165 if not self.phase2 else 210, 0.72, 0.30, 20 if self.phase2 else 15, (255, 80, 35), "inferno_roar"))
            shots = 7 if self.phase2 else 5
            for i in range(shots):
                d = pygame.Vector2(1, 0).rotate(i * 360 / shots + self.timer * 18)
                projectiles.append(Projectile(self.pos.x, self.pos.y, d.x * 290, d.y * 290, 8, 12 if self.phase2 else 9, "enemy", ORANGE, 3.0))
            self.pattern_cd = 1.95 if not self.phase2 else 1.52
        else:
            for i in range(5 if self.phase2 else 3):
                point = self.clamp_to_walkable(player.pos if i == 0 else pygame.Vector2(*self.random_walkable_point(72)), 65)
                self.warning_attacks.append(BossWarning("circle", point, 48 if self.phase2 else 40, 0.82, 0.27, 18 if self.phase2 else 13, (255, 120, 35), "inferno_meteor"))
            self.pattern_cd = 2.05 if not self.phase2 else 1.6
        effects.append(Effect(self.pos.x, self.pos.y, 88, (255, 95, 35), 0.25))
        return
    return _ORIGINAL_FINAL_BOSS_UPDATE(self, dt, player, projectiles, traps, effects, spawn_enemy)
Boss.update = _final_boss_update

_ORIGINAL_FINAL_BOSS_DRAW = Boss.draw
def _draw_forest_guardian_motion_fx(self, surface):
    if self.dead or self.attack_timer <= 0:
        return
    pulse = 0.45 + 0.55 * abs(math.sin(self.timer * 9.0))
    fx = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    if self.forest_last_pattern == "ranged":
        origin = pygame.Vector2(self.visual_pos.x, self.visual_pos.y - 270)
        for side in (-1, 1):
            start = origin + pygame.Vector2(side * 170, 12)
            end = start + pygame.Vector2(side * 480, -20)
            pygame.draw.line(fx, (110, 255, 155, int(90 + pulse * 100)), start, end, 18)
            pygame.draw.line(fx, (235, 255, 210, int(115 + pulse * 110)), start, end, 6)
            pygame.draw.circle(fx, (140, 255, 170, int(120 + pulse * 80)), start, 24)
    else:
        base = pygame.Vector2(self.visual_pos.x, self.visual_pos.y - 35)
        pygame.draw.ellipse(fx, (95, 245, 130, int(36 + pulse * 38)), (base.x - 310, base.y - 72, 620, 145), 8)
        for i in range(9):
            angle = -160 + i * 40 + math.sin(self.timer * 3.0 + i) * 8
            d = pygame.Vector2(1, 0).rotate(angle)
            start = base + d * 70
            end = base + d * (230 + 32 * pulse)
            pygame.draw.line(fx, (95, 210, 105, int(72 + pulse * 80)), start, end, 9)
            pygame.draw.line(fx, (80, 55, 28, int(95 + pulse * 55)), start, end, 4)
    surface.blit(fx, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

def _final_boss_draw(self, surface, font):
    if self.floor == FOREST_GUARDIAN_FLOOR:
        frame = _forest_current_frame(self)
        if frame:
            draw_frame = frame
            death_progress = 0.0
            if getattr(self, "forest_death_state", "") == "dying":
                death_progress = clamp(getattr(self, "forest_death_timer", 0.0) / FOREST_GUARDIAN_DEATH_ANIM_TIME, 0.0, 1.0)
                draw_frame = frame.copy()
                fade_start = 0.45
                if death_progress > fade_start:
                    draw_frame.set_alpha(int(255 * (1.0 - (death_progress - fade_start) / (1.0 - fade_start))))
            bob = 0 if death_progress else math.sin(self.timer * 3.5) * 3
            death_offset_y = int(44 * death_progress)
            rect = draw_frame.get_rect(midbottom=(int(self.visual_pos.x), int(self.visual_pos.y + bob + death_offset_y)))
            self.visual_rect = rect
            draw_ellipse_shadow(surface, self.pos, self.radius, 170, 3.2, 0.50)
            surface.blit(draw_frame, rect)
            _draw_forest_guardian_motion_fx(self, surface)
        else:
            self.draw_dark_beast_boss(surface)
        panel = pygame.Rect(WIDTH // 2 - 285, 44, 570, 68)
        hud = pygame.Surface(panel.size, pygame.SRCALPHA)
        pygame.draw.rect(hud, (0, 0, 0, 150), hud.get_rect(), border_radius=8)
        pygame.draw.rect(hud, (*self.color, 210), hud.get_rect(), 2, border_radius=8)
        surface.blit(hud, panel.topleft)
        draw_text(surface, font, "6F Boss - Forest Guardian", WIDTH // 2, 54, WHITE, center=True)
        draw_bar(surface, WIDTH // 2 - 260, 82, 520, 16, self.hp, self.max_hp, self.color)
        draw_text(surface, font, f"HP {max(0, int(self.hp))} / {self.max_hp}", WIDTH // 2, 102, WHITE, center=True)
        if self.phase2:
            draw_text(surface, font, "Phase 2 - Ancient Fury", WIDTH // 2, 126, (120, 245, 145), center=True)
        return
    if self.floor == ICE_DRAGON_FLOOR:
        self.draw_floor15(surface, font)
        panel = pygame.Rect(WIDTH // 2 - 285, 44, 570, 72)
        hud = pygame.Surface(panel.size, pygame.SRCALPHA)
        pygame.draw.rect(hud, (0, 0, 0, 150), hud.get_rect(), border_radius=8)
        pygame.draw.rect(hud, (105, 205, 255, 210), hud.get_rect(), 2, border_radius=8)
        surface.blit(hud, panel.topleft)
        draw_text(surface, font, "16F Boss - Ice Dragon", WIDTH // 2, 54, WHITE, center=True)
        draw_bar(surface, WIDTH // 2 - 260, 82, 520, 16, self.hp, self.max_hp, self.color)
        draw_text(surface, font, f"HP {max(0, int(self.hp))} / {self.max_hp}", WIDTH // 2, 102, WHITE, center=True)
        return
    if self.floor == INFERNO_LIGER_FLOOR:
        return _liger_draw(self, surface, font)
    if self.floor == FINAL_CORE_PATTERN_FLOOR:
        _draw_final_core_image_boss(self, surface)
        if self.phase2:
            draw_text(surface, font, "Phase 2 - Core Overload", WIDTH // 2, 126, (255, 100, 125), center=True)
        return
    return _ORIGINAL_FINAL_BOSS_DRAW(self, surface, font)
Boss.draw = _final_boss_draw

_ORIGINAL_FINAL_GAME_GENERATE_ROOMS = Game.generate_rooms
def _final_generate_rooms(self):
    rooms = {}
    for floor in range(20, 0, -1):
        if floor == 1:
            rooms[floor] = Room(floor, ROOM_FINAL)
        elif floor in (ICE_DRAGON_FLOOR, INFERNO_LIGER_FLOOR, FOREST_GUARDIAN_FLOOR):
            rooms[floor] = Room(floor, ROOM_BOSS)
        elif floor in (15, 10, 5):
            rooms[floor] = Room(floor, ROOM_NORMAL)
        elif 17 <= floor <= 19:
            rooms[floor] = Room(floor, random.choices([ROOM_NORMAL, ROOM_SURVIVAL, ROOM_REWARD, ROOM_REST], weights=[6, 2, 1.2, 1], k=1)[0])
        elif 12 <= floor <= 14:
            rooms[floor] = Room(floor, random.choices([ROOM_NORMAL, ROOM_WILD, ROOM_SURVIVAL, ROOM_REWARD, ROOM_SHOP], weights=[3, 4, 2, 1.2, 1], k=1)[0])
        elif 7 <= floor <= 9:
            rooms[floor] = Room(floor, random.choices([ROOM_EARTH, ROOM_ELITE, ROOM_NORMAL, ROOM_SHOP, ROOM_REWARD], weights=[4, 2, 3, 1, 1.2], k=1)[0])
        elif 2 <= floor <= 4:
            rooms[floor] = Room(floor, random.choices([ROOM_ELITE, ROOM_SURVIVAL, ROOM_ELECTRIC, ROOM_POISON, ROOM_SHOP, ROOM_REWARD], weights=[3, 2, 2, 2, 1, 1.2], k=1)[0])
        else:
            rooms[floor] = Room(floor, ROOM_NORMAL)
    return rooms
Game.generate_rooms = _final_generate_rooms

_ORIGINAL_FINAL_GAME_GET_WORLD_BACKGROUND = Game.get_world_background
def _final_game_get_world_background(self, room):
    if getattr(room, "bg_key", "") == "forest_guardian_stage":
        key = (room.bg_key, room.world_width, room.world_height)
        if key in self.world_backgrounds:
            return self.world_backgrounds[key]
        base = self.backgrounds.get("forest_guardian_stage") or load_image_optional(FOREST_GUARDIAN_STAGE_BACKGROUND, alpha=False)
        bg = scale_cover(base, (room.world_width, room.world_height)) if base else pygame.Surface((room.world_width, room.world_height))
        if not base:
            bg.fill((10, 18, 16))
        self.world_backgrounds[key] = bg
        return bg
    if getattr(room, "bg_key", "") == "final_core_stage":
        key = (room.bg_key, room.world_width, room.world_height)
        if key in self.world_backgrounds:
            return self.world_backgrounds[key]
        base = self.backgrounds.get("final_core_stage") or load_image_optional(FINAL_CORE_STAGE_BACKGROUND, alpha=False)
        bg = scale_cover(base, (room.world_width, room.world_height)) if base else pygame.Surface((room.world_width, room.world_height))
        if not base:
            bg.fill((14, 8, 24))
        self.world_backgrounds[key] = bg
        return bg
    return _ORIGINAL_FINAL_GAME_GET_WORLD_BACKGROUND(self, room)
Game.get_world_background = _final_game_get_world_background

_ORIGINAL_FINAL_GAME_DRAW_WORLD_COMBAT_FLOOR = Game.draw_world_combat_floor
def _final_game_draw_world_combat_floor(self, surface, room):
    if getattr(room, "bg_key", "") == "forest_guardian_stage":
        if DEBUG_WALKABLE:
            floor = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            pygame.draw.polygon(floor, (90, 235, 125, 80), room.walkable_polygon)
            pygame.draw.polygon(floor, (140, 255, 170, 160), room.walkable_polygon, 3)
            surface.blit(floor, (0, 0))
        return
    if getattr(room, "bg_key", "") == "final_core_stage":
        if DEBUG_WALKABLE:
            floor = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            pygame.draw.polygon(floor, (190, 95, 255, 70), room.walkable_polygon)
            pygame.draw.polygon(floor, (230, 160, 255, 160), room.walkable_polygon, 3)
            surface.blit(floor, (0, 0))
        return
    return _ORIGINAL_FINAL_GAME_DRAW_WORLD_COMBAT_FLOOR(self, surface, room)
Game.draw_world_combat_floor = _final_game_draw_world_combat_floor

_ORIGINAL_FINAL_GAME_ENTER_FLOOR = Game.enter_floor
def _final_game_enter_floor(self, floor):
    _ORIGINAL_FINAL_GAME_ENTER_FLOOR(self, floor)
    if getattr(self.current_room, "bg_key", "") in ("forest_guardian_stage", "final_core_stage"):
        start = pygame.Vector2(self.current_room.world_width * 0.50, self.current_room.floor_bottom_y - 105)
        self.player.pos = clamp_point_to_polygon(start, self.current_room.walkable_polygon, self.player.radius)
        if getattr(self.current_room, "boss", None):
            self.current_room.boss.set_arena(self.current_room.arena_rect, self.current_room.walkable_polygon, self.current_room.floor_top_y, self.current_room.floor_bottom_y)
        self.camera.reset(self.player.pos, self.current_room.world_width, self.current_room.world_height, self.current_room)
    if self.current_room and self.current_room.room_type in (ROOM_BOSS, ROOM_FINAL):
        self.announcement_timer = 0.0
        if not self.room_started:
            self.current_room.setup()
            self.current_room.reward_processed = False
            self.room_started = True
            self.player.invuln = max(self.player.invuln, 0.18)
        if getattr(self.current_room, "boss", None):
            boss = self.current_room.boss
            boss.pattern_cd = min(getattr(boss, "pattern_cd", 0.0), 0.18)
            if hasattr(boss, "liger_roar_opening"):
                boss.liger_roar_opening = min(getattr(boss, "liger_roar_opening", 0.0), 0.08)
            if hasattr(boss, "ice_dragon_state_timer") and getattr(boss, "ice_dragon_ai_state", "") == "idle":
                boss.ice_dragon_state_timer = 0.0
        self.message_timer = min(self.message_timer, 0.15)
Game.enter_floor = _final_game_enter_floor

def _draw_fixed_boss_hp_overlay(game):
    room = getattr(game, "current_room", None)
    boss = getattr(room, "boss", None) if room else None
    if not boss or boss.dead or boss.floor not in (ICE_DRAGON_FLOOR, INFERNO_LIGER_FLOOR, FOREST_GUARDIAN_FLOOR, FINAL_CORE_PATTERN_FLOOR):
        return
    color = boss.color
    if boss.floor == ICE_DRAGON_FLOOR:
        title = "16F Boss - Ice Dragon"
    elif boss.floor == INFERNO_LIGER_FLOOR:
        title = "11F Boss - LIGER-X11"
    elif boss.floor == FOREST_GUARDIAN_FLOOR:
        title = "6F Boss - Forest Guardian"
    else:
        title = "1F Final Boss - Final Core"
    hp_text = f"HP {max(0, int(boss.hp))} / {boss.max_hp}"
    panel = pygame.Rect(WIDTH // 2 - 285, 78, 570, 58)
    overlay = pygame.Surface(panel.size, pygame.SRCALPHA)
    pygame.draw.rect(overlay, (0, 0, 0, 178), overlay.get_rect(), border_radius=8)
    pygame.draw.rect(overlay, (*color, 230), overlay.get_rect(), 2, border_radius=8)
    game.screen.blit(overlay, panel.topleft)
    draw_text(game.screen, game.font, title, WIDTH // 2, panel.y + 7, WHITE, center=True)
    draw_bar(game.screen, panel.x + 25, panel.y + 31, panel.width - 50, 14, boss.hp, boss.max_hp, color)
    draw_text(game.screen, game.font_sm, hp_text, WIDTH // 2, panel.y + 46, WHITE, center=True)

_ORIGINAL_FINAL_DRAW_PLAYING = Game.draw_playing
def _final_draw_playing(self):
    _ORIGINAL_FINAL_DRAW_PLAYING(self)
    _draw_fixed_boss_hp_overlay(self)
Game.draw_playing = _final_draw_playing

_ORIGINAL_FINAL_ROOM_UPDATE = Room.update
def _final_room_update(self, dt, player, sounds):
    was_boss_alive = bool(getattr(self, "boss", None) and not self.boss.dead)
    result = _ORIGINAL_FINAL_ROOM_UPDATE(self, dt, player, sounds)
    if self.boss and self.boss.floor == ICE_DRAGON_FLOOR:
        if not getattr(self.boss, "ready_to_clear", False):
            self.cleared = False
        elif self.boss.dead:
            self.cleared = True
    if was_boss_alive and self.boss and self.boss.dead:
        self.boss.warning_lines = []
        self.boss.warning_attacks.clear()
        if hasattr(self.boss, "floor15_summon_queue"):
            self.boss.floor15_summon_queue.clear()
        if hasattr(self.boss, "active_tornadoes"):
            self.boss.active_tornadoes.clear()
        self.projectiles = [p for p in self.projectiles if getattr(p, "owner", None) != "enemy"]
    return result
Room.update = _final_room_update

_ORIGINAL_FINAL_ROOM_DRAW_ENTITIES = Room.draw_entities
def _final_room_draw_entities(self, surface, font, player=None):
    draw_boss = boss_should_draw_after_death_state(self.boss)
    large_fixed_boss = draw_boss and self.boss and self.boss.floor in (ICE_DRAGON_FLOOR, FOREST_GUARDIAN_FLOOR)
    if self.boss and self.boss.floor == FOREST_GUARDIAN_FLOOR and not draw_boss:
        if player:
            draw_lumizone_aura(surface, player)
        for trap in self.traps:
            trap.draw(surface)
        for projectile in self.projectiles:
            projectile.draw(surface)
        actors = []
        for enemy in self.enemies:
            actors.append((enemy.pos.y, enemy.draw))
        if player:
            for pet in player.pets:
                actors.append((pet.pos.y, pet.draw))
            actors.append((player.pos.y, player.draw))
        for _, draw_actor in sorted(actors, key=lambda item: item[0]):
            draw_actor(surface)
        for effect in self.effects:
            effect.draw(surface)
        return
    if not large_fixed_boss:
        return _ORIGINAL_FINAL_ROOM_DRAW_ENTITIES(self, surface, font, player)
    if player:
        draw_lumizone_aura(surface, player)
    self.boss.draw(surface, font)
    if hasattr(self.boss, "draw_warnings"):
        self.boss.draw_warnings(surface)
    for trap in self.traps:
        trap.draw(surface)
    for projectile in self.projectiles:
        projectile.draw(surface)
    actors = []
    for enemy in self.enemies:
        actors.append((enemy.pos.y, enemy.draw))
    if player:
        for pet in player.pets:
            actors.append((pet.pos.y, pet.draw))
        actors.append((player.pos.y, player.draw))
    for _, draw_actor in sorted(actors, key=lambda item: item[0]):
        draw_actor(surface)
    for effect in self.effects:
        effect.draw(surface)
Room.draw_entities = _final_room_draw_entities

def _balanced_lower_floor_enemy_level(floor, level):
    level_map = {10: 6, 9: 7, 8: 8, 7: 9, 5: 6, 4: 7, 3: 8, 2: 9}
    return level_map.get(floor, level)

_ORIGINAL_FINAL_ENEMY_INIT = Enemy.__init__
def _final_enemy_init(self, enemy_type, x, y, level=1, zone_key="20_16", floor=None):
    if floor is not None:
        level = _balanced_lower_floor_enemy_level(floor, level)
    _ORIGINAL_FINAL_ENEMY_INIT(self, enemy_type, x, y, level, zone_key, floor)
Enemy.__init__ = _final_enemy_init

_ORIGINAL_TRUE_END_DRAW_END_SCREEN = Game.draw_end_screen
def _true_end_draw_end_screen(self, title, subtitle, color):
    if self.state == "win":
        if not getattr(self, "ending_image", None):
            self.ending_image = self.load_ending_image()
        if getattr(self, "ending_image", None):
            self.screen.blit(self.ending_image, (0, 0))
            return
    return _ORIGINAL_TRUE_END_DRAW_END_SCREEN(self, title, subtitle, color)
Game.draw_end_screen = _true_end_draw_end_screen

if __name__ == "__main__":
    Game().run()
