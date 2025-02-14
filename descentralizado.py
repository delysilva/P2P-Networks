import networkx as nx
import matplotlib.pyplot as plt

class PeerUnstructured:
    def __init__(self, id):
        self.id = id
        self.files = []

    def add_file(self, file_name):
        """Adiciona um arquivo ao peer."""
        self.files.append(file_name)

    def has_file(self, file_name):
        """Verifica se o peer possui o arquivo."""
        return file_name in self.files


class P2PUnstructuredNetwork:
    def __init__(self, num_peers):
        self.graph = nx.Graph()
        self.peers = {i: PeerUnstructured(i) for i in range(num_peers)}
        for peer_id in self.peers:
            self.graph.add_node(peer_id)

    def connect_peers(self, peer1, peer2):
        """Conecta dois peers na rede."""
        self.graph.add_edge(peer1, peer2)

    def add_file_to_peer(self, peer_id, file_name):
        """Adiciona um arquivo a um peer."""
        self.peers[peer_id].add_file(file_name)

    def find_file(self, start_peer, file_name, ttl):
        """Busca um arquivo na rede usando flooding."""
        visited = set()
        queue = [(start_peer, ttl)]

        while queue:
            current_peer, remaining_ttl = queue.pop(0)
            if current_peer in visited:
                continue
            visited.add(current_peer)

            if self.peers[current_peer].has_file(file_name):
                print(f"Arquivo '{file_name}' encontrado no peer {current_peer}.")
                return current_peer

            if remaining_ttl > 0:
                for neighbor in self.graph.neighbors(current_peer):
                    queue.append((neighbor, remaining_ttl - 1))

        print(f"Arquivo '{file_name}' não encontrado.")
        return None


# Simulação
if __name__ == "__main__":
    network = P2PUnstructuredNetwork(num_peers=5)

    # Conectar peers
    network.connect_peers(0, 1)
    network.connect_peers(1, 2)
    network.connect_peers(1, 3)
    network.connect_peers(3, 4)

    # Adicionar arquivos
    network.add_file_to_peer(2, "arquivo1.txt")

    # Buscar arquivos
    network.find_file(start_peer=0, file_name="arquivo1.txt", ttl=2)

    # Visualizar grafo da rede
    nx.draw(network.graph, with_labels=True, node_color='lightblue', node_size=800)
    plt.show()