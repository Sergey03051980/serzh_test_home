from src.masks import get_mask_card_number, get_mask_account

print(get_mask_card_number("1234567890123456"))  # 1234 56** **** 3456
print(get_mask_account("1234567890"))           # **7890
