import math

from hypothesis import given, strategies as st
from customs_duty import parse_declaration, duty_amount, hs_chapter


# Valid-looking inputs, used to check the functions still give correct answers
categories = st.text(alphabet=st.characters(min_codepoint=97, max_codepoint=122),
                     min_size=1, max_size=15)
amounts = st.floats(min_value=0, max_value=1e9, allow_nan=False)
rates = st.floats(min_value=0, max_value=100, allow_nan=False)


# Fuzz tests: no input may crash the functions

@given(st.text() | st.none())
def test_parse_declaration_no_crash(s):
    try:
        parse_declaration(s)
    except Exception as e:
        assert False, f"parse_declaration crashed with: {e}"


@given(st.text() | st.none())
def test_duty_amount_no_crash(s):
    try:
        duty_amount(s)
    except Exception as e:
        assert False, f"duty_amount crashed with: {e}"


@given(st.text() | st.none())
def test_hs_chapter_no_crash(s):
    try:
        hs_chapter(s)
    except Exception as e:
        assert False, f"hs_chapter crashed with: {e}"


# Fuzz tests on structured inputs that look valid but hide edge cases

@given(st.text(), st.text())
def test_parse_declaration_any_parts_no_crash(category, value):
    try:
        parse_declaration(f"{category}:{value}")
    except Exception as e:
        assert False, f"parse_declaration crashed with: {e}"


@given(st.builds("{}@{}".format, st.floats(), st.floats()) | st.text())
def test_duty_amount_is_never_negative_or_nan(s):
    try:
        result = duty_amount(s)
    except Exception:
        return  # crashes are reported by test_duty_amount_no_crash
    assert result is None or (math.isfinite(result) and result >= 0)


@given(st.text())
def test_hs_chapter_is_a_real_chapter(s):
    try:
        result = hs_chapter(s)
    except Exception:
        return  # crashes are reported by test_hs_chapter_no_crash
    assert result is None or 1 <= result <= 97


# Property tests: valid inputs still give the right answer

@given(categories, amounts)
def test_parse_declaration_valid(category, value):
    assert parse_declaration(f" {category.upper()} :{value}") == (category, value)


@given(amounts, rates)
def test_duty_amount_valid(value, rate):
    assert math.isclose(duty_amount(f"{value}@{rate}"), value * rate / 100,
                        rel_tol=1e-9, abs_tol=1e-9)


@given(st.integers(min_value=1, max_value=97), st.integers(min_value=0, max_value=9999))
def test_hs_chapter_valid(chapter, rest):
    assert hs_chapter(f"{chapter:02d}{rest // 100:02d}.{rest % 100:02d}") == chapter
