# Copyright 2024 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    edit_raw_materials = fields.Boolean(
        string="Edit Raw Materials?", default=False, readonly=True
    )

    @api.multi
    def _generate_moves(self):
        for production in self:
            production.edit_raw_materials = False
            production._generate_finished_moves()
            factor = (
                production.product_uom_id._compute_quantity(
                    production.product_qty, production.bom_id.product_uom_id
                )
                / production.bom_id.product_qty
            )
            boms, lines = production.bom_id.explode(
                production.product_id,
                factor,
                picking_type=production.bom_id.picking_type_id,
            )
            production._generate_raw_moves(lines)

        return True

    @api.multi
    def action_confirm(self):
        for production in self:
            production.edit_raw_materials = True
            production._adjust_procure_method()
            production.move_raw_ids._action_confirm()
            production._generate_price_unit()

        return True

    @api.multi
    def _generate_price_unit(self):
        for production_id in self:
            domain = []
            values = {}
            mrp_bom_line_obj = self.env["mrp.bom.line"]
            production_bom_id = production_id.bom_id
            production_cost = 0.0
            production_qty = production_id.product_qty

            if production_id.routing_id:
                routing = production_id.routing_id
            else:
                routing = production_id.bom_id.routing_id

            if routing and routing.location_id:
                source_location = routing.location_id
            else:
                source_location = production_id.location_src_id

            for move_raw_id in production_id.move_raw_ids:
                bom_line_id = move_raw_id.bom_line_id

                if not bom_line_id:
                    domain += [
                        ("bom_id", "=", production_bom_id.id),
                        ("product_id", "=", move_raw_id.product_id.id),
                    ]
                    bom_line_id = mrp_bom_line_obj.sudo().search(domain, limit=1)

                    if not bom_line_id:
                        values["bom_id"] = production_bom_id.id
                        values["product_id"] = move_raw_id.product_id.id
                        values["product_uom_id"] = move_raw_id.product_uom.id
                        values["product_qty"] = move_raw_id.product_uom_qty
                        bom_line_id = mrp_bom_line_obj.sudo().create(values)

                unit_factor = move_raw_id.product_uom_qty / production_qty or 0.0
                move_raw_id.write(
                    {
                        "name": production_id.name,
                        "bom_line_id": bom_line_id.id,
                        "picking_type_id": production_id.picking_type_id.id,
                        "price_unit": move_raw_id.product_id.standard_price,
                        "origin": production_id.name,
                        "warehouse_id": source_location.get_warehouse().id,
                        "group_id": production_id.procurement_group_id.id,
                        "propagate": production_id.propagate,
                        "unit_factor": unit_factor,
                    }
                )
                production_cost += move_raw_id.price_unit * move_raw_id.product_uom_qty

            for move_finished_id in production_id.move_finished_ids:
                move_finished_id.write({"price_unit": production_cost / production_qty})

        return True
