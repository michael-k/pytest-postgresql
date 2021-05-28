"""Test for NoopExecutor."""
from pytest_postgresql.executor import PostgreSQLExecutor
from pytest_postgresql.compat import psycopg2
from pytest_postgresql.executor_noop import NoopExecutor
from pytest_postgresql.retry import retry


def test_noproc_version(postgresql_proc: PostgreSQLExecutor) -> None:
    """
    Test the way postgresql version is being read.

    Version behaves differently for postgresql >= 10 and differently for older ones
    """
    postgresql_noproc = NoopExecutor(
        postgresql_proc.host,
        postgresql_proc.port,
        postgresql_proc.user,
        postgresql_proc.options,
    )
    noproc_version = retry(
        lambda: postgresql_noproc.version,  # type: ignore[no-any-return]
        possible_exception=psycopg2.OperationalError,
    )
    assert postgresql_proc.version == noproc_version


def test_noproc_cached_version(postgresql_proc: PostgreSQLExecutor) -> None:
    """Test that the version is being cached."""
    postgresql_noproc = NoopExecutor(
        postgresql_proc.host, postgresql_proc.port, postgresql_proc.user, postgresql_proc.options
    )
    ver = retry(
        lambda: postgresql_noproc.version,  # type: ignore[no-any-return]
        possible_exception=psycopg2.OperationalError,
    )
    with postgresql_proc.stopped():
        assert ver == postgresql_noproc.version
