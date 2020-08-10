# -*- coding: utf-8 -*-
import json
import pprint
import logging
import requests

from werkzeug import urls, utils
from odoo import http, _
from odoo.http import request
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)

class BarionController(http.Controller):

    @http.route(['/payment/barion/callback'], type='http', auth='public', csrf=False)
    def payment_barion_callback(self, paymentId, **post):
        acquirer_reference = paymentId if paymentId else post.get('paymentId')
        transaction = request.env['payment.transaction'].sudo().search([('acquirer_reference', '=', acquirer_reference)], limit=1)
        
        resp = transaction.get_status()
        
        status = resp.get("Status")
        _logger.info("Barion payment status: %s", status)
        
        transaction.process(status)

        return "OK"


    @http.route(['/payment/barion/prepare_transaction'], type='http', auth='public', csrf=False)
    def payment_barion_prepare_transaction(self, **post):

        baseurl = http.request.env['ir.config_parameter'].get_param('web.base.url')
        transaction = request.env['payment.transaction'].search([('reference', '=', post.get('reference'))], limit=1)

        barion_items = []
        for order in transaction.sale_order_ids:
            #order.action_done()
            order_lines = order.order_line if isinstance(order.order_line, list) else [order.order_line]
            for line in order_lines:
                #_logger.info('Order line: %s', pprint.pformat(line.fields_get()))
                barion_items.append({
                    "Name": line.name_short,
                    "Description": line.name,
                    "Quantity": line.product_uom_qty,
                    "Unit": line.product_uom.name,
                    "UnitPrice": line.price_unit,
                    "ItemTotal": line.price_total,
                    "SKU": line.product_id.default_code
                })
        
        barion_data = {
            "POSKey": transaction.acquirer_id.barion_private_key,
            "PaymentType": transaction.acquirer_id.barion_payment_type,
            "PaymentRequestId": transaction.reference,
            "GuestCheckOut": "true",
            "FundingSources": ["All"],
            "Currency": transaction.currency_id.name,
            "Transactions": [
                {
                    "POSTransactionId": transaction.reference,
                    "Payee": transaction.acquirer_id.barion_payee,
                    "Total": transaction.amount,
                    "Items": barion_items
                }
            ],
            "RedirectUrl": baseurl + transaction.return_url,
            "CallbackUrl": baseurl + "/payment/barion/callback"
        }

        if transaction.acquirer_id.barion_payment_type == "DelayedCapture":
            barion_data["DelayedCapturePeriod"] = '7.00:00:00'

        _logger.info('Barion data %s', pprint.pformat(barion_data))

        url = 'https://api.test.barion.com/v2/Payment/Start' if transaction.acquirer_id.state == 'test' else 'https://api.barion.com/v2/Payment/Start'
        resp = requests.post(url, json=barion_data)
        _logger.info("Barion request: Received response:\n%s", resp.content)

        resp.raise_for_status()
        resp = json.loads(resp.content)

        transaction.write({
            "acquirer_reference": resp.get("PaymentId")
        })

        return utils.redirect(resp.get("GatewayUrl"))
