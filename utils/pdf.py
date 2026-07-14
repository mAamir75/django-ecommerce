import weasyprint
from django.template.loader import render_to_string
from django.contrib.staticfiles import finders





def generate_invoice_pdf(order):

    html = render_to_string('orders/order/pdf.html', {'order':order})
    return weasyprint.HTML(string=html).write_pdf(stylesheets=[weasyprint.CSS(finders.find('css/pdf.css'))])