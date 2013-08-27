def topological_sort(g):
    """Return a list of vertices of directed acyclic graph g in topological
    order.

    If graph g has a cycle, the result will be incomplete.

    This algorithm runs in O(n+m) time using O(n) auxiliary space if g is
    represented using a adjacency list/map.
    """
    topo = []       # a list of vertices placed in topological order.
    ready = []      # list of vertices that have no remaining constraints
    incount = {}    # keep track of in-degree for each vertex
    for u in g.vertices():
        incount[u] = g.degree(u, False)
        if incount[u] == 0:
            ready.append(u)
    while len(ready) > 0:
        u = ready.pop()
        topo.append(u)
        for e in g.incident_edges(u):
            v = e.opposite(u)
            incount[v] -= 1
            if incount[v] == 0:
                ready.append(v)
    return topo

if __name__ == '__main__':
    from graph_examples import figure_14_12 as example
    g = example()
    for u in topological_sort(g):
        print (u.element())
