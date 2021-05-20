import datetime

from trade_platform.models import WorkShiftPlan, WorkShift, Position

SET_UP_DATA = {
    'default': {
        'plan_name': '',
        'work_shifts_count': 10,
        'work_shift_positions': 5,
        'start_date': datetime.date.today(),
        'end_date': datetime.date.today()
    },
    0: {
        'plan_name': 'plan1',
        'work_shifts_count': 10,
        'work_shift_positions': 5,
        'start_date': datetime.date.today(),
        'end_date': datetime.date.today()
    },
    1: {
        'plan_name': 'plan2',
        'work_shifts_count': 15,
        'work_shift_positions': 10,
        'start_date': datetime.date.today(),
        'end_date': datetime.date.today()
        },
    2: {
        'plan_name': 'plan3',
        'work_shifts_count': 13,
        'work_shift_positions': 3,
        'start_date': datetime.date.today(),
        'end_date': datetime.date.today()
        }
}

class ShiftPlanCreator:

    @staticmethod
    def create_work_shifts(plan, work_shifts_count):
        workshift_objects = WorkShift.objects.bulk_create([WorkShift(name=number, workshit_plan=plan) for number in range(int(work_shifts_count))])

        return workshift_objects

    @staticmethod
    def create_shift_plan(plan_name, start_date, end_date):
        plan = WorkShiftPlan.objects.create(
            name=plan_name,
            startdate=start_date,
            enddate=end_date,
        )

        return plan

    @staticmethod
    def assign_positions(work_shifts, positions):
        for work_shift in work_shifts:
            work_shift.positions.set(positions) #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


    @staticmethod
    def create_positions(amount):
        position_objects = Position.objects.bulk_create(
            [Position(first_name=number, last_name=number) for number in range(int(amount))])

        return position_objects

    @staticmethod
    def create_test_data(amount):
        positions_objects = ShiftPlanCreator.create_positions(amount)
        for entry in range(len(SET_UP_DATA)-1):
            set_up_data = SET_UP_DATA.get(entry, SET_UP_DATA['default'])
            plan = ShiftPlanCreator.create_shift_plan(set_up_data['plan_name'],
                                                      set_up_data['start_date'],
                                                      set_up_data['end_date'])
            work_shifts = ShiftPlanCreator.create_work_shifts(plan,
                                                             set_up_data['work_shifts_count'])
            if len(positions_objects)<=set_up_data['work_shift_positions']:
                ShiftPlanCreator.assign_positions(work_shifts,
                                                  positions_objects[:int(set_up_data['work_shift_positions'])])
            else:
                ShiftPlanCreator.assign_positions(work_shifts,
                                                  positions_objects)
