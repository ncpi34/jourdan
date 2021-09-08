from order.models import Order
import io
from order.pdf_class import PdfClass
import os


class PDFGenerator(PdfClass):
    """
    Pdf Generator Class
    get infos and call class method PdfClass
    """

    @classmethod
    def build_pdf(cls, user, order):
        filename = order.unique_number
        order = Order.objects.get(id=order.pk)
        date = str(order.date)[0:10]

        # open buffer
        buffer = io.BytesIO()

        cls.story(buffer, order, user, date)
        pdf_buffer = buffer.getvalue()

        # create directory
        if not os.path.exists('pdf_clients'):
            os.makedirs('pdf_clients')

        file = open(f"pdf_clients/{filename}.pdf", "wb")
        file.write(pdf_buffer)

        # close buffer
        buffer.close()

        return f"pdf_clients/{filename}.pdf"
