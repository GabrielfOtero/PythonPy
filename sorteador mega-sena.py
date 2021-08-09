##Sorteador Mega-Sena
##Criado por GabOtero
##Criar o Range de números associados ao date e ao Random
import random
import datetime
linha='-'*75
text0='por Gabriel Otero'
text1='Mega-Sena Generator'
sequencia=random.sample(range(60),6)
sequencia.sort()
print (linha)
print (text1.center(75,'*'))
print (linha)
print ('\n\n')
print ('Os Números Sorteados são: ', sequencia, '.')
print ('\n\n')
print (text0.center(75,'-'))

## Grava todas as sequências em um arquivo.txt para ver quando precisar utilizando POO
arquivo = open("Mega_Sena.txt","a+")
data=datetime.datetime.now().strftime("%A (%a) %d/%m/%Y %I:%M:%S %p")
arquivo.write("\n Data: %s - numeros da sorte: %s" % (data, sequencia))
arquivo.close()
ler = open("Mega_Sena.txt","r")
texto = ler.read()
ler.close()

