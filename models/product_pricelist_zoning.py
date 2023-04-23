# -*- coding: utf-8 -*-

from __future__ import absolute_import

from odoo import api, models, fields


class ProductPricelistZoning(models.Model):
    _name = 'product.pricelist.zoning'

    @api.model
    def _get_default_currency_id(self):
        return self.env.user.company_id.currency_id.id

    @api.model
    def _get_default_item_ids(self):
        ProductPricelistItem = self.env['product.pricelist.zoning.item']
        vals = ProductPricelistItem.default_get(
            ProductPricelistItem._fields.keys()
        )
        return [[0, False, vals]]

    name = fields.Char(
        string='Pricelist Name',
        required=True,
        translate=True,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
        help=(
            'If unchecked, it will allow you to hide the pricelist without removing it.'
        )
    )
    item_ids = fields.One2many(
        comodel_name='product.pricelist.item',
        inverse_name='pricelist_id',
        string='Pricelist Items',
        copy=True,
        default=_get_default_item_ids
    )
    zone_ids = fields.One2many(
        comodel_name='product.zone',
        inverse_name='pricelist_id',
        string='Related Zones',
    )
    value = fields.Float(string='Value', )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=_get_default_currency_id,
        required=True
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
    )


class PricelistItem(models.Model):
    _inherit = 'product.pricelist.item'
    _name = 'product.pricelist.zoning.item'
    _description = 'Pricelist Zoning Item'

    base_pricelist_id = fields.Many2one(
        comodel_name='product.pricelist',
        string='Other Pricelist',
    )
    pricelist_id = fields.Many2one(
        comodel_name='product.pricelist.zoning',
        string='Pricelist Zoning',
        index=True,
        ondelete='cascade'
    )
