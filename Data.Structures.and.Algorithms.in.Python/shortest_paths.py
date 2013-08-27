from priority_queue import AdaptableHeapPriorityQueue

def shortest_path_lengths(g, src):
    """Compute shortest-path distances from src to reachable vertices of g.

    Graph g can be undirected or directed, but must be weighted such that
    e.element() returns a non-negative weight for each edge e.

    Return dictionary mapping each reachable vertex to its distance from src.

    For a graph with n vertices and m edges, Dijkstra's algorithm can compute
    the distance from s to all other vertices in the better of O(n**2) or
    O((n+m)logn) time.
    """
    return __shortest_path_lengths_noinf(g, src)

def __shortest_path_lengths_noinf(g, src):
    """Compute shortest-path distances from src to reachable vertices of g
    without python inf notation."""
    dist = {}    # dist[v] is upper bound from s to v
    cloud = {}    # map reachable v to its dist[v] value
    pq = AdaptableHeapPriorityQueue() # vertex v will have key dist[v]
    pq_locator = {}    # map from vertex to its pq locator

    dist[src] = 0
    pq_locator[src] = pq.add(0, src)
    while not pq.is_empty():
        key, u = pq.remove_min()
        cloud[u] = key      # its correct dist[u] value
        del pq_locator[u]   # u is no longer needed
        for edge in g.incident_edges(u):    # outgoing edges (u, v)
            v = edge.opposite(u)
            if v not in cloud:
                # perform relaxation step on edge (u, v)
                new_dist = dist[u] + edge.element()
                if v not in dist:
                    # add an vertex to dist until after an edge reaches it
                    dist[v] = new_dist
                    # and add it to the priority queue and save locator for
                    # future updates
                    pq_locator[v] = pq.add(new_dist, v)
                elif dist[v] > new_dist:    # If better path to v exists...
                    dist[v] = new_dist      # update the distance, and...
                    pq.update(pq_locator[v], new_dist, v)  # the pq entry
    # Now, dist and cloud are the same, they both only include the reachable
    # vertices.
    return cloud

def __shortest_path_lengths_inf(g, src):
    """Compute shortest-path distances from src to reachable vertices of g
    with python inf notation."""

    dist = {}                         # dist[v] is upper bound from s to v
    cloud = {}                        # map reachable v to its dist[v] value
    pq = AdaptableHeapPriorityQueue() # vertex v will have key dist[v]
    pq_locator = {}                   # map from vertex to its pq locator

    # for each vertex v of the graph, add an entry to the priority queue, with
    # the source having distance 0 and all others having infinite distance
    for v in g.vertices():
        if v is src:
            dist[v] = 0
        else:
            dist[v] = float('inf')          # syntax for positive infinity
        pq_locator[v] = pq.add(dist[v], v)  # save locator for future updates

    while not pq.is_empty():
        key, u = pq.remove_min()
        cloud[u] = key                  # its correct dist[u] value
        del pq_locator[u]               # u is no longer in pq
        for e in g.incident_edges(u):   # outgoing edges (u,v)
            v = e.opposite(u)
            if v not in cloud:
                # perform relaxation step on edge (u,v)
                wgt = e.element()
                if dist[u] + wgt < dist[v]:         # better path to v?
                    dist[v] = dist[u] + wgt         # update the distance, and
                    pq.update(pq_locator[v], dist[v], v)        # the pq entry

    return cloud      # only includes reachable vertices

def shortest_path_tree(g, src, dist):   # O(n+m)
    """Reconstruct shortest-path tree rooted at vertex src, given distance
    map dist.

    Return tree as a map from each reachable vertex v (other than src) to the
    edge e = (u, v) that is used to reach v from its parent u in the tree.
    """
    tree = {}
    for v in dist:
        if v is not src:
            for e in g.incident_edges(v, False):    # consider INCOMING edges
                u = e.opposite(v)
                wgt = e.element()
                if dist[v] == dist[u] + wgt:
                    tree[v] = e     # edge e is used to reach v
    return tree

if __name__ == "__main__":
    from graph_examples import figure_14_15 as example
    g = example()
    for v in g.vertices():
        if v.element() == "BWI":
            src = v
    vert_dists = shortest_path_lengths(g, src)
    for vertex, dist in vert_dists.items():
        print (str(vertex), ":", dist)

