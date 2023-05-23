import pdfkit
import wkhtmltopdf

config = pdfkit.configuration(wkhtmltopdf='C:/PythonProjects/wkhtmltox-0.12.5-1.msvc2015-win64')
link = 'https://kms.coupang.net/pages/viewpage.action?pageId=4391357'
save = "C:/Users/zeno915/Desktop/pycharm/pdf_test.pdf"
save2 = "C:/Users/zeno915/Desktop/pycharm/pdf_test1.pdf"
pdfkit.from_url('http://google.com', save)

# pdfkit.from_file('test.html', 'out.pdf')
# pdfkit.from_string('Hello!', 'out.pdf')



pdfkit.from_url('http://google.com', save2, configuration=config)

