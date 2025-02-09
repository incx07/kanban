#!/usr/bin/python3
# coding=utf-8

#   Copyright 2022 getcarrier.io
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

""" API """
import json
import flask_restful  # pylint: disable=E0401
from flask import request
from marshmallow.exceptions import ValidationError
from pylon.core.tools import log  # pylint: disable=E0611,E0401

from tools import auth  # pylint: disable=E0401

from plugins.kanban.schemas.board import board_schema, clone_board_schema


class API(flask_restful.Resource):  # pylint: disable=R0903
    """ API Resource """

    def __init__(self, module):
        self.module = module
        self.rpc = self.module.context.rpc_manager.call


    @auth.decorators.check_api(["orchestration.kanban.boards.create"])
    def post(self):
        """Clone board"""
        payload = request.json        
        try:
            payload = clone_board_schema.load(payload)
        except ValidationError as err:
            messages = getattr(err, 'messages', None)
            return {"ok":False, "error": json.dumps(messages)}, 400

        result = self.module.clone_board(payload)
        
        if not result["ok"]:
            return result, 400

        result['item'] = board_schema.dump(result['item']) 
        return result, 201


        
