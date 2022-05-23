import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def add_vertices(vertices):
    n = int(input('Enter number of vertices:'))
    while n == 0:
        n = int(input('Number of vertices cannot be zero(Try Again):'))

    for i in range(len(vertices), len(vertices) + n):
        if isinstance(vertices, list):
            vertices.append(i)
        else:
            vertices = np.append(vertices, np.array(i))

    vertices = np.array(vertices)

    return vertices


def add_edges(edges, vertices):
    while True:
        e = input('Enter Edge(x,y) or type \'q\' to exit: ')
        if e == 'q':
            break

        e_list = list(map(int, e.split(',')))
        if e_list[0] in vertices and e_list[1] in vertices:
            edges = np.append(edges, np.array([e_list]), axis=0)
        else:
            print("One of the vertex is NOT present!")

    return edges


def adjacency_matrix(vertices, edges, directed):
    adj_mat = np.zeros((vertices.size, vertices.size), int)
    for i in edges:
        adj_mat[i[0]][i[1]] += 1
        if not directed:
            adj_mat[i[1]][i[0]] += 1
        elif i[0] == i[1]:
            adj_mat[i[1]][i[0]] = 2

    return adj_mat


def clear():
    vertices = []
    edges = np.empty((0, 2), int)

    directed = int(input("\nSelect Type of Graph\n1. Directed Graph\n2. Un-Directed Graph\nEnter your choice:"))
    if directed == 1:
        directed = True
    else:
        directed = False

    return vertices, edges, directed


def find_adj(vertices, find_v, mat):
    adj_v = []
    for v in vertices:
        if mat[find_v][v] != 0:
            adj_v.append(v)

    return adj_v


def dfs(vertices, explore, mat, visited, stack, sec):
    if explore not in visited:
        if not sec:
            stack.append(explore)
        visited.add(explore)
        for v in find_adj(vertices, explore, mat):
            dfs(vertices, v, mat, visited, stack, sec)


def validate(vertices, edges):
    if len(vertices) == 0:
        print("Please add vertices first...")
        return False
    elif edges.size == 0:
        print("Please add edges first...")
        return False
    else:
        return True


def degree(mat, directed):
    print("By Handshaking Lemma,", end=" ")
    if directed:
        print("No. of edges are", mat.sum())
        indegree = mat.sum(axis=0)
        outdegree = mat.sum(axis=1)

        print("Indegree:\nSum of Columns")
        for i in range(indegree.size):
            print(f"d-({i})={indegree[i]}")

        print("Outdegree:\nSum of Rows")
        for i in range(outdegree.size):
            print(f"d+({i})={outdegree[i]}")
    else:
        print("No. of edges are", mat.sum() / 2)
        print("Degree of each vertex:")
        deg = mat.sum(axis=0)
        for i in range(deg.size):
            print(f"d({i})={int(deg[i] / 2)}")


def draw_graph(adj_mat, direction):
    if direction:
        temp = nx.MultiDiGraph()
    else:
        temp = nx.Graph()
    G = nx.from_numpy_matrix(adj_mat, parallel_edges=True, create_using=temp)
    nx.draw(G, arrows=direction, with_labels=True, connectionstyle='arc3, rad = 0.1')
    plt.show()


def numgraph():
    vertices, edges, directed = clear()

    while True:
        print(
            "\nMenu\n1. Add Vertices\n2. Add edge\n3. Adjacency Matrix\n4. Clear Graph\n5. Find Strongly Connected "
            "Components.\n6. Find Degree of each vertex\n7. Havel-Hakimi Algorithm\n8. Draw\n0. EXIT") 
        choice = int(input("Enter your choice:"))

        if choice == 0:
            break
        elif choice == 1:
            vertices = add_vertices(vertices)
            print(vertices)
        elif choice == 2:
            if len(vertices) == 0:
                print("Please add vertices first...")
            else:
                edges = add_edges(edges, vertices)
                print(edges)
        elif choice == 3:
            if validate(vertices, edges):
                adj_mat = adjacency_matrix(vertices, edges, directed)
                print("Adjacency Matrix:")
                print(adj_mat)
        elif choice == 4:
            vertices, edges, directed = clear()
        elif choice == 5:
            if validate(vertices, edges):
                adj_mat = adjacency_matrix(vertices, edges, directed)
                visited = set()
                stack = []

                for i in vertices:
                    dfs(vertices, i, adj_mat, visited, stack, False)

                tr = adj_mat.transpose()

                visited = set()
                scc = []

                for s in stack:
                    stack.pop(0)
                    if s not in visited:
                        visited = set()
                        dfs(vertices, s, tr, visited, stack, True)
                        scc.append(visited)

                for i in range(len(scc) - 1, -1, -1):
                    if i != 0:
                        print(scc[i] - scc[i - 1])
                    else:
                        print(scc[i])

                print(f"There are {len(scc)} Strongly Connected Components.")

                if len(scc) == 1 and scc[0] == set(vertices):
                    print("Graph is Strongly Connected Components!")
        elif choice == 6:
            if validate(vertices, edges):
                adj_mat = adjacency_matrix(vertices, edges, directed)
                degree(adj_mat, directed)
        elif choice == 7:
            pass
            """
            degree_seq = input("Please Enter Degree Sequence:")
            degree_seq = set(degree_seq.split(','))
            degree_seq = {int(i) for i in degree_seq}
            print(degree_seq)

            for d in degree_seq:
                if d < len(degree_seq) - 1 or (sum(degree_seq) % 2) == 0:
                    print("Not Graphical Sequence...")
                else:"""
        elif choice == 8:
            adj_mat = adjacency_matrix(vertices, edges, directed)
            draw_graph(adj_mat, directed)


if __name__ == '__main__':
    numgraph()
