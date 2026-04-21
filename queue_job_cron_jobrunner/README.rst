Description
===========

This module implements a simple ``queue.job`` runner using ``ir.cron``
triggers.

It's meant to be used on environments where the regular job runner can't
be run, like on Odoo.sh.

Unlike the regular job runner, where jobs are dispatched to the
HttpWorkers, jobs are processed on the CronWorker threads by the job
runner crons. This is a design decision because:

- Odoo.sh puts HttpWorkers to sleep when there's no network activity
- HttpWorkers are meant for traffic. Users shouldn't pay the price of
  background tasks.

For now, it only implements the most basic features of the ``queue_job``
runner, notably no channel capacity nor priorities. Please check the
ROADMAP for further details.


Usecase
=======




Installation
============




Configuration
=============

Warning

Don't use this module if you're already running the regular
``queue_job`` runner.

For the easiest case, no configuration is required besides installing
the module.

To avoid CronWorker CPU timeout from abruptly stopping the job
processing cron, it's recommended to launch Odoo with
``--limit-time-real-cron=0``, to disable the CronWorker timeout
altogether.

Note

In Odoo.sh, this is done by default.

Parallel execution of jobs can be achieved by leveraging multiple
``ir.cron`` records:

- Make sure you have enough CronWorkers available (Odoo CLI
  ``--max-cron-threads``)
- Duplicate the ``queue_job_cron`` cron record as many times as needed,
  until you have as much records as cron workers.


Usage
=====




Contributer
===========

- `Camptocamp <https://www.camptocamp.com>`__

     - Iván Todorovich <ivan.todorovich@camptocamp.com>


Credits
=======




History
=======



