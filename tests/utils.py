from django.db import connection


def raw_text(value):
    """Return a raw JSON column fetched with a plain cursor as ``str``.

    Oracle hands back a ``LOB`` rather than a string, so tests that assert on
    the stored document's text have to read it out first.
    """
    if value is None or isinstance(value, str):
        return value
    if hasattr(value, "read"):
        return value.read()
    if isinstance(value, (bytes, bytearray, memoryview)):
        return bytes(value).decode()
    return str(value)


def skip_if_json_sorts_as_text(test):
    """Skip an ORDER BY assertion on backends that sort JSON values as text.

    Ordering by a virtual field becomes ``ORDER BY <key transform>``, and the
    database does the comparison. PostgreSQL, MySQL and SQLite compare the
    extracted number numerically; MariaDB and Oracle compare it as a string,
    so 10 sorts before 2. Called at run time so it sees the test connection.
    """
    if connection.vendor == "oracle":
        test.skipTest("Oracle compares JSON-extracted values as text")
    if connection.vendor == "mysql" and connection.mysql_is_mariadb:
        test.skipTest("MariaDB compares JSON-extracted values as text")
