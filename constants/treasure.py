"""
    Most of the treasure digging rewards were acquired from https://petpedia.fandom.com/
    Thank you preserving this data!
"""

class Treasure:
    TOWN_FOREST = ["Belt Stanchions", "Travel Backpack", "Travel Globe Decor", "Travel Metal Detector", "Travel Suitcase", "Escalator", "Baggage Trolley", "Travel Digital Clock", "Newspaper Stall", "Big Bird Wings"]
    
    DEEP_OCEAN = ["Blue Mermaid Dress", "Curly Long Wig", "Deep Ocean Bathtub", "Deep Ocean Bed", "Deep Ocean Chair", "Deep Ocean Mirror", "Deep Ocean Table", "Happy Dolphin", "Magic Mermaid Dress", "Treasure Bait", "Water Drop Hat"]
    
    ENCHANTED_POND = ["Enchanted Pond Archway", "Enchanted Pond Firefly", "Firefly Wings", "Frog Prince Potion", "Frog Princess Dress", "Frog Princess Floor", "Frog Princess Headdress", "Frog Princess Nymphaea Seat", "Frog Princess Shoes", "Frog Princess Wallpaper", "Magical Fireflies Tree Seed"]
    
    HAUNTED_SWAMP = ["Haunted Captain's Mask", "Haunted Captain's Poster", "Haunted Captain's Wig", "Haunted Parrot", "Haunted Pirate Barrel", "Haunted Pirate Eyepatch", "Haunted Pirate Scimitars", "Haunted Skeleton Chandelier", "Skeleton Captain Plushie", "Haunted Pirate Bandana", "Haunted Captain Hat"]
    
    THE_MOON = ["Cute Alien Plushie", "Flying Purple UFO", "Hungry Alien Hat", "Red Alien Plushie", "Space Flag", "Space Floor", "Spaceship Commander Chair", "Spaceship Relaxation Chair", "Spaceship Robot Guard", "Spaceship Tiller", "Space Wallpaper"]
    
    VANILLA_CHOCO_POND = ["Basket Of Chocolates", "Birthday Wall Decor", "Choco Ship", "Melted Chocolate Wig", "Chocolate Crown", "Birthday Noisemaker", "Chocolate Box", "Choco Lamp", "Chocolate Tiara", "Choco Photo Frame", "Chocolate Bird"]
    
    CRYSTAL_CAVE = ["Crystal Cave Floor", "Crystal Cave Teddy", "Crystal Cave Wallpaper", "Crystal Princess Dress", "Crystal Princess Hair Flower", "Crystal Princess Shoes", "Crystal Princess Wig", "Mystery Crystal Tree Seed", "Mystery Crystal Wig Dye", "Crystal Cave Wings"]
    
    ANCIENT_EGYPT = ["Ancient Golden Bracelet", "Ancient Pets Wall Painting", "Ancient Pets Wallpaper", "Ancient Sarcophagus", "Cleopatra Tunic", "Cleopatra Wig", "Egyptian Oasis", "Pharaoh Headdress", "Pharaoh Snake Crown", "Pharaoh Tunic", "Sacred Cat Statue"]
    
    PAWITCHED = ["Magical Potion Bowl", "Double Bun Wig", "Magic Carpet", "Magic Poster", "Magical Dove Jubble", "Magical Sceptre", "Magical Tiara", "Owl On Orb", "Pawitched Goblet", "Wizard Eye Piece", "Pawitched Mirror"]
    
    FABLES = ["Fable Bonfire", "Fable Signboard", "Fable Picnic Basket", "Fable Wood Floor", "Purple Flower Bed", "Fable Wood Wallpaper", "Fable Picnic Mat", "Country Girl Wig", "Fables Tyre Swing", "Picnic Cap", "Fable Ethereal Wigs"]
    
    WINTER_FAIRYLAND = ["Winter Fairy Crown", "Winter Fairy Cute Wig", "Winter Fairy Cute Dress", "Winter Fairy Boots", "Winter Fairy Tree Seed", "Winter Fairy Wallpaper", "Winter Fairy Floor", "Winter Fairy Log", "Winter Fairy Cake Decor", "Winter Fairy Fawn Plushie", "Winter Fairy Owl Summoning Bracelet"]
    
    GARDEN_PARADISE = ["Garden Bench", "Garden Bird House", "Gardening Boots", "Flower Dress", "Butterfly Mask", "Flower Wig", "Garden Shears", "Garden Light Statue II", "Lawn Mower", "Flower Crown", "Spring Butterflies Summoning Bracelet"]
    
    ENCHANTED_FOREST = ["Enchanted Fireflies", "Flowers Crown", "Magic Pixie Wings", "Mushroom Decor", "Pixie Dress", "Pixie Forest Floor", "Pixie Forest Wallpaper", "Pixie Mask", "Pixie Shoes", "Romantic Pixie Wig", "Wooden Pixie Chair"]
    
    DARK_CHRISTMAS = ["Pumpkinhead Snowman", "Dark Christmas Tree Decor", "Dark Christmas Banner", "Skull Christmas Lights", "Dark Christmas Signboard", "Dark Christmas Pile of Snow", "Santa's Black Cat", "Dark Christmas Mailbox", "Evil Santa Clock", "Dark Christmas Fireplace", "Raven Black Wings", "Evil Santa Beard"]
    
    LOST_TREASURES = [] # Dinamically generated?
    
    INTO_THE_WILD = ["Welcome To The Jungle Signboard", "Bees Gone Wild", "Wild Vines Decor", "Lotus Pond", "Wild Camp Fire", "Forest Angel Wings", "Wild Jungle Hat", "Periwinkle Bush", "Cobweb Plant Decor", "Wild Water Plant", "Wild Waterfall", "Wild Birds Nest"] 

    MAPPING = {
        1: TOWN_FOREST,
        3: ANCIENT_EGYPT,
        4: DEEP_OCEAN,
        5: THE_MOON,
        6: LOST_TREASURES,
        8: WINTER_FAIRYLAND,
        9: ENCHANTED_POND,
        10: CRYSTAL_CAVE,
        11: GARDEN_PARADISE,
        12: FABLES,
        13: PAWITCHED,
        14: VANILLA_CHOCO_POND,
        15: HAUNTED_SWAMP,
        16: DARK_CHRISTMAS,
        17: INTO_THE_WILD
    }