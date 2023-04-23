# -*- coding: utf-8 -*-

from __future__ import absolute_import

from odoo import api, models, SUPERUSER_ID


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    @api.multi
    def get_products_not_in_zone(self):
        self.ensure_one()
        product_ids = [line.product_id for line in self.order_line]
        partner = self.partner_id.sudo(SUPERUSER_ID)
        partner_city = partner.city_id
        rajaongkir_id = partner_city and partner_city.rajaongkir_id or None
        zone_id = self.env['product.zone'].sudo(SUPERUSER_ID)._identify_zone_by_rajaongkir_id(rajaongkir_id)
        result = []
        if zone_id:
            result = [
                product for product in product_ids if product.zone_id and product.zone_id.id != zone_id
            ]
        return result
