# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 09:31:55 2019

@author: B04770
"""

#############################

from pylab import savefig


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def GraficarCat_vs_TGT(df, campo, tgt):
    df['rank'] = round(df[campo].rank(pct=True) * 9)
    
    a = pd.DataFrame(df.groupby([campo])[['idx']].agg('nunique', np.sum)).reset_index()
    a.columns= [campo, 'Clientes']
    b = pd.DataFrame(df.groupby([campo])[[tgt]].agg( np.sum)).reset_index()
    c = a.merge(b, how='left')
    c['TGT_p'] = (c[tgt] / c['Clientes'] )* 100
    c['TGT_p'] = round(c['TGT_p'].astype('int64') ) 
    c['TGT'] = round(c['TGT'].astype('int64') )
    c['Clientes'] = round(c['Clientes'].astype('int64'))
    
    width = .35 # width of a bar
    
    c[['Clientes']].plot(kind='bar', width = width)
    c['TGT_p'].plot(secondary_y=True, color='g')
    
    ax = plt.gca()
    ax.set_xticklabels(c[campo])
    
    savefig('graph.png')
          
    return c
    
def GraficarNum_vs_TGT(df, campo, tgt):        
    df['rank'] = round(df[campo].rank(pct=True) * 9)
    v = pd.DataFrame(df.groupby(['rank'])[campo].agg([np.min, np.max])).reset_index()
    a = pd.DataFrame(df.groupby(['rank'])[['idx']].agg('nunique', np.sum)).reset_index()
    a.columns= ['rank', 'Clientes']
    b = pd.DataFrame(df.groupby(['rank'])[[tgt]].agg( np.sum)).reset_index()
    c = v.merge(a, how='left').merge(b, how='left')    
    c['TGT_p'] = round(c[tgt] / c['Clientes'] * 100)
        
    c['TGT_p'] = round(c['TGT_p'].astype('int64'))    
    c['TGT'] = round(c['TGT'].astype('int64'),)
    c['Clientes'] = round(c['Clientes'].astype('int64'))
    c['amax'] = round(c['amax'].astype('float64'), 1)
    c['amin'] = round(c['amin'].astype('float64'), 1)   
    
    width = .35 # width of a bar    
    c[['Clientes']].plot(kind='bar', width = width)
    c['TGT_p'].plot(secondary_y=True, color='g')
    
    ax = plt.gca()
    ax.set_xticklabels((c['rank']))    
    savefig('graph.png')
        
    return c
    

def Graficar_Variables(pDataFrame, categorical_variables, tgt):
    
    from fpdf import FPDF
    numerical_cols = pDataFrame.columns[~pDataFrame.columns.isin(categorical_variables)]
    
    pdf = FPDF()
    
    if 1 > 2:
        for campo in numerical_cols :
            if campo != 'idx':
                print('---------------------' , campo)
                print('---------------------' )
                df = GraficarNum_vs_TGT(pDataFrame, campo, tgt)            
                pdf.add_page()
                pdf.set_xy(0, 0)
                pdf.set_font('arial', 'B', 10)
                pdf.cell(60)
                pdf.cell(75, 10, "Análisis de la variable " + campo, 0, 2, 'C')
                pdf.cell(90, 10, " ", 0, 2, 'C')
                pdf.set_xy(0, 30)
                pdf.cell(30, 10, 'Rank', 1, 0, 'C')
                pdf.cell(30, 10, 'Mínimo', 1, 0, 'C')
                pdf.cell(30, 10, 'Máximo', 1, 0, 'C')
                pdf.cell(30, 10, 'Clientes', 1, 0, 'C')
                pdf.cell(30, 10, 'TGT', 1, 0, 'C')
                pdf.cell(30, 10, '% TGT', 1, 2, 'C')
                pdf.set_font('arial', '', 10)
                renglon = 40        
                for i in range(0, len(df)):
                    pdf.set_xy(0, renglon)
                    renglon += 10
                    pdf.cell(30, 10, '%s' % (df['rank'].iloc[i]), 1, 0, 'C')
                    pdf.cell(30, 10, '%s' % (str(df.amin.iloc[i])), 1, 0, 'C')
                    pdf.cell(30, 10, '%s' % (str(df.amax.iloc[i])), 1, 0, 'C')
                    pdf.cell(30, 10, '%s' % (str(df.Clientes.iloc[i])), 1, 0, 'C')
                    pdf.cell(30, 10, '%s' % (str(df.TGT.iloc[i])), 1, 0, 'C')
                    pdf.cell(30, 10, '%s' % (str(df.TGT_p.iloc[i])), 1, 2, 'C')                    
                pdf.cell(90, 10, " ", 0, 2, 'C')
                pdf.cell(-150)        
                pdf.image('graph.png', x = None, y = None, w = 0, h = 0, type = '', link = '')
        
    for campo in numerical_cols :
        if campo != 'idx':
            print(campo)
            df = GraficarCat_vs_TGT(pDataFrame, campo, tgt)            
            pdf.add_page()
            pdf.set_xy(0, 0)
            pdf.set_font('arial', 'B', 10)
            pdf.cell(60)
            pdf.cell(75, 10, "Análisis de la variable " + campo, 0, 2, 'C')
            pdf.cell(90, 10, " ", 0, 2, 'C')
            pdf.set_xy(0, 30)
            pdf.cell(30, 10, campo, 1, 0, 'C')
            pdf.cell(30, 10, 'Clientes', 1, 0, 'C')
            pdf.cell(30, 10, 'TGT', 1, 0, 'C')
            pdf.cell(30, 10, '% TGT', 1, 2, 'C')
            pdf.set_font('arial', '', 10)
            renglon = 40        
            for i in range(0, len(df)):
                pdf.set_xy(0, renglon)
                renglon += 10
                pdf.cell(30, 10, '%s' % (df[campo].iloc[i]), 1, 0, 'C')
                pdf.cell(30, 10, '%s' % (str(df.Clientes.iloc[i])), 1, 0, 'C')
                pdf.cell(30, 10, '%s' % (str(df.TGT.iloc[i])), 1, 0, 'C')
                pdf.cell(30, 10, '%s' % (str(df.TGT_p.iloc[i])), 1, 2, 'C')            
            pdf.cell(90, 10, " ", 0, 2, 'C')
            pdf.cell(-150)        
            pdf.image('graph.png', x = None, y = None, w = 0, h = 0, type = '', link = '')            

            plt.close('all')
            
    pdf.output(r'C:\Users\b04770\Desktop\Findo_8_Python\test.pdf', 'F')

#Graficar_Variables(ABT_Final, categorical_cols, 'TGT')


def Graficar_Variables2(pDataFrame, categorical_variables, tgt):
    # pDataFrame = df[a.col]
    # pDataFrame = ABT_Final
    # categorical_variables= categorical_cols
    #tgt = 'TGT'
    from fpdf import FPDF
    numerical_cols = pDataFrame.columns[~pDataFrame.columns.isin(categorical_variables)]    
    for campo in numerical_cols :            
        if (campo != 'idx') & (campo != 'cuit') & (campo != 'Unnamed: 0') :
            try:
                print('---------------------' , campo)
                print('---------------------' )
                pdf = FPDF()
    
                df = GraficarNum_vs_TGT(pDataFrame, campo, tgt)            
                pdf.add_page()
                pdf.set_xy(0, 0)
                pdf.set_font('arial', 'B', 10)
                pdf.cell(60)
                pdf.cell(75, 10, "Análisis de la variable " + campo, 0, 2, 'C')
                pdf.cell(90, 10, " ", 0, 2, 'C')
                pdf.set_xy(30, 30)
                pdf.cell(30, 5, 'Rank', 1, 0, 'C')
                pdf.cell(30, 5, 'Mínimo', 1, 0, 'C')
                pdf.cell(30, 5, 'Máximo', 1, 0, 'C')
                pdf.cell(30, 5, 'Clientes', 1, 0, 'C')
                pdf.cell(30, 5, 'TGT', 1, 0, 'C')
                pdf.cell(30, 5, '% TGT', 1, 2, 'C')
                pdf.set_font('arial', '', 10)
                renglon = 35
                for i in range(0, len(df)):
                    if renglon > 250:
                        renglon = 10                 
                        pdf.add_page()
                    pdf.set_xy(30, renglon)
                    renglon += 5
                    pdf.cell(30, 5, '%s' % (df['rank'].iloc[i]), 1, 0, 'C')
                    pdf.cell(30, 5, '%s' % (str(df.amin.iloc[i])), 1, 0, 'C')
                    pdf.cell(30, 5, '%s' % (str(df.amax.iloc[i])), 1, 0, 'C')
                    pdf.cell(30, 5, '%s' % (str(df.Clientes.iloc[i])), 1, 0, 'C')
                    pdf.cell(30, 5, '%s' % (str(df.TGT.iloc[i])), 1, 0, 'C')
                    pdf.cell(30, 5, '%s' % (str(df.TGT_p.iloc[i])) + '%', 1, 2, 'C')                    
                pdf.cell(90, 30, " ", 0, 2, 'C')
                pdf.set_xy(30, renglon + 40)  
                pdf.image('graph.png', x = None, y = None, w = 0, h = 0, type = '', link = '')
                pdf.output(r'./' + campo + '.pdf', 'F')
            except:
                print('error ', campo)
                pass
    for campo in categorical_variables:
        if (campo != 'idx') & (campo != 'cuit') & (campo != 'Unnamed: 0') :
            try:
                pdf = FPDF()
                print('---------------------' , campo)
                print('---------------------' )
                df = GraficarCat_vs_TGT(pDataFrame, campo, tgt)            
                
                pdf.add_page()
                pdf.set_xy(0, 0)
                pdf.set_font('arial', 'B', 10)
                pdf.cell(60)
                pdf.cell(75, 10, "Análisis de la variable " + campo, 0, 2, 'C')
                pdf.cell(90, 10, " ", 0, 2, 'C')
                pdf.set_xy(30, 30)
                pdf.cell(50, 5, campo, 1, 0, 'C')
                pdf.cell(30, 5, 'Clientes', 1, 0, 'C')
                pdf.cell(30, 5, 'TGT', 1, 0, 'C')
                pdf.cell(30, 5, '% TGT', 1, 2, 'C')
                pdf.set_font('arial', '', 10)
                renglon = 35
                for i in range(0, len(df)):                
                    if renglon > 250:
                        renglon = 10                 
                        pdf.add_page()
                    pdf.set_xy(30, renglon)
                    renglon += 5                
                    pdf.cell(50, 5, '%s' % (df[campo].iloc[i]), 1, 0, 'C')
                    pdf.cell(30, 5, '%s' % (str(df.Clientes.iloc[i])), 1, 0, 'C')
                    pdf.cell(30, 5, '%s' % (str(df.TGT.iloc[i])), 1, 0, 'C')
                    pdf.cell(30, 5, '%s' % (str(df.TGT_p.iloc[i])) + '%', 1, 2, 'C')            
                pdf.cell(90, 30, " ", 0, 2, 'C')
                #pdf.cell(-150)        
                pdf.set_xy(30, renglon + 40)
                pdf.image('graph.png', x = None, y = None, w = 0, h = 0, type = '', link = '')            
                pdf.output(r'./' + campo + '.pdf', 'F')
            
            except:
                print('error ', campo)
                pass