from odoo import fields, models
from odoo.exceptions import UserError
from .tipax_request import TipaxProvider

class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'
    delivery_type = fields.Selection(selection_add=[('tipax','Tipax')], ondelete={'tipax':'set default'})
    tipax_api_key = fields.Char(copy=False, groups='base.group_system')
    tipax_origin_id = fields.Integer(default=16555239)
    tipax_city_id = fields.Integer(default=1565)
    tipax_service_id = fields.Integer(default=1)
    tipax_payment_type = fields.Integer(default=80)
    tipax_packing_id = fields.Integer(default=4)
    tipax_pack_type = fields.Integer(default=20)
    tipax_content_id = fields.Integer(default=9)
    tipax_currency_id = fields.Many2one('res.currency', string='Confirmed API currency')
    tipax_amount_factor = fields.Float(default=1, help='Multiply API amounts by this factor to obtain the configured currency; confirm units with Tipax.')
    tipax_success_callback = fields.Char()
    tipax_failure_callback = fields.Char()

    def action_tipax_test(self):
        self.ensure_one()
        self._tipax_check_company()
        TipaxProvider(self).request('GET','Cities')
        return {'type':'ir.actions.client','tag':'display_notification','params':{'title':'Tipax','message':'Cities request succeeded','type':'success'}}

    def _tipax_check_company(self):
        self.ensure_one()
        if not self.company_id or self.company_id not in self.env.companies:
            raise UserError('Select a carrier belonging to an allowed company.')

    def tipax_rate_shipment(self, order):
        return {'success':False,'price':0,'error_message':'Use Get Tipax Price on the transfer after entering parcel dimensions and declared value.','warning_message':False}

    def tipax_send_shipping(self, pickings):
        self.ensure_one()
        # Explicit registration on picking only; never create an order during stock validation.
        return [{'exact_price':p.tipax_company_price,'tracking_number':p.carrier_tracking_ref or False} for p in pickings]

    def tipax_get_tracking_link(self, picking):
        return False

    def tipax_cancel_shipment(self, picking):
        picking.action_tipax_cancel()
