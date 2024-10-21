# -*- coding: utf-8 -*-

import requests


import json
#from dotenv import load_dotenv
from dotenv import load_dotenv
#from dotenv import dotenv_values
import os 
import sys
import re


class ThirdPartyIA:
    def __init__(self, url, post, host_api_key):
        self.url=url
        self.method_http=post
        self.host_api_key=host_api_key

    def transaction(self, textPrompt):
        self.textPrompt=textPrompt
        
        headers = {"Content-Type": "application/json"}
        payload = "{\"contents\":[{\"parts\":[{\"text\":\""+str(self.textPrompt)+"\"}]}]}"
        #exit(self.url+"?key="+self.host_api_key)
        response = requests.request(self.method_http, self.url+"?key="+self.host_api_key, data=payload, headers=headers)    
        return response
        


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

if __name__=='__main__':

    load_dotenv()
    
    HOST = os.getenv("HOST_API_GOOGLE_GEMINI")
    
    method_http = "POST"
    API_KEY = os.getenv("API_KEY_GOOGLE_GEMINI")
     
    
    textDescription = "Faça uma texto descrevando esta vaga de emprego no formato para instagram e que tenha as palavras chave: emprego e Guarulhos, o link deve estar na descrição e baseado no texto abaixo:Descrição: A Cushman & Wakefield é uma empresa multinacional que atua no ramo imobiliário. Trabalhamos para sermos o provedor global preferencial de serviços imobiliários, oferecendo as soluções mais criativas e inovadoras de forma consistente, gerando valor significativo aos nossos clientes. Queremos aumentar ainda mais a diversidade das nossas pessoas, pois entendemos que essa é a chave para a inovação. Por isso, incentivamos que mulheres, pessoas da comunidade LGBTQIAPN+, indígenas, afrodescendentes, pessoas com deficiência, maiores de 50 anos se candidatem as nossas vagas. Celebramos a diversidade e o nosso compromisso é criar um ambiente inclusivo para todos os colaboradores.Um dia na vida do Assistente de Almoxarifado:Controle de estoque de material de escritório e manutenção;Compra de material de escritório e manutenção;Receber materiais, realizar entrada das NFs no sistema;Controlar as saídas de estoque no sistema;Elaboração e preenchimento de documentos e relatórios;O que fará você obter sucesso?Formado(a) no Ensino Médio ou cursando Ensino Superior em Administração, Ciências Contábeis ou áreas correlatas;Pacote Office básico (foco em Excel);Experiência em rotinas de almoxarifado/estoque;Disponibilidade para atuar na região de Guarulhos/SP, na região do Aeroporto, de segunda a sexta-feira das 8h às 17h48.Oferecemos:Vale-refeição;Assistência médica;Assistência odontológica;Seguro de vida;Gympass;Desconto em cursos e faculdades;Auxílio-funeral;Empréstimo Consignado Itaú;Programa de Apoio Psicológico;IVI – Plataforma de Cuidado Emocional;Auxílio Creche (para mães);Auxílio Enxoval;Calendário Mensal de Saúde e Bem-Estar;Comitê de Ações Sociais;Agenda de Diversidade (Encontro Presenciais, Webinar, grupos de diversidade);3 mil cursos Linkedin Learning disponíveis;Oportunidade de Carreira.Quer se sentir desafiado, motivado e valorizado todos os dias? Inspirar mudanças e deixar um legado? Faça parte do time da Cushman & Wakefield e ajude-nos na construção de um mundo de negócios melhor! \n\n https://www.vagas.com.br/vagas/v2648782/assistente-de-almoxarifado-guarulhos-sp"
    
    textDescription = textDescription.encode('utf-8')
    #exit()
    #self, url, post, host_api_key
    gemini = ThirdPartyIA(HOST,  method_http, API_KEY)

    result = gemini.transaction(textDescription)
    print(result.text.encode("utf-8"))
    print("fim")
    exit(0)