# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.base_rest.controllers import main


class EastlogChecklistPrivateApiController(main.RestController):
    _root_path = '/eastlog_checklist/private/v1/'
    _collection_name = 'eastlog_checklist.private.services'
    _default_auth = 'user'
