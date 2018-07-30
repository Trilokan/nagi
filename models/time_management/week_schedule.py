# -*- coding: utf-8 -*-

from odoo import fields, api, exceptions
from datetime import datetime, timedelta
from .. import surya


# Week Schedule

PROGRESS_INFO = [('draft', 'Draft'), ('scheduled', 'Scheduled')]
TIME_DELAY_HRS = 5
TIME_DELAY_MIN = 30


class WeekSchedule(surya.Sarpam):
    _name = "week.schedule"
    _inherit = "mail.thread"

    from_date = fields.Date(string="From Date", required=True)
    till_date = fields.Date(string="Till Date", required=True)
    schedule_detail = fields.One2many(comodel_name="week.schedule.detail",
                                      inverse_name="schedule_id",
                                      string="Schedule Detail")
    off_detail = fields.One2many(comodel_name="week.off.detail",
                                 inverse_name="schedule_id",
                                 string="Week-Off Detail")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    writter = fields.Text(string="Writter", track_visibility="always")

    @api.constrains("from_date", "till_date")
    def check_date(self):
        """ From Date < Till Date """
        from_date = datetime.strptime(self.from_date, "%Y-%m-%d")
        till_date = datetime.strptime(self.till_date, "%Y-%m-%d")
        if from_date > till_date:
            raise exceptions.ValidationError("Error! From Date should be greater than Till Date")

        days = (till_date - from_date).days + 1

        if days != 7:
            raise exceptions.ValidationError("Error! From Date and Till Date should be within a week")

        if from_date.weekday() != 0:
            raise exceptions.ValidationError("Error! Week should start from Monday")

        week_schedule = self.env["week.schedule"].search_count([("from_date", "=", self.from_date),
                                                                ("till_date", "=", self.till_date)])
        if week_schedule > 1:
            raise exceptions.ValidationError("Error! Duplicate Week Schedule")

    def generate_attendance(self):
        from_date = datetime.strptime(self.from_date, "%Y-%m-%d")
        till_date = datetime.strptime(self.till_date, "%Y-%m-%d")
        date_range = (till_date - from_date).days + 1

        recs = self.schedule_detail

        for day in range(0, date_range):
            current_date_obj = from_date + timedelta(days=day)
            next_date_obj = current_date_obj + timedelta(days=1)
            current_date = current_date_obj.strftime("%Y-%m-%d")
            next_date = next_date_obj.strftime("%Y-%m-%d")

            attendance_detail = []
            for rec in recs:
                for person_id in rec.person_ids:
                    expected_from_time = "{0} {1}:{2}:00".format(current_date,
                                                                 rec.shift_id.from_hours,
                                                                 rec.shift_id.from_minutes)

                    if rec.shift_id.end_day == 'current_day':
                        expected_till_time = "{0} {1}:{2}:00".format(current_date,
                                                                     rec.shift_id.till_hours,
                                                                     rec.shift_id.till_minutes)
                    elif rec.shift_id.end_day == 'next_day':
                        expected_till_time = "{0} {1}:{2}:00".format(next_date,
                                                                     rec.shift_id.till_hours,
                                                                     rec.shift_id.till_minutes)

                    new_from_time_obj = datetime.strptime(expected_from_time, "%Y-%m-%d %H:%M:%S") - timedelta(minutes=(TIME_DELAY_HRS * 60) + TIME_DELAY_MIN)
                    new_till_time_obj = datetime.strptime(expected_till_time, "%Y-%m-%d %H:%M:%S") - timedelta(minutes=(TIME_DELAY_HRS * 60) + TIME_DELAY_MIN)

                    record_data = {"shift_id": rec.shift_id.id,
                                   "person_id": person_id.id,
                                   "day_progress": "working_day",
                                   "expected_from_time": new_from_time_obj.strftime("%Y-%m-%d %H:%M:%S"),
                                   "expected_till_time": new_till_time_obj.strftime("%Y-%m-%d %H:%M:%S")}

                    holiday = self.env["week.off.detail"].search([("date", "=", current_date),
                                                                  ("person_ids", "=", person_id.id),
                                                                  ("schedule_id", "=", self.id)])

                    if holiday:
                        record_data["day_progress"] = "holiday"

                    attendance_detail.append((0, 0, record_data))

            month_id = self.env["month.attendance"].search([("period_id.from_date", "<=", current_date),
                                                            ("period_id.till_date", ">=", current_date)])

            if not month_id:
                raise exceptions.ValidationError("Error! Attendance Month is not set")

            self.env["time.attendance"].create({"date": current_date,
                                                "month_id": month_id.id,
                                                "attendance_detail": attendance_detail})

    @api.multi
    def trigger_schedule(self):
        self.check_date()
        self.generate_attendance()
        self.write({'progress': 'scheduled'})

    @api.constrains('schedule_detail', 'off_detail')
    def check_employee_duplication(self):
        recs = self.schedule_detail

        person_list = []
        for rec in recs:
            for person_id in rec.person_ids:
                if person_id.id in person_list:
                    raise exceptions.ValidationError("Error! Employee {0} assign to multiple shift".format(person_id.name))
                person_list.append(person_id.id)

        recs = self.off_detail

        for rec in recs:
            if (self.from_date > rec.date) or (rec.date > self.till_date):
                raise exceptions.ValidationError("Error! Week-Off date must be within a week")


class WeekScheduleDetail(surya.Sarpam):
    _name = "week.schedule.detail"

    shift_id = fields.Many2one(comodel_name="time.shift", string="Shift", required=True)
    person_ids = fields.Many2many(comodel_name="hos.person", string="Employee", required=True)
    schedule_id = fields.Many2one(comodel_name="week.schedule", string="Schedule")
    progress = fields.Selection(PROGRESS_INFO, string='Progress', related='schedule_id.progress')


class WeekOffDetail(surya.Sarpam):
    _name = "week.off.detail"

    date = fields.Date(string="Date", required=True)
    person_ids = fields.Many2many(comodel_name="hos.person", string="Employee", required=True)
    schedule_id = fields.Many2one(comodel_name="week.schedule", string="Schedule")
    progress = fields.Selection(PROGRESS_INFO, string='Progress', related='schedule_id.progress')

