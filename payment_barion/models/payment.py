# coding: utf-8

from datetime import datetime
from uuid import uuid4
import json
import pprint
import logging
import requests

from odoo.http import request
from odoo import api, exceptions, fields, models, _

_logger = logging.getLogger(__name__)

class PaymentAcquirerBarion(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('barion', 'Barion')])
    barion_payee = fields.Char(string='Payee email address', required_if_provider='barion')
    barion_private_key = fields.Char(string='Private key', required_if_provider='barion')
    barion_pixel_enabled = fields.Boolean(string='Use basic Barion Pixel')
    barion_pixel_id = fields.Char(string='Pixel ID', required_if_barion_pixel_enabled=True)
    barion_payment_type = fields.Selection(selection=[('Immediate','Immediate'),('DelayedCapture','Delayed Capture')], string='Payment Type', default='Immediate', required_if_provider='barion')
    
    def barion_get_form_action_url(self):
        self.ensure_one()
        return '/payment/barion/prepare_transaction'

    def _get_feature_support(self):
        """Get advanced feature support by provider.

        Each provider should add its technical in the corresponding
        key for the following features:
            * fees: support payment fees computations
            * authorize: support authorizing payment (separates
                         authorization and capture)
            * tokenize: support saving payment data in a payment.tokenize
                        object
        """
        res = super(PaymentAcquirerBarion, self)._get_feature_support()
        res['fees'].append('barion')
        res['authorize'].append('barion')
        return res


class TxBarion(models.Model):
    _inherit = 'payment.transaction'

    @api.model
    def _barion_form_get_tx_from_data(self, data):
        """ Given a data dict coming from barion, verify it and find the related
        transaction record. """
        reference = data.get('paymentId')
        
        if not reference:
            _logger.info('Barion: received data with missing reference')
            raise ValidationError(error_msg)
        tx = self.search([('acquirer_reference', '=', reference)])
        if not tx or len(tx) > 1:
            error_msg = 'Barion: received data for reference %s' % (reference)
            if not tx:
                error_msg += '; no order found'
            else:
                error_msg += '; multiple order found'
            _logger.info(error_msg)
            raise ValidationError(error_msg)
        return tx[0]

    def get_status(self):
        #get payment state data
        barion_data = {
            "POSKey": self.acquirer_id.barion_private_key,
            "PaymentId": self.acquirer_reference
        }

        url = 'https://api.test.barion.com/v2/Payment/GetPaymentState' if self.acquirer_id.state == 'test' else 'https://api.barion.com/v2/Payment/GetPaymentState'
        resp = requests.get(url, params = barion_data)
        _logger.info("Barion request: Received response:\n%s", resp.content)

        resp.raise_for_status()
        resp = json.loads(resp.content)
        return resp

    def process(self, status):
        if status == "Succeeded":
            self._set_transaction_done()
        if status == "Authorized":
            self._set_transaction_authorized()
        if status == "Canceled":
            self._set_transaction_cancel()
        if status == "Failed" or status == "Expired":
            self._set_transaction_error()

    def capture_transaction(self):
        resp=self.get_status()
        transactions = []
        for tr in resp.get("Transactions"):
            transactions.append({"TransactionId": tr.get("TransactionId")})

        barion_data = {
            "POSKey": self.acquirer_id.barion_private_key,
            "PaymentId": self.acquirer_reference,
            "Transactions": transactions
        }
        
        url = 'https://api.test.barion.com/v2/Payment/Capture' if self.acquirer_id.state == 'test' else 'https://api.barion.com/v2/Payment/Capture'
        resp = requests.post(url, json=barion_data)
        _logger.info("Barion request: Received response:\n%s", resp.content)

        resp.raise_for_status()
        resp = json.loads(resp.content)

        if resp.get("IsSuccessful"):
            self.process(resp.get("Status"))
            return True
        return False

    def void_transaction(self):
        barion_data = {
            "POSKey": self.acquirer_id.barion_private_key,
            "PaymentId": self.acquirer_reference
        }

        url = 'https://api.test.barion.com/v2/Payment/CancelAuthorization' if self.acquirer_id.state == 'test' else 'https://api.barion.com/v2/Payment/CancelAuthorization'
        resp = requests.post(url, json=barion_data)
        _logger.info("Barion request: Received response:\n%s", resp.content)

        resp.raise_for_status()
        resp = json.loads(resp.content)

        if resp.get("IsSuccessful"):
            self.process(resp.get("Status"))
            return True
        return False

    # def refund_transaction(self):
    #     resp=self.get_status()
    #     transactions = []
    #     for tr in resp.get("Transactions"):
    #         transactions.append({"TransactionId": tr.get("TransactionId")})

    #     barion_data = {
    #         "POSKey": self.acquirer_id.barion_private_key,
    #         "PaymentId": self.acquirer_reference,
    #         "Transactions": [{
    #             "TransactionId": transactions
    #         }]
    #     }

    #     url = 'https://api.test.barion.com/v2/Payment/Capture' if self.acquirer_id.state == 'test' else 'https://api.barion.com/v2/Payment/Capture'
    #     resp = requests.get(url, params = barion_data)
    #     _logger.info("Barion request: Received response:\n%s", resp.content)

    #     resp.raise_for_status()
    #     resp = json.loads(resp.content)

    #     if not resp.get("Errors") or resp.get("Errors") == []:
    #         self.process(resp.get("Status"))
    #     else:
    #         raise Warning(_('Refund could not be completed'), resp.get("Errors"))

    def action_capture(self):
        if any([t.state != 'authorized' for t in self]):
            raise ValidationError(_('Only transactions having the capture status can be captured.'))
        for tx in self:
            tx.capture_transaction()

    def action_void(self):
        if any([t.state != 'authorized' for t in self]):
            raise ValidationError(_('Only transactions being authorized can be canceled.'))
        for tx in self:
            tx.void_transaction()

    def barion_s2s_capture_transaction(self, **kwargs):
        self.ensure_one()
        return self.capture_transaction()

    def barion_s2s_void_transaction(self, **kwargs):
        self.ensure_one()
        return self.void_transaction()
    
    # def action_refund(self):
    #     if any([t.state != 'done' for t in self]):
    #         raise ValidationError(_('Only transactions being authorized can be canceled.'))
    #     for tx in self:
    #         tx.refund_transaction()