from datetime import date
from dateutil.relativedelta import relativedelta
from Vehicles.vehicle import Vehicle


class Motorbike(Vehicle):
    MAINTENANCE_KMS = 1000
    def next_itv(self):
        today = date.today()
        next_date = self.matriculation_date + relativedelta(years=4)

        while next_date <= today:
            next_date += relativedelta(years=2)
        return next_date

    def next_maintenance(self):
        today = date.today()
        next_date = self.matriculation_date + relativedelta(years=1)

        while next_date <= today:
            next_date += relativedelta(years=1)
        next_km = self.mileage + self.MAINTENANCE_KMS
        return f"Next maintenance: {next_date} or at {next_km:.0f} km"