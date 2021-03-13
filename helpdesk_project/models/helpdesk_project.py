# -*- coding: utf-8 -*-
# eYssen IT Services - See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

import logging
_logger = logging.getLogger(__name__)




class HelpdeskTicket(models.Model):
    
    _inherit = 'helpdesk.ticket'
    
    
    task_ids = fields.Many2many(comodel_name='project.task', relation='helpdesk_ticket_project_task', column1='ticket_id', column2='task_id')





class ProjectTask(models.Model):
    
    _inherit = 'project.task'
    
    
    ticket_ids = fields.Many2many(comodel_name='helpdesk.ticket', relation='helpdesk_ticket_project_task', column1='task_id', column2='ticket_id')
