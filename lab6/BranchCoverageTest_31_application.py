import pytest
import coupon_validator
from coupon_validator import coupon_discount, best_discount, is_expired


def test_empty_cart():
    with pytest.raises(ValueError, match="empty cart"):
        coupon_discount("WELCOME10", 0, True, "mon")


def test_welcome_new_user():
    assert coupon_discount("WELCOME10", 200, True, "mon") == 20


def test_welcome_existing_user():
    assert coupon_discount("WELCOME10", 200, False, "mon") == 0


def test_weekend_large_cart():
    assert coupon_discount("WEEKEND20", 600, True, "sat") == 120


def test_weekend_small_cart():
    assert coupon_discount("WEEKEND20", 200, True, "sun") == 50


def test_weekend_weekday():
    assert coupon_discount("WEEKEND20", 600, True, "mon") == 0


def test_flat_large_cart():
    assert coupon_discount("FLAT100", 400, True, "mon") == 100


def test_flat_at_threshold():
    assert coupon_discount("FLAT100", 300, True, "mon") == 0


def test_unknown_coupon():
    assert coupon_discount("INVALID", 500, True, "mon") == 0


def test_best_discount_empty_list():
    assert best_discount([], 500, True, "sat") == 0


def test_best_discount_highest_value():
    assert best_discount(
        ["WELCOME10", "WEEKEND20"], 600, True, "sat"
    ) == 120


def test_best_discount_zero_value():
    assert best_discount(["INVALID"], 500, True, "mon") == 0


def test_best_discount_cap(monkeypatch):
    monkeypatch.setattr(
        coupon_validator, "coupon_discount", lambda *args: 500
    )
    assert best_discount(["TEST"], 500, True, "mon") == 200


def test_zero_validity():
    assert is_expired(10, 5, 0) is True


def test_negative_validity():
    assert is_expired(10, 5, -1) is True


def test_not_expired():
    assert is_expired(10, 5, 5) is False


def test_expired():
    assert is_expired(11, 5, 5) is True