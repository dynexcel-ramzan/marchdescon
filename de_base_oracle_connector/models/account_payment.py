# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
from odoo.exceptions import ValidationError


logger = logging.getLogger(__name__)




class AccountPayment(models.Model):
    _inherit = 'account.payment'

    ora_ledger_label = fields.Char(string="Journal Label")


















