from memory.memory import load_memory, save_memory
from memory.manager import MemoryManager


def test_load_memory_has_canonical_schema():
    data = load_memory()

    assert isinstance(data, dict)
    assert data["schema_version"] == "0.2.0"
    assert isinstance(data["data"], dict)


def test_canonical_categories_exist():
    data = load_memory()

    memory = data["data"]

    assert "profile" in memory
    assert "preferences" in memory
    assert "facts" in memory
    assert "conversation" in memory
    assert "tasks" in memory
    assert "system" in memory


def test_memory_manager_set_and_get():
    manager = MemoryManager()

    assert manager.set(
        "profile",
        "test_name",
        "NOVA_TEST_USER",
    )

    assert manager.get(
        "profile",
        "test_name",
    ) == "NOVA_TEST_USER"


def test_memory_manager_has():
    manager = MemoryManager()

    manager.set(
        "profile",
        "test_has",
        True,
    )

    assert manager.has(
        "profile",
        "test_has",
    )


def test_memory_manager_get_category():
    manager = MemoryManager()

    manager.set(
        "profile",
        "test_category",
        "value",
    )

    profile = manager.get_category("profile")

    assert isinstance(profile, dict)
    assert profile["test_category"] == "value"


def test_memory_manager_delete():
    manager = MemoryManager()

    manager.set(
        "profile",
        "test_delete",
        "temporary",
    )

    assert manager.has(
        "profile",
        "test_delete",
    )

    assert manager.delete(
        "profile",
        "test_delete",
    )

    assert not manager.has(
        "profile",
        "test_delete",
    )


def test_memory_manager_missing_value():
    manager = MemoryManager()

    assert manager.get(
        "profile",
        "does_not_exist",
    ) is None


def test_memory_manager_default_value():
    manager = MemoryManager()

    assert manager.get(
        "profile",
        "does_not_exist",
        "DEFAULT",
    ) == "DEFAULT"


def test_memory_manager_invalid_set():
    manager = MemoryManager()

    assert not manager.set(
        "",
        "test",
        "value",
    )

    assert not manager.set(
        "profile",
        "",
        "value",
    )