import pytest

from parade.catalog import (
    CONSTELLATION_CATALOG,
    celestial_body_index,
    celestial_body_at,
    validate_celestial_body,
    catalog_size,
)


class TestConstellationCatalog:
    def test_catalog_has_27_bodies(self):
        assert catalog_size() == 27

    def test_catalog_contains_all_lowercase_letters(self):
        for c in "abcdefghijklmnopqrstuvwxyz":
            assert c in CONSTELLATION_CATALOG

    def test_catalog_contains_void(self):
        assert " " in CONSTELLATION_CATALOG

    def test_void_is_last_body(self):
        assert celestial_body_index(" ") == 26

    def test_index_of_first_body(self):
        assert celestial_body_index("a") == 0

    def test_index_of_last_letter(self):
        assert celestial_body_index("z") == 25

    def test_body_at_index_zero(self):
        assert celestial_body_at(0) == "a"

    def test_body_at_index_26(self):
        assert celestial_body_at(26) == " "

    def test_round_trip_all_bodies(self):
        for i in range(27):
            body = celestial_body_at(i)
            assert celestial_body_index(body) == i


class TestValidation:
    def test_valid_body_passes(self):
        validate_celestial_body("a")

    def test_void_passes(self):
        validate_celestial_body(" ")

    def test_uppercase_rejected(self):
        with pytest.raises(ValueError, match="Unknown celestial body"):
            validate_celestial_body("A")

    def test_digit_rejected(self):
        with pytest.raises(ValueError, match="Unknown celestial body"):
            validate_celestial_body("1")

    def test_empty_string_rejected(self):
        with pytest.raises(ValueError, match="Unknown celestial body"):
            validate_celestial_body("")

    def test_multi_char_rejected(self):
        with pytest.raises(ValueError, match="Unknown celestial body"):
            validate_celestial_body("ab")
