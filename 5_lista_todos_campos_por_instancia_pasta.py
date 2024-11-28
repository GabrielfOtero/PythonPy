
from datetime import datetime
import xml.etree.ElementTree as ET
import csv
import pandas as pd
import os
import glob


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
    return texto.replace('\r\n', ' ').replace(';', ' ')
    
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

    
    j_instancias=[]
    j_transf={}
    instancia_tipo={}
    instancia_transf={}
    for instances1 in root.iter('INSTANCE'):
        nome_instancia=instances1.get("NAME")
        j_instancias.append(nome_instancia)
        instancia_tipo[nome_instancia]=instances1.get("TYPE")
        instancia_transf[nome_instancia]=instances1.get("TRANSFORMATION_NAME")
        #print(f"{nome_instancia}, {instancia_tipo[nome_instancia]}, {instancia_transf[nome_instancia]}")
    
    
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
            if transform2.get('NAME') in ['Source Filter','Sql Query','Lookup condition','Lookup table name','Lookup Source Filter','Lookup Sql Override']:
                str_valor_filter=remover_quebras_de_linha(transform2.get('VALUE'))
                lista_props_source.append([transform2.get('NAME'),str_valor_filter])

        for transform3 in transformation.iter('METADATAEXTENSION'):
            #print(transformation.get('NAME'))      
            #print(transform3.get('DOMAINNAME'))
            if transform3.get('DOMAINNAME') in ['SQL_Transform']:
                str_valor_filter=remover_quebras_de_linha(transform3.get('VALUE'))
                lista_props_source.append([transform3.get('NAME'), str_valor_filter])
    

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
            
            if instance_name not in j_transf:
                j_transf[instance_name] = []
            j_transf[instance_name].append((field.get('NAME'), data_type, precision, scale, expression ))

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
            expression=""
            if instance_name not in j_transf:
                j_transf[instance_name] = []
            j_transf[instance_name].append((field.get('NAME'), data_type, precision, scale, expression ))

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
            
            if instance_name is not None:
                field_name = instance_name + '.' + field.get('NAME')
            data_type = field.get('DATATYPE')
            precision = field.get('PRECISION')
            scale = field.get('SCALE')
            data_types[field_name] = data_type
            precision_scale[field_name] = (precision, scale)
            
            expression=""
            if instance_name not in j_transf:
                j_transf[instance_name] = []
            j_transf[instance_name].append((field.get('NAME'), data_type, precision, scale, expression ))
        
        
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
        if to_instance not in connections:
            connections[to_instance] = []
        connections[to_instance].append((from_instance, from_field, from_field_name, to_field, to_field_name ))
        #print_to_txt(txt_file,f"{from_instance},{to_instance},{from_field},{from_field_name},{to_field},{to_field_name}")
    


    dic_aux={}
    

    chaves_ordenadas = sorted(filters.keys())

    
    # print_to_txt(txt_file,f"====================================================== ")
    # print_to_txt(txt_file,f"=============== SOURCE FILTERS ======================= ")
    # print_to_txt(txt_file,f"====================================================== \n")
    print_to_txt(f"{txt_file}_SOURCES",f"NOME; TIPO; VALOR ")    
    for curr in chaves_ordenadas:
        #print_to_txt(txt_file,f"{curr}")
        for key2, inst2 in filters[curr]:
            print_to_txt(f"{txt_file}_SOURCES",f"{curr};    {key2}; {inst2} ")    


    """
     __  __       _         _                       
    |  \/  | __ _(_)_ __   | |    ___   ___  _ __   
    | |\/| |/ _` | | '_ \  | |   / _ \ / _ \| '_ \  
    | |  | | (_| | | | | | | |__| (_) | (_) | |_) | 
    |_|  |_|\__,_|_|_| |_| |_____\___/ \___/| .__/  
                                            |_|     
    """

    def depara_tipo(tipo, escala):

        if any(aux_tipo in tipo for aux_tipo in ['number','decimal','numeric','integer','float']):
            if escala=="0":
                return "long"
            else:
                return "double"
        elif any(aux_tipo in tipo for aux_tipo in  ['char','varchar']):
            return "string"
        elif any(aux_tipo in tipo for aux_tipo in  ['datetime','datetime2']):
            return "timestamp"
        else:
            return tipo
        
    print_to_txt(txt_file,f"INSTANCIA; ORDEM; CAMPO; TIPO; TRANSFORMACAO")
    for j1 in j_instancias:
        if True: #instancia_tipo[j1]=="TARGET":
            #print(f"{j1} {instancia_transf[j1]}") 
            #print(j1)
            if instancia_transf[j1] in j_transf:
                for field_name, data_type, precision, scale, expression in j_transf[ instancia_transf[j1]]:
                    
                    #print(f"      {field_name}, {data_type}, {precision}, {scale}, {expression} ")
                    datatype_conv=depara_tipo(data_type,scale)
                    aux_expression=remover_quebras_de_linha(expression)


                    #print(aux_expression2.decode('utf-8'))
                    print_to_txt(txt_file, f"{instancia_transf[j1]};;{field_name};{datatype_conv};{aux_expression}")

    return source_infos

# Get the current date and time
now = datetime.now()

# Format the date and time as month-day-hour-minute
formatted = now.strftime("%y%m%d_%H%M")

camada="SILVER"
camada="GOLD"


pasta="PowerCenter/etl1"
pasta="PowerCenter/pwc_conjunto_completo_XML/ETL1"
pasta="PowerCenter/pwc_conjunto_completo_XML/ETL2"
pasta="PowerCenter/ESPA"
pasta="Python"

for file_path in glob.glob(os.path.join(pasta, "*.xml")):
    print(os.path.basename(file_path))
    nome_arquivo=os.path.basename(file_path)
    
    arquivo_in= file_path

    # Exemplo de uso
    #arquivo_out= f"{formatted}_extr_PWC_{nome_arquivo}_{camada}_lista_campos.csv"
    arquivo_out= f"{pasta}/{nome_arquivo}_lista_campos.csv"

    data={}

    # Chama função principal 
    data = extract_mapping(arquivo_in, arquivo_out,camada)
    df = pd.read_csv(arquivo_out, delimiter=';',encoding='ISO-8859-1')
    df = df.drop_duplicates()
    df = df.dropna(how='all')
    df.to_excel(f'{pasta}/{nome_arquivo}_todos_campos_instancia.xlsx', index=False)
    deletar_arquivo(arquivo_out)

    df2 = pd.read_csv(f"{arquivo_out}_SOURCES", delimiter=';')
    df2.to_excel(f'{pasta}/{nome_arquivo}_SOURCES.xlsx', index=False)
    deletar_arquivo(f"{arquivo_out}_SOURCES")

