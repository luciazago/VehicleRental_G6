from datetime import date
from dateutil.relativedelta import relativedelta
from Vehicles.vehicle import Vehicle


class Car(Vehicle):
    def next_itv(self):
        today = date.today()
        next_date = self.matriculation_date + relativedelta(years=4)

        while next_date <= today:
            age = relativedelta(next_date, self.matriculation_date).years

            if age < 10:
                next_date += relativedelta(years=2)
            else:
                next_date += relativedelta(years=1)
        return next_date

    def next_maintenance(self):
        today = date.today()
        next_date = self.matriculation_date + relativedelta(years=1)

        while next_date <= today:
            next_date += relativedelta(years=1)
        return f"Next maintenance: {next_date}"