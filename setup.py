#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 21:11:45 2023

@author: nfamartins
"""

from setuptools import setup, find_packages

setup(
    name="ongsys",
    version="0.1",
    description="Um pacote para interação com a API da OngSys",
    author="Nathália Martins",
    author_email="nathalia@akaua.com.br",
    packages=find_packages(),
		install_requires=[
        'pandas',
        'requests'
    ],
)
