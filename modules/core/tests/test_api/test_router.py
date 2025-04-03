from core.api.router import foo


def test_foo() -> None:
    assert foo() == "worked"
