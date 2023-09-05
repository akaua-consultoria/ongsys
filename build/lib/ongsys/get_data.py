#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 12:01:47 2023

@author: nfamartins
"""

import requests
import pandas as pd


def get_data(endpoint, user, apikey, params=None):
    
    # Criar objeto de autenticação básica
    auth = requests.auth.HTTPBasicAuth(user, apikey)
    url = 'https://www.ongsys.com.br/app/index.php/api/v2/'
    
    # set dataframe
    df = pd.DataFrame()
    
    # set page number
    params['pageNumber'] = '1'
    
    # primeira página
    try:
        # requisição GET para a API com a autenticação básica
        response = requests.get(url+endpoint, auth=auth, params=params)
        
        # total de instâncias para conferência
        totalRecords = response.json()['totalRecords']
        
    except requests.exceptions.RequestException as e:
        # Ocorreu um erro ao fazer a requisição
        print("Erro de conexão:", str(e))
        return None
    
    
    #paginação
    while response.status_code == 200:
        
        # resposta em formato JSON
        data = response.json()
        
        # transforma dados em dataframe
        df = pd.concat([df,pd.json_normalize(data['data'])], ignore_index=True)
        
        # próxima página
        params['pageNumber'] = str(int(params['pageNumber']) + 1)
        response = requests.get(url+endpoint, auth=auth, params=params)
    
    # alterando o nome das colunas (tirando os .)
    df = df.rename(columns=lambda x: x.replace('.', '_'))
        
    return (df,totalRecords)