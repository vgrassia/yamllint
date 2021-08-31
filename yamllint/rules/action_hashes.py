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


import yaml

from yamllint.linter import LintProblem


ID = 'action-hashes'
TYPE = 'token'
CONF = {}
DEFAULT = {}


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
