import pytest

from memory.interfaces import MemoryStore


def test_memory_store_is_abstract():
    with pytest.raises(TypeError):
        MemoryStore()


def test_memory_store_exposes_get():
    assert hasattr(MemoryStore, "get")


def test_memory_store_exposes_set():
    assert hasattr(MemoryStore, "set")


def test_memory_store_exposes_delete():
    assert hasattr(MemoryStore, "delete")
