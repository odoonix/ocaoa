import json
import uuid
from urllib.parse import quote
from odoo import fields, models, api
from odoo.exceptions import UserError
from .tipax_request import TipaxProvider
import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    tipax_is_carrier = fields.Boolean(compute='_compute_tipax_carrier')
    tipax_direction = fields.Selection([('collection','Customer collection'),('outgoing','Send to customer')], default='outgoing', required=True)
    tipax_address_id = fields.Many2one('res.partner', string='Customer shipping address')
    tipax_customer_city = fields.Integer()
    tipax_weight = fields.Float(default=1)
    tipax_length = fields.Float(default=20)
    tipax_width = fields.Float(default=15)
    tipax_height = fields.Float(default=10)
    tipax_value = fields.Float(string='Declared value (API units)')
    tipax_service = fields.Integer(default=1)
    tipax_payment = fields.Integer(default=80)
    tipax_packing = fields.Integer(default=4)
    tipax_pack = fields.Integer(default=20)
    tipax_content = fields.Integer(default=9)
    tipax_barcode = fields.Char(copy=False)
    tipax_trace = fields.Char(copy=False, readonly=True)
    tipax_status = fields.Char(copy=False, readonly=True)
    tipax_status_id = fields.Integer(copy=False, readonly=True)
    tipax_order_id = fields.Char(copy=False, readonly=True)
    tipax_correlation = fields.Char(copy=False, readonly=True)
    tipax_history = fields.Text(copy=False, readonly=True)
    tipax_estimate = fields.Float(copy=False, readonly=True)
    tipax_final = fields.Float(copy=False, readonly=True)
    tipax_company_price = fields.Float(copy=False, readonly=True)
    tipax_state = fields.Selection([('draft','Draft'),('pending','Verify registration'),('sent','Registered'),('cancel_requested','Cancellation requested'),('cancelled','Cancelled')], default='draft', copy=False, readonly=True)
    tipax_previous_id = fields.Many2one('stock.picking', copy=False, check_company=True)
    tipax_last_error = fields.Char(copy=False, readonly=True)
    tipax_last_sync = fields.Datetime(copy=False, readonly=True)
    tipax_handover = fields.Datetime(copy=False, readonly=True)
    tipax_handover_user = fields.Many2one('res.users', copy=False, readonly=True)

    tipax_state_label = fields.Char(compute='_compute_tipax_state_label')
    tipax_confirmed = fields.Boolean(compute='_compute_tipax_confirmed')

    @api.depends('tipax_state', 'tipax_order_id', 'tipax_status_id', 'carrier_tracking_ref')
    def _compute_tipax_confirmed(self):
        for p in self:
            p.tipax_confirmed = bool(p.tipax_state == 'sent' and p.tipax_order_id
                                     and p.carrier_tracking_ref and p.tipax_status_id > 0)

    @api.depends('tipax_state', 'tipax_confirmed')
    def _compute_tipax_state_label(self):
        labels = dict(self._fields['tipax_state']._description_selection(self.env))
        for p in self:
            state = 'pending' if p.tipax_state == 'sent' and not p.tipax_confirmed else p.tipax_state
            p.tipax_state_label = labels.get(state, state or '')

    @api.depends('carrier_id.delivery_type')
    def _compute_tipax_carrier(self):
        for p in self:
            p.tipax_is_carrier = p.carrier_id.delivery_type == 'tipax'

    @api.onchange('carrier_id')
    def _onchange_tipax_carrier(self):
        c = self.carrier_id
        if c.delivery_type == 'tipax':
            self.tipax_service = c.tipax_service_id
            self.tipax_payment = c.tipax_payment_type
            self.tipax_packing = c.tipax_packing_id
            self.tipax_pack = c.tipax_pack_type
            self.tipax_content = c.tipax_content_id
            self.tipax_direction = 'collection' if self.picking_type_code == 'incoming' else 'outgoing'

    def _tipax_provider(self):
        self.ensure_one()
        c = self.carrier_id
        if c.delivery_type != 'tipax' or c.company_id != self.company_id:
            raise UserError('Choose a Tipax carrier belonging to this transfer company.')
        c._tipax_check_company()
        return TipaxProvider(c)

    def _tipax_address(self, partner, city):
        address = ', '.join(filter(None, [
            partner.street,
            partner.street2,
            partner.city,
        ]))

        mobile = partner.mobile or partner.phone

        if not city or not address or not mobile or not partner.name:
            raise UserError(
                'Address, contact name, mobile and Tipax city ID are required.'
            )

        return {
            'cityId': city,
            'fullAddress': address,
            'postalCode': partner.zip or '',
            'floor': '',
            'unit': '',
            'no': '',
            'latitude': str(partner.partner_latitude or ''),
            'longitude': str(partner.partner_longitude or ''),
            'description': '',
            'beneficiary': {
                'fullName': partner.name,
                'mobile': mobile,
                'phone': partner.phone or '',
                'nationalId': '',
            },
        }

    def _tipax_package(self):
        self.ensure_one()
        c = self.carrier_id
        if min(self.tipax_weight,self.tipax_length,self.tipax_width,self.tipax_height,self.tipax_value,self.tipax_service,self.tipax_payment,self.tipax_pack,self.tipax_content,self.tipax_customer_city,c.tipax_city_id) <= 0:
            raise UserError('Enter positive dimensions, weight, declared value and Tipax IDs.')
        customer = self._tipax_address(self.tipax_address_id or self.partner_id,self.tipax_customer_city)
        package = {'weight':self.tipax_weight,'length':self.tipax_length,'width':self.tipax_width,'height':self.tipax_height,'packageValue':self.tipax_value,'serviceId':self.tipax_service,'paymentType':self.tipax_payment,'packType':self.tipax_pack,'packageContentId':self.tipax_content,'pickupType':10,'distributionType':10,'description':self.name,'enableLabelPrivacy':False,'cod':0,'cashAmount':0,'payInPlaceAmount':0,'barcode':self.tipax_barcode or '', 'customParcelTitle':self.name,'bubbleWrapAmount':0,'glueAmount':0,'salaryAmount':0}
        if self.tipax_packing:
            package['packingId'] = self.tipax_packing
        if self.tipax_direction == 'collection':
            package.update(origin=customer,destination=self._tipax_address(self.company_id.partner_id,c.tipax_city_id))
        else:
            if not c.tipax_origin_id:
                raise UserError('Configure predefined origin ID.')
            package.update(originId=c.tipax_origin_id,destination=customer,isUnsual=False)
        return package

    def _tipax_convert(self, amount):
        c = self.carrier_id
        if not c.tipax_currency_id or c.tipax_amount_factor <= 0:
            raise UserError('Confirm API currency and amount factor on carrier.')
        return c.tipax_currency_id._convert(amount*c.tipax_amount_factor,self.company_id.currency_id,self.company_id,fields.Date.today())

    def action_tipax_price(self):
        self.ensure_one()
        provider = self._tipax_provider()
        p = self._tipax_package()
        keys = ('weight','length','width','height','packageValue','serviceId','paymentType','packType','packageContentId','pickupType','distributionType','packingId')
        item = {k:p[k] for k in keys if k in p}
        item.update(origin={'cityId':self.tipax_customer_city if self.tipax_direction=='collection' else self.carrier_id.tipax_city_id},destination={'cityId':self.carrier_id.tipax_city_id if self.tipax_direction=='collection' else self.tipax_customer_city})
        result = provider.request('POST','Pricing',{'packageInputs':[item],'discountCode':''})
        for row in result if isinstance(result,list) else []:
            for rate in row.values():
                if isinstance(rate,dict) and rate.get('serviceId') == self.tipax_service and 'finalPrice' in rate:
                    self.write({'tipax_estimate':rate['finalPrice'],'tipax_company_price':self._tipax_convert(rate['finalPrice'])})
                    return
        raise UserError('No matching Tipax rate returned.')

    def action_tipax_register(self):
        self.ensure_one()
        provider = self._tipax_provider()
        if self.state == 'cancel' or self.tipax_state != 'draft' or self.carrier_tracking_ref:
            raise UserError('Already registered, pending verification or cancelled.')
        c = self.carrier_id
        if not c.tipax_success_callback or not c.tipax_failure_callback:
            raise UserError('Configure both callback URLs.')
        self._tipax_convert(0)
        package = self._tipax_package()
        self.env.cr.execute('SELECT id FROM stock_picking WHERE id=%s FOR UPDATE NOWAIT',[self.id])
        self.invalidate_recordset(['state','tipax_state','carrier_tracking_ref'])
        if self.state == 'cancel' or self.tipax_state != 'draft' or self.carrier_tracking_ref:
            raise UserError('Registration already attempted.')
        trace = 'ODOO-' + uuid.uuid4().hex[:12]

        _logger.warning("TIPAX NEW TRACE CODE: %s", trace)
        _logger.warning("TIPAX MODULE PATH: %s", __file__)
        self.write({'tipax_trace':trace,'tipax_state':'pending','tipax_last_error':False})
        payload = {'packages':[package],'traceCode':trace,'secondaryTraceCode':'','customerSubstationCode':'','discountCode':'','successCallbackUrl':c.tipax_success_callback,'failureCallbackUrl':c.tipax_failure_callback,'receiverKioskId':0}
        try:
            result = provider.request('POST','OmOrder' if self.tipax_direction=='collection' else 'OmOrder/WithPreDefinedOrigin',payload)
            if not isinstance(result, dict):
                raise UserError('Invalid registration response.')
            self.tipax_correlation = result.get('correlationId') or False
            codes = result.get('trackingCodesWithTitles')
            if not isinstance(codes, list) or len(codes) != 1 or not isinstance(codes[0], dict):
                raise UserError('No unique tracking code returned.')
            tracking = codes[0].get('trackingCode')
            if not isinstance(tracking, str) or not tracking.strip():
                raise UserError('Invalid tracking code returned.')
            self.write({'carrier_tracking_ref': tracking.strip(), 'tipax_state': 'pending'})
        except UserError as e:
            self.tipax_last_error = str(e)
            return {'type':'ir.actions.client','tag':'display_notification','params':{'title':'Verify in Tipax before retry','message':str(e),'type':'warning','sticky':True}}

    def action_tipax_track(self):
        self.ensure_one()
        try:
            with self.env.cr.savepoint():
                self._tipax_track()
        except UserError as error:
            self.write({'tipax_last_error': str(error), 'tipax_last_sync': fields.Datetime.now()})
            return {'type': 'ir.actions.client', 'tag': 'display_notification',
                    'params': {'title': 'Tipax tracking', 'message': str(error),
                               'type': 'warning', 'sticky': True}}

    def _tipax_track(self):
        self.ensure_one()
        provider = self._tipax_provider()
        if self.carrier_tracking_ref:
            result = provider.request('POST','Tracking/ByTrackingCode',[self.carrier_tracking_ref])
        else:
            raise UserError('No tracking code. Verify registration in Tipax before retrying.')
        rows = result if isinstance(result, list) else [result]
        matches = [r for r in rows if isinstance(r, dict)
                   and r.get('trackingCode') == self.carrier_tracking_ref]
        if len(matches) != 1:
            raise UserError('No unique matching parcel returned.')
        r = matches[0]
        try:
            status_id = int(r.get('statusId') or 0)
        except (TypeError, ValueError):
            raise UserError('Invalid Tipax status.')
        vals = {'tipax_status': r.get('status'), 'tipax_status_id': status_id,
                'tipax_order_id': r.get('orderId') or self.tipax_order_id,
                'tipax_history': json.dumps(r.get('parcelStatusHistories') or [], ensure_ascii=False, indent=2),
                'tipax_last_sync': fields.Datetime.now(), 'tipax_last_error': False}
        if status_id == 34:
            vals['tipax_state'] = 'cancelled'
        elif self.tipax_state in ('pending', 'sent'):
            vals['tipax_state'] = 'sent' if r.get('orderId') and status_id > 0 else 'pending'
        price = r.get('priceDetail') or {}
        if price.get('finalAmount') is not None:
            vals.update(tipax_final=price['finalAmount'],tipax_company_price=self._tipax_convert(price['finalAmount']))
        self.write(vals)

    def action_tipax_cancel(self):
        for p in self:
            provider = p._tipax_provider()
            if not p.tipax_confirmed or p.tipax_handover:
                raise UserError('Cancellation requires a registered parcel not handed over.')
            p._tipax_track()
            if p.tipax_state == 'cancelled':
                continue
            if not p.tipax_confirmed or p.tipax_status_id != 30:
                raise UserError('Cancellation restricted to collecting status 30 in this test build.')
            provider.request('PUT','Parcels/Cancel/'+quote(p.carrier_tracking_ref,safe=''))
            p.tipax_state='cancel_requested'

    def action_tipax_handover(self):
        for p in self:
            p._tipax_provider()
            if not p.tipax_confirmed or p.tipax_handover or p.tipax_status_id in (34, 50, 51, 52):
                raise UserError('Only registered parcels not already handed over.')
        self.write({'tipax_handover':fields.Datetime.now(),'tipax_handover_user':self.env.uid})

    @api.model
    def _cron_tipax_tracking(self):
        for p in self.search([('tipax_state','in',['sent','pending','cancel_requested']),('carrier_tracking_ref','!=',False),'|',('tipax_state','=','cancel_requested'),('tipax_status_id','not in',[50,51,52])],limit=200,order='tipax_last_sync asc'):
            try:
                with self.env.cr.savepoint():
                    p.with_company(p.company_id)._tipax_track()
            except UserError as e:
                p.write({'tipax_last_error':str(e),'tipax_last_sync':fields.Datetime.now()})