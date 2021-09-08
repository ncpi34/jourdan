from reportlab.lib.pagesizes import A4
from account.models import CustomUser, Address
from order.models import Order, OrderItems
from reportlab.lib.units import cm, inch, mm, pica, toLength
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import Image
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from abc import ABC

PAGESIZE = A4
BASE_MARGIN = 10 * mm
style_right = ParagraphStyle(name='right', parent=getSampleStyleSheet()['Normal'], alignment=TA_RIGHT)
style_left = ParagraphStyle(name='left', parent=getSampleStyleSheet()['Normal'], alignment=TA_LEFT)


class PdfClass(ABC):
    """
    Class to generate nice pdf
    """

    @classmethod
    def story(cls, buffer, order, request, date):
        doc = SimpleDocTemplate(
            buffer,
            pagesize=PAGESIZE,
            topMargin=BASE_MARGIN,
            leftMargin=BASE_MARGIN,
            rightMargin=BASE_MARGIN,
            bottomMargin=BASE_MARGIN
        )
        img = 'media/img/logo.png'
        logo = Image(img, width=100, height=100)

        body_style = cls.get_body_style()
        title_style = cls.get_title_style()
        footer_style = cls.get_footer_style()
        title_table_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')])
        body_table_style = TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')])

        story = [
            logo,
            Table([
                [
                    [Paragraph("A.R DE COMMANDE N° {}".format(order.unique_number), style_left),
                     Paragraph(f"{cls.get_delivery(order)}", style_left),
                     Paragraph(f"{cls.get_status(order)}", style_left),
                     # Paragraph(f"message: {cls.get_value_or_custom_value(order.message)}", style_left)
                     ],
                    cls.getinfo_from_user(request)
                ],
            ],
                rowHeights=[1 * inch], style=title_table_style),

            Paragraph(f'Commande du {date}', body_style),

            Table(cls.get_products(order.pk), rowHeights=15 * mm, style=body_table_style),

            Paragraph(f'Total:{order.get_total_cost()}€ TTC', body_style),

            Paragraph("Nos B'Elles Saisons - 419 Grand'Rue 34980 Saint-Gély-du-Fesc ", footer_style),

        ]

        doc.build(
            story,
            onFirstPage=cls.add_page_number,
            onLaterPages=cls.add_page_number,
        )

    @staticmethod
    def add_page_number(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 10)
        page_number_text = "%d" % doc.page
        canvas.drawCentredString(
            0.75 * inch,
            0.75 * inch,
            page_number_text
        )
        canvas.restoreState()

    @staticmethod
    def get_title_style():
        sample_style_sheet = getSampleStyleSheet()
        body_style = sample_style_sheet['BodyText']
        body_style.fontSize = 10
        return body_style

    @staticmethod
    def get_body_style():
        sample_style_sheet = getSampleStyleSheet()
        body_style = sample_style_sheet['Heading1']
        body_style.fontSize = 12
        body_style.fonName = 'Helvetica'
        body_style.alignment = TA_CENTER
        body_style.spaceAfter = 40
        body_style.spaceBefore = 40
        body_style.textColor = colors.black
        return body_style

    @staticmethod
    def get_footer_style():
        sample_style_sheet = getSampleStyleSheet()
        body_style = sample_style_sheet['BodyText']
        body_style.fontSize = 8
        body_style.fonName = 'Helvetica'
        body_style.alignment = TA_CENTER
        # body_style.spaceAfter = 40
        body_style.spaceBefore = 10
        body_style.textColor = colors.black
        return body_style

    @staticmethod
    def get_products(order_id):
        products = OrderItems.objects.filter(order__id=order_id)
        tab = []
        for item in products:
            table = [item.article_code, item.name, item.price_with_taxes,
                     item.quantity, item.get_cost_with_taxes()]
            tab.append(table)

        tab.insert(0, ['Référence', 'Désignation', 'Prix Unitaire', 'Quantité', 'Total TTC'])
        return tab

    @staticmethod
    def get_address(user):
        address_list = []
        try:
            address_list0 = Address.objects.filter(user=user).values_list("street")[0][0]
            address_list1 = Address.objects.filter(user=user).values_list("apartment")[0][0]
            address_list2 = " ".join(list(Address.objects.filter(user=user).values_list("zip", "city")[0]))
            address_list.append(Paragraph(f"{address_list0}", style_right))
            address_list.append(Paragraph(f"{address_list1}", style_right))
            address_list.append(Paragraph(f"{address_list2}", style_right))
        except:
            pass
        return address_list

    @classmethod
    def getinfo_from_user(cls, request):
        try:
            user = CustomUser.objects.get(id=request.user.id)
        except Exception:
            user = CustomUser.objects.get(id=request.id)

        user_list = [
            Paragraph(f"Code client: {user.email}", style_right),
            Paragraph(f"Téléphone: {user.phone}", style_right)
        ]

        address_list = cls.get_address(user)
        user_list.append(Paragraph(f"{user.last_name} {user.first_name}", style_right))

        return user_list + address_list

    @staticmethod
    def get_delivery(order):
        if order.delivery:
            return "Livraison"
        return "Click & Collect"

    @staticmethod
    def get_value_or_custom_value(field):
        if field:
            return field
        return ""

    @staticmethod
    def get_status(order):
        if order.status == "Paid":
            return "Payé"
        return "Non Payé"
