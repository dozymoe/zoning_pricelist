# -*- coding: utf-8 -*-

from __future__ import absolute_import

import re

from odoo import api, models, fields, SUPERUSER_ID


class ProductZone(models.Model):
    _name = 'product.zone'

    name = fields.Char(string='Name', required=True, )
    description = fields.Char(string='Description', )
    identifier_rules = fields.Text(string='Identifier Rules', required=True, )
    code_ids = fields.One2many(
        'product.zone.code',
        'product_zone_id',
        'Codes',
        copy=True,
    )
    pricelist_id = fields.Many2one(
        comodel_name='product.pricelist.zoning',
        string='Pricelist Zoning',
        index=True,
        ondelete='cascade'
    )

    @api.model
    def get_zone_rules(self):
        result = {}
        for record in self.sudo(SUPERUSER_ID).search([]):
            if record.identifier_rules:
                result[record.id] = record.identifier_rules.strip()
        return result

    @api.model
    def _identify_zone_by_string(self, string):
        zone_rules = self.get_zone_rules()
        for zone_id, identifier_rules in zone_rules.items():
            for identifier_rule in identifier_rules.split('\n'):
                if re.findall(identifier_rule, string):
                    return zone_id
        return False

    @api.model
    def _identify_zone_by_rajaongkir_id(self, rajaongkir_id):
        rows = self.sudo(SUPERUSER_ID).search([('code_ids.value', '=', rajaongkir_id)])
        return rows and rows[0] and rows[0].id or False


class ProductZoneCode(models.Model):
    _name = 'product.zone.code'
    _order = 'value'

    name = fields.Char(string='Name', required=True, )
    value = fields.Integer(string='Value', required=True, index=True)
    product_zone_id = fields.Many2one(
        'product.zone', 'Zone', ondelete='cascade'
    )
