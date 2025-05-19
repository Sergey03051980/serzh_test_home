"""
Модуль для маскировки банковских карт и счетов
"""
from .masks import get_mask_account, get_mask_card_number

__all__ = ["get_mask_card_number", "get_mask_account"]
