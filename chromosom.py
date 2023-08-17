from random import randint

'''
создадим класс Chromosome- с 3мя свойствами:

rating рейтинг хромосомы
size размер хромосомы (длина массива генов)
genes масив генов хромосомы (то, что свмо раньше было хромосомой)
'''
class Chromosome:
    def __init__(self, size, gene_pool):
        self.rating = 0
        self.size = size
        self.genes = bytearray(size)
        if gene_pool is not None:
            self.set_random_genes(gene_pool)
    '''
        функция для генерации случайной хромосомы. принимает 2 параметра:
        длина, котор. нужно получить и набор генов, которого нужно сделать зромосому.
        '''
    def set_random_genes(self, gene_pool):
        gene_pool_range = len(gene_pool) - 1
        for i in range(self.size):
            rand_pos = randint(0, gene_pool_range)
            self.genes[i] = gene_pool[rand_pos]

def create_population(pop_size, chromo_size, genes):
    '''
     в функ. заполнения популяции мы передаем размер попул., размер хромо.
     и генофонд, чтобы не зависить от глобальных переменных
    '''
    population = [None] * pop_size
    for i in range(pop_size):
        population[i] = Chromosome(chromo_size, gene_pool)

    return population
'''
фун. вычисления рейтинга - расстояние между 2мя строками
напишим сразу для всей популяции, т.к. других применений у нее нет
'''
def calc_rating(population, final_chromo):
    for chromo in population:
        chromo.rating = chromo.size
        for i in range(chromo.size):
            if chromo.genes[i] == final_chromo[i]:
                chromo.rating -= 1
'''
сортировкой пузырьком сделаем сортировку хромо по рейтингу
'''
def sort_population(population):
    size = len(population)
    repeat = True
    while repeat:
        repeat = False
        for i in range(0, size - 1):
            bubble = population[i]
            if (bubble.rating > population[i + 1].rating):
                population[i] = population[i + 1]
                population[i + 1] = bubble
                repeat = True
    
def select(population, survivors):
    # elitism selection
    size = len(survivors)
    for i in range(size):
        survivors[i] = population[i]

def repopulate(population, parents, children_count):
    '''
        теперь имея функ. для выбора родителей и для скрещиванияб напишим функцию,
        которая заполняет 2ю половину популяции потоками(родители сохраняются в первой половине)
        '''
    pop_size = len(population)
    while children_count < pop_size:
        p1_pos = get_parent_index(parents, None)
        p2_pos = get_parent_index(parents, p1_pos)
        p1 = parents[p1_pos]
        p2 = parents[p2_pos]
        population[children_count] = cross(p1, p2)
        population[children_count + 1] = cross(p2, p1)
        children_count += 2

def get_parent_index(parents, exclude_index):
    '''
        Среди выживших нужно отобрать пары родителей для потомства
        и заменит 2ю половину
        '''
    size = len(parents)
    while True:
        index = randint(0, size - 1)
        if exclude_index is None or exclude_index != index:
            return index

def cross(chromo1, chromo2):
    '''
    мы вибираем случайную позицию внутри хромо и потомок получает гены родит №1 от
    начала до этой позиции и вторую половину от родит№2

    каждые 2 родит. пораждают пару потомков. т.е. функ. cross() вызываем дважды:
    (род1, род2) и (род2, род1)
        '''
    size = chromo1.size
    point = randint(0, size - 1)
    child = Chromosome(size, None)
    for i in range(point):
        child.genes[i] = chromo1.genes[i]
    for i in range(point, size):
        child.genes[i] = chromo2.genes[i]

    return child

def mutate(population, chromo_count, gene_count, gene_pool):
    '''
     можно подвегать мутации хоть 50% популяции,
    но кол-во генов лучше задать 1.
    это означает, что за 1 раз мутирует только 1 символ в строке
    эта мутация может как приблизить к рез. так и наоборо
        '''
    pop_size = len(population)
    gene_pool_size = len(gene_pool)
    for i in range(chromo_count):
        chromo_pos = randint(0, pop_size - 1)
        chromo = population[chromo_pos]
        for j in range(gene_count):
            gene_pos = randint(0, gene_pool_size - 1)
            gene = gene_pool[gene_pos]
            gene_pos = randint(0, chromo.size - 1)
            chromo.genes[gene_pos] = gene
'''
вывод порядковый номкр и рейтинг
'''
def print_population(population):
    i = 0
    for chromo in population:
        i += 1
        print(str(i) + '. ' + str(chromo.rating) + ': ' + chromo.genes.decode())
'''
генофонд - это строка справочник, которая содержит все возможные гены. 
Его и финал. строку(хромасому) мы закодируем в байковую строку
'''
gene_pool = bytearray(b'abcdefghijklmnopqrstuvwxyz ') # весь алфавит

final_chromo = bytearray(b'i love myself') # целевая фраза

chromo_size = len(final_chromo)
population_size = 20
'''
для селекции возьмём метод элит - лучшая половина популяции, 
которая сама переходит и пораждает вторую половину

список уже отсортирован по рейтингу, поэтому задача селекции решина(берем топ-10)
и нам нужно сделать отбор. т.е. поместить избранников в список выживших

Заведём для выживших список фикс. длинны заранее и будем им пользоваться всё время
'''
survivors = [None] * (population_size // 2)

population = create_population(population_size, chromo_size, gene_pool)

iteration_count = 0

while True:  
    iteration_count += 1  # СЧЕТЧИК ПОКОЛЕНИЯ
    calc_rating(population, final_chromo) # Расчёт рейтинга популяции
    sort_population(population) #сортировка популяции, в нач. - элита
    print('*** ' + str(iteration_count) + ' ***')
    print_population(population) 
    if population[0].rating == 0:   
        '''
        при достижении целевой строки у 1й хромосомы рейтин = 0
        обнаружив - прерываем цикл
        '''
        break
    # if iteration_count==20:break
    select(population, survivors)   # отбор элиты - родителей в первую часть
    repopulate(population, survivors, population_size // 2)   #2ю часть заполняем детьми
    mutate(population, 10, 1, gene_pool) # выполняем мутацию по 1му гену