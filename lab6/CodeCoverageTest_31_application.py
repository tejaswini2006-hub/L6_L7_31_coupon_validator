
import pytest
from coupon_validator import coupon_discount, best_discount, is_expired


def test_welcome_coupon_new_user():
    assert coupon_discount("WELCOME10", 200, True, "mon") == 20


def test_welcome_coupon_existing_user():
    assert coupon_discount("WELCOME10", 200, False, "mon") == 0


def test_empty_cart():
    with pytest.raises(ValueError, match="empty cart"):
        coupon_discount("WELCOME10", 0, True, "mon")


def test_weekend_coupon_large_cart():
    assert coupon_discount("WEEKEND20", 500, True, "sat") == 100


def test_weekend_coupon_small_cart():
    assert coupon_discount("WEEKEND20", 200, False, "sun") == 50


def test_weekend_coupon_weekday():
    assert coupon_discount("WEEKEND20", 500, True, "mon") == 0


def test_flat_coupon_eligible_cart():
    assert coupon_discount("FLAT100", 400, False, "mon") == 100


def test_flat_coupon_ineligible_cart():
    assert coupon_discount("FLAT100", 300, False, "mon") == 0


def test_unknown_coupon():
    assert coupon_discount("INVALID", 200, False, "mon") == 0


def test_best_discount_selects_highest():
    assert best_discount(
        ["WELCOME10", "FLAT100"], 500, True, "mon"
    ) == 100


def test_best_discount_applies_cap():
    assert best_discount(["WEEKEND20"], 100, False, "sat") == 40


def test_best_discount_empty_list():
    assert best_discount([], 200, False, "mon") == 0


def test_coupon_expired():
    assert is_expired(20, 5, 10) is True


def test_coupon_not_expired():
    assert is_expired(10, 5, 10) is False
