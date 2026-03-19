"""Database configuration tests."""

from src.config.database import get_db_session


def test_get_db_session_yields_session():
    """get_db_session should yield and close a session."""
    generator = get_db_session()
    session = next(generator)

    assert session is not None

    try:
        next(generator)
    except StopIteration:
        pass
