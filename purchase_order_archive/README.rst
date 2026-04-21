Description
===========

On a system with a high volume of purchases, the number of purchase
orders displayed in the list view can become huge. This module allows to
archive Purchase Orders that are in status Locked or Cancelled.

If a purchase order is archived, it will be hidden from the purchase
orders list view.

This module only depends on module purchase, but it could be used in
combination with OCA module 'record_archiver' in order to automatically
archive old purchase orders.


Usecase
=======




Installation
============




Configuration
=============




Usage
=====

To archive purchase orders, you need to:

1. Open the tree view of purchase orders.
2. Select a purchase order (in status Locked or Cancelled) you want to
   archive.
3. Click on Action > Archive. Confirm.
4. The purchase order is now archived.

To unarchive purchase orders, you need to:

1. Open the tree view of purchase orders.
2. In the filter box select the Archived filter. The list of archived
   purchase orders will be displayed.
3. Select the purchase order (in status Locked or Cancelled) you want to
   restore to Active.
4. Click on Action > Unarchive.
5. The purchase order is now active.


Contributer
===========

- Andrea Stirpe <a.stirpe@onestein.nl>
- Christihan Laurel <laurel@vauxoo.com>
- `Binhex <https://binhex.cloud/>`__:

  - Mario Luis <m.luis@binhex.cloud>


Credits
=======




History
=======



