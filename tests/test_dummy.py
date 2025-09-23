import pytest


def test_pass_1():
    assert True


def test_pass_2():
    assert 1 == 1


def test_pass_3():
    assert "a".upper() == "A"


def test_pass_4():
    assert [1, 2, 3][0] == 1


def test_pass_5():
    assert 5 > 2


def test_pass_6():
    assert True is not False


def test_pass_7():
    assert len("test") == 4


def test_pass_8():
    assert 10 / 2 == 5


def test_pass_9():
    assert isinstance({}, dict)


def test_pass_10():
    assert sum([1, 2, 3]) == 6


def test_fail_1():
    assert False


def test_fail_2():
    assert 1 == 2


def test_fail_3():
    assert "a".upper() == "a"


def test_fail_4():
    assert [1, 2, 3][0] == 2


def test_fail_5():
    assert 5 < 2


def test_skip_1():
    pytest.skip("skipping test 1")


def test_skip_2():
    pytest.skip("skipping test 2")


def test_skip_3():
    pytest.skip("skipping test 3")


def test_skip_4():
    pytest.skip("skipping test 4")


def test_skip_5():
    pytest.skip("skipping test 5")
