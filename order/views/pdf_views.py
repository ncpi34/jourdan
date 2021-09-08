from django.http import HttpResponse
from order.models import Order
import io
from order.pdf_class import PdfClass
import logging

db_logger = logging.getLogger('db')


class PdfCreator(PdfClass):

    @classmethod
    def build_pdf(cls, request, **kwargs):
        try:
            db_logger.info("DEBUT order/pdf_views")
            # get file name
            file_name: str = Order.objects.get(id=int(kwargs['order_id'])).unique_number
            db_logger.info(f"file_name => {file_name}")

            # get order
            order: Order = Order.objects.get(id=int(kwargs['order_id']))
            db_logger.info(f"order => {order}")

            # get date split
            date: str = str(order.date)[0:10]
            db_logger.info(f"date => {date}")

            # create file
            buffer = io.BytesIO()
            data = cls.story(buffer, order, request, date)

            # send response to browser
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=' + file_name + '.pdf'
            response.write(buffer.getvalue())

            # close buffer
            buffer.close()
            db_logger.info("FIN order/pdf_views")
            return response
        except Exception as e:
            db_logger.exception(f"erreur order/pdf_views => {e}")
