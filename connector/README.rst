
Description
===========

This is a framework designed to build connectors with external systems,
usually called ``Backends`` in the documentation.

Documentation: http://odoo-connector.com

It features:

-  A jobs queue

      In which the connectors can push functions (synchronization tasks)
      to be executed later.

-  An event pattern

      The connectors can subscribe listener functions on the events,
      executed when the events are fired.

-  Connector base classes

      Called ``ConnectorUnit``.

      Include base classes for the use in connectors, ready to be
      extended:

      -  ``Synchronizer``: flow of an import or export
      -  ``Mapper``: transform a record according to mapping rules
      -  ``Binder``: link external IDs with local IDS
      -  ``BackendAdapter``: adapter interface for the exchanges with
         the backend
      -  But ``ConnectorUnit`` can be extended to accomplish any task

-  A multi-backend support

      Each ``ConnectorUnit`` can be registered amongst a backend type
      (eg. Magento) and a backend version (allow to have a different
      ``Mapper`` for each backend's version for instance)

It is used for example used to connect
`Magento <http://odoo-magento-connector.com>`__ and
`Prestashop <https://github.com/OCA/connector-prestashop>`__, but also
used with Solr, CMIS, ...





Usage
=====

This module does nothing on its own. It is a ground for developing
advanced connector modules. For further information, please go on:
http://odoo-connector.com


Contributer
===========

-  Guewen Baconnier at Camptocamp
-  Alexandre Fayolle at Camptocamp
-  Benoit Guillot at Akretion
-  Nicolas Bessi at Camptocamp
-  Joël Grand-Guillaume at Camptocamp
-  Arthur Vuillard at Akretion
-  Sebastien Beau at Akretion
-  Laurent Mignon at Acsone
-  Leonardo Pistone at Camptocamp
-  David Béal at Akretion
-  Christophe Combelles at Anybox
-  Stéphane Bidoul at Acsone
-  Malte Jacobi at IBO / HTW
-  Laetitia Gangloff at Acsone
-  David Lefever at Taktik S.A.
-  Jos de Graeve at Apertoso NV
-  Jean-Sébastien Suzanne at Anybox
-  Leonardo Donelli at MONK Software
-  Mathias Colpaert
-  Yannick Vaucher at Camptocamp
-  Nicolas Piganeau at NDP Systèmes
-  Florent Thomas at Mind And Go
-  Matthieu Dietrich at Camptocamp
-  Olivier Laurent at Acsone
-  Eric Antones at NuoBiT Solutions S.L.
-  Asier Neira at Factor Libre S.L.
-  Nguyen Minh Chien at Trobz.


Credits
=======

The migration of this module from 18.0 to 19.0 was financially supported
by Camptocamp.


History
=======

Next
----

12.0.1.0.0 (2018-11-26)
-----------------------

-  [MIGRATION] from 12.0 branched at rev. 324e006


