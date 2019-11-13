class Metrics:
    def __init__(self):
        self._byte = 0
        self._latency = 0

    def get_byte(self):
        return self._byte

    def get_latency(self):
        return self._latency

    def update_byte(self, byte):
        self._byte += byte

    def update_latency(self, latency):
        self._latency += latency
