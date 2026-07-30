"""Deliberately empty.

Every test module declares the models it needs next to the tests that use
them. Django's ``migrate --run-syncdb`` only creates tables for apps whose
``AppConfig.models_module`` is set, and that attribute is only populated when
the app package contains a ``models`` module -- so this file has to exist for
those test models to get their tables.
"""
