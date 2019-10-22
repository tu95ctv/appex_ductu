from odoo import api, fields, models


class JobRequest(models.Model):
    _inherit = 'eastlog_job_request.job_request'

    @api.multi
    def close_dialog(self):
        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def edit_dialog(self):
        form_view = self.env.ref('eastlog_job_request.job_request_view_form')
        return {
            # 'name': _('Task'),
            'res_model': 'project.task',
            'res_id': self.id,
            'views': [(form_view.id, 'form'), ],
            'type': 'ir.actions.act_window',
            'target': 'inline'
        }
