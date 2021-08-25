# -*- coding: utf-8 -*-
# Copyright (C) 2021 Vince Grassia
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Use this rule to control the use of flow mappings or number of spaces inside
braces (``{`` and ``}``).

.. rubric:: Options

* ``forbid`` is used to forbid the use of flow mappings which are denoted by
  surrounding braces (``{`` and ``}``). Use ``true`` to forbid the use of flow
  mappings completely. Use ``non-empty`` to forbid the use of all flow
  mappings except for empty ones.
* ``min-spaces-inside`` defines the minimal number of spaces required inside
  braces.
* ``max-spaces-inside`` defines the maximal number of spaces allowed inside
  braces.
* ``min-spaces-inside-empty`` defines the minimal number of spaces required
  inside empty braces.
* ``max-spaces-inside-empty`` defines the maximal number of spaces allowed
  inside empty braces.

.. rubric:: Default values (when enabled)

.. code-block:: yaml

 rules:
   braces:
     forbid: false
     min-spaces-inside: 0
     max-spaces-inside: 0
     min-spaces-inside-empty: -1
     max-spaces-inside-empty: -1

.. rubric:: Examples

#. With ``braces: {forbid: true}``

   the following code snippet would **PASS**:
   ::

    object:
      key1: 4
      key2: 8

   the following code snippet would **FAIL**:
   ::

    object: { key1: 4, key2: 8 }

#. With ``braces: {forbid: non-empty}``

   the following code snippet would **PASS**:
   ::

    object: {}

   the following code snippet would **FAIL**:
   ::

    object: { key1: 4, key2: 8 }

#. With ``braces: {min-spaces-inside: 0, max-spaces-inside: 0}``

   the following code snippet would **PASS**:
   ::

    object: {key1: 4, key2: 8}

   the following code snippet would **FAIL**:
   ::

    object: { key1: 4, key2: 8 }

#. With ``braces: {min-spaces-inside: 1, max-spaces-inside: 3}``

   the following code snippet would **PASS**:
   ::

    object: { key1: 4, key2: 8 }

   the following code snippet would **PASS**:
   ::

    object: { key1: 4, key2: 8   }

   the following code snippet would **FAIL**:
   ::

    object: {    key1: 4, key2: 8   }

   the following code snippet would **FAIL**:
   ::

    object: {key1: 4, key2: 8 }

#. With ``braces: {min-spaces-inside-empty: 0, max-spaces-inside-empty: 0}``

   the following code snippet would **PASS**:
   ::

    object: {}

   the following code snippet would **FAIL**:
   ::

    object: { }

#. With ``braces: {min-spaces-inside-empty: 1, max-spaces-inside-empty: -1}``

   the following code snippet would **PASS**:
   ::

    object: {         }

   the following code snippet would **FAIL**:
   ::

    object: {}
"""


import yaml

from yamllint.linter import LintProblem
# from yamllint.rules.common import spaces_after, spaces_before


ID = 'action-hashes'
TYPE = 'token'
CONF = {}
DEFAULT = {}
# CONF = {'forbid': (bool, 'non-empty'),
#         'min-spaces-inside': int,
#         'max-spaces-inside': int,
#         'min-spaces-inside-empty': int,
#         'max-spaces-inside-empty': int}
# DEFAULT = {'forbid': False,
#            'min-spaces-inside': 0,
#            'max-spaces-inside': 0,
#            'min-spaces-inside-empty': -1,
#            'max-spaces-inside-empty': -1}


def check(conf, token, prev, next, nextnext, context):
    if isinstance(token, yaml.ScalarToken) and token.value == 'uses':
        try:
            _, hash = nextnext.value.split('@')
        except:
            yield LintProblem(token.start_mark.line + 1,
                              token.end_mark.column + 1,
                              'action does not have a valid hash (missing \'@\' character')
            return

        # Check if length is 40 characters (20-bytes)
        if len(hash) < 40 or len(hash) > 40:
            yield LintProblem(token.start_mark.line + 1,
                              token.end_mark.column + 1,
                              'action does not have a valid hash (not 40 chars)')

        # Check if hash is hexadecimal chars only
        try:
            int(hash, 16)
        except ValueError:
            yield LintProblem(token.start_mark.line + 1,
                              token.end_mark.column + 1,
                              'action does not have a valid hash (not all hexadecimal characters)')
