import math


def bits_per_vertex(k):
    """Calculate the number of bits needed per vertex."""
    return math.ceil(math.log2(k))


def decode_individual(graph, individual):
    """
    Decodes the binary bitstring individual into a list of integer colors per vertex.
    Returns None if any color is invalid (i.e. >= graph.k).
    """
    width = bits_per_vertex(graph.k)
    expected_length = graph.n * width
    
    if len(individual) != expected_length:
        return None
    
    colors = []
    for i in range(graph.n):
        start = i * width
        chunk = individual[start : start + width]
        
        # Convert bit chunk to integer color
        color = 0
        for bit in chunk:
            color = (color << 1) | int(bit)
            
        if color >= graph.k:
            return None  # Invalid color encoding
            
        colors.append(color)
        
    return colors


def get_unique_edges(graph):
    """Extract unique undirected edges (u, v) with u < v from the adjacency list."""
    edges = []
    for u in range(graph.n):
        curr = graph.graph[u]
        while curr is not None:
            v = curr.vertex
            if u < v:
                edges.append((u, v))
            curr = curr.next
    return edges


def eval_graph(graph, individual):
    """
    Question 2: Standard graph-coloring fitness helper.
    Computes satisfied edges / total edges.
    Returns a one-item tuple: (fitness,)
    """
    colors = decode_individual(graph, individual)
    if colors is None:
        return (0.0,)
    
    edges = get_unique_edges(graph)
    if not edges:
        return (0.0,)
    
    satisfied = 0
    for u, v in edges:
        if colors[u] != colors[v]:
            satisfied += 1
            
    fitness = satisfied / len(edges)
    return (fitness,)


def eval_balance(graph, individual):
    """
    Question 1: Balanced-coloring fitness.
    Fitness = (satisfied_edges / m) * product_over_colors(count(c) / n)
    Returns a one-item tuple: (fitness,)
    """
    colors = decode_individual(graph, individual)
    if colors is None:
        return (0.0,)
    
    # 1. Edge satisfaction fraction
    edge_fitness = eval_graph(graph, individual)[0]
    if edge_fitness == 0.0:
        return (0.0,)
    
    # 2. Color balance product term
    balance_product = 1.0
    for color in range(graph.k):
        count_c = colors.count(color)
        if count_c == 0:
            return (0.0,)  # Missing color bucket makes product 0
        balance_product *= (count_c / graph.n)
        
    total_fitness = edge_fitness * balance_product
    return (total_fitness,)


def encode_colors(colors, k):
    """Helper to convert a list of vertex colors back into a bitstring individual."""
    width = bits_per_vertex(k)
    bitstring = []
    for color in colors:
        for shift in range(width - 1, -1, -1):
            bitstring.append((color >> shift) & 1)
    return bitstring


def one_neutral(graph, individual):
    """
    Question 3: One-step Neutrality.
    Calculates fraction of single vertex color changes that preserve eval_graph fitness.
    Returns a float: neutral_count / total_mutations
    """
    colors = decode_individual(graph, individual)
    if colors is None:
        return 0.0
    
    original_fitness = eval_graph(graph, individual)[0]
    total_mutations = graph.n * (graph.k - 1)
    
    if total_mutations == 0:
        return 0.0
    
    neutral_count = 0
    
    for vertex in range(graph.n):
        original_color = colors[vertex]
        
        for new_color in range(graph.k):
            if new_color == original_color:
                continue
            
            # Create mutated color array
            mutated_colors = list(colors)
            mutated_colors[vertex] = new_color
            
            # Encode back to bitstring individual
            mutant_individual = encode_colors(mutated_colors, graph.k)
            mutant_fitness = eval_graph(graph, mutant_individual)[0]
            
            # Check if fitness is preserved
            if math.isclose(mutant_fitness, original_fitness, rel_tol=1e-12, abs_tol=1e-12):
                neutral_count += 1
                
    return neutral_count / total_mutations
