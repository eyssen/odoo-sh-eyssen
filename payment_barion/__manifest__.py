# -*- coding: utf-8 -*-

{
    'name': 'Barion Payment Acquirer',
    'author': 'eYssen IT Services',
    'website': 'https://eyssen.hu',
    'category': 'Accounting/Payment',
    'summary': 'Payment Acquirer: Barion Implementation',
    'version': '1.0',
    'description': """Barion Payment Acquirer""",
    'depends': ['payment','website'],
    'data': [
        'views/payment_views.xml',
        'views/payment_barion_templates.xml',
        'data/payment_acquirer_data.xml',
    ],
    'installable': True,
    'post_init_hook': 'create_missing_journal_for_acquirers',
    'uninstall_hook': 'uninstall_hook',
}
