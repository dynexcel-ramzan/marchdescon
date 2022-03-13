# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
from odoo.exceptions import ValidationError


logger = logging.getLogger(__name__)




class AccountJournal(models.Model):
    _inherit = 'account.journal'

    ora_ledger_label = fields.Char(string="Journal Label")


















