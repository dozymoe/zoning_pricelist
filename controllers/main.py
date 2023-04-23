# -*- coding: utf-8 -*-

from __future__ import absolute_import
from odoo import http, SUPERUSER_ID
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleSchool(WebsiteSale):


    def _get_search_domain(self, search, category, attrib_values):
        domain = super(WebsiteSaleSchool, self)._get_search_domain(
            search, category, attrib_values
        )
        if (
            request.env.user and request.env.user.partner_id and
            request.env.user.partner_id.is_school_buyer
        ):
            partner = request.env.user.partner_id.sudo(SUPERUSER_ID)
            partner_city = partner.city_id
            rajaongkir_id = partner_city and partner_city.rajaongkir_id or None
            zone_id = request.env['product.zone'].sudo(SUPERUSER_ID)._identify_zone_by_rajaongkir_id(rajaongkir_id)

            if zone_id:
                domain += [('zone_id', 'in', (int(zone_id), False))]
        return domain


    @http.route()
    def cart(self, **post):
        order = request.website.sale_get_order()
        if order:
            from_currency = order.company_id.currency_id
            to_currency = order.pricelist_id.currency_id
            compute_currency = lambda price: from_currency.compute(price, to_currency)
        else:
            compute_currency = lambda price: price

        values = {
            'website_sale_order': order,
            'compute_currency': compute_currency,
            'suggested_products': [],
            'products_not_in_zone': [],
        }
        if order:
            _order = order
            if not request.env.context.get('pricelist'):
                _order = order.with_context(pricelist=order.pricelist_id.id)
            values['suggested_products'] = _order._cart_accessories()

        real_order = request.env['sale.order'].sudo(SUPERUSER_ID).browse(
            order.id
        )
        if real_order:
            products_not_in_zone = real_order.get_products_not_in_zone()
            values['products_not_in_zone'] = products_not_in_zone

        if post.get('type') == 'popover':
            # force no-cache so IE11 doesn't cache this XHR
            return request.render(
                "website_sale.cart_popover",
                values,
                headers={'Cache-Control': 'no-cache'}
            )

        if post.get('code_not_available'):
            values['code_not_available'] = post.get('code_not_available')

        return request.render("website_sale.cart", values)
