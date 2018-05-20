"""
Logger initialisation.
"""

import logging
from typing import Iterable, TextIO

import coloredlogs

import bestmobabot.responses
from bestmobabot.constants import SPAM


logger = logging.getLogger('bestmobabot')
logging.addLevelName(SPAM, 'SPAM')


def get_logging_level(verbosity: int) -> int:
    if verbosity == 0:
        return logging.INFO
    if verbosity == 1:
        return logging.DEBUG
    return SPAM


def install_logging(logger: logging.Logger, verbosity: int, stream: TextIO):
    coloredlogs.install(
        get_logging_level(verbosity),
        fmt='%(asctime)s %(levelname)s %(message)s',
        logger=logger,
        stream=stream,
    )


def log_heroes(emoji: str, message: str, heroes: Iterable['bestmobabot.responses.Hero']):
    logger.info(f'{emoji} {message}')
    for hero in sorted(heroes, reverse=True, key=bestmobabot.responses.Hero.order):
        logger.info(f'{emoji} {hero}')


def log_reward(reward: 'bestmobabot.responses.Reward'):
    reward.log(logger)


def log_rewards(rewards: Iterable['bestmobabot.responses.Reward']):
    for reward in rewards:
        log_reward(reward)


def log_arena_result(result: 'bestmobabot.responses.ArenaResult'):
    logger.info('👍 You won!' if result.win else '👎 You lose.')
    for i, battle in enumerate(result.battles, start=1):
        logger.info(f'👊 Battle #{i}: {"⭐" * battle.stars if battle.win else "lose."}')
    log_reward(result.reward)
