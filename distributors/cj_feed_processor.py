from xml.dom import minidom

class CjFeed:
    def __init__(self, source=None):
        self.loadSource(source)
        
    def _load(self, source):
        sock = toolbox.openAnything(source)
        xmldoc = minidom.parse(sock).documentElement
        sock.close()
        return xmldoc
        
    def loadSource(self, source):
        """load source"""
        self.source = self._load(source)
