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
from yaml.tokens import BlockSequenceStartToken, FlowSequenceStartToken, ScalarToken

from yamllint.linter import LintProblem
# from yamllint.rules.common import spaces_after, spaces_before


ID = 'action-name'
TYPE = 'token'
CONF = {}
DEFAULT = {}

MAP, SEQ = range(2)


class Parent(object):
    def __init__(self, type):
        self.type = type
        self.keys = []

    def __str__(self):
        if self.type == 0:
            type = "MAP"
        elif self.type == 1:
            type = "SEQ"
        return "Type: " + type + " | Keys: " + str(self.keys)

    def get(self, key):
        result = []

        for x in self.keys:
            if x.value == key:
                result.append(x)

        return result


def check(conf, token, prev, next, nextnext, context):
    # If we don't have a stack, create an empty list to hold one.
    if 'stack' not in context:
        context['stack'] = []

    # If we are starting a MAP Block/Flow append it to the stack.
    if isinstance(token, (yaml.BlockMappingStartToken,
                          yaml.FlowMappingStartToken)):
        context['stack'].append(Parent(MAP))

    # If we are starting a SEQ Block/Flow append it to the stack.
    elif isinstance(token, (yaml.BlockSequenceStartToken,
                            yaml.FlowSequenceStartToken)):
        context['stack'].append(Parent(SEQ))

    # If we have a Key token with a Scalar value token next,
    # append it to the keys of the last MAP/SEQ in the stack.
    elif (isinstance(token, yaml.KeyToken) and
          isinstance(next, yaml.ScalarToken)):
        context['stack'][-1].keys.append(next)

    # If we are ending a Block/FlowMap/FlowSeq then run some checks
    # against the stack.
    elif isinstance(token, (yaml.BlockEndToken,
                            yaml.FlowMappingEndToken,
                            yaml.FlowSequenceEndToken)):
        # Check to make sure 'name' key exists for workflow.
        if len(context['stack']) == 1:
            workflow_name = context['stack'][0].get('name')
            if len(workflow_name) != 1:
                yield LintProblem(context['stack'][0].keys[0].start_mark.line + 1,
                                  context['stack'][0].keys[0].end_mark.column + 1,
                                  'missing name key for workflow')

        # Check to make sure 'name' key exists for jobs.
        if len(context['stack']) == 3:
            jobs = context['stack'][0].get('jobs')
            if len(jobs) == 1:
                job_names = context['stack'][2].get('name')
                if len(job_names) != 1:
                    yield LintProblem(context['stack'][1].keys[-1].start_mark.line + 1,
                                      context['stack'][1].keys[-1].end_mark.column + 1,
                                      'missing name key for job')

        # Check to make sure 'name' key exists for steps.
        if len(context['stack']) == 5:
            steps = context['stack'][2].get('steps')
            if len(steps) == 1:
                step_names = context['stack'][4].get('name')
                if len(step_names) != 1:
                    yield LintProblem(context['stack'][4].keys[0].start_mark.line + 1,
                                      context['stack'][4].keys[0].end_mark.column + 1,
                                      'missing name key for step')

        context['stack'].pop()
