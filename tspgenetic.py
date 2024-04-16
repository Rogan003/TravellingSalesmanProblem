import random
import numpy as np

# python recnik u kom kljucevi predstavljaju nazive (brojeve) gradove, a vrednosti lokaciju (par koordinata)
cities = {}



# funkcija za ucitavanje podataka iz data_tsp.txt
def load_data():
    with open("data_tsp.txt", "r") as f:
        for line in f.readlines():
            items = line.split()
            
            cities[items[0]] = [float(items[1]), float(items[2])]
            
            

# funkcija koja vraca razdaljinu izmedju dva prosledjena grada
def dist(key_one, key_two):
    return np.sqrt((cities[key_one][0] - cities[key_two][0]) ** 2 + (cities[key_one][1] - cities[key_two][1]) ** 2)

# funkcija koja vraca razdaljinu izmedju svih gradova na jednom obilasku
def route_dist(route):
    distance = 0
    
    for i in range(len(route) - 1):
        distance += dist(route[i], route[i + 1])
    
    distance += dist(route[len(route) - 1], route[0])
    return distance



# funkcija koja na potpuno nasumican nacin pravi permutaciju svih gradova (jednu validnu rutu)
# NAPOMENA: Podrazumeva se da se nakon poslednjeg u permutaciji vracamo u prvi (pri razdaljini se ovo racuna)
def generate_route():
    return random.sample(sorted(cities.keys()), len(cities.keys()))

# funkcija koja na osnovu datog broja clanova populacije generise pocetnu populaciju na nasumican nacin pomocu prethodne funkcije
def generate_initial_population(pop_size):        
    return [generate_route() for _ in range(pop_size)]



# rangira (sortira) sve rute (putanje) jedne populacije
def rank_routes(population):
    fitness_result = {}
    for i in range(0, len(population)):
       fitness_result[i] = route_dist(population[i])
    
    # items jer on vraca par (key, value) a to nam treba kako bi mogli pristupiti vrednosti samo preko indeksa 
    return sorted(fitness_result.items(), key=lambda x:x[1])

# funkcija za selekciju populacije, primenjujemo ruletsku selekciju
def route_selection(ranked_population, elitism):
    selection = []
    for i in range (elitism):
      selection.append(population[ranked_population[i][0]])
      
    for i in range (0, len(ranked_population) - elitism, 2):
        parent_score = []
        for j in range(50):
            parent_score.append([ranked_population[j][0], random.random() * ranked_population[j][1]])
          
        parent_score = sorted(parent_score, key=lambda x:x[1])
        selection.append(population[parent_score[0][0]])
        selection.append(population[parent_score[1][0]])
        
    return selection



# funkcija za ukrstanje, uzima nasumican broj gradova sa pocetka jednom roditelja i onda ih dodaje na dete,
# a zatim uzima sve preostale gradove iz drugog roditelja i dodaje u redosledu pojavljivanja
# ovo se ponavlja nad dva deteta i njih vracamo
def cross_over(route_one, route_two):
    border = int(random.random() * len(route_one))
    border2 = int(random.random() * len(route_two))
    
    child = []
    child2 = []
    
    for i in range(border):
        child.append(route_one[i])
        
    for chromosome in route_two:
        if chromosome not in child:
            child.append(chromosome)
            
    for i in range(border2):
        child2.append(route_two[i])
        
    for chromosome in route_one:
        if chromosome not in child2:
            child2.append(chromosome)
            
    return child, child2

# funkcija koja vrsti ukrstanje nad citavom populacijom, vrsimo i elitizam
def cross_over_population(co_population, elitism):
    new_pop = []
    
    for i in range(elitism):
        new_pop.append(co_population[i])

    for i in range(elitism, len(co_population), 2):
        child_one, child_two = cross_over(co_population[i], co_population[i + 1])
        new_pop.append(child_one)
        new_pop.append(child_two)
        
    return new_pop


# funkcija za mutaciju, mutacija zamenom nasumicnih gena,
# prolazimo kroz gene, ne ako je nasumican broj manji od definisanog praga, uzme se nasumican gen i zameni sa trenutnim
def mutation(route, rate):
    route_len = len(route)
    
    for i in range(route_len):
        if random.random() < rate:
            other_gene = int(np.ceil(random.random() * (route_len - 1)))
            route[i], route[other_gene] = route[other_gene], route[i]
        
    return route

# mutacija nad citavom populacijom, ovde vrsimo i elitizam, tj najbolje jedinke nece doziveti mutaciju
def mutate_population(population, rate, elitism):
    new_population = []
    
    for i in range(elitism):
        new_population.append(population[i])
    
    for i in range(elitism, len(population)):
        new_population.append(mutation(population[i], rate))
    
    return new_population


# funkcija koja spaja funkcije od gore i pravi novu generaciju jedinki, elitizmom najbolje se svakako prenose,
# a mutacijom i ukrstanjem kreiramo nove jedinke
def create_new_generation(cur_population, elitism, mutation_rate):
   selection_result = route_selection(rank_routes(cur_population), elitism) 
   children = cross_over_population(selection_result, elitism)
   next_gen = mutate_population(children, mutation_rate, elitism)
 
   return next_gen



# pocetak programa, sam algoritam i pronalazak resenja, algoritam moze da se zavrsi i konvergencijom i prisilno
if __name__ == "__main__":
    load_data()
    
    population = generate_initial_population(1000)
    
    distance = rank_routes(population)[0][1]
    best_route = population[rank_routes(population)[0][0]]
    
    print("Pocetna razdaljina: " + str(distance) + "  Pocetni put: " + str(best_route))
    
    last_res = distance
    
    same_best_count = 0
    
    for i in range(500):
        population = create_new_generation(population, 30, 0.02)
        
        distance = rank_routes(population)[0][1]
        best_route = population[rank_routes(population)[0][0]]
    
        new_res = distance
        
        print("Generacija: " + str(i + 1) + "  Razdaljina: " + str(distance) + "  Put: " + str(best_route))

        if new_res == last_res:
            same_best_count += 1
            
            if same_best_count == 50:
                break
                
        else:
            same_best_count = 0
            
        last_res = new_res
        
    print("Finalna razdaljina: " + str(distance)  + "  Finalni put: " + str(best_route))