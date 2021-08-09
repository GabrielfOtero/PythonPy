# CALCULADORA CIENTÍFICA v: 1.0
# 
#


print("\t Calculadora Científica\n ")

continuar = input(" \t Por favor digite seu nome: \n")

print("\t Seja Bem Vindo",continuar)

print(" \t Para continuar, escolha uma das seguintes opções:\n")

while True:
    start = input("Para Contas Básicas: \n'1'\n"
                  "Para Circulos: \n'2'\n"
                  "Para Equação de Segundo Grau: \n'3'\n"
                  "Para Potências: \n'4'\n"
                  "Para Geometria: \n'5'\n"
                  "Para Função: \n'6'\n"
                  "Para Velocidade Média: \n'7'\n"
                  "Para Sair do Programa: \n'n'\n")





    if start == 'n':
        print("\t Obrigado por usar minha Calculadora!\n")
        exit()


        

    if start == '1':

        print("\t Operações Básicas: \n")

        import math

        primeiro = input("\t Digite o Primeiro Número:\n ")
        segundo = input("\t Digite o Segundo Número:\n ")
        operacao = input("\t Digite a Operação:\n ")

        resultado = None
        if operacao == '+':
            resultado = float(primeiro) + float(segundo)
        elif operacao == "-":
            resultado = float(primeiro) - float(segundo)
        elif operacao == "*":
            resultado = float(primeiro) * float(segundo)
        elif operacao == "/":
            resultado = float(primeiro) / float(segundo)
        else:
            print("\t Impossíve Realizar a Operação!\n ")

        if resultado:
            print("\t Resultado: {0}".format(resultado))

            break

        continue
        

    if start == '2':
        print("\t Circulos: \n")


        print("\t Para Continuar Escolha uma das Opções Baixo: \n")

        a = input("Área do Círculo ----> \n'1'\n"
                  "Comprimento do Círculo ----> \n'2'\n"
                  "Sair ----> \n'n'\n")


        if a == 'n':
            print("\t Obrigado!\n")

            exit()


        if a == '1':
            print("\t Área do Círculo: \n")

            import math

            pi = 3.14

            r = input("Informe o Valor do Raio: ")

            resp = (float(r) * float(r)) * pi

            print("\t A Área do Círculo é:",resp,"\n")

            break


        if a == '2':
            print("\t Comprimento do Círculo: \n")

            import math


            pi = 3.14

            r = input("Digite o Valor do Raio: ")

            resp = (float(r) * 2) * pi

            print("\t O Comprimento do Círculo é:",resp,"\n")


            break


        else:
            print("\t Carácter Inválido!\n")

            continue



    if start == '3':

        print("\t Equação do Segundo Grau: \n")
        import math

        a = int(input("Digite um valor para a: "))
        b = int(input("Digite um valor para b: "))
        c = int(input("Digite um valor para c: "))

        delta = b*b - 4 * a * c

        if delta < 0:
             print("\t Esta Operação Não Possui Raizes Reais\n ")
        elif delta == 0:
            raiz = (-1 * b + math.sqrt(delta)) / (2 * a)
            print("\t A Equação Possui Apenas 1 Raiz Real",raiz)
        elif delta > 0:
            raiz1 = (-1 * b + math.sqrt(delta)) / (2 * a)
            raiz2 = (-1 * b - math.sqrt(delta)) / (2 *a)
            print("\t  As Raízes da Equação São:",raiz1, "E",raiz2)

            continue


    if start == '4':
        print("\t Potenciação: \n")
        print("Para prosseguir escolha uma das seguintes opções: ")


        
        while True:
            st = input("Potenciação: \n'1'\n"
                       "Sair: \n'n'\n")

         

            if st == '1':
                print("\t Potências: \n")
                

                import math
                

                a = input("Digite um valor para a: ")
                b = input("Digite um valor para b: ")
                

                resp = None
                
        
                resp = float(a) ** float(b)

                if resp:
                    print("\t Resultado: {0}".format(resp))

                    break

          
    if start == '5':
        print("\t Geometria: \n")

        print("Para Prosseguir, escolha uma das opções abaixo: \n")

        g = input("Teorema de Pitágoras: \n'1'\n"
                  "Áreas: \n'2'\n"
                  "Perímetros: \n'3'\n"
                  "Semelhança de Triângulos: \n'4'\n"
                  "Sair: \n'n'\n")


        if g == 'n':
            print("\t Obrigado por usar minha Calculadora!\n")
            exit()


            break

        if g == '1':
            import math
            
            print("\t Teorema de Pitágoras: \n")

            a = float(input("Digite o Valor do Cateto 1: "))
            b = float(input("Digite o Valor do Cateto 2: "))

            resp = math.sqrt((a*a)+(b*b))

            print("O Valor da Hipotenusa é:",resp)
            break

        if g == '2':
            print("\t Áreas: \n")

            print("Selecione a figura Geométrica: ")

            o = input("Quadrado ----> \n'1'\n"
                      "Retângulo ----> \n'2'\n"
                      "Triângulo ----> \n'3'\n"
                      "Trapézio ----> \n'4'\n"
                      "Cubo ----> \n'5'\n"
                      "Sair ----> \n'n'\n")


            if o == 'n':
                print("\t Obrigdo por usar minha Calculadora!\n")
                exit()
                break


            if o == '1':
                print("\t Quadrado: \n")

                a = input("Digite o valor de um dos lados do Quadrado: ")

                resp = float(a) * float(a)

                print("A área do Quadrado é:",resp)

                while True:
                    a = input("\t Gostaria de sair do Programa? Pressione \n'S'\n para Sair\n")

                    if a == 's':
                        print("\t Obrigado por usar minha Calculadora!\n")
                        exit()
                        break


            if o == '2':
                print("\t Retângulo: \n")

                a = input("Digite o Valor da Base do Retângulo: ")
                b = input("Digite o Valor do Lado do Retângulo: ")

                resp = float(a) * float(b)

                print("A área do Retângulo é:",resp)

                while True:
                    a = input("\t Gostaria de Sair do Programa? Pressione \n'S'\n Para Sair\n")

                    if a == 's':
                        print("\t Obrigado por usar minha Calculadora!\n")
                        exit()
                        break


            if o == '3':
                print("\t Triângulo: \n")

                a = input("Digite o valor da Base do Triângulo: ")
                b = input("Digite o valor da Altura do Triângulo: ")

                resp = (float(a) * float(b)) / 2

                print("Aárea do Triângulo é:",resp)

                while True:
                    a = input("\t Gostaria de Sair do Programa? Pressione \n'S'\n Para Sair\n")

                    if a == 's':
                        print("\t Obrigado por usar minha Calculadora!\n")
                        exit()
                        break


            if o == '4':
                print("\t Trapézio: \n")

                a = input("Digite o Valor da Base Maior do Trapézio: ")
                b = input("Digite o Valor da Base Maior do Trapézio: ")
                c = input("Digite o Valor da Altura do Trapézio: ")
                

                resp = ((float(a) + float(b)) * float(c)) / 2

                print("A área do Trapézio é:",resp)

                while True:
                    a = input("\t Gostaria de Sair do Programa? Pressione \n'S'\n Para Sair\n")

                    if a == 's':
                        print("\t Obrigado por usar minha Calculadora!\n")
                        exit()
                        break


            if o == '5':
                print("\t Cubo: \n")

                a = input("Digite o valor de um Lado do Quadrado: ")

                resp = float(a) * 6

                print("A área do Cubo é:",resp)
                break

    if start == '6':
        print("\t Funções: \n")

        print("Para prosseguir, selecione uma das opções: ")

        a = input("Descobrir o Valor de Y----> \n'1'\n"
                  "Descobrir o Valor de X ----> \n'2'\n"
                  "Sair ----> \n'n'\n")


        if a == 'n':
            print("\t  Obrigado por usar minha Calculadora!\n")

            exit()

            break


        if a == '1':
            print('\t Valor de Y: \n')

            b = input("Digite o Valor de X: ")
            c = input("Digite o Valor de B: ")

            resp = float(c) + float(b)

            print("\t O Valor de Y é:",resp,"\n")

            break


        if a == '2':
            print("\t Valor de X: \n")

            b = input("Digite O Valor de Y: ")
            c = input("Digite O Valor de B: ")

            resp = float(c) - float(b)

            print('\t O Valor de X é:',resp,'\n')

            break


        else:
            print ("\t Caractere Inválido!\n")
            continue


            break



    if start == '7':
        print ("\t Velocidade Média: \n")

        a = input('Informe a Distância Percorrida: ')
        b = input("Informe o tempo Gasto (Em Horas): ")
                  



        resp = float(a) / float(b)

        print("\t A Velocidade Média é:",resp,"\n")

##Obrigado por Usar!