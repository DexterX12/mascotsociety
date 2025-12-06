import zlib
from xml.etree import ElementTree
import os

class Database:
    def __init__(self) -> None:
        self._db_path:str = os.path.join(os.path.dirname(__file__), "static/assets/YMtWIOks1W")
        self.items:list[dict] = []

    def load(self) -> None:
        with open(self._db_path, "rb") as f:
            decompressed = zlib.decompress(f.read())
            xml_root = ElementTree.fromstring(decompressed.decode('utf-8'))
            self._populate_items(xml_root)
    
    def _populate_items(self, root=None) -> None:
        for child in root:
            if not root.tag == "itemgroup":
                self._populate_items(child)
            
            self.items.append(child.attrib)

    def findItemByToken(self, token:str) -> dict:
        for item in self.items:
            if item['token'] == token:
                return item
        return {}
