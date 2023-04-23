import re

QUERY_RESULT_SIZE = 100

zones = env['product.zone'].search([])


products_offset = 0
while True:
    products = env['product.template'].search([], offset=products_offset,
            limit=QUERY_RESULT_SIZE)

    if products:
        products_offset += QUERY_RESULT_SIZE
    else:
        break

    for product in products:
        for zone in zones:
            if not product.zone_id and re.search(zone.identifier_rules, product.name):
                print(product.name)
                product.write({'zone_id': zone.id})


partners_offset = 0
while True:
    partners = env['res.partner'].search([('is_school_buyer', '=', True),
            ('city_id', '!=', False)], offset=partners_offset,
            limit=QUERY_RESULT_SIZE)

    if partners:
        partners_offset += QUERY_RESULT_SIZE
    else:
        break

    for partner in partners:
        print(partner.name)
    partners._compute_zone_id()


env.cr.commit()
