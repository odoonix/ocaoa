
Description
===========

This module implements a component system and is a base block for the
Connector Framework. It can be used without using the full Connector
though.

Documentation: http://odoo-connector.com/

You may also want to check the `Introduction to Odoo
Components <https://dev.to/guewen/introduction-to-odoo-components-bn0>`__
by @guewen.





Usage
=====

As a developer, you have access to a component system. You can find the
documentation in the code or on http://odoo-connector.com

In a nutshell, you can create components:

::

   from odoo.addons.component.core import Component

   class MagentoPartnerAdapter(Component):
       _name = 'magento.partner.adapter'
       _inherit = 'magento.adapter'

       _usage = 'backend.adapter'
       _collection = 'magento.backend'
       _apply_on = ['res.partner']

And later, find the component you need at runtime (dynamic dispatch at
component level):

::

   def run(self, external_id):
       backend_adapter = self.component(usage='backend.adapter')
       external_data = backend_adapter.read(external_id)

In order for tests using components to work, you will need to use the
base class provided by \`odoo.addons.component.tests.common\`:

-  TransactionComponentCase

There are also some specific base classes for testing the component
registry, using the ComponentRegistryCase as a base class. See the
docstrings in tests/common.py.


Contributer
===========

-  Guewen Baconnier <guewen.baconnier@camptocamp.com>
-  Laurent Mignon <laurent.mignon@acsone.eu>
-  Simone Orsi <simone.orsi@camptocamp.com>
-  Thien Vo <thienvh@trobz.com>


Credits
=======

The migration of this module from 18.0 to 19.0 was financially supported
by Camptocamp.


History
=======

16.0.1.0.0 (2022-10-04)
-----------------------

-  [MIGRATION] from 15.0

15.0.1.0.0 (2021-11-25)
-----------------------

-  [MIGRATION] from 14.0

14.0.1.0.0 (2020-10-22)
-----------------------

-  [MIGRATION] from 13.0

13.0.1.0.0 (2019-10-23)
-----------------------

-  [MIGRATION] from 12.0

12.0.1.0.0 (2018-10-02)
-----------------------

-  [MIGRATION] from 11.0 branched at rev. 324e006


