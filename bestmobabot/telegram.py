from __future__ import annotations

from contextlib import AbstractContextManager
from http import HTTPStatus
from typing import Any, List, Optional

from loguru import logger
from requests import Session

from bestmobabot import constants
from bestmobabot.settings import TelegramSettings


class Telegram:
    def __init__(self, session: Session, settings: TelegramSettings):
        self.session = session
        self.token = settings.token
        self.chat_id = settings.chat_id

    def send_message(self, text: str) -> int:
        return self.call(
            'sendMessage',
            chat_id=self.chat_id,
            text=text,
            parse_mode='Markdown',
        )['message_id']

    def pin_chat_message(self, message_id: int) -> bool:
        # FIXME
        return self.call('pinChatMessage', chat_id=self.chat_id, message_id=message_id)

    def call(self, method: str, **kwargs: Any) -> Any:
        response = self.session.post(
            f'https://api.telegram.org/bot{self.token}/{method}',
            json=kwargs,
            timeout=constants.API_TIMEOUT,
        )
        if response.status_code != HTTPStatus.OK:
            raise TelegramException(response.text)
        result = response.json()
        if not result.get('ok'):
            raise TelegramException(result.get('description'))
        return result['result']


class TelegramLogger(AbstractContextManager):
    def __init__(self, telegram: Optional[Telegram]):
        self.telegram = telegram
        self.lines: List[str] = []

    def __enter__(self) -> TelegramLogger:
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.flush()

    def append(self, *lines: str) -> TelegramLogger:
        if self.telegram:
            self.lines.extend(lines)
        return self

    def flush(self, pin=False) -> TelegramLogger:
        if not self.telegram or not self.lines:
            return self
        try:
            message_id = self.telegram.send_message('\n'.join(self.lines))
            if pin:
                self.telegram.pin_chat_message(message_id)
        except Exception as e:
            logger.warning('Telegram API error: {}', e)
        self.lines.clear()
        return self


class TelegramException(Exception):
    """
    Raised when Telegram API call has failed.
    """
