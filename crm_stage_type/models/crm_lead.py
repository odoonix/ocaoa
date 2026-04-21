# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Lead(models.Model):
    _inherit = "crm.lead"

    
    stage_id = fields.Many2one(
        'crm.stage', string='Stage', index=True, tracking=True,
        compute='_compute_stage_id', readonly=False, store=True,
        copy=False, group_expand='_read_group_stage_ids', ondelete='restrict',
        domain=(
        "["
        "'&',"
            "'|',"
                "('lead_type', '=', type),"
                "('lead_type', '=', 'both'),"
            "'|',"
                "'|',"
                    "('team_ids', '=', False),"
                    "('team_ids', 'in', team_id),"
                "('team_ids', '!=', False)"
        "]"
    ),
    )

    @api.model
    def _read_group_stage_ids(self, stages, domain):
        ctx_type = self.env.context.get("default_type")
        team_id = self.env.context.get('default_team_id')

        search_domain = []

        if ctx_type:
            search_domain += [('lead_type', 'in', [ctx_type, 'both'])]

        if team_id:
            search_domain += [
                '|', 
                    ('team_ids', '=', False), 
                    ('team_ids', 'in', [team_id])
            ]
        else:
            search_domain += [
                '|',
                    ('team_ids', '=', False), 
                    ('team_ids', '!=', False)
            ]

        stage_ids = self.env['crm.stage'].sudo()._search(
            search_domain,
            order='sequence'
        )

        return self.env['crm.stage'].browse(stage_ids)

    def _stage_find(self, team_ids=False, domain=None, order="sequence"):
        # check whether we should try to add a condition on type
        domain = domain or []
        if not any(
            [term for term in domain if len(term) == 3 and term[0] == "lead_type"]
        ):
            types = ["both"]
            ctx_type = self.env.context.get("default_type")
            if ctx_type:
                types += [ctx_type]
            domain.append(("lead_type", "in", types))
        return super(Lead, self)._stage_find(team_ids, domain, order)

    def merge_opportunity(self, user_id=False, team_ids=False):
        opportunities_head = super(Lead, self).merge_opportunity(user_id, team_ids)
        if opportunities_head.team_ids:
            team_stage_ids = self.env["crm.stage"].search(
                [
                    ("team_ids", "in", [opportunities_head.team_ids.ids, False]),
                    ("lead_type", "in", [opportunities_head.type, "both"]),
                ],
                order="sequence",
            )
            if opportunities_head.stage_id not in team_stage_ids:
                opportunities_head.write(
                    {"stage_id": team_stage_ids[0] if team_stage_ids else False}
                )
        return opportunities_head

    def _convert_opportunity_data(self, customer, team_ids=False):
        value = super(Lead, self)._convert_opportunity_data(customer, team_ids)
        if (not self.stage_id or self.stage_id.lead_type == "lead") and team_ids:
            stage = self._stage_find(
                team_ids=team_ids, domain=[("lead_type", "in", ["opportunity", "both"])]
            )
            value["stage_id"] = stage.id
        return value
