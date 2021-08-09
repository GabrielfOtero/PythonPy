class Fibonacci:
    def __init__(self, maximo=2000000):
        #Inicializa os dois primeiros numeros
        self.atual, self.proximo = 0, 1
        self.maximo = maximo

    def __iter__(self):
        #Retorna o objeto iterável
        return self

    def __next__(self):
        #Fim da iteração, raise StopIteration
        if self.atual > self.maximo:
            raise StopIteration

        # Salva o valor a ser retornaro
        retorno = self.atual

        # Atualiza o proximo elemento
        self.atual, self.proximo = self.proximo, self.atual + self.proximo

        return retorno

objeto_fibonacci = Fibonacci(maximo=2000000)

for fibonacci in objeto_fibonacci:
    print("Sequencia: {}".format(fibonacci))