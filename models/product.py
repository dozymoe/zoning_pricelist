# -*- coding: utf-8 -*-

from __future__ import absolute_import

from odoo import api, models, fields, SUPERUSER_ID


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    @api.depends('name')
    def _compute_zone_id(self):
        for record in self:
            record.zone_id = self.env['product.zone'].sudo(
                SUPERUSER_ID
            )._identify_zone_by_string(record.name)

    # @api.multi
    # @api.depends('zone_id')
    # def _compute_zoning_list_price(self):
    #     for record in self:
    #         if record.zone_id:
    #             record.zoning_list_price = record.zone_id.
    #         else:
    #             record.zoning_list_price = record.list_price

    zone_id = fields.Many2one(
        comodel_name='product.zone',
        string='Related Zone ID',
        compute='_compute_zone_id',
        store=True,
    )
    # zoning_list_price = fields.Float(
    #     string='Zoning Price Unit',
    #     compute='_compute_zoning_list_price',
    # )
