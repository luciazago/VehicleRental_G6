from datetime import date
from dateutil.relativedelta import relativedelta
from Vehicles.vehicle import Vehicle

class Truck(Vehicle):
    MAINTENANCE_KMS = 1000
    MAINTENANCE_MONTHS = 2

    def next_itv(self):
        today = date.today()
        next_date = self.matriculation_date + relativedelta(years=1)

        while next_date <= today:
            age = relativedelta(next_date, self.matriculation_date).years
            if age < 10:
                next_date += relativedelta(years=1)
            else:
                next_date += relativedelta(months=6)
        return next_date

    def next_maintenance(self):
        next_date = date.today() + relativedelta(months=self.MAINTENANCE_MONTHS)
        next_km = self.mileage + self.MAINTENANCE_KMS

        return f"Next maintenance: {next_date} or at {next_km:.0f} km"