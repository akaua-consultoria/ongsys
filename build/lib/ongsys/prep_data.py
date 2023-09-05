#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 14:27:40 2023

@author: nfamartins
"""
import pandas as pd
import json

## o dataframe resultante de contas a pagar e receber tem duas colunas que podem se comportar de maneira "não prevista"
## as colunas 'rateios' e 'baixaTipo' tem um número não pré-definido de entradas, por isso serão separadas 

def prep_data(df):
    
    # padronizando a coluna de identificação
    try:
        df = df.rename(columns={'codigo': 'codLancamento'})
    except:
        pass        
    
    # adicionando uma coluna de índice 
    df.reset_index(inplace=True)
    
    # renomeando a coluna
    df = df.rename(columns={'index': 'ide'})
    
    # separando rateios 
    try:
        df_rateios = df.loc[:, ['ide','codLancamento','rateios']]
        df_rateios = df_rateios.explode(['rateios'])
        df_rateios = pd.json_normalize(json.loads(df_rateios.to_json(orient='records')))
        df_rateios = df_rateios.rename(columns=lambda x: x.replace('.', '_')) # padronizando o nome das colunas
        df_rateios = df_rateios.astype(str) # transformando tudo em str
        
        try:
            df_rateios = df_rateios.drop(['rateios'], axis=1)
        except:
            pass
        
        # dropando a coluna do df principal
        df = df.drop(['rateios'], axis=1)
        print('tem rateios')
        
    except:
        df_rateios = None
    
    # separando baixaTipo 
    try:
        df_baixaTipo = df.loc[:, ['ide','codLancamento','baixaTipo']]
        df_baixaTipo = df_baixaTipo.explode(['baixaTipo'])
        df_baixaTipo = pd.json_normalize(json.loads(df_baixaTipo.to_json(orient='records')))
        
        try:
            df_baixaTipo = df_baixaTipo.drop(['baixaTipo'], axis=1)
        except:
            pass
        
        df_baixaTipo = df_baixaTipo.rename(columns=lambda x: x.replace('.', '_')) # padronizando o nome das colunas
        df_baixaTipo = df_baixaTipo.astype(str) # transformando tudo em str
        
        # dropando a coluna do df principal
        df = df.drop(['baixaTipo'], axis=1)
        print('tem baixaTipo')
        
    except:
        df_baixaTipo = None
        
    df = df.astype(str) # transformando tudo em str para evitar problemas de inserção no servidor
    
    return(df,df_rateios,df_baixaTipo)
    