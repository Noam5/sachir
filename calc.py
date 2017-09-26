# -*- coding: utf-8 -*-

# שכר ממוצע במשק
AVG_SALARY_IN_ECONOMY = 9049

class Fund(object):
    """
    קרן
    """
    def __init__(self):
        self.accumulation = 0

    def deposit(self, amount):
        """
        הפקדה
        """
        self.accumulation += amount

class PensionFund(Fund):
    """
    קרן פנסיה
    """
    def __init__(self):
        Fund.__init__(self)
        self.mekadem_kitzba = "?"

    def calculate_kitzbat_pensia(self):
        """
        חישוב קצבת פנסיה חודשית
        """
        return self.accumulation / self.mekadem_kitzba

    def calculate_tikrat_pikadon_lekeren_pensia(self):
        """
        תקרת פיקדון לקרן פנסיה
        """
        return (2 * AVG_SALARY_IN_ECONOMY) * 0.205

    def get_max_base_salary(self):
        """

        """
        raise NotImplementedError("Abstract method")

    def calculate_deposit(self, insured_salary, year, month):
        """
        חישוב הפקדה לקרן פנסיה
        """
        if year >= 2017:
            # from 1.1.17
            this_month_percent = 0.065
        elif year <= 2016 and month <= 6:
            # Until 30.6.16
            this_month_percent = 0.05
        else:
            # from 1.7.16 until 31.12.16
            this_month_percent = 0.0625

        employees_deposit = insured_salary * this_month_percent
        employeers_deposit = insured_salary * this_month_percent
        pitzuim = insured_salary * 1/12
        return employees_deposit, employeers_deposit, pitzuim

class HishtalmutFund(Fund):
    """
    קרן השתלמות
    """
    def get_max_base_salary(self):
        """

        """
        raise NotImplementedError("Abstract method")


class Insurance(object):
    pass


class ManagersInsurance(Fund):
    """
    ביטוח מנהלים
    """
    def calculate_deposit(self, insured_salary, year, month):
        """
        חישוב הפקדה לביטוח מנהלים
        """
        this_month_percent = 5.0 / 100

        employees_deposit = insured_salary * this_month_percent
        employeers_deposit = insured_salary * this_month_percent
        pitzuim = insured_salary * 1/12
        return employees_deposit, employeers_deposit, pitzuim

class GemelBox(object):
    """
    קופת גמל
    """
    pass

class MonthlySalary(object):
    """
    משכורת חודשית
    """
    def __init__(self, bruto, zicui_points):
        self.bruto = bruto
        self.neto = bruto
        self.zicui_points = zicui_points
        self.funds = []

    def add_fund(self, fund):
        """

        """
        self.funds.append(fund)

    def add_insurance(self, fund):
        """

        """
        pass

    def employee_deposit_to_fund(self, fund, amount):
        """

        """
        print "Employee deposits %s shekel to %s" % (amount, fund)
        fund.deposit(amount)
        self.neto -= amount

    def employer_deposit_to_fund(self, fund, amount):
        """

        """
        print "Employer deposits %s shekel to %s" % (amount, fund)
        fund.deposit(amount)

    def calculate_tax_by_salary_and_zicui(self, salary, zicui_points):
        """
        חישוב מס לפי שכר ונקודות זיכוי
        """
        tax_levels_salary = [5220, 8920, 13860, 19800, 41410, 66960]
        tax_levels = [0.1, 0.14, 0.21, 0.31, 0.34, 0.48, 0.5]

        zicui_points = zicui_points * 216
        tax = 0

        if (salary > tax_levels_salary[5]):
            tax += (salary - tax_levels_salary[5]) * tax_levels[6]
            salary = tax_levels_salary[5]

        if (salary > tax_levels_salary[4]):
            tax += (salary - tax_levels_salary[4]) * tax_levels[5]
            salary = tax_levels_salary[4]

        if (salary > tax_levels_salary[3]):
            tax += (salary - tax_levels_salary[3]) * tax_levels[4]
            salary = tax_levels_salary[3]

        if (salary > tax_levels_salary[2]):
            tax += (salary - tax_levels_salary[2]) * tax_levels[3]
            salary = tax_levels_salary[2]

        if (salary > tax_levels_salary[1]):
            tax += (salary - tax_levels_salary[1]) * tax_levels[2]
            salary = tax_levels_salary[1]

        if (salary > tax_levels_salary[0]):
            tax += (salary - tax_levels_salary[0]) * tax_levels[1]
            salary = tax_levels_salary[0]

        if (salary > 0):
            tax += salary * tax_levels[0]


        if (tax - zicui_points < 0):
            return 0
        return round(tax - zicui_points)


    def tax_deduction(self):
        """
        ניכוי מס הכנסה
        """
        tax = self.calculate_tax_by_salary_and_zicui(self.bruto, self.zicui_points)
        print "Paying %.2f shekel to taxes" % tax
        self.neto -= tax
        return tax

    def health_insurance_deduction(self):
        """
        ניכוי ביטוח בריאות
        """
        deduction = 3.10 / 100 * 5678

        if deduction > 0:
            deduction += (self.bruto - 5678) * 5.00 / 100

        print "Paying %.2f to Health insurance" % deduction
        self.neto -= deduction
        return deduction

    def bituah_leumi_deduction(self):
        """
        ניכוי ביטוח לאומי
        """
        deduction = 0.40 / 100 * 5678

        if deduction > 0:
            deduction += (self.bruto - 5678) * 7.00 / 100

        print "Paying %.2f to bituah leumi" % deduction
        self.neto -= deduction
        return deduction

    def calc(self):
        """

        """
        tax = self.tax_deduction()
        health_insurance = self.health_insurance_deduction()
        bituah_leumi = self.bituah_leumi_deduction()

        for fund in self.funds:
            if isinstance(fund, HishtalmutFund):
                max_base_salary = fund.get_max_base_salary()
                employee_deposit = max_base_salary / 4.0 / 10
                employer_deposit = (max_base_salary / 4.0) * 3 / 10
                self.employee_deposit_to_fund(fund, employee_deposit)
                self.employer_deposit_to_fund(fund, employer_deposit)
            elif isinstance(fund, PensionFund) or isinstance(fund, ManagersInsurance):
                max_base_salary = fund.get_max_base_salary()
                employee_deposit, employer_deposit, pitzuim = fund.calculate_deposit(max_base_salary, 2016, 6)
                self.employee_deposit_to_fund(fund, employee_deposit)
                self.employer_deposit_to_fund(fund, employer_deposit)
                self.employer_deposit_to_fund(fund, pitzuim)

        return tax, health_insurance, bituah_leumi, self.neto

def calculate_sheerim_pension_salary(insured_salary):
    """
    חישוב שכר שארים מהפנסיה
    """
    return 0.6 * insured_salary



def calculate_mas_on_pitzuim(years_worked):
    """
    חישוב מס על פיצויים לאחר פיטורין
    """
    ptor_mas_each_year = 12000
    return years_worked * ptor_mas_each_year
