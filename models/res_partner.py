# -*- coding: utf-8 -*-

from __future__ import absolute_import

from odoo import api, models, fields, _, SUPERUSER_ID


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    @api.depends('is_school_buyer', 'city_id')
    def _compute_zone_id(self):
        for record in self:
            if record.is_school_buyer:
                partner_city = record.city_id
                rajaongkir_id = partner_city and partner_city.rajaongkir_id or None
                if rajaongkir_id:
                    record.zone_id = self.env['product.zone'].sudo(
                        SUPERUSER_ID
                    )._identify_zone_by_rajaongkir_id(rajaongkir_id)
                else:
                    record.zone_id = False
            else:
                record.zone_id = False

    zone_id = fields.Many2one(
        comodel_name='product.zone',
        string=_('Related Zone ID'),
        compute='_compute_zone_id',
        store=True,
    )
