import multidict
import pytest
from typing import Any

pytest.importorskip("multidict._multidict")
testcapi = pytest.importorskip("testcapi")

pytestmark = pytest.mark.capi

MultiDictStr = multidict.MultiDict[str]


@pytest.fixture(scope="module", params=["capi", "cyapi"])
def capi(request: pytest.FixtureRequest) -> Any:
    return getattr(testcapi, request.param)


def test_md_new(capi: Any) -> None:
    md = capi.md_new(0)
    assert isinstance(md, multidict.MultiDict)
    assert len(md) == 0


def test_md_type(capi: Any) -> None:
    assert capi.md_type() is multidict.MultiDict


def test_md_add(capi: Any) -> None:
    md: MultiDictStr = multidict.MultiDict()
    capi.md_add(md, "key", "value")
    assert len(md) == 1
    assert list(md.items()) == [("key", "value")]


def test_md_clear(capi: Any) -> None:
    md: MultiDictStr = multidict.MultiDict(key="val")
    capi.md_clear(md)
    assert len(md) == 0


@pytest.mark.parametrize(
    "key, expected",
    [
        pytest.param("key", ("val", True), id="found"),
        pytest.param("key2", ("default", False), id="notfound"),
    ],
)
def test_md_setdefault(capi: Any, key: str, expected: tuple[str, bool]) -> None:
    md: MultiDictStr = multidict.MultiDict(key="val")
    ret = capi.md_setdefault(md, key, "default")
    assert ret == expected
