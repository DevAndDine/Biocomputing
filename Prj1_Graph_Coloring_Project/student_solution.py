import random
from deap import base, creator, tools, algorithms


class Node:
    def __init__(self, vertex):
        self.vertex = vertex
        self.next = None


class Graph:
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.graph = {}
        for i in range(n):
            self.graph[i] = None
        self.edges = []

    def add_edge(self, u, v):
        if (u, v) not in self.edges and (v, u) not in self.edges and u != v:
            self.edges.append((u, v))
            
            # Add to u's linked list
            node_v = Node(v)
            node_v.next = self.graph[u]
            self.graph[u] = node_v
            
            # Add to v's linked list
            node_u = Node(u)
            node_u.next = self.graph[v]
            self.graph[v] = node_u


def init_graph(file_path):
    # Q1: Read graph file and build graph with adjacency linked list
    f = open(file_path, 'r')
    lines = f.readlines()
    f.close()
    
    cleaned_lines = []
    for line in lines:
        s = line.strip()
        if s:
            cleaned_lines.append(s)
            
    n = int(cleaned_lines[0])
    k = int(cleaned_lines[1])
    g = Graph(n, k)
    
    for i in range(2, len(cleaned_lines)):
        parts = cleaned_lines[i].split()
        if len(parts) == 2:
            u = int(parts[0])
            v = int(parts[1])
        elif len(parts) == 1:
            val_str = parts[0]
            mid = len(val_str) // 2
            u = int(val_str[:mid])
            v = int(val_str[mid:])
        g.add_edge(u, v)
        
    return g


def decode_individual(graph, individual):
    # Q2: Decode binary genome into color assignments
    bits_per_node = 1
    while (1 << bits_per_node) < graph.k:
        bits_per_node += 1
        
    if len(individual) < graph.n * bits_per_node:
        return None
        
    colors = {}
    for i in range(graph.n):
        node_bits = individual[i * bits_per_node : (i + 1) * bits_per_node]
        val = 0
        for b in node_bits:
            val = (val << 1) + b
        if val >= graph.k:
            return None  # Invalid color encoding
        colors[i] = val
        
    return colors


def eval_graph(graph, individual):
    # Q2: Evaluate fitness based on satisfied edges
    colors = decode_individual(graph, individual)
    if colors is None:
        return (0.0,)
        
    if len(graph.edges) == 0:
        return (1.0,)
        
    satisfied = 0
    for edge in graph.edges:
        u = edge[0]
        v = edge[1]
        if colors[u] != colors[v]:
            satisfied += 1
            
    score = satisfied / len(graph.edges)
    return (score,)


def run_ga(file_path, population_size=300, ngen=200, cxpb=0.8, mutpb=0.3):
    # Q3: Run genetic algorithm using DEAP components
    graph = init_graph(file_path)
    
    bits_per_node = 1
    while (1 << bits_per_node) < graph.k:
        bits_per_node += 1
    genome_length = graph.n * bits_per_node

    if not hasattr(creator, "FitnessMax"):
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    if not hasattr(creator, "Individual"):
        creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("attr_bool", random.randint, 0, 1)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, genome_length)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", lambda ind: eval_graph(graph, ind))
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=1.0 / genome_length if genome_length > 0 else 0.5)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pop = toolbox.population(n=population_size)
    hof = tools.HallOfFame(1)

    algorithms.eaSimple(pop, toolbox, cxpb=cxpb, mutpb=mutpb, ngen=ngen, halloffame=hof, verbose=False)

    best_individual = hof[0]
    return best_individual.fitness.values[0]

