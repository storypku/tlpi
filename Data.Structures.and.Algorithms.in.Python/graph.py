import random

class Graph:
    """Representation of a simple graph using a adjacency map."""

    # ----  nested Vertex class  ---- #
    class Vertex:
        """Lightweight vertex structure for a graph."""
        __slots__ = "_element"

        def __init__(self, x):
            """Don't call constructor directly. Use Graph's
            insert_vertex(x)."""
            self._element = x

        def element(self):
            """Return element associated with this vertex."""
            return self._element

        def __hash__(self): # will allow vertex to be a map/set key
            return hash(id(self))

        def __str__(self):
            return str(self._element)

    # ----  nested Edge class  ---- #
    class Edge:
        """Lightweight edge structure for a graph."""
        __slots__ = "_origin", "_destination", "_element"

        def __init__(self, u, v, x):
            """Don't call constructor directly. Use Graph's insert_edge(u, v,
            x)."""
            self._origin = u
            self._destination = v
            self._element = x

        def endpoints(self):
            """Return (u, v) tuple for vertices u and v."""
            return (self._origin, self._destination)

        def opposite(self, v):
            """Return the vertex that is opposite v on the edge."""
            if not isinstance(v, Graph.Vertex):
                raise TypeError("v must be a Vertex")
            if v not in self.endpoints():
                raise ValueError("v not incident to edge")
            return self._destination if v is self._origin else self._origin

        def element(self):
            """Return element associated with this edge."""
            return self._element

        def __hash__(self): # will allow edge to be a map/set key
            return hash( (self._origin, self._destination) )

        def __str__(self):
            return "({0}, {1}, {2})".format(self._origin, self._destination,
                                            self._element)

    # ---- Graph methods ---- #
    def __init__(self, directed=False):
        """Create an empty graph (undirected, by default).

        Graph is directed if optional parameter is set to True.
        """
        self._outgoing = {}
        # only created second map for directed graph; use alias for undirected
        self._incoming = {} if directed else self._outgoing

    def is_directed(self):
        """Return True if this is a directed graph; False if undirected.

        Property is based on the original declaration of the graph, not its
        contents.
        """
        return self._incoming is not self._outgoing

    def vertex_count(self): # O(1)
        """Return the number of vertices in the graph."""
        return len(self._outgoing)

    def vertices(self): # O(n) where n is the number of vertices
        """Return an iteration of all vertices of the graph."""
        return self._outgoing.keys()

    def edge_count(self):   # O(n)
        """Return the number of edges in the graph."""
        total = sum(len(self._outgoing[v]) for v in self._outgoing)
        # for undirected graphs, make sure not to double-count edges
        return total if self.is_directed() else total // 2

    def edges(self): # O(n+m)
        """Return a set of all edges of the graph."""
        result = set()
        for secondary_map in self._outgoing.values():
            result.update(secondary_map.values())
        return result

    def _validate_vertex(self, v):
        """Verify that v is a Vertex of this graph."""
        if not isinstance(v, self.Vertex):
            raise TypeError("Vertex expected")
        if v not in self._outgoing:
            raise ValueError("Vertex does not belong to this graph.")

    def get_edge(self, u, v): # O(1) expected
        """Return the edge from u to v, or None if not adjacent."""
        self._validate_vertex(u)
        self._validate_vertex(v)
        return self._outgoing[u].get(v) # returns None if v not adjacent

    def degree(self, v, outgoing=True): # O(1) expected
        """Return number of (outgoing) edges incident to vertex v in the
        graph.

        If graph is directed, optional parameter used to count incoming edges
        when set False.
        """
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        return len(adj[v])

    def incident_edges(self, v, outgoing=True): # O(degree(v))
        """Return all (outgoing) edges incident to vertex v in the graph.

        If graph is directed, optional parameter used to request incoming
        edges if set False.
        """
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        for edge in adj[v].values():
            yield edge

    def insert_vertex(self, x=None): # O(1) expected
        """Insert and return a new Vertex with element x."""
        v = self.Vertex(x)
        self._outgoing[v] = {}
        if self.is_directed():
            self._incoming[v] = {}  # need distinct map for incoming edges
        return v

    def insert_edge(self, u, v, x=None): # O(1) expected
        """Insert and return a new Edge from u and v with auxiliary element
        x.

        Raise a ValueError if u and v are not vertices of the graph or if u
        and v are already adjacent.
        """
        if self.get_edge(u, v) is not None:      # includes error checking
            raise ValueError("u and v are already adjacent")
        e = self.Edge(u, v, x)
        self._outgoing[u][v] = e
        self._incoming[v][u] = e
        return e

    def __expire_edge(self, e):
        """Helper function for removing edge e: mark its expiration and help
        garbage collection."""
        e._origin = e._destination = e._element = None

    def remove_edge(self, e): # O(1) expected
        """Remove and return element of edge e from the graph."""
        if not isinstance(e, Graph.Edge):
            raise TypeError("e must be an Edge")
        if e._origin is None:
            raise ValueError("e is already removed from this graph.")
        u, v = e.endpoints()
        del self._outgoing[u][v]
        del self._incoming[v][u]
        result = e.element()
        self.__expire_edge(e)
        return result

    def remove_vertex(self, v): # O(degree(v))
        """Remove vertex v and all its incident edges from the graph."""
        self._validate_vertex(v)
        directed = self.is_directed()
        for u in self._outgoing[v].keys():
            e = self._incoming[u][v]
            self.__expire_edge(e)
            del self._incoming[u][v]
        del self._outgoing[v]
        if directed:
            for u in self._incoming[v].keys():
                e = self._outgoing[u][v]
                self.__expire_edge(e)
                del self._outgoing[u][v]
            del self._incoming[v]
        return v.element()

    def __DFS_recursive(self, u, discovered, outgoing=True):
        """Perform DFS of the undiscovered portion of the graph starting at
        Vertex u.

        discovered is a dictionary mapping each vertex to the edge that was
        used to discover it during the Depth-First-Search process. (u should
        be "discovered" prior to the call.)

        Newly discovered vertices will be added to the dictionary as a res-
        ult.
        """
        for e in self.incident_edges(u, outgoing):
            v = e.opposite(u)
            if v not in discovered:
                discovered[v] = e
                self.__DFS_recursive(v, discovered, outgoing)

    def __DFS(self, u, outgoing=True):
        """Helper function to return a Python dictionary mapping each vertex
        to the edge that was used to discover it during the DFS process star-
        ting from vertex u.
        """
        discovered = {u:None}
        self.__DFS_recursive(u, discovered, outgoing)
        return discovered

    def path(self, u, v):
        """
        Return the path from u to v (Suppose that u and v are distinct).
        """
        self._validate_vertex(u)
        self._validate_vertex(v)
        discovered = self.__DFS(u)
        path_ = []   # empty path by default
        if (v is not u) and (v in discovered):
            path_.append(v)
            walk = v
            while walk is not u:
                e = discovered[walk]  # find edge leading to walk
                parent = e.opposite(walk)
                path_.append(parent)
                walk = parent
            path_.reverse()  # reorient path from u to v
        return path_

    def is_connected(self):  # O(n+m)
        """Return True if the graph is connected (for undirected graphs) or
        strongly connected (for directed graphs); False otherwise."""
        vertex_count = self.vertex_count()
        if vertex_count < 2:
            return True
        v = random.choice(list(self.vertices())) # choose an arbitrary vertex
        discovered = self.__DFS(v)
        if not self.is_directed():
            return len(discovered) == vertex_count
        elif len(discovered) != vertex_count: # for directed graph
                return False
        else:
            discovered = self.__DFS(v, False)
            return len(discovered) == vertex_count

    def DFS_complete(self):
        """Perform DFS for entire graph and return forest as a dictionary.

        Return maps each vertex v to the edge that was used to discover it.
        (Vertices that are roots of a DFS tree are mapped to None.)

        For undirected graphs, the returned discovery dictionary represents a
        DFS forest for the entire graph.

        NOTE: this method is not of much use for directed graphs for now as
        a result of the complexity for finding strongly connected components
        of a directed graph. However, there does exist an approach for com-
        puting those components in O(n+m) time, making use of two separate
        DFS traversals.
        """
        if self.is_directed:
            raise NotImplementedError("Support for finding strongly connected"
                " components of directed graphs not implemented")
        forest = {}
        for v in self.vertices():
            if v not in forest:
                forest[v] = None
                self.__DFS_recursive(v, forest)
        return forest

