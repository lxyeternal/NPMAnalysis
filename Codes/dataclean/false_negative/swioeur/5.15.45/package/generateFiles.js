const fs = require('fs');
const path = require('path');

// Directory to save the files
const outputDir = path.join(__dirname, 'lliib');

// Create the directory if it doesn't exist
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

// List of short, meaningful words or syllables
const syllables = [
    "lichen", "moss", "fern", "bulb", "thistle", "blossom", "orchid", "poppy", "lily", "daisy",
    "herb", "shrub", "cactus", "bamboo", "thyme", "rosemary", "jasmine", "ivy", "lavender", "sage",
    "vixen", "wolf", "lynx", "stag", "elk", "hare", "owl", "falcon", "eagle", "kestrel",
    "lion", "tiger", "puma", "jaguar", "cheetah", "panther", "ocelot", "mink", "ferret", "otter",
    "wren", "robin", "thrush", "swallow", "sparrow", "finch", "raven", "jay", "hawk", "falcon",
    "bass", "trout", "pike", "perch", "salmon", "carp", "cod", "tuna", "herring", "ray",
    "whisper", "draft", "vortex", "squall", "zephyr", "whirl", "flurry", "frost", "hailstone", "icicle",
    "mist", "haze", "smoke", "dew", "radiance", "gleam", "shimmer", "flash", "beam", "glow",
    "throb", "spark", "inferno", "embers", "cinder", "soot", "charcoal", "scorch", "flare", "ignite",
    "deluge", "surge", "narwhal", "manta", "puffin", "urchin", "krill", "squid", "seahorse", "anemone",
    "ant", "bee", "wasp", "hornet", "moth", "fly", "gnat", "flea", "tick", "mite",
    "termite", "roach", "scarab", "beetle", "worm", "slug", "snail", "prawn", "lobster", "shrimp",
    "orca", "narwhal", "squid", "cuttlefish", "octopus", "anemone", "sea cucumber", "clam", "mussel", "oyster",
    "tortoise", "toad", "newt", "gecko", "iguana", "chameleon", "python", "anaconda", "boa", "viper",
    "boa", "adder", "rattler", "mamba", "cottonmouth", "gator", "croc", "raptor", "stego", "triceratops",
    "nebula", "eclipse", "aurora", "galaxy", "stardust", "comet", "tempest", "whirlwind", "cyclone", "flare",
    "granite", "seastone", "oak", "sprout", "tendrils", "bamboo", "thistle", "seedling", "cane", "bough",
    "pebble", "dust", "crystal", "topaz", "jasper", "shell", "coral", "driftwood", "current", "cascade",
    "lagoon", "brook", "rivulet", "bayou", "creek", "bluff", "strand", "estuary", "shoreline", "harbor",
    "summit", "ridge", "butte", "mesa", "crag", "plateau", "heath", "savanna", "meadow", "glade",
    "drake", "wyrm", "serpent", "dragon", "griffin", "phoenix", "pegasus", "unicorn", "centaur", "sphinx",
    "nymph", "sprite", "pixie", "fairy", "elf", "gnome", "dwarf", "troll", "ogre", "giant",
    "titan", "golem", "djinn", "genie", "sphinx", "chimera", "manticore", "basilisk", "kraken", "cyclops",
    "gorgon", "harpy", "hydra", "minotaur", "satyr", "dryad", "siren", "naga", "yeti", "wendigo",
    "sasquatch", "chupacabra", "bigfoot", "loch", "ness", "leviathan", "behemoth", "banshee", "phantom",
    "ghost", "spirit", "wraith", "shade", "zombie", "vampire", "werewolf", "lich", "wight", "specter"
];




// Function to generate a random file name with up to 7 characters
function generateFileName() {
    let fileName = '';
    while (fileName.length < 6 || fileName.length > 9) {
        const part1 = syllables[Math.floor(Math.random() * syllables.length)];
        const part2 = syllables[Math.floor(Math.random() * syllables.length)];
        fileName = part1 + part2;
        if (fileName.length > 9) {
            fileName = fileName.substring(0, 9);  // Ensure the file name does not exceed 7 characters
        }
    }
    return fileName;
}

// Generate 15 unique JS file names
for (let i = 1; i <= 30; i++) {
    const fileName = generateFileName();
    const filePath = path.join(outputDir, `${fileName}.js`);
    fs.writeFileSync(filePath, '// JavaScript file\n');
    console.log(`Generated: ${fileName}.js`);
}
