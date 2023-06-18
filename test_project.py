from project import get_jpy_price, get_usd_price, bm_index_calculator, price_varience, off_ex_rate, calc

def test_get_jpy_price():
    assert get_jpy_price() == 450


def test_get_usd_price():
    assert get_usd_price() == 5.15


def test_bm_index_calculator():
    assert bm_index_calculator(450, 5.15) == 87


def test_price_varience():
    assert price_varience(139, 88) == "58%"


def test_off_ex_rate():
    assert type(off_ex_rate()) == int


def test_calc():
    assert calc(1000, 87) == 11