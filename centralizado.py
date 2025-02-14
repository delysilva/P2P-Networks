class CentralizedIndex:
    def __init__(self):
        self.index = {}  # Tabela centralizada: {arquivo: [lista de peers]}

    def add_file(self, peer_id, file_name):
        """Adiciona um arquivo à tabela centralizada."""
        if file_name not in self.index:
            self.index[file_name] = []
        self.index[file_name].append(peer_id)
        print(f"Arquivo '{file_name}' registrado no peer {peer_id}.")

    def find_file(self, file_name):
        """Busca um arquivo na tabela centralizada."""
        if file_name in self.index:
            peers = self.index[file_name]
            print(f"Arquivo '{file_name}' encontrado nos peers: {peers}")
            return peers
        else:
            print(f"Arquivo '{file_name}' não encontrado.")
            return []


# Simulação
if __name__ == "__main__":
    central_index = CentralizedIndex()

    # Adicionar arquivos
    central_index.add_file(peer_id=1, file_name="arquivo1.txt")
    central_index.add_file(peer_id=2, file_name="arquivo1.txt")
    central_index.add_file(peer_id=3, file_name="arquivo1.txt")

    # Buscar arquivos
    central_index.find_file(file_name="arquivo1.txt")
    central_index.find_file(file_name="arquivo_inexistente.txt")
