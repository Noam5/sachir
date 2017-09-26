# -*- coding: utf-8 -*-

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer
from calc import *


class MatrixHishtalmutFund(HishtalmutFund):
    MAX_BASE_SALARY = 15712

    def get_max_base_salary(self):
        """

        """
        return self.MAX_BASE_SALARY


class MyPensionFund(PensionFund):
    MAX_BASE_SALARY = 19000

    def get_max_base_salary(self):
        """
        חישוב סכום מבוטח לקרן פנסיה
        """
        return self.MAX_BASE_SALARY


class MyManagersInsurance(ManagersInsurance):

    def __init__(self, bruto, pension_fund):
        """

        """
        ManagersInsurance.__init__(self)
        self.bruto = bruto
        self.pension_fund = pension_fund

    def get_max_base_salary(self):
        """
        חישוב סכום מבוטח לביטוח מנהלים
        """
        return self.bruto - self.pension_fund.get_max_base_salary()


def parse_matrix_salary_pdf(pdf_path):
    fp = open(pdf_path, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser)
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    for page in PDFPage.create_pages(document):

        # read the page into a layout object
        interpreter.process_page(page)
        layout = device.get_result()

        # loop over the object list
        for obj in layout._objs:

            if int(obj.bbox[0]) == 377 and obj.bbox[2] == 409.075:
                health_insurance = float(obj.get_text().strip().replace(",", ""))

            if int(obj.bbox[0]) == 479 and obj.bbox[2] == 510.555:
                bituah_leumi = float(obj.get_text().strip().replace(",", ""))

            if int(obj.bbox[0]) == 539 and obj.bbox[2] == 571.217:
                mas = float(obj.get_text().strip().replace(",", ""))

            if int(obj.bbox[0]) == 30 and obj.bbox[2] == 67.217:
                bruto_salary = float(obj.get_text().split()[0].replace(",", ""))
                # ניכויי התחייבות
                other_fees = float(obj.get_text().split()[4].replace(",", ""))
                neto_salary = float(obj.get_text().split()[5].replace(",", ""))

            if int(obj.bbox[0]) == 39 and obj.bbox[2] == 55.152:
                zicui_points = float(obj.get_text().strip().replace(",", ""))

            #if obj.bbox[2] == 218.595:
            #    #zicui_points = float(obj.get_text().strip().replace(",", ""))
            #    obj.get_text().split(".")

    return health_insurance, bituah_leumi, mas, bruto_salary, zicui_points, other_fees, neto_salary

def main():
    printed_health_insurance, printed_bituah_leumi, printed_tax, printed_salary, zicui_points, other_fees, printed_neto_salary = parse_matrix_salary_pdf("/home/noam/workspace/Salary calculator/PaySlip2016-06.pdf")

    print "Monthly salary: %s, zicui points: %s" % (printed_salary, zicui_points)

    # Define funds
    pf = MyPensionFund()
    hf = MatrixHishtalmutFund()
    mi = MyManagersInsurance(printed_salary, pf)

    # Define salary and add the funds
    m = MonthlySalary(printed_salary, zicui_points)
    m.add_fund(pf)
    m.add_fund(hf)
    m.add_fund(mi)

    # calculate neto
    calculated_tax, calculated_health_insurance, calculated_bituah_leumi, calculated_neto = m.calc()
    calculated_neto = calculated_neto - other_fees

    print
    print "tax, calculated :%s, printed: %s, diff: %s" % (calculated_tax, printed_tax, calculated_tax - printed_tax)
    print "health insurance, calculated :%s, printed: %s" % (calculated_health_insurance, printed_health_insurance)
    print "bituah leumi, calculated :%s, printed: %s" % (calculated_bituah_leumi, printed_bituah_leumi)
    print "neto, calculated: %s, printed: %s, diff: %s" % (calculated_neto, printed_neto_salary, calculated_neto - printed_neto_salary)

if __name__ == "__main__":
    main()
