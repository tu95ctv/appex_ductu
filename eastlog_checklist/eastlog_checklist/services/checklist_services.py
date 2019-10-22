from odoo.addons.component.core import Component

from odoo.addons.base_rest.components.service import to_int, to_bool


class ChecklistService(Component):
    _inherit = 'base.rest.service'
    _name = 'checklist.service'
    _usage = 'checklist'
    _collection = 'eastlog_checklist.private.services'
    _description = """
        Checklist Services
        Access to the checklist services is only allowed to authenticated users.
        If you are not authenticated go to <a href='/web/login'>Login</a>
    """

    def get(self, _id):
        """
        Get checklist's informations
        """

        return self._to_json(self._get(_id))

    def search(self, name=None):
        """
        Searh checklist by name.
        If "name" is not specified, it will return all checklists.
        """
        if name:
            checklists = self.env['eastlog_checklist.checklist'].name_search(
                name)
            checklists = self.env['eastlog_checklist.checklist'].browse(
                [i[0] for i in checklists])
        else:
            checklists = self.env['eastlog_checklist.checklist'].search([])
        rows = []
        res = {
            'count': len(checklists),
            'rows': rows
        }
        for checklist in checklists:
            rows.append(self._to_json(checklist))
        return res

    # pylint:disable=method-required-super
    # def create(self, **params):
    #     """
    #     Create a new partner
    #     """
    #     partner = self.env['res.partner'].create(
    #         self._prepare_params(params))
    #     return self._to_json(partner)

    # def update(self, _id, **params):
    #     """
    #     Update partner informations
    #     """
    #     partner = self._get(_id)
    #     partner.write(self._prepare_params(params))
    #     return self._to_json(partner)

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
        return self.env['eastlog_checklist.checklist'].browse(_id)

    # def _prepare_params(self, params):
    #     for key in ['country', 'state']:
    #         if key in params:
    #             val = params.pop(key)
    #             if val.get('id'):
    #                 params["%s_id" % key] = val['id']
    #     return params

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

    # def _validator_create(self):
    #     res = {
    #         'name': {'type': 'string', 'required': True, 'empty': False},
    #         'street': {'type': 'string', 'required': True, 'empty': False},
    #         'street2': {'type': 'string', 'nullable': True},
    #         'zip': {'type': 'string', 'required': True, 'empty': False},
    #         'city': {'type': 'string', 'required': True, 'empty': False},
    #         'phone': {'type': 'string', 'nullable': True, 'empty': False},
    #         'state': {
    #             'type': 'dict',
    #             'schema': {
    #                 'id': {
    #                     'type': 'integer',
    #                     'coerce': to_int,
    #                     'nullable': True
    #                 },
    #                 'name': {
    #                     'type': 'string',
    #                 }
    #             }
    #         },
    #         'country': {
    #             'type': 'dict',
    #             'schema': {
    #                 'id': {
    #                     'type': 'integer',
    #                     'coerce': to_int,
    #                     'required': True,
    #                     'nullable': False
    #                 },
    #                 'name': {
    #                     'type': 'string',
    #                 }
    #             },
    #         },
    #         'is_company': {'coerce': to_bool, 'type': 'boolean'},
    #     }
    #     return res

    # def _validator_return_create(self):
    #     return self._validator_return_get()

    # def _validator_update(self):
    #     res = self._validator_create()
    #     for key in res:
    #         if 'required' in res[key]:
    #             del res[key]['required']
    #     return res

    # def _validator_return_update(self):
    #     return self._validator_return_get()

    # def _validator_archive(self):
    #     return {}

    def _to_json(self, checklist):
        res = {
            'id': checklist.id,
            'name': checklist.name,
            'category': checklist.category.name,
        }
        if checklist.sub_checklist_ids and len(checklist.sub_checklist_ids) > 0:
            sub_checklist_ids = []
            for sub_checklist_id in checklist.sub_checklist_ids:
                sub_checklist_data = {
                    'id': sub_checklist_id.id,
                    'name': sub_checklist_id.name,
                    'checklist_id': sub_checklist_id.checklist_id.id,
                }
                if sub_checklist_id.item_ids and len(sub_checklist_id.item_ids) > 0:
                    item_ids = []
                    for item_id in sub_checklist_id.item_ids:
                        item_ids.append({
                            'id': item_id.id,
                            'name': item_id.name,
                            'sub_checklist_id': item_id.sub_checklist_id.id,
                        })
                    sub_checklist_data['item_ids'] = item_ids
                sub_checklist_ids.append(sub_checklist_data)

            res['sub_checklist_ids'] = sub_checklist_ids
        return res
