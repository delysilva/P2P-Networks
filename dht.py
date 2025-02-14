import hashlib
import networkx as nx
import matplotlib.pyplot as plt

class PeerDHT:
    def __init__(self, id, max_peers):
        self.id = id  # Identificador único do peer
        self.files = {}  # Tabela hash para armazenar arquivos (chave -> valor)
        self.successor = None  # Próximo peer no anel
        self.max_peers = max_peers  # Total de peers na rede

    def add_file(self, file_name):
        """Insere um arquivo na tabela local."""
        file_hash = self.hash_function(file_name)
        self.files[file_hash] = file_name
        print(f"Arquivo '{file_name}' (hash {file_hash}) armazenado no peer {self.id}.")

    def find_file(self, file_name, path=None):
        """Procura por um arquivo no anel e registra o caminho percorrido."""
        if path is None:
            path = []
        path.append(self.id)

        file_hash = self.hash_function(file_name)
        if file_hash in self.files:
            print(f"Arquivo '{file_name}' encontrado no peer {self.id}.")
            return path
        else:
            print(f"Peer {self.id}: Arquivo '{file_name}' não encontrado. Encaminhando para o próximo.")
            if self.successor:
                return self.successor.find_file(file_name, path)
            else:
                print("Erro: Nenhum sucessor encontrado!")
                return path

    def hash_function(self, key):
        """Calcula o hash de uma chave para mapear ao espaço de chaves."""
        return int(hashlib.sha1(key.encode()).hexdigest(), 16) % self.max_peers


class P2PStructuredNetwork:
    def __init__(self, num_peers):
        self.num_peers = num_peers
        self.peers = [PeerDHT(i, num_peers) for i in range(num_peers)]

        # Conecta os peers em forma de anel
        for i in range(num_peers):
            self.peers[i].successor = self.peers[(i + 1) % num_peers]

    def add_file_to_peer(self, peer_id, file_name):
        """Adiciona um arquivo a um peer específico."""
        self.peers[peer_id].add_file(file_name)

    def find_file_in_network(self, start_peer_id, file_name):
        """Busca um arquivo a partir de um peer inicial."""
        print(f"\nIniciando busca pelo arquivo '{file_name}' a partir do peer {start_peer_id}.")
        path = self.peers[start_peer_id].find_file(file_name)
        print(f"Caminho percorrido: {path}")
        return path

    def visualize_network(self):
        """Visualiza a rede estruturada como um anel."""
        graph = nx.DiGraph()
        for peer in self.peers:
            graph.add_edge(peer.id, peer.successor.id)
        nx.draw_circular(graph, with_labels=True, node_color='lightgreen', node_size=800, font_size=10)
        plt.title("Rede P2P Estruturada (DHT - Anel)")
        plt.show()


# Exemplo de uso
if __name__ == "__main__":
    # Cria uma rede estruturada com 10 peers.
    network = P2PStructuredNetwork(num_peers=10)

    # Adiciona arquivos a peers específicos.
    network.add_file_to_peer(peer_id=2, file_name="arquivo1.txt")
    network.add_file_to_peer(peer_id=7, file_name="arquivo2.txt")



    # Busca os arquivos na rede e exibe os caminhos percorridos.
    network.find_file_in_network(start_peer_id=0, file_name="arquivo1.txt")
    network.find_file_in_network(start_peer_id=5, file_name="arquivo2.txt")

    # Visualiza a rede como um anel.
    network.visualize_network()
