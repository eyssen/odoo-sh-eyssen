# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2019-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
#  -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2019-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE URL <https://store.webkul.com/license.html/> for full copyright and licensing details.
#################################################################################
{
  "name"                 :  "Website Product Pack",
  "summary"              :  "Add Bundle Products in your website for increasing your ecommerce",
  "category"             :  "Website",
  "version"              :  "3.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Website-Product-Pack.html",
  "description"          :  """http://webkul.com/blog/odoo-website-product-pack/
                              Website pack product allows you to create the packs or bundles of the products. 
                              You can sell the products in bundles on website. You can create pack products in backend also.
                              """,
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_product_pack&version=13.0",
  "depends"              :  [
                             'wk_product_pack',
                             'website_sale',
                            ],
  "data"                 :  [
                             'data/website_product_pack_data.xml',
                             'views/product_template_view.xml',
                             'views/template.xml',
                             'security/ir.model.access.csv',
                            ],
  "demo":['data/demo.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  30,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}