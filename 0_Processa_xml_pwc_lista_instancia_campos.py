"""

SILVER
tabela_origem, campo_origem (nome físico), precisao, escala 

GOLD
tabela_origem, campo_origem, campo_destino, precisao, escala, obs (expressões de conversão)

"""


# v5.7
# volta as origens, mapeamento de instancia e campos
# 

from datetime import datetime
import xml.etree.ElementTree as ET
import csv
import pandas as pd
import os

#import json

#trecho para tratar limite de recursividade, quando funcão principal não era deterministica
#import sys
#sys.setrecursionlimit(10500)

"""

   __                  /\/|                              _ _ _                     
  / _|_   _ _ __   ___|/\/   ___  ___    __ _ _   ___  _(_) (_) __ _ _ __ ___  ___ 
 | |_| | | | '_ \ / __/ _ \ / _ \/ __|  / _` | | | \ \/ / | | |/ _` | '__/ _ \/ __|
 |  _| |_| | | | | (_| (_) |  __/\__ \ | (_| | |_| |>  <| | | | (_| | | |  __/\__ \
 |_|  \__,_|_| |_|\___\___/ \___||___/  \__,_|\__,_/_/\_\_|_|_|\__,_|_|  \___||___/
                   )_)                                                             

"""
# Define a function to add a new sheet to an existing Excel file and write data to it
def add_sheet_to_excel(file_path, sheet_name, data):
    # Load the existing Excel file
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:
        # Convert the data to a DataFrame
        df = pd.DataFrame(data)
        # Write the DataFrame to the new sheet
        df.to_excel(writer, sheet_name=sheet_name)


def deletar_arquivo(nome_arquivo):
    try:
        os.remove(nome_arquivo)
        print(f"Arquivo '{nome_arquivo}' foi deletado com sucesso.")
    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado.")


#checa dicionario
def check_string_in_dict(s, d, instancia):
    chaves={}
    # Verifica se s é uma chave no dicionário
    if s in d:
        #"string é indice"
        return s

    # Verifica se s é uma substring de qualquer valor no dicionário
    for key, value in d.items():
        if s in str(value):
            #string está nos valores
            if instancia in key:
                chaves[key] = value 

    # Se s não é uma chave nem uma substring de qualquer valor, retorna False
    #if len(chaves)>0:
    #    print("...")
    return chaves

def remover_quebras_de_linha(texto):
    if texto is None:
        return ''
    return texto.replace('\r\n', '') #.replace('\r', '')
    
def print_to_txt(nome_arquivo, linha):
    with open(nome_arquivo, mode='a' ) as arquivo_txt:
        arquivo_txt.write(f"{linha}\n")
        


"""
   __                  /\/|                    _            _             _ 
  / _|_   _ _ __   ___|/\/_  ___    _ __  _ __(_)_ __   ___(_)_ __   __ _| |
 | |_| | | | '_ \ / __/ _` |/ _ \  | '_ \| '__| | '_ \ / __| | '_ \ / _` | |
 |  _| |_| | | | | (_| (_| | (_) | | |_) | |  | | | | | (__| | |_) | (_| | |
 |_|  \__,_|_| |_|\___\__,_|\___/  | .__/|_|  |_|_| |_|\___|_| .__/ \__,_|_|
                   )_)             |_|                       |_|            

 # recebe um xml gerado de exportação de mapeamento do Power Center e devolve uma planilha 
 # com os rastreamentos de transformações de cada campo da origem
"""

def extract_mapping(xml_file, txt_file, nivel, debug=False):
    
    """
    # funcao recursiva para percorrer as conexoes e montar a sequencia de campos usados
    """
    
    def list_connections(field_atual, instance_atual, sequencia):
        
        chave_expressao={}
        # verifica se instancia e campo já estão na sequencia
        b_sequencia_contem_campo = f"{instance_atual}.{field_atual}" in sequencia
        
        if b_sequencia_contem_campo == False:
            sequencia.append(f"{instance_atual}.{field_atual}")
            
            for source_instance, connections_list in connections.items():                
                for to_instance, from_field, from_field_name, to_field, to_field_name in connections_list:
                    if from_field_name == field_atual and source_instance == instance_atual :
                        return list_connections(to_field_name, to_instance, sequencia)
            
            #usado para verificar UNIONS
            chave_dependencia=field_dependency.get(f"{instance_atual}.{field_atual}")
            if chave_dependencia !=None:
                next_instance = instance_atual
                next_field = chave_dependencia
    
                return list_connections(next_field, next_instance, sequencia)
            
            
            chave_expressao=check_string_in_dict(field_atual,expressions, instance_atual)
 
            # if len(chave_expressao)>1:
            #     raise TypeError(f"Campo {field_atual} da instância {instance_atual} possui mais de um caminho")
            # elif len(chave_expressao)>0:
           
            # verifica se a sequencia de transformacoes 
            if len(chave_expressao)>0:
                # se tiver mais uma chave_expressao, ha uma bifurcacao no caminho, verifica se ha variavel de saida
                if len(chave_expressao)>1:
                    #verifica se tem variavel "out" 
                    str_aux=  field_atual.replace("in_","out_")
                    for chave0, valor0 in chave_expressao.items():
                        if str_aux in chave0:
                            #print(",,,")
                            aux_chave = chave0 # next(iter(chave_expressao))
                        
                            partes=aux_chave.split('.')
                            next_instance=partes[0]
                            next_field = partes[1]
                            return list_connections(next_field, next_instance, sequencia)
                else:
                    for chave, valor in chave_expressao.items():
                        #print(f"{chave} - {valor}")

                        aux_chave=next(iter(chave_expressao))
                        
                        partes=aux_chave.split('.')
                        next_instance=partes[0]
                        next_field = partes[1]
            
                        return list_connections(next_field, next_instance, sequencia)
        
        return sequencia
    
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Create a dictionary to store the connections
    connections = {}
    # Create a dictionary to store the data types of the fields
    data_types = {}
    # Create a dictionary to store the expressions of the fields
    expressions = {}
    # Create a dictionary to store the descriptions of the instances
    descriptions = {}
    # Create a dictionary to store precisions 
    precision_scale={}
    # Create a dictionary to store filters
    filters={}
    field_dependency={}
    source_infos=[]

    """
     _____                     __                            _   _             
    |_   _| __ __ _ _ __  ___ / _| ___  _ __ _ __ ___   __ _| |_(_) ___  _ __  
      | || '__/ _` | '_ \/ __| |_ / _ \| '__| '_ ` _ \ / _` | __| |/ _ \| '_ \ 
      | || | | (_| | | | \__ \  _| (_) | |  | | | | | | (_| | |_| | (_) | | | |
      |_||_|  \__,_|_| |_|___/_|  \___/|_|  |_| |_| |_|\__,_|\__|_|\___/|_| |_|
        
    # Iterate over all TRANSFORMFIELD elements to get the data types and expressions
    """

    # Iterate over all TRANSFORMATION elements to get the descriptions
    for transformation in root.iter('TRANSFORMATION'):
        instance_name = transformation.get('NAME')
        description = transformation.get('DESCRIPTION')
        descriptions[instance_name] = description

        lista_props_source=[]
        # Iterate over all TRANSFORMFIELD elements to get the filters
        for transform2 in transformation.iter('TABLEATTRIBUTE'):
            if transform2.get('NAME') in ['Source Filter','Sql Query','Lookup condition','Lookup table name']:
                lista_props_source.append([transform2.get('NAME'),transform2.get('VALUE')])
        
        if len(lista_props_source)>0:
            filters[instance_name]=lista_props_source
         
         # Iterate over all TRANSFORMFIELD elements within the current TRANSFORMATION
        for field in transformation.iter('TRANSFORMFIELD'):
            
            field_name = field.get('NAME')
            if instance_name is not None:
                field_name = instance_name + '.' + field_name
            data_type = field.get('DATATYPE')
            precision = field.get('PRECISION')
            scale = field.get('SCALE')
            expression = field.get('EXPRESSION')
            data_types[field_name] = data_type
            precision_scale[field_name] = (precision, scale)
            expressions[field_name] = expression
            #print(f"{field_name} - {expression}")

        # Iterate over all TRANSFORMFIELD elements to get FIELDDEPENDENCY used on UNIONS
        for field in transformation.iter('FIELDDEPENDENCY'):
            
            field_name = field.get('INPUTFIELD')
            if instance_name is not None:
                field_name = instance_name + '.' + field_name
            field_dependency[field_name]=field.get('OUTPUTFIELD')

    """
     ____                           
    / ___|  ___  _   _ _ __ ___ ___ 
    \___ \ / _ \| | | | '__/ __/ _ \
     ___) | (_) | |_| | | | (_|  __/
    |____/ \___/ \__,_|_|  \___\___|
                                 
    # Iterate over all SOURCE elements to get the descriptions
    """
    
    source_instances=[]

    for transformation in root.iter('SOURCE'):

        instance_name = transformation.get('NAME')
        description = transformation.get('DESCRIPTION')
        descriptions[instance_name] = description

        source_instances.append(instance_name)
        
        # Iterate over all TRANSFORMFIELD elements within the current TRANSFORMATION
        for field in transformation.iter('SOURCEFIELD'):
            
            field_name = field.get('NAME')
            if instance_name is not None:
                field_name = instance_name + '.' + field_name
            data_type = field.get('DATATYPE')
            precision = field.get('PRECISION')
            scale = field.get('SCALE')
            data_types[field_name] = data_type
            precision_scale[field_name] = (precision, scale)

    """
     _____                    _   
    |_   _|_ _ _ __ __ _  ___| |_ 
      | |/ _` | '__/ _` |/ _ \ __|
      | | (_| | | | (_| |  __/ |_ 
      |_|\__,_|_|  \__, |\___|\__|
                    |___/          
    # Iterate over all TARGET elements to get the descriptions                                               
    """
    
    for transformation in root.iter('TARGET'):
        target_instance = transformation.get('NAME')
        instance_name = transformation.get('NAME')
        description = transformation.get('DESCRIPTION')
        descriptions[instance_name] = description

         # Iterate over all TRANSFORMFIELD elements within the current TRANSFORMATION
        for field in transformation.iter('TARGETFIELD'):
        
            field_name = field.get('NAME')
            if instance_name is not None:
                field_name = instance_name + '.' + field_name
            data_type = field.get('DATATYPE')
            precision = field.get('PRECISION')
            scale = field.get('SCALE')
            data_types[field_name] = data_type
            precision_scale[field_name] = (precision, scale)
        
    """
      ____                            _             
     / ___|___  _ __  _ __   ___  ___| |_ ___  _ __ 
    | |   / _ \| '_ \| '_ \ / _ \/ __| __/ _ \| '__|
    | |__| (_) | | | | | | |  __/ (__| || (_) | |   
     \____\___/|_| |_|_| |_|\___|\___|\__\___/|_|   
                                                 
    # Iterate over all CONNECTOR elements                                                
    """
    
    for connector in root.iter('CONNECTOR'):
        # Extract the transformation sequence information
        
        from_instance = connector.get('FROMINSTANCE')
        from_field = from_instance + '.' + connector.get('FROMFIELD')
        from_field_name = connector.get('FROMFIELD')
        to_instance = connector.get('TOINSTANCE')
        to_field = to_instance + '.' + connector.get('TOFIELD')
        to_field_name = connector.get('TOFIELD')

        # Add the connection to the dictionary
        if from_instance not in connections:
            connections[from_instance] = []
        connections[from_instance].append((to_instance, from_field, from_field_name, to_field, to_field_name ))
    
    # Find the source definition (the key that does not appear as a value in the dictionary)
    source = [key for key in connections if all(key != value[0] for values in connections.values() for value in values)][0]
    
    # Print the transformations in order from the source definition to the target
    current_instance = source
    info_origem=''
        
    # Cabeçalhos
    # ------------------------------

    # SILVER
    # tabela_origem, campo_origem (nome físico), precisao, escala 
    # writer.writerow(["Tabela_origem", "Campo_origem", "Precisao", "Escala"])

    # GOLD
    # tabela_origem, campo_origem, campo_destino, precisao, escala, obs (expressões de conversão)
    # writer.writerow(["Tabela_origem", "Campo_origem","Campo_destino", "Precisao", "Escala","Observações"])

    if nivel=="SILVER":
        cabecalho= ["Tabela_origem", "Campo_origem", "Tipo_origem","Precisao", "Escala"]
    else:
        cabecalho=["Tabela_origem", "Campo_origem","Tipo_origem","Precisao", "Escala","Campo_destino","Tipo_destino", "Precisao", "Escala","Observações"]
    
    

    
    #Adicionar dados de filtros em dicionário que adicionará uma segunda planilha "origens" no xls final
    dic_aux={}
    
    print_to_txt(txt_file,f"=============== SOURCE FILTERS ======================= ")
    for key2, inst2 in filters.items():
        
        print_to_txt(txt_file,f"{key2}")
        for valor in inst2:
            print_to_txt(txt_file,f"    {valor[0]}: {valor[1]} ")
        print_to_txt(txt_file,f"")
    """
     __  __       _         _                       
    |  \/  | __ _(_)_ __   | |    ___   ___  _ __   
    | |\/| |/ _` | | '_ \  | |   / _ \ / _ \| '_ \  
    | |  | | (_| | | | | | | |__| (_) | (_) | |_) | 
    |_|  |_|\__,_|_|_| |_| |_____\___/ \___/| .__/  
                                            |_|     
    """

    for current_instance_global in source_instances:
        current_instance = current_instance_global
        
        
        print_to_txt(txt_file,f"=============== ORIGEM {current_instance} ======================= \n")
        while current_instance in connections:
            imprime_header = True
            
            for to_instance, from_field, from_field_name, to_field, to_field_name in connections[current_instance]:
                if imprime_header:
                    print_to_txt(txt_file,f" ({descriptions.get(current_instance, 'No description available')})\n ")
                    print_to_txt(txt_file,f"{current_instance} -->  {to_instance} \n")
                    imprime_header=False    

                precisionf, scalef = precision_scale.get(from_field, ('Unknown', 'Unknown'))
                precisiont, scalet = precision_scale.get(to_field, ('Unknown', 'Unknown'))
            
                print_to_txt(txt_file, f"    - {from_field_name} [{data_types.get(from_field, 'Unknown')}({precisionf},{scalef})] --> {to_field_name} [{data_types.get(to_field, 'Unknown')}({precisiont},{scalet})]  ")
                
                if expressions.get(from_field)!=None:
                    #print(f"     Expression for {from_field_name}: \n        {expressions.get(from_field, 'No expression available')} \n")
                    if remover_quebras_de_linha(expressions.get(from_field, ''))!='':
                        print_to_txt(txt_file,f"            Tratamento: {remover_quebras_de_linha(expressions.get(from_field, ''))}")
                
                #if expressions.get(to_field)!=None:
                #    print_to_txt(txt_file,f"       Expression TO: \n        {expressions.get(to_field, 'No expression available')} ")


                
                #print(f"    {from_field_name} {data_type}({precision},{scale}) --> {to_field_name} ({data_types.get(to_field, 'Unknown')}) in {to_instance}")

                #if to_instance in filters:
                #    print(f"    Filter applied in {to_instance}: {filters[to_instance]}")
                #if current_instance in source_filters and source_filters[current_instance]:
                #    print(f"    Source filter applied in {current_instance}: {source_filters[current_instance]}")
            current_instance = connections[current_instance][0][0]
            print_to_txt(txt_file,"\n")
        
        print_to_txt(txt_file,f"\n")
            
            

    return source_infos
    

# Get the current date and time
now = datetime.now()

# Format the date and time as month-day-hour-minute
formatted = now.strftime("%y%m%d_%H%M")

camada="SILVER"
camada="GOLD"

#nome_arquivo="arquivo"
nome_arquivo="m_DWAR2470_etl1_carrega_tempr_bare_apolc_segur_re_espa 2"
nome_arquivo="m_DWAR2470_etl1_carrega_tempr_bare_apolc_segur_re_rebn 1"
nome_arquivo="m_DWAR2470_etl1_carrega_tempr_bare_apolc_segur_re_rebp 1"
nome_arquivo="m_DWAR2470_etl1_carrega_tempr_bare_apolc_segur_re_rebp_fsen 1"
nome_arquivo="m_DWAR2470_etl1_carrega_tempr_bare_apolc_segur_re_rebp_negociaveis 1"

#demo

pasta="PowerCenter/ESPA"
nome_arquivo="m_DWAR2470_etl1_carrega_tempr_bare_apolc_segur_re_espa"




pasta="PowerCenter"
nome_arquivo="m_DWAR2470_etl1_carrega_tempr_bare_apolc_segur_re_rebp_negociaveis 1"

arquivo_in= f"{pasta}/{nome_arquivo}.xml"

arquivo_out= f"{pasta}/{formatted}_extr_PWC_{nome_arquivo}_{camada}_lista_campos.txt"



data={}

# Chama função principal 
data = extract_mapping(arquivo_in, arquivo_out,camada)

