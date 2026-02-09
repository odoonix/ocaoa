# Copyright 2013-2020 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import models


class SetJobsToDone(models.TransientModel):
    _inherit = "queue.requeue.job"
    _name = "queue.jobs.to.done"
    _description = "Set all selected jobs to done"

    def set_done(self):
<<<<<<< HEAD
        # Only jobs with state WAIT_DEPENDENCIES, PENDING, ENQUEUED or FAILED
        # will change to DONE
=======
>>>>>>> parent of 17a8035 ([UP]remove modules)
        jobs = self.job_ids
        jobs.button_done()
        return {"type": "ir.actions.act_window_close"}
