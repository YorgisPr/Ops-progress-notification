#%%
# Import the required Module
import tabula
# Read a PDF File
df = tabula.read_pdf("maren.pdf", pages='all')[0]
# convert PDF into CSV
tabula.convert_into("maren.pdf", "maren.csv", output_format="csv", pages='all')
print(df)


#%%
import pdfplumber
from openpyxl import Workbook
import os

# %%
def keep_visible_lines(obj):
    """If the object is a hidden line, remove it."""
    if obj["object_type"] == "rect":
        return obj["non_stroking_color"] == 0

    return True
# %%
    # with pdfplumber.open(r"C:\Users\pir.gprountzos\Downloads\maren.pdf") as pdf:
    # workbook = Workbook()
    # sheet = workbook.active

    # for page in pdf.pages:
    #     page = page.filter(keep_visible_lines)
    #     table = page.extract_table()

    #     for row in table:
    #         sheet.append(([None] * (6 - len(row))) + row)

    #     workbook.save("Excel1.xlsx")

import pdfplumber
from openpyxl import Workbook

with pdfplumber.open(r"C:\\Users\\pir.gprountzos\\Downloads\\maren.pdf") as p:
    workbook = Workbook()  # New blank Excel workbook
    sheet = workbook.active  # activation sheet
    for i in range(1,6):  # Traverse 4 pages-6 page
        page = p.pages[i]
        table = page.extract_table()  # Extract table data
        print(table)
        for row in table:  # Traverse all rows
            print(row)
            sheet.append(row)  # Append write data by row
        workbook.save(r"C:\\Users\\pir.gprountzos\\Downloads\\Excel1.xlsx")  # Save file named Excel
        print("The first%d page PDF Extraction complete" % i) 

