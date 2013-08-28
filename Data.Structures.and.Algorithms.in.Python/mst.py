from priority_queue import AdaptableHeapPriorityQueue

def MST_PrimJarnik(g):
    """Compute a minimum spanning tree of simple connected weighted graph g.

    Return a list of edges that comprise the MST (in arbitrary order).
    """
    dist = {}   # dist[v] is bound on distance to tree
    tree = []   # list of edges in spanning tree
    pq = AdaptableHeapPriorityQueue()   # dist[v] maps to value (v, e=(u, v))
    pq_locator = {} # map from vertex to its pq locator

    # for each vertex v of the graph, add an entry to the priority queue,
    # with the source having distance 0 and all others having infinite dist-
    # ance.
    for v in g.vertices():
        dist[v] = float("inf") if len(dist) > 0 else 0
        pq_locator[v] = pq.add(dist[v], (v, None))

    while not pq.is_empty():
        _, (u, edge) = pq.remove_min()  # unpack tuple from pq
        del pq_locator[u]               # u is no longer in pq
        if edge is not None:
            tree.append(edge)           # add edge to tree
        for link in g.incident_edges(u):
            v = link.opposite(u)
            if v in pq_locator: # thus v not yet in tree
                # see if edge (u, v) better connects v to the growing tree
                wgt = link.element()
                if wgt < dist[v]:
                    dist[v] =  wgt          # update the distance and ...
                    pq.update(pq_locator[v], wgt, (v, link)) # the pq entry
    return tree

if __name__ == "__main__":
    from graph_examples import figure_14_15 as example
    graph = example()
    edges = MST_PrimJarnik(graph)
    for edge in edges:
        print(str(edge))
