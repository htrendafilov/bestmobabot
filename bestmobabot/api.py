"""
Game API wrapper.
"""

import hashlib
import json
import random
import re
import string
from datetime import datetime
from time import sleep, time
from typing import Any, Dict, Iterable, List, Optional, Tuple, Type, TypeVar, Union

from bs4 import BeautifulSoup, Tag
from loguru import logger
from pydantic import BaseModel
from requests import Session

from bestmobabot import constants
from bestmobabot.database import Database
from bestmobabot.dataclasses_ import (
    ArenaEnemy,
    ArenaResult,
    Boss,
    Expedition,
    GrandArenaEnemy,
    HallOfFame,
    Hero,
    Letter,
    Mission,
    Offer,
    Quest,
    Quests,
    Replay,
    Result,
    Reward,
    ShopSlot,
    Tower,
    User,
)
from bestmobabot.enums import BattleType
from bestmobabot.settings import Settings


class APIError(Exception):
    """
    General API error.
    """


class AlreadyError(APIError):
    """
    Raised when something, for instance a quest, is already done.
    """


class InvalidSessionError(APIError):
    """
    Raised when session is expired.
    """


class NotEnoughError(APIError):
    """
    Raised when not enough resources.
    """


class NotAvailableError(APIError):
    pass


class NotFoundError(APIError):
    pass


class ArgumentError(APIError):
    """
    Raised when there is an invalid argument in API request.
    """


class InvalidBattleError(APIError):
    """
    Raised when invalid battle result is submitted.
    """


class OutOfRetargetDelta(APIError):
    pass


class InvalidSignatureError(APIError):
    """
    Raised when invalid request signature is provided.
    Usually, this happens when session is expired.
    """


class API:
    GAME_URL = 'https://hero-wars.com/'
    API_URL = 'https://heroes-wb.nextersglobal.com/api/'

    auth_token: str
    user_id: str
    player_id: str
    request_id: int
    session_id: str

    def __init__(self, session: Session, db: Database, settings: Settings):
        self.session = session
        self.db = db
        self.settings = settings

        # Store last API results for debugging.
        self.last_responses: List[str] = []

    def prepare(self, invalidate_session: bool = False):
        if not invalidate_session:
            try:
                state: Dict[str, Any] = self.db[f'api:{self.settings.web.email}:state']
            except KeyError:
                logger.info('Previously saved state is missing.')
            else:
                logger.info('Using saved credentials.')
                self.user_id = state['user_id']
                self.auth_token = state['auth_token']
                self.session_id = state['session_id']
                try:
                    self.request_id = self.db[f'api:{self.settings.web.email}:request_id']
                except KeyError:
                    self.request_id = 0
                return

        #self.authenticate_hw_web()

        logger.debug('Logging into Hero-Wars.com…')
        with self.session.get(self.GAME_URL, timeout=constants.API_TIMEOUT) as response:
            response.raise_for_status()

        headers = {
            'Content-Type': 'application/json'
        }
        with self.session.post(self.GAME_URL+'login', headers=headers, data='{"email":"hriditr@pm.me","password":"Hw#896745","remember":1}', timeout=constants.API_TIMEOUT) as response:
            logger.info('Status: {} {}.', response.status_code, response.url)
            response.raise_for_status()

        with self.session.get(self.GAME_URL, timeout=constants.API_TIMEOUT) as response:
            response.raise_for_status()
            print(response.text)
            app_page = response.text



        # Look for params variable in the script.
        match = re.search(r'window.NXFlashVars\s?=\s?({[^\}]+\})', app_page)
        assert match, 'NXFlashVars not found'
        flashvars=match.groups(1)

        self.auth_token = self.get_var('auth_key', flashvars[0])
        logger.debug('Authentication token: {}', self.auth_token)
        self.user_id = str(self.get_var('uid', flashvars[0]))
        self.session_id = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(14))
        self.request_id = 0

        self.db[f'api:{self.settings.web.email}:state'] = {
            'user_id': self.user_id,
            'auth_token': self.auth_token,
            'session_id': self.session_id,
        }

    def get_var(self, key, string):
        key = re.search(rf"{key}\s*:\s*'?([a-zA-Z0-9-+/.]+)'?,", string)
        assert key, f"variable not found for key: {key}"
        return key.group(1)

    def call(
            self,
            name: str,
            arguments: Optional[Dict[str, Any]] = None,
            random_sleep=True,
            log_result=False,
    ) -> Result:
        # TODO: perhaps, accept a return response type and return a typed response.
        try:
            return self._call(name, arguments=arguments, random_sleep=random_sleep, log_result=log_result)
        except (InvalidSessionError, InvalidSignatureError) as e:
            logger.warning('Invalid session: {}.', e)
            self.prepare(invalidate_session=True)
            logger.info('Retrying the call…')
            return self._call(name, arguments=arguments, random_sleep=random_sleep, log_result=log_result)

    def _call(self, name: str, *, arguments: Optional[Dict[str, Any]], random_sleep, log_result) -> Result:
        self.request_id += 1
        self.db[f'api:{self.settings.web.email}:request_id'] = self.request_id

        # Emulate human behavior a little.
        sleep_time = random.uniform(5.0, 10.0) if random_sleep and self.request_id != 1 else 0.0
        logger.info(f'#{self.request_id}: {name}({arguments or {} }) in {sleep_time:.1f} seconds…')
        sleep(sleep_time)

        calls = [{'ident': name, 'name': name, 'args': arguments or {}}]
        data = json.dumps({"session": None, "calls": calls})
        headers = {
            'X-Auth-Application-Id': '3',
            'X-Auth-Network-Ident': 'web',
            'X-Auth-Player-Id': self.player_id,
            'X-Auth-Session-Id': self.session_id,
            'X-Auth-Session-Key': '',
            'X-Auth-Token': self.auth_token,
            'X-Auth-User-Id': self.user_id,
            'X-Env-Library-Version': '1',
            'X-Request-Id': str(self.request_id),
            'X-Requested-With': 'XMLHttpRequest',
            'X-Server-Time': f'{time():.3f}',
        }
        if self.request_id == 1:
            headers['X-Auth-Session-Init'] = '1'
        headers["X-Auth-Signature"] = self.sign_request(data, headers)

        # API developers are very funny people…
        # They return errors in a bunch of different ways. 🤦

        with self.session.post(self.API_URL, data=data, headers=headers, timeout=constants.API_TIMEOUT) as response:
            self.last_responses.append(response.text.strip())
            logger.trace(f'#{self.request_id}: status {response.status_code}.')
            response.raise_for_status()
            try:
                item = response.json()
            except ValueError:
                if response.text == 'Invalid signature':
                    raise InvalidSignatureError(response.text)
                raise APIError(response.text)

        if 'results' in item:
            result = Result.parse_obj(item['results'][0]['result'])
            if result.is_error:
                raise self.make_exception(result.response['error'])
            if log_result:
                logger.debug('Result: {}', result.response)
            return result
        if 'error' in item:
            raise self.make_exception(item['error'])
        raise ValueError(item)

    @staticmethod
    def sign_request(data: str, headers: dict) -> str:
        fingerprint = ''.join(
            f'{key}={value}'
            for key, value in sorted(
                (key[6:].upper(), value)
                for key, value in headers.items()
                if key.startswith('X-Env')
            )
        )
        data = ':'.join((
            headers['X-Request-Id'],
            headers['X-Auth-Token'],
            headers['X-Auth-Session-Id'],
            data,
            fingerprint,
        )).encode('utf-8')
        return hashlib.md5(data).hexdigest()

    exception_classes = {
        'Already': AlreadyError,
        'ArgumentError': ArgumentError,
        'common\\rpc\\exception\\InvalidSession': InvalidSessionError,
        'Invalid battle': InvalidBattleError,
        'NotAvailable': NotAvailableError,
        'NotEnough': NotEnoughError,
        'NotFound': NotFoundError,
        'outOfRetargetDelta': OutOfRetargetDelta,
    }

    @classmethod
    def make_exception(cls, error: Union[Dict, str]) -> APIError:
        if isinstance(error, dict):
            name = error.get('name')
            return cls.exception_classes.get(name, APIError)(error)
        if isinstance(error, str):
            return cls.exception_classes.get(error, APIError)(error)
        return APIError(error)

    # User.
    # ------------------------------------------------------------------------------------------------------------------

    def register(self):
        self.call('registration', {'user': {'referrer': {'type': 'menu', 'id': '0'}}})

    def get_user_info(self) -> User:
        return User.parse_obj(self.call('userGetInfo').response)

    def get_all_heroes(self, random_sleep=True) -> List[Hero]:
        return list_of(Hero, self.call('heroGetAll', random_sleep=random_sleep).response)

    # Daily bonus.
    # ------------------------------------------------------------------------------------------------------------------

    def farm_daily_bonus(self, vip) -> Reward:
        return Reward.parse_obj(self.call('dailyBonusFarm', {'vip': vip}).response)

    # Expeditions.
    # ------------------------------------------------------------------------------------------------------------------

    def list_expeditions(self) -> List[Expedition]:
        return list_of(Expedition, self.call('expeditionGet').response)

    def farm_expedition(self, expedition_id: str) -> Reward:
        return Reward.parse_obj(self.call('expeditionFarm', {'expeditionId': expedition_id}).response['reward'])

    def send_expedition_heroes(self, expedition_id: str, hero_ids: List[str]) -> Tuple[datetime, Quests]:
        response = self.call('expeditionSendHeroes', {'expeditionId': expedition_id, 'heroes': hero_ids})
        return datetime.fromtimestamp(response.response['endTime']).astimezone(), response.quests

    # Quests.
    # ------------------------------------------------------------------------------------------------------------------

    def get_all_quests(self) -> Quests:
        return list_of(Quest, self.call('questGetAll').response)

    def farm_quest(self, quest_id: str) -> Reward:
        return Reward.parse_obj(self.call('questFarm', {'questId': quest_id}).response)

    # Mail.
    # ------------------------------------------------------------------------------------------------------------------

    def get_all_mail(self) -> List[Letter]:
        return list_of(Letter, self.call('mailGetAll').response['letters'])

    def farm_mail(self, letter_ids: Iterable[str]) -> Dict[str, Reward]:
        result = self.call('mailFarm', {'letterIds': list(letter_ids)})
        return {letter_id: Reward.parse_obj(item or {}) for letter_id, item in result.response.items()}

    # Chests.
    # ------------------------------------------------------------------------------------------------------------------

    def buy_chest(self, is_free=True, chest='town', is_pack=False) -> List[Reward]:
        result = self.call('chestBuy', {'free': is_free, 'chest': chest, 'pack': is_pack})
        return list_of(Reward, result.response['rewards'])

    # Daily gift.
    # ------------------------------------------------------------------------------------------------------------------

    def send_daily_gift(self) -> Quests:
        return self.call('clanSendDailyGifts').quests

    def get_clan_available_gifts(self):
        result = self.call('clanGetAvailableDailyGifts')
        return result.response['giftUids']

    # Arena.
    # ------------------------------------------------------------------------------------------------------------------

    def find_arena_enemies(self) -> List[ArenaEnemy]:
        return list_of(ArenaEnemy, self.call('arenaFindEnemies').response)

    def attack_arena(self, user_id: str, hero_ids: Iterable[str]) -> Tuple[ArenaResult, Quests]:
        result = self.call('arenaAttack', {'userId': user_id, 'heroes': list(hero_ids)})
        return ArenaResult.parse_obj(result.response), result.quests

    def find_grand_enemies(self) -> List[GrandArenaEnemy]:
        # Random sleep is turned off because model prediction takes some time already.
        return list_of(GrandArenaEnemy, self.call('grandFindEnemies', random_sleep=False).response)

    def attack_grand(self, user_id: str, hero_ids: List[List[str]]) -> Tuple[ArenaResult, Quests]:
        result = self.call('grandAttack', {'userId': user_id, 'heroes': hero_ids})
        return ArenaResult.parse_obj(result.response), result.quests

    def farm_grand_coins(self) -> Reward:
        return Reward.parse_obj(self.call('grandFarmCoins').response['reward'] or {})

    def set_grand_heroes(self, hero_ids: List[List[str]]):
        self.call('grandSetHeroes', {'heroes': hero_ids})

    # Freebie.
    # ------------------------------------------------------------------------------------------------------------------

    def check_freebie(self, gift_id: str) -> Optional[Reward]:
        response = self.call('freebieCheck', {'giftId': gift_id}).response
        return Reward.parse_obj(response) if response else None

    # Zeppelin gift.
    # ------------------------------------------------------------------------------------------------------------------

    def farm_zeppelin_gift(self) -> Reward:
        return Reward.parse_obj(self.call('zeppelinGiftFarm').response)

    def farm_zeppelin_subscription(self) -> Reward:
        return Reward.parse_obj(self.call('subscriptionFarm').response)

    # Artifact chests.
    # ------------------------------------------------------------------------------------------------------------------

    def open_artifact_chest(self, amount=1, is_free=True) -> List[Reward]:
        response = self.call('artifactChestOpen', {'amount': amount, 'free': is_free}).response
        return list_of(Reward, response['chestReward'])

    # Battles.
    # ------------------------------------------------------------------------------------------------------------------

    def get_battle_by_type(self, battle_type: BattleType, offset=0, limit=20) -> List[Replay]:
        response = self.call('battleGetByType', {'type': battle_type.value, 'offset': offset, 'limit': limit}).response
        return list_of(Replay, response['replays'])

    # Missions.
    # https://github.com/eigenein/bestmobabot/wiki/Raids
    # ------------------------------------------------------------------------------------------------------------------

    def raid_mission(self, mission_id: str, times=1) -> List[Reward]:
        response = self.call('missionRaid', {'times': times, 'id': mission_id}).response
        return list_of(Reward, response)

    def get_all_missions(self) -> List[Mission]:
        return list_of(Mission, self.call('missionGetAll').response)

    # Boss.
    # https://github.com/eigenein/bestmobabot/wiki/Boss
    # ------------------------------------------------------------------------------------------------------------------

    def get_all_bosses(self) -> List[Boss]:
        return list_of(Boss, self.call('bossGetAll').response)

    def raid_boss(self, boss_id: str) -> Reward:
        return Reward.parse_obj(self.call('bossRaid', {'bossId': boss_id}).response['everyWinReward'])

    def open_boss_chest(self, boss_id: str) -> Tuple[List[Reward], Quests]:
        result = self.call('bossOpenChest', {'bossId': boss_id, 'starmoney': 0, 'amount': 1})
        return list_of(Reward, result.response['rewards']['free']), result.quests

    # Shop.
    # ------------------------------------------------------------------------------------------------------------------

    def get_shop(self, shop_id: str) -> List[ShopSlot]:
        response = self.call('shopGet', {'shopId': shop_id}).response
        return list_of(ShopSlot, response['slots'])

    def shop(self, *, slot_id: str, shop_id: str) -> Reward:
        return Reward.parse_obj(self.call('shopBuy', {'slot': slot_id, 'shopId': shop_id}).response)

    # Tower.
    # ------------------------------------------------------------------------------------------------------------------

    def get_tower_info(self) -> Tower:
        return Tower.parse_obj(self.call('towerGetInfo').response)

    def skip_tower_floor(self) -> Tuple[Tower, Reward]:
        response = self.call('towerSkipFloor').response
        return Tower.parse_obj(response['tower']), Reward.parse_obj(response['reward'])

    def buy_tower_buff(self, buff_id: int) -> Tower:
        return Tower.parse_obj(self.call('towerBuyBuff', {'buffId': buff_id}).response)

    def open_tower_chest(self, number: int) -> Tuple[Reward, Quests]:
        assert number in (0, 1, 2)
        result = self.call('towerOpenChest', {'num': number})
        return Reward.parse_obj(result.response['reward']), result.quests

    def next_tower_floor(self) -> Tower:
        return Tower.parse_obj(self.call('towerNextFloor').response)

    def next_tower_chest(self) -> Tower:
        return Tower.parse_obj(self.call('towerNextChest').response)

    def tower_getSkullReward(self) -> Reward:
        result = self.call('tower_getSkullReward', log_result=True)
        return Reward.parse_obj(self.call('tower_farmSkullReward', log_result=True).response)

    def tower_farmPointRewards(self) -> Reward:
        return Reward.parse_obj(
            self.call('tower_farmPointRewards', {"points":[200,3000,10000,15000,20000,25000,35000,45000,60000]}, log_result=True).response
        )

    # Offers.
    # ------------------------------------------------------------------------------------------------------------------

    def get_all_offers(self) -> List[Offer]:
        return list_of(Offer, self.call('offerGetAll').response)

    def farm_offer_reward(self, offer_id: str) -> Reward:
        return Reward.parse_obj(self.call('offerFarmReward', {'offerId': offer_id}).response)

    # Titans.
    # ------------------------------------------------------------------------------------------------------------------

    def open_titan_artifact_chest(self, amount: int, free: bool = True) -> Tuple[List[Reward], Quests]:
        result = self.call('titanArtifactChestOpen', {'amount': amount, 'free': free})
        return list_of(Reward, result.response['reward']), result.quests

    # Hero Upgrade
    # ------------------------------------------------------------------------------------------------------------------
    def upgrade_hero_skill(
            self,
            hero_id: str,
            skill: str,
    ) -> Result:
        return self.call('heroUpgradeSkill', {
            'heroId': hero_id,
            'skill': skill
        }, log_result=True)

    def upgrade_hero_skin(
            self,
            hero_id: str,
            skinId: str,
    ) -> Result:
        return self.call('heroSkinUpgrade', {
            'heroId': hero_id,
            'skinId': skinId
        }, log_result=True)


    # Runes.
    # ------------------------------------------------------------------------------------------------------------------

    def enchant_hero_rune(
            self,
            hero_id: str,
            tier: str,
            consumables: Optional[Dict[str, int]] = None,
    ) -> Result:
        return self.call('heroEnchantRune', {
            'heroId': hero_id,
            'tier': tier,
            'items': {'consumable': consumables or {'1': 1}}},
                         )

    # Hero titan gifts
    # ------------------------------------------------------------------------------------------------------------------

    def level_up_titan_hero_gift(self, hero_id: str) -> Quests:
        return self.call('heroTitanGiftLevelUp', {'heroId': hero_id}).quests

    def drop_titan_hero_gift(self, hero_id: str) -> Tuple[Reward, Quests]:
        result = self.call('heroTitanGiftDrop', {'heroId': hero_id})
        return Reward.parse_obj(result.response), result.quests

    # Hall of Fame
    # ------------------------------------------------------------------------------------------------------------------

    def get_hall_of_fame(self) -> HallOfFame:
        return HallOfFame.parse_obj(self.call('hallOfFameGet').response)

    def farm_hall_of_fame_trophy_reward(self, trophy_id: str) -> Reward:
        return Reward.parse_obj(self.call('hallOfFameFarmTrophyReward', {
            'trophyId': trophy_id,
            'rewardType': 'champion',
        }).response)


TModel = TypeVar('TModel', bound=BaseModel)


def list_of(type_: Type[TModel], items: Iterable) -> List[TModel]:
    """
    Used to protect from changing a response from list to dictionary and vice versa.
    This often happens with the game updates.
    """
    if isinstance(items, dict):
        # Treat lists and dictionaries equally, because there're two possibilities in the responses:
        # 1. `[{"id": "1", ...}]`
        # 2. `{"1": {"id": "1"}, ...}`
        items = items.values()
    return [type_(**item) for item in items]
