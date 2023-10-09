from reportlab.pdfgen import canvas
import tkinter as tk
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

def GeneratePDF(fig, fig1, fig2, fig3, fig4, fig5):
    try:
        nome_pdf = 'EnergyReport'  #input('Informe o nome do PDF: ')
        pdf = canvas.Canvas('{}.pdf'.format(nome_pdf))
        # x = 720
        # x -= 20
        #pdf.drawString(247, x, 'al')
        pdf.drawImage(fig, 30, 620, width=250, height=180)
        pdf.drawImage(fig1, 270, 620, width=250, height=180)
        pdf.drawImage(fig2, 270, 450, width=250, height=180)
        pdf.drawImage(fig3, 30, 450, width=250, height=180)
        pdf.drawImage(fig4, 270, 270, width=250, height=180)
        pdf.drawImage(fig5, 30, 270, width=250, height=180)
        pdf.setTitle(nome_pdf)
        pdf.setFont("Helvetica-Oblique", 18)
        pdf.drawString(200,800, 'Brazilian Energy Market Report')
        pdf.setFont("Helvetica-Bold", 12)
        pdf.save()
        print('{}.pdf criado com sucesso!'.format(nome_pdf))
    except:
        print('Erro ao gerar {}.pdf'.format(nome_pdf))
