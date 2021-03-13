# -*- coding: utf-8 -*-
##############################################################################
#
#    eYssen IT Services Ltd.
#    Copyright (C) 2008-TODAY eYssen IT Services Ltd. (<https://eyssen.hu>).
#    Author: eYssen IT Services (<https://eyssen.hu>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': u"Helpdesk Project Integration",
    'description': """
        Helpdesk Project Integration
    """,
    'summary': """
        Helpdesk Project Integration
     """,
    'author': "eYssen IT Services",
    'website': "https://eyssen.hu",
    'category': 'Project',
    'version': '13.0.1.0.0',
    'license': 'LGPL-3',

    'depends': [
        'helpdesk',
        'helpdesk_timesheet',
        'project',
    ],

    'data': [
        'views/helpdesk_project.xml',
    ],
    
    'application': False,
    'installable': True,
    'auto_install': False,
}
