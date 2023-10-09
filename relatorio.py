import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import locale
from time import gmtime, strftime
from datetime import date, datetime as dt, timedelta as delta
import datetime
from gerarPDF import GeneratePDF
from DadosAbertosONS import DadosONS
from infrastructure.postgres import Postgres
locale.setlocale(locale.LC_ALL, "pt_BR.utf8")

ano=2023
mes=10

# df=DadosONS.constrainedoff(ano, mes)
# print(df)

df=DadosONS.balanco(ano)
print(df)

today = date.today()
last_day = today - delta(2)
last_day = last_day.strftime('%Y-%m-%d %H:%M:%S')
plt.rcParams.update({
    'axes.formatter.use_locale': True,
})
fig, ax = plt.subplots(figsize=(30,20))
# (sns.lineplot(data=df[df['id_subsistema']=='SE'][df['din_instante']>=last_day]['val_carga'],x=df['din_instante']>=last_day, color='orange', label='SUDESTE', linewidth=3.0),
#  sns.lineplot(data=df[df['id_subsistema']=='S'][df['din_instante']>=last_day]['val_carga'], x=df['din_instante']>=last_day, color='blue', label='SUL', linewidth= 3.0),
#  sns.lineplot(data=df[df['id_subsistema']=='N'][df['din_instante']>=last_day]['val_carga'], x=df['din_instante']>=last_day, color='green', label='NORDESTE', linewidth= 3.0),
#  sns.lineplot(data=df[df['id_subsistema']=='NE'][df['din_instante']>=last_day]['val_carga'], x=df['din_instante']>=last_day, color='red', label='NORTE', linewidth= 3.0))
(sns.lineplot(data=df[df['id_subsistema']=='SE'][df['din_instante']>=last_day], x='din_instante', y='val_carga', color='orange', label='SUDESTE', linewidth=3.0),
sns.lineplot(data=df[df['id_subsistema']=='S'][df['din_instante']>=last_day], x='din_instante', y='val_carga', color='blue', label='SUL', linewidth=3.0),
sns.lineplot(data=df[df['id_subsistema']=='N'][df['din_instante']>=last_day], x='din_instante', y='val_carga', color='green', label='NORDESTE', linewidth=3.0),
 sns.lineplot(data=df[df['id_subsistema']=='NE'][df['din_instante']>=last_day], x='din_instante', y='val_carga', color='green', label='NORDESTE', linewidth=3.0))
ax.set_title('Energy Demand - Hourly', fontsize=40)
ax.set_xlabel('DATA', fontsize=30)
ax.set_ylabel('MWmed',fontsize=30)
ax.legend(fontsize=25)
# plt.show()
plt.savefig('figuras\demand.png')

# MMGD

plt.rcParams.update({
    'axes.formatter.use_locale': True,
})
fig, ax = plt.subplots(figsize=(30,20))
(sns.lineplot(data=df[df['id_subsistema']=='SE'][df['din_instante']>=last_day], x='din_instante', y='val_germmgd', color='orange', label='SUDESTE', linewidth=3.0),
sns.lineplot(data=df[df['id_subsistema']=='S'][df['din_instante']>=last_day], x='din_instante', y='val_germmgd', color='blue', label='SUL', linewidth=3.0),
sns.lineplot(data=df[df['id_subsistema']=='N'][df['din_instante']>=last_day], x='din_instante', y='val_germmgd', color='green', label='NORDESTE', linewidth=3.0),
 sns.lineplot(data=df[df['id_subsistema']=='NE'][df['din_instante']>=last_day], x='din_instante', y='val_germmgd', color='green', label='NORDESTE', linewidth=3.0))
ax.set_title('MMGD - Hourly', fontsize=40)
ax.set_xlabel('DATA', fontsize=30)
ax.set_ylabel('MWmed',fontsize=30)
ax.legend(fontsize=25)
plt.savefig('figuras\mmgd.png')

# Hidraulic

plt.rcParams.update({
    'axes.formatter.use_locale': True,
})
fig, ax = plt.subplots(figsize=(30,20))
(sns.lineplot(data=df[df['id_subsistema']=='SE'][df['din_instante']>=last_day], x='din_instante', y='val_gerhidraulica', color='orange', label='SUDESTE', linewidth=3.0),
sns.lineplot(data=df[df['id_subsistema']=='S'][df['din_instante']>=last_day], x='din_instante', y='val_gerhidraulica', color='blue', label='SUL', linewidth=3.0),
sns.lineplot(data=df[df['id_subsistema']=='N'][df['din_instante']>=last_day], x='din_instante', y='val_gerhidraulica', color='green', label='NORDESTE', linewidth=3.0),
 sns.lineplot(data=df[df['id_subsistema']=='NE'][df['din_instante']>=last_day], x='din_instante', y='val_gerhidraulica', color='green', label='NORDESTE', linewidth=3.0))
ax.set_title('Hidraulic Generation - Hourly', fontsize=40)
ax.set_xlabel('DATA', fontsize=30)
ax.set_ylabel('MWmed',fontsize=30)
ax.legend(fontsize=25)
plt.savefig('figuras\hidro.png')

# Thermal Gen
plt.rcParams.update({
    'axes.formatter.use_locale': True,
})
fig, ax = plt.subplots(figsize=(30,20))
(sns.lineplot(data=df[df['id_subsistema']=='SE'][df['din_instante']>=last_day], x='din_instante', y='val_gertermica', color='orange', label='SUDESTE', linewidth=3.0),
sns.lineplot(data=df[df['id_subsistema']=='S'][df['din_instante']>=last_day], x='din_instante', y='val_gertermica', color='blue', label='SUL', linewidth=3.0),
sns.lineplot(data=df[df['id_subsistema']=='N'][df['din_instante']>=last_day], x='din_instante', y='val_gertermica', color='green', label='NORDESTE', linewidth=3.0),
 sns.lineplot(data=df[df['id_subsistema']=='NE'][df['din_instante']>=last_day], x='din_instante', y='val_gertermica', color='green', label='NORDESTE', linewidth=3.0))
ax.set_title('Thermical Generation - Hourly', fontsize=40)
ax.set_xlabel('DATA', fontsize=30)
ax.set_ylabel('MWmed',fontsize=30)
ax.legend(fontsize=25)
plt.savefig('figuras\genterm.png')

# Eolic

plt.rcParams.update({
    'axes.formatter.use_locale': True,
})
fig, ax = plt.subplots(figsize=(30,20))
(sns.lineplot(data=df[df['id_subsistema']=='SE'][df['din_instante']>=last_day], x='din_instante', y='val_gereolica', color='orange', label='SUDESTE', linewidth=3.0),
sns.lineplot(data=df[df['id_subsistema']=='S'][df['din_instante']>=last_day], x='din_instante', y='val_gereolica', color='blue', label='SUL', linewidth=3.0),
sns.lineplot(data=df[df['id_subsistema']=='N'][df['din_instante']>=last_day], x='din_instante', y='val_gereolica', color='green', label='NORDESTE', linewidth=3.0),
 sns.lineplot(data=df[df['id_subsistema']=='NE'][df['din_instante']>=last_day], x='din_instante', y='val_gereolica', color='green', label='NORDESTE', linewidth=3.0))
ax.set_title('Eolic Generation - Hourly', fontsize=40)
ax.set_xlabel('DATA', fontsize=30)
ax.set_ylabel('MWmed',fontsize=30)
ax.legend(fontsize=25)
plt.savefig('figuras\eolic.png')

# Solar
plt.rcParams.update({
    'axes.formatter.use_locale': True,
})
fig, ax = plt.subplots(figsize=(30,20))
(sns.lineplot(data=df[df['id_subsistema']=='SE'][df['din_instante']>=last_day], x='din_instante', y='val_gersolar', color='orange', label='SUDESTE', linewidth=3.0),
sns.lineplot(data=df[df['id_subsistema']=='S'][df['din_instante']>=last_day], x='din_instante', y='val_gersolar', color='blue', label='SUL', linewidth=3.0),
sns.lineplot(data=df[df['id_subsistema']=='N'][df['din_instante']>=last_day], x='din_instante', y='val_gersolar', color='green', label='NORDESTE', linewidth=3.0),
 sns.lineplot(data=df[df['id_subsistema']=='NE'][df['din_instante']>=last_day], x='din_instante', y='val_gersolar', color='green', label='NORDESTE', linewidth=3.0))
ax.set_title('Fotovoltaic Generation - Hourly', fontsize=40)
ax.set_xlabel('DATA', fontsize=30)
ax.set_ylabel('MWmed',fontsize=30)
ax.legend(fontsize=25)
plt.savefig('figuras\solar.png')

GeneratePDF(r'C:\Users\alex.lourenco\Documents\PycharmProjects\BrazilEnergyMarketReport\figuras\demand.png', r'C:\Users\alex.lourenco\Documents\PycharmProjects\BrazilEnergyMarketReport\figuras\mmgd.png',  r'C:\Users\alex.lourenco\Documents\PycharmProjects\BrazilEnergyMarketReport\figuras\hidro.png', r'C:\Users\alex.lourenco\Documents\PycharmProjects\BrazilEnergyMarketReport\figuras\genterm.png', r'C:\Users\alex.lourenco\Documents\PycharmProjects\BrazilEnergyMarketReport\figuras\eolic.png', r'C:\Users\alex.lourenco\Documents\PycharmProjects\BrazilEnergyMarketReport\figuras\solar.png')