import pytest
from felix.core.engine_components.health_component import Health


@pytest.fixture
def health_object() -> Health:
    return Health(1, 2, 75, 0, 100)


class TestHealth:
    def test_health(self, health_object: Health):
        with pytest.raises(ValueError):
            health_object.health = health_object.min_health - 1

        with pytest.raises(ValueError):
            health_object.health = health_object.max_health + 1

        with pytest.raises(ValueError):
            health_object.max_health = health_object.min_health - 1

        with pytest.raises(ValueError):
            health_object.min_health = health_object.max_health + 1

        health_object.health = health_object.max_health

        assert health_object.max_health == health_object.health

        health_object.health = health_object.min_health

        assert health_object.min_health == health_object.health
