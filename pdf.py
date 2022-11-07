import pdfkit

def make_pdf():
    #the tutorial: https://python-bloggers.com/2022/06/convert-html-to-pdf-using-python/
    #Define path to wkhtmltopdf.exe
    path_to_wkhtmltopdf = r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
    #Define path to HTML file
    path_to_file = 'htmlTable.html'
    #Point pdfkit configuration to wkhtmltopdf.exe
    config = pdfkit.configuration()
    #Convert HTML file to PDF
    pdfkit.from_file(path_to_file, output_path='pomodoroSummary.pdf', configuration=config)

    print(" pdf making is done")