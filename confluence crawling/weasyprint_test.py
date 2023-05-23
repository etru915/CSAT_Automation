import sys
from PyQt5.QtGui import QTextDocument
from PyQt5 import QtGui, QtWidgets, QtPrintSupport
from PyQt5.QtWidgets import QApplication



app = QApplication(sys.argv)

doc = QTextDocument
location = "C:/Users/zeno915/Desktop/pycharm/pdf_test.pdf"
html = open("C:/Users/zeno915/Desktop/aa.html" ,encoding='cp949').read()
doc.setHtml(html)

printer = QtPrintSupport()
printer.setOutputFileName(location)
printer.setOutputFormat(QtPrintSupport.PdfFormat)
printer.setPageSize(QtPrintSupport.A4)
printer.setPageMargins (15,15,15,15,QtPrintSupport.Millimeter)

doc.print_(printer)
print ("done!")