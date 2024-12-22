"""
PDF report generator for crop analysis
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime

class PDFReportGenerator:
    def __init__(self, filename="crop_report.pdf"):
        self.filename = filename
        self.doc = SimpleDocTemplate(filename, pagesize=letter)
        self.styles = getSampleStyleSheet()
        self.elements = []

    def add_header(self, text):
        self.elements.append(Paragraph(text, self.styles['Heading1']))
        self.elements.append(Spacer(1, 12))

    def add_subheader(self, text):
        self.elements.append(Paragraph(text, self.styles['Heading2']))
        self.elements.append(Spacer(1, 8))

    def add_paragraph(self, text):
        self.elements.append(Paragraph(text, self.styles['Normal']))
        self.elements.append(Spacer(1, 6))

    def add_crop_recommendations(self, recommendations):
        self.add_subheader("Mahsul Önerileri")
        data = [["Mahsul", "Uyumluluk Skoru"]]
        for crop, score, _ in recommendations:
            data.append([crop, f"{score:.2f}"])
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        self.elements.append(table)
        self.elements.append(Spacer(1, 12))

    def add_sensor_data(self, sensor_data):
        self.add_subheader("Sensör Verileri")
        data = [["Parametre", "Değer"]]
        for key, value in sensor_data.items():
            data.append([key, f"{value:.1f}"])
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        self.elements.append(table)
        self.elements.append(Spacer(1, 12))

    def add_alerts_and_recommendations(self, alerts, recommendations):
        if alerts:
            self.add_subheader("Uyarılar")
            for alert in alerts:
                self.add_paragraph(f"• {alert}")
        
        if recommendations:
            self.add_subheader("Öneriler")
            for recommendation in recommendations:
                self.add_paragraph(f"• {recommendation}")

    def generate(self):
        """Generate the final PDF report"""
        self.add_header(f"Akıllı Tarım Raporu")
        self.add_paragraph(f"Oluşturulma Tarihi: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        self.doc.build(self.elements)
        return self.filename