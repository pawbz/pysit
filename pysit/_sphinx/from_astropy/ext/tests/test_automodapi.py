# Licensed under a 3-clause BSD style license - see LICENSE.rst

import os

from ....tests.helper import pytest
pytest.importorskip('sphinx')  # skips these tests if sphinx not present


class FakeConfig(object):
    """
    Mocks up a sphinx configuration setting construct for automodapi tests
    """
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)


class FakeApp(object):
    """
    Mocks up a `sphinx.application.Application` object for automodapi tests
    """
    def __init__(self, **configs):
        self.config = FakeConfig(**configs)
        self.info = []
        self.warnings = []

    def info(self, msg, loc):
        self.info.append((msg, loc))

    def warn(self, msg, loc):
        self.warnings.append((msg, loc))


am_replacer_str = """
This comes before

.. automodapi:: pysit._sphinx.from_astropy.ext.tests.test_automodapi
{options}

This comes after
"""

am_replacer_basic_expected = """
This comes before

pysit._sphinx.from_astropy.ext.tests.test_automodapi Module
-----------------------------------------------

.. automodule:: pysit._sphinx.from_astropy.ext.tests.test_automodapi

Functions
^^^^^^^^^

.. automodsumm:: pysit._sphinx.from_astropy.ext.tests.test_automodapi
    :functions-only:
    :toctree: api/
    {empty}

Classes
^^^^^^^

.. automodsumm:: pysit._sphinx.from_astropy.ext.tests.test_automodapi
    :classes-only:
    :toctree: api/
    {empty}

Class Inheritance Diagram
^^^^^^^^^^^^^^^^^^^^^^^^^

.. automod-diagram:: pysit._sphinx.from_astropy.ext.tests.test_automodapi
    :private-bases:

This comes after
""".format(empty='').replace('/', os.sep)
# the .format is necessary for editors that remove empty-line whitespace


def test_am_replacer_basic():
    """
    Tests replacing an ".. automodapi::" with the automodapi no-option
    template
    """
    from ..automodapi import automodapi_replace

    fakeapp = FakeApp(automodapi_toctreedirnm='api')
    result = automodapi_replace(am_replacer_str.format(options=''), fakeapp)

    assert result == am_replacer_basic_expected

am_replacer_noinh_expected = """
This comes before

pysit._sphinx.from_astropy.ext.tests.test_automodapi Module
-----------------------------------------------------------

.. automodule:: pysit._sphinx.from_astropy.ext.tests.test_automodapi

Functions
^^^^^^^^^

.. automodsumm:: pysit._sphinx.from_astropy.ext.tests.test_automodapi
    :functions-only:
    :toctree: api/
    {empty}

Classes
^^^^^^^

.. automodsumm:: pysit._sphinx.from_astropy.ext.tests.test_automodapi
    :classes-only:
    :toctree: api/
    {empty}


This comes after
""".format(empty='').replace('/', os.sep)


def test_am_replacer_noinh():
    """
    Tests replacing an ".. automodapi::" with no-inheritance-diagram
    option
    """
    from ..automodapi import automodapi_replace

    fakeapp = FakeApp(automodapi_toctreedirnm='api')
    ops = ['', ':no-inheritance-diagram:']
    ostr = '\n    '.join(ops)
    result = automodapi_replace(am_replacer_str.format(options=ostr), fakeapp)

    assert result == am_replacer_noinh_expected

am_replacer_titleandhdrs_expected = """
This comes before

pysit._sphinx.from_astropy.ext.tests.test_automodapi Module
&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

.. automodule:: pysit._sphinx.from_astropy.ext.tests.test_automodapi

Functions
*********

.. automodsumm:: pysit._sphinx.from_astropy.ext.tests.test_automodapi
    :functions-only:
    :toctree: api/
    {empty}

Classes
*******

.. automodsumm:: pysit._sphinx.from_astropy.ext.tests.test_automodapi
    :classes-only:
    :toctree: api/
    {empty}

Class Inheritance Diagram
*************************

.. automod-diagram:: pysit._sphinx.from_astropy.ext.tests.test_automodapi
    :private-bases:


This comes after
""".format(empty='').replace('/', os.sep)


def test_am_replacer_titleandhdrs():
    """
    Tests replacing an ".. automodapi::" entry with title-setting and header
    character options.
    """
    from ..automodapi import automodapi_replace

    fakeapp = FakeApp(automodapi_toctreedirnm='api')
    ops = ['', ':title: A new title', ':headings: &*']
    ostr = '\n    '.join(ops)
    result = automodapi_replace(am_replacer_str.format(options=ostr), fakeapp)

    assert result == am_replacer_titleandhdrs_expected


am_replacer_nomain_str = """
This comes before

.. automodapi:: pysit._sphinx.from_astropy.ext.automodapi
    :no-main-docstr:

This comes after
"""

am_replacer_nomain_expected = """
This comes before

pysit._sphinx.from_astropy.ext.automodapi Module
------------------------------------------------



Functions
^^^^^^^^^

.. automodsumm:: pysit._sphinx.from_astropy.ext.automodapi
    :functions-only:
    :toctree: api/
    {empty}


This comes after
""".format(empty='').replace('/', os.sep)


def test_am_replacer_nomain():
    """
    Tests replacing an ".. automodapi::" with "no-main-docstring" .
    """
    from ..automodapi import automodapi_replace

    fakeapp = FakeApp(automodapi_toctreedirnm='api')
    result = automodapi_replace(am_replacer_nomain_str, fakeapp)

    assert result == am_replacer_nomain_expected


am_replacer_skip_str = """
This comes before

.. automodapi:: pysit._sphinx.from_astropy.ext.automodapi
    :skip: something1
    :skip: something2

This comes after
"""

am_replacer_skip_expected = """
This comes before

pysit._sphinx.from_astropy.ext.automodapi Module
------------------------------------------------

.. automodule:: pysit._sphinx.from_astropy.ext.automodapi

Functions
^^^^^^^^^

.. automodsumm:: pysit._sphinx.from_astropy.ext.automodapi
    :functions-only:
    :toctree: api/
    :skip: something1,something2


This comes after
""".format(empty='').replace('/', os.sep)


def test_am_replacer_skip():
    """
    Tests using the ":skip: option in an ".. automodapi::" .
    """
    from ..automodapi import automodapi_replace

    fakeapp = FakeApp(automodapi_toctreedirnm='api')
    result = automodapi_replace(am_replacer_skip_str, fakeapp)

    assert result == am_replacer_skip_expected


am_replacer_invalidop_str = """
This comes before

.. automodapi:: pysit._sphinx.from_astropy.ext.automodapi
    :invalid-option:

This comes after
"""


def test_am_replacer_invalidop():
    """
    Tests that a sphinx warning is produced with an invalid option.
    """
    from ..automodapi import automodapi_replace

    fakeapp = FakeApp(automodapi_toctreedirnm='api')
    automodapi_replace(am_replacer_invalidop_str, fakeapp)

    expected_warnings = [('Found additional options invalid-option in '
                          'automodapi.', None)]

    assert fakeapp.warnings == expected_warnings
