Description
===========

This module extends the functionality of product to support dimensions
(length, width and height). Also computes the volume automatically when
you change one of these dimensions.

This module was previously hosted on
https://github.com/ingadhoc/odoo-addons and before that on
https://launchpad.net/~ingenieria-adhoc.


Usecase
=======




Installation
============




Configuration
=============




Usage
=====

To use this module :

1. Go to Product View > Inventory
2. Edit Dimensional UoM and the three dimensions

If the product has got more than one variant, the dimensions (and the
volume) are visible only in the variants.


Contributer
===========

- Juan Jose Scarafia <jjs@ingadhoc.com>
- Leonardo Pistone <leonardo.pistone@camptocamp.com>
- Denis Leemann <denis.leemann@camptocamp.com>
- Kumar Aberer <kumar.aberer@braintec-group.com>
- `C2i Change 2 improve <http://www.c2i.es>`__:

  - Eduardo Magdalena <emagdalena@c2i.es>

- Carlos Lopez <celm1990@gmail.com>
- `Trobz <https://trobz.com>`__:

  - Thao Le <thaolt@trobz.com>


Credits
=======

The migration of this module from 16.0 to 17.0 was financially supported
by Camptocamp.


History
=======

| [ The change log. The goal of this file is to help readers
| understand changes between version. The primary audience is end users
  and integrators. Purely technical changes such as code refactoring
  must not be mentioned here.

This file may contain ONE level of section titles, underlined with the ~
(tilde) character. Other section markers are forbidden and will likely
break the structure of the README.rst or other documents where this
fragment is included. ]

13.0.1.0.0 (2020-04-16)
-----------------------

- [MIG] Migration from Odoo 12.0 to 13.0
- [IMP] Black, isort, prettier

16.0.1.0.0 (2022-10-11)
-----------------------

- [MIG] Migration from Odoo 15.0 to 16.0
- [IMP] Black, isort, prettier (pre-commit)

