import os
import zlib
from xml.etree import ElementTree
from .utils.hash import hashInt32
from pathlib import Path

class Database:
    def __init__(self) -> None:
        self._db_path:str = os.path.join(os.path.dirname(__file__), Path("./static/assets/YMtWIOks1W"))
        self.items:list[dict] = []

    def load(self) -> None:
        with open(self._db_path, "rb") as f:
            decompressed = zlib.decompress(f.read())
            xml_root = ElementTree.fromstring(decompressed.decode('utf-8'))
            self._populateItems(xml_root)
    
    def _populateItems(self, root=None) -> None:
        if root is None:
            return

        for child in root:
            if not root.tag == "itemgroup":
                self._populateItems(child)
            else:
                if "min" in child.tag: continue
                if "name" in child.attrib:
                    child.attrib["itemHash"] = hashInt32(child.attrib["name"])

                self.items.append(child.attrib)

    def find_item_by_token(self, token:str) -> dict:
        for item in self.items:
            if "token" in item and item["token"] == token:
                return item
        return {}
    
    def find_item_by_name(self, name:str) -> dict:
        for item in self.items:
            if "name" in item and item["name"] == name:
                return item
        return {}
    
    def find_item_by_hash(self, item_hash:int) -> dict:
        for item in self.items:
            if "itemHash" in item and item["itemHash"] == item_hash:
                return item
        return {}
    
    def get_non_buyable_items(self) -> list[dict]:
        non_buyable_items = []
        for item in self.items:
            if "properties" in item and "nonBuyable" in item["properties"]:
                non_buyable_items.append(item)
        
        return non_buyable_items


