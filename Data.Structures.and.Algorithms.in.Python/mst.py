from priority_queue import AdaptableHeapPriorityQueue
from priority_queue import HeapPriorityQueue

def MST_PrimJarnik(g):  # O((n+m)logn)
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

def MST_Kruskal(g):
    """Compute a minimum spanning tree of a simple connected weighted graph g
    using Kruskal's algorithm.

    Return a list of edges that comprise the MST.
    """
    tree = []                   # list of edges in spanning tree
    pq = HeapPriorityQueue()    # entries are edges in g, with weights as key
    forest = Partition()        # keeps track of forest clusters
    position = {}               # map each node to its Partition entry

    for v in g.vertices():
        position[v] = forest.make_group(v)
    for e in g.edges():
        pq.add(e.element(), e)  # edge's element is assumed to be its weight

    size = g.vertex_count()
    while len(tree) != size - 1 and not pq.is_empty():
        # tree not spanning and unprocessed remain
        weight, edge = pq.remove_min()
        u, v = edge.endpoints()
        a = forest.find(position[u])
        b = forest.find(position[v])
        if a != b:
            tree.append(edge)
            forest.union(a, b)

    return tree

class Partition:
    """Union-find structure for maintaining disjoint sets."""
    # ---- nested Position class ---- #
    class Position:
        __slots__ = "_container", "_element", "_size", "_parent"

        def __init__(self, _container, e):
            """Create a new position that is the leader of its own group."""
            self._container = _container    # reference to Partition instance
            self._element = e
            self._size = 1
            self._parent = self

        def element(self):
            """Return element stored at this position."""
            return self._element

    # ---- public Partition methods ---- #
    def make_group(self, e):
        """Make a new group containing element e, and returns its Position."""
        return self.Position(self, e)

    def find(self, p):
        """Find the group containing p and return the position of its leader.
        """
        if p._parent != p:
            # overwrite pos._parent after recursion
            p._parent = self.find(p._parent)
        return p._parent

    def union(self, p, q):
        """Merges the groups containing elements p and q."""
        a = self.find(p)
        b = self.find(q)
        if a is not b:
            if a._size > b._size:
                b._parent = a
                a._size += b._size
            else:
                a._parent = b
                b._size += a._size

if __name__ == "__main__":
    from graph_examples import figure_14_15 as example
    graph = example()
    edges = MST_PrimJarnik(graph)
    for edge in edges:
        print(str(edge))
    print("="*20)
    edges = MST_Kruskal(graph)
    for edge in edges:
        print(str(edge))
