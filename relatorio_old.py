import pandas as pd
from Postgres.Postgres import Postgres
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import locale
from time import gmtime, strftime
from datetime import date, datetime as dt, timedelta as delta
import datetime
from reportlab.pdfgen import canvas
from gerarPDF import GeneratePDF
import pyodbc
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
locale.setlocale(locale.LC_ALL, "pt_BR.utf8")

query = f'''select 
                previsto_para,
                modelo,
                fonte,
                bacia,
                sub_bacia,
                valor
            from public.vw_historico_previsao_precipitacao
            where previsto_em = '2021-10-18'
            and modelo in ('ETA40', 'GEFS', 'ECENS', 'ETAGEFS')
            and percentil = 'avg'
            --and fonte = 'ONS'
            order by previsto_para, bacia, sub_bacia;
            '''
query_pld = f'''select 
                previsto_em,
                previsto_para,
                sudeste,
                sul,
                nordeste,
                norte,
                importancia,
                inserido_em
            from series_semanais.preco_decomp
            where previsto_em = '2022-11-18'
            '''
db_pld = Postgres(database='SeriesTemporaisCcee')
aux_pld = db_pld.read(query=query_pld, to_dict=True)
pld = pd.DataFrame(data=aux_pld)

query_prec = f'''select 
                data_hora,
                pld,
                submercado,
                inserido_em
            from series_horarias.preco_oficial            
            '''
aux_prec_oficial = db_pld.read(query=query_prec, to_dict=True)
preco_oficial = pd.DataFrame(data=aux_prec_oficial)
#print(preco_oficial)

plt.rcParams.update({
    'axes.formatter.use_locale': True,
})
today = date.today()
last_day = today - delta(30)
last_day_all = today - delta(60)
last_day = last_day.strftime('%Y-%m-%d %H:%M:%S')
fig, ax = plt.subplots(figsize=(30,20))
(sns.lineplot(data=preco_oficial[preco_oficial['submercado']=='SUDESTE'][preco_oficial['data_hora']>=last_day]['pld'], color='orange', label='SUDESTE', linewidth=3.0),
 sns.lineplot(data=preco_oficial[preco_oficial['submercado']=='SUL'][preco_oficial['data_hora']>=last_day]['pld'], color='blue', label='SUL', linewidth= 3.0),
 sns.lineplot(data=preco_oficial[preco_oficial['submercado']=='NORDESTE'][preco_oficial['data_hora']>=last_day]['pld'], color='green', label='NORDESTE', linewidth= 3.0),
 sns.lineplot(data=preco_oficial[preco_oficial['submercado']=='NORTE'][preco_oficial['data_hora']>=last_day]['pld'], color='red', label='NORTE', linewidth= 3.0))
ax.set_title('Preço de Liquidação das Diferenças - Diário', fontsize=50)
ax.set_xlabel('DATA', fontsize=40)
ax.set_ylabel('R$/ MWmed',fontsize=40)
ax.legend(fontsize=25)
# plt.show()
#plt.savefig('pld.png')

def rpacomercializadora():
    connection_string = "DRIVER={SQL Server};SERVER=CL01VTF02ENVSQL;DATABASE=RPACOMERCIALIZADORA;UID=UGPL01T02F58;PWD=P.GaX1Y2zP"
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
    engine = create_engine(connection_url)
    return engine
#def armazenamento():
eng = rpacomercializadora()
query_earm = """SELECT 
           data, 
           SECO,
           S,
           NE,
           N
        FROM ENA.BASE_EARM"""
df = pd.read_sql(query_earm, eng)
last = last_day_all.strftime('%Y-%m-%d')
fig, ax = plt.subplots(figsize=(30,20))
(sns.lineplot(data=df[df['data'] >= last]['SECO'], color='orange', label='SUDESTE', linewidth=3.0),
 sns.lineplot(data=df[df['data'] >= last]['S'], color='blue', label='SUL', linewidth=3.0),
 sns.lineplot(df[df['data'] >= last]['N'], color='green', label='NORDESTE', linewidth=3.0),
 sns.lineplot(data=df[df['data'] >= last]['NE'], color='red', label='NORTE', linewidth=3.0))
ax.set_title('ENERGIA ARMAZENADA', fontsize=50)
ax.set_xlabel('DATA', fontsize=40)
ax.set_ylabel('PERCENTUAL (%)',fontsize=40)
ax.legend(fontsize=25)
# plt.show()
plt.savefig('earm.png')

query_ena = """SELECT 
           data, 
           SECO,
           S,
           NE,
           N
        FROM ENA.BASE_ENA"""

df_ena = pd.read_sql(query_ena, eng)
last = last_day_all.strftime('%Y-%m-%d')
fig, ax = plt.subplots(figsize=(30,20))
(sns.lineplot(data=df_ena[df_ena['data'] >= last]['SECO'], color='orange', label='SUDESTE', linewidth=3.0),
 sns.lineplot(data=df_ena[df_ena['data'] >= last]['S'], color='blue', label='SUL', linewidth=3.0),
 sns.lineplot(data=df_ena[df_ena['data'] >= last]['N'], color='green', label='NORDESTE', linewidth=3.0),
 sns.lineplot(data=df_ena[df_ena['data'] >= last]['NE'], color='red', label='NORTE', linewidth=3.0))
ax.set_title('ENERGIA NATURAL AFLUENTE Submercado', fontsize=50)
ax.set_xlabel('DATA', fontsize=40)
ax.set_ylabel('MWmed',fontsize=40)
ax.legend(fontsize=20)
# plt.show()
plt.savefig('ena.png')

# Preco Mesa
query_prec_mesa = f'''select 
                data_marcacao,
                produto,
                inicio_suprimento,
                fim_suprimento,
                fonte,
                tipo_preco,
                preco_bid,
                preco_ask
            from public.marcacao_mercado            
            '''
db_mercado = Postgres(database='DadosMercado')
aux_prec_mesa = db_mercado.read(query=query_prec_mesa, to_dict=True)
preco_oficial_mesa = pd.DataFrame(data=aux_prec_mesa)
print(preco_oficial_mesa)
#print(preco_oficial_mesa[preco_oficial_mesa['produto']=='M0'][preco_oficial_mesa['tipo_preco']=='Fixo']['preco_bid'])
fig, ax = plt.subplots(figsize=(30,20))
(sns.lineplot(data=preco_oficial_mesa[preco_oficial_mesa['produto']=='M0'][preco_oficial_mesa['data_marcacao']>=last_day_all][preco_oficial_mesa['tipo_preco']=='Fixo']['preco_bid'], color='orange', label='M0-PRECO FIXO', linewidth=3.0),
 sns.lineplot(data=preco_oficial_mesa[preco_oficial_mesa['produto']=='M1'][preco_oficial_mesa['data_marcacao']>=last_day_all][preco_oficial_mesa['tipo_preco']=='Fixo']['preco_bid'], color='blue', label='M1-PRECO FIXO', linewidth=3.0),
 sns.lineplot(data=preco_oficial_mesa[preco_oficial_mesa['produto']=='M2'][preco_oficial_mesa['data_marcacao']>=last_day_all][preco_oficial_mesa['tipo_preco']=='Fixo']['preco_bid'], color='green', label='M2-PRECO FIXO', linewidth=3.0),
 sns.lineplot(data=preco_oficial_mesa[preco_oficial_mesa['produto']=='M3'][preco_oficial_mesa['data_marcacao']>=last_day_all][preco_oficial_mesa['tipo_preco']=='Fixo']['preco_bid'], color='red', label='M3-PRECO FIXO', linewidth=3.0))
ax.set_title('PREÇO DE MERCADO', fontsize=50)
ax.set_xlabel('DATA', fontsize=40)
ax.set_ylabel('R$/MWmed',fontsize=40)
ax.legend(fontsize=20)
#plt.show()
# plt.savefig('mercado.png')
#Mercado Trimestre
day = today - delta(4)
fig, ax = plt.subplots(figsize=(30,20))
(sns.lineplot(data=preco_oficial_mesa[preco_oficial_mesa['produto']=='Q1/A1'][preco_oficial_mesa['data_marcacao']>=day]['preco_bid'], color='orange', label='Q1/A1-PRECO FIXO', linewidth=3.0),
 sns.lineplot(data=preco_oficial_mesa[preco_oficial_mesa['produto']=='Q2/A1'][preco_oficial_mesa['data_marcacao']>=day]['preco_bid'], color='blue', label='Q2/A1-PRECO FIXO', linewidth=3.0),
 sns.lineplot(data=preco_oficial_mesa[preco_oficial_mesa['produto']=='Q3/A1'][preco_oficial_mesa['data_marcacao']>=day]['preco_bid'], color='green', label='Q3/A1-PRECO FIXO', linewidth=3.0),
 sns.lineplot(data=preco_oficial_mesa[preco_oficial_mesa['produto']=='Q4/A1'][preco_oficial_mesa['data_marcacao']>=day]['preco_bid'], color='red', label='Q4/A1-PRECO FIXO', linewidth=3.0))
ax.set_title('PREÇO DE MERCADO - TRIMESTRE', fontsize=50)
ax.set_xlabel('DATA', fontsize=40)
ax.set_ylabel('R$/MWmed',fontsize=40)
ax.legend(fontsize=20)
#plt.show()
plt.savefig('mercado_tri.png')


# ENA POR BACIA
query_ena_res = """SELECT 
           data, 
           GRANDE,
           PARANAIBA,
           TIETE,
           PARANAPANEMA_SE,
           PARANA,
           PARAGUAI,
           PARAIBA_DO_SUL,
           DOCE,
           MUCURI,
           ITABAPOANA, 
           SAO_FRANCISCO_SE,
           TOCANTINS_SE, 
           JEQUITINHONHA_SE,
           AMAZONAS_SE,
           ITAJAI,
           CAPIVARI,
           PARANAPANEMA_S,
           URUGUAI,
           IGUACU,
           XINGU,
           AMAZONAS_N,
           ARAGUARI,
           TOCANTINS_N,
           SAO_FRANCISCO_NE,
           PARNAIBA,
           PARAGUACU          
        FROM ENA.ENA_BACIA"""
df_ena_bacia = pd.read_sql(query_ena_res, eng)
last = last_day_all.strftime('%Y-%m-%d')
fig, ax = plt.subplots(figsize=(30,20))
(sns.lineplot(data=df_ena_bacia[df_ena_bacia['data'] >= last][['GRANDE','PARANAIBA','TIETE', 'PARAIBA_DO_SUL', 'PARANA', 'PARANAPANEMA_SE', 'SAO_FRANCISCO_SE','TOCANTINS_SE']], color='orange', linewidth=3.0))
 # sns.lineplot(data=df_ena_bacia[df_ena_bacia['data'] >= last], color='blue', label='SUL', linewidth=3.0),
 # sns.lineplot(df_ena_bacia[df_ena_bacia['data'] >= last], color='green', label='NORDESTE', linewidth=3.0),
 # sns.lineplot(data=df_ena_bacia[df_ena_bacia['data'] >= last], color='red', label='NORTE', linewidth=3.0))
ax.set_title('ENA POR BACIA - SUDESTE', fontsize=50)
ax.set_xlabel('DATA', fontsize=40)
ax.set_ylabel('MWmed',fontsize=40)
ax.legend(fontsize=10)
# plt.show()
# plt.savefig('ena_sudeste.png')



GeneratePDF(r'C:\Users\alex.lourenco\PycharmProjects\RelatorioOnePage\pld.png', r'C:\Users\alex.lourenco\PycharmProjects\RelatorioOnePage\earm.png', r'C:\Users\alex.lourenco\PycharmProjects\RelatorioOnePage\ena.png', r'C:\Users\alex.lourenco\PycharmProjects\RelatorioOnePage\mercado.png', r'C:\Users\alex.lourenco\PycharmProjects\RelatorioOnePage\ena_sudeste.png', r'C:\Users\alex.lourenco\PycharmProjects\RelatorioOnePage\mercado_tri.png')





