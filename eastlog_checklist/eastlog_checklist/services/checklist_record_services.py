import datetime
from odoo.addons.component.core import Component

from odoo.addons.base_rest.components.service import to_int, to_bool
from odoo.exceptions import MissingError


class ChecklistRecordService(Component):
    _inherit = 'base.rest.service'
    _name = 'checklist_record.service'
    _usage = 'checklist_record'
    _collection = 'eastlog_checklist.private.services'
    _description = """
        Checklist Record Services
        Access to the checklist record services is only allowed to authenticated users.
        If you are not authenticated go to <a href='/web/login'>Login</a>
    """

    def get(self, _id):
        """
        Get checklist record's informations
        """
        try:
            res = self._to_json(self._get(_id))
        except MissingError:
            res = 'Record does not exist or has been deleted.'
        except:
            res = 'Something else went wrong.'
        return res

    def search(self, name=None):
        """
        Searh checklist_record by name.
        If "name" is not specified, it will return all checklists.
        """
        if name:
            checklist_records = self.env['eastlog_checklist.checklist_record'].name_search(
                name)
            checklist_records = self.env['eastlog_checklist.checklist_record'].browse(
                [i[0] for i in checklist_records])
        else:
            checklist_records = self.env['eastlog_checklist.checklist_record'].search([
            ])
        rows = []
        res = {
            'count': len(checklist_records),
            'rows': rows
        }
        for checklist_record in checklist_records:
            rows.append(self._to_json(checklist_record))
        return res

    # pylint:disable=method-required-super
    def create(self, **params):
        """
        Create a new checklist record
        """
        params = self._prepare_params_for_create(params)
        try:
            # checklist_record = self.env['eastlog_checklist.checklist_record'].create(
            #     params)
            # res = self._to_json(checklist_record)
            self.env['eastlog_checklist.checklist_record'].create(
                params)
            res = True
        except:
            res = False
        return res

    def update(self, _id, **params):
        """
        Update checklist_record informations
        """
        checklist = self._get(_id)
        checklist.write(self._prepare_params_for_update(params))
        # return self._to_json(partner)
        return True

    # def archive(self, _id, **params):
    #     """
    #     Archive the given partner. This method is an empty method, IOW it
    #     don't update the partner. This method is part of the demo data to
    #     illustrate that historically it's not mandatory to defined a schema
    #     describing the content of the response returned by a method.
    #     This kind of definition is DEPRECATED and will no more supported in
    #     the future.
    #     :param _id:
    #     :param params:
    #     :return:
    #     """
    #     return {'response': 'Method archive called with id %s' % _id}

    # The following method are 'private' and should be never never NEVER call
    # from the controller.

    def _get(self, _id):
        return self.env['eastlog_checklist.checklist_record'].browse(_id)

    def _prepare_params_for_create(self, params):
        key = 'sub_checklist_record_ids'
        if key in params:
            val = params.pop(key)
            sub_checklist_record_ids = []
            for sub_checklist_record in val:
                if 'item_record_ids' in sub_checklist_record:
                    sub_checklist_record['item_record_ids'] = [
                        (0, 0, item_record) for item_record in sub_checklist_record['item_record_ids']]
                sub_checklist_record_ids.append((0, 0, sub_checklist_record))
            params[key] = sub_checklist_record_ids

        if 'date_submitted' in params:
            date_value = params.pop('date_submitted')
            params['date_submitted'] = datetime.datetime.strptime(
                date_value, '%Y-%m-%d')
        return params

    def _prepare_params_for_update(self, params):
        key = 'sub_checklist_record_ids'
        if key in params:
            val = params.pop(key)
            sub_checklist_record_ids = []
            for sub_checklist_record in val:
                if 'item_record_ids' in sub_checklist_record:
                    sub_checklist_record['item_record_ids'] = [
                        (1, item_record['id'], item_record) for item_record in sub_checklist_record['item_record_ids']]
                sub_checklist_record_ids.append(
                    (1, sub_checklist_record['id'], sub_checklist_record))
            params[key] = sub_checklist_record_ids
        return params

    # Validator
    # def _validator_return_get(self):
    #     res = self._validator_create()
    #     res.update({
    #         'id': {'type': 'integer', 'required': True, 'empty': False},
    #     })
    #     return res

    def _validator_search(self):
        return {
            'name': {
                'type': 'string',
                'nullable': False,
                'required': False,
            },
        }

    # def _validator_return_search(self):
    #     return {
    #         'count': {'type': 'integer', 'required': True},
    #         'rows': {
    #             'type': 'list',
    #             'required': True,
    #             'schema': {
    #                 'type': 'dict',
    #                 'schema': self._validator_return_get()
    #             }
    #         }
    #     }

    def _validator_create(self):
        res = {
            'name': {'type': 'string', 'required': True, 'empty': False},
            'checklist_id': {
                'type': 'integer',
                'coerce': to_int,
                'required': True,
            },
            'date_submitted': {'type': 'string'},
            'user_id': {
                'type': 'integer',
                'coerce': to_int,
                'required': True,
            },
            'sub_checklist_record_ids': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'name': {
                            'type': 'string',
                        },
                        'sub_checklist_id': {
                            'type': 'integer',
                            'coerce': to_int,
                            'required': True,
                        },
                        'item_record_ids': {
                            'type': 'list',
                            'schema': {
                                'type': 'dict',
                                'schema': {
                                    'name': {
                                        'type': 'string',
                                    },
                                    'item_id': {
                                        'type': 'integer',
                                        'coerce': to_int,
                                    },
                                    'has_problem': {
                                        'type': 'boolean',
                                        'coerce': to_bool,
                                    },
                                    'user_id': {
                                        'type': 'integer',
                                        'coerce': to_int,
                                        'required': True,
                                    },
                                    'comment': {
                                        'type': 'string',
                                    },
                                    'media_url': {
                                        'type': 'string'
                                    },
                                    'media_type': {
                                        'type': 'string',
                                    },
                                    'is_done': {
                                        'type': 'boolean',
                                        'coerce': to_bool,
                                    },
                                }
                            }
                        }
                    }
                }
            },
        }
        return res

    # def _validator_return_create(self):
    #     return self._validator_return_get()

    def _validator_update(self):
        res = {
            'id': {'type': 'integer', 'coerce': to_int, 'required': True, 'empty': False},
            # 'date_submitted': {'type': 'string'},
            'user_id': {
                'type': 'integer',
                'coerce': to_int,
                'required': True,
            },
            'sub_checklist_record_ids': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'id': {
                            'type': 'integer',
                            'coerce': to_int,
                            'required': False,
                        },
                        'item_record_ids': {
                            'type': 'list',
                            'schema': {
                                'type': 'dict',
                                'schema': {
                                    'id': {
                                        'type': 'integer',
                                        'coerce': to_int,
                                        'required': False,
                                    },
                                    'has_problem': {
                                        'type': 'boolean',
                                        'coerce': to_bool,
                                        'required': False,
                                    },
                                    'user_id': {
                                        'type': 'integer',
                                        'coerce': to_int,
                                        'required': True,
                                    },
                                    'comment': {
                                        'type': 'string',
                                        'required': False,
                                    },
                                    'media_url': {
                                        'type': 'string',
                                        'required': False,
                                    },
                                    'media_type': {
                                        'type': 'string',
                                        'required': False,
                                    },
                                    'is_done': {
                                        'type': 'boolean',
                                        'coerce': to_bool,
                                        'required': False,
                                    },
                                }
                            }
                        }
                    }
                }
            },
        }
        return res

    # def _validator_return_update(self):
    #     return self._validator_return_get()

    # def _validator_archive(self):
    #     return {}

    def _to_json(self, checklist_record):
        res = {
            'id': checklist_record.id,
            'name': checklist_record.name,
            'checklist': checklist_record.checklist_id.name,
            'checklist_id': checklist_record.checklist_id.id,
            'date_submitted': checklist_record.date_submitted,
            'user_id': checklist_record.user_id.id,
            'user_name': checklist_record.user_id.name,
            'is_done': checklist_record.is_done,
            'has_problem': checklist_record.has_problem,
        }
        if checklist_record.sub_checklist_record_ids and len(checklist_record.sub_checklist_record_ids) > 0:
            sub_checklist_record_ids = []
            for sub_checklist_record_id in checklist_record.sub_checklist_record_ids:
                sub_checklist_record_data = {
                    'id': sub_checklist_record_id.id,
                    'name': sub_checklist_record_id.name,
                    'checklist_record_id': sub_checklist_record_id.checklist_record_id.id,
                    'sub_checklist_id': sub_checklist_record_id.sub_checklist_id.id,
                    'is_done': sub_checklist_record_id.is_done,
                    'has_problem': sub_checklist_record_id.has_problem,
                }
                if sub_checklist_record_id.item_record_ids and len(sub_checklist_record_id.item_record_ids) > 0:
                    item_record_ids = []
                    for item_record_id in sub_checklist_record_id.item_record_ids:
                        item_record_ids.append({
                            'id': item_record_id.id,
                            'name': item_record_id.name,
                            'item_id': item_record_id.item_id.id,
                            'has_problem': item_record_id.has_problem,
                            'user_id': item_record_id.user_id.id,
                            'comment': item_record_id.comment,
                            'media_url': item_record_id.media_url,
                            'media_type': item_record_id.media_type,
                            'sub_checklist_record_id': item_record_id.sub_checklist_record_id.id,
                            'is_done': item_record_id.is_done,
                        })
                    sub_checklist_record_data['item_record_ids'] = item_record_ids
                sub_checklist_record_ids.append(sub_checklist_record_data)

            res['sub_checklist_record_ids'] = sub_checklist_record_ids
        return res
