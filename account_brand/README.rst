
Description
===========

This module allows you to send branded invoices to your customers. It
adds a brand field on the invoice and the brand information to the PDF
report.


Usecase
=======




Installation
============




Configuration
=============

It is important to note that the "brand use level" **should** be set to
``Optional`` or ``Required``. The brand use level is configured in the
Users & Companies settings. By default it is set to 'Do not use brands
on business document'. Then the field to select a brand on the invoice
view will not be available.

To change the "brand use level":

#. Go to Settings > General Settings #. Select the brand use level, the
following options are available:
``Do not use brands on business document`` (Default) ``Optional``
``Required``


Usage
=====

To use this module, you need to:

1. Go to Accounting > Customers > Invoices
2. Select or create an invoice
3. Enter the information and select the brand
4. Print the PDF report. It includes the style and information of the
   brand.

To do point 4, the `Brand External Report
Layout <https://github.com/OCA/brand/tree/18.0/brand_external_report_layout/README.rst>`__
OCA module must be installed.


Contributer
===========

-  Raphael Lee <rlee@opensourceintegrators.com>
-  Steve Campbell <scampbell@opensourceintegrators.com>
-  Maxime Chambreuil <mchambreuil@opensourceintegrators.com>
-  `Obertix <https://www.obertix.net>`__:

   -  Vicent Cubells

-  Ammar Officewala <aofficewala@opensourceintegrators.com>
-  bosd <<c5e2fd43-d292-4c90-9d1f-74ff3436329a@anonaddy.me>


Credits
=======

-  Open Source Integrators <https://www.opensourceintegrators.com>


History
=======




Development
===========



