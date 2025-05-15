const fs = require('fs');
const path = require('path');

// Directory to save the files
const outputDir = path.join(__dirname, 'indocs');

// Create the directory if it doesn't exist
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

// List of short, meaningful words or syllables
const syllables = [
    "whisper", "draft", "vortex", "squall", "zephyr", "glide", "flurry", "rime", "sleet", "crystal",
    "droplet", "veil", "haze", "smoke", "dew", "radiance", "glimmer", "flare", "flicker", "beam",
    "throb", "glint", "spark", "blaze", "cinder", "soot", "coal", "char", "flame", "kindle",
    "bass", "trout", "pike", "perch", "salmon", "carp", "cod", "tuna", "herring", "ray",
    "aphid", "drone", "hornet", "moth", "gnat", "flea", "tick", "mite", "beetle", "scarab",
    "termite", "roach", "scarab", "worm", "slug", "snail", "prawn", "lobster", "shrimp", "crab",
    "deluge", "torrent", "orca", "manta", "marlin", "seal", "urchin", "salmon", "krill", "reef",
    "lichen", "bulb", "thorn", "blossom", "petal", "poppy", "iris", "thyme", "shrub", "succulent",
    "bamboo", "vine", "ivy", "orchid", "sage", "mint", "lavender", "herb", "cactus", "bush",
    "vixen", "wolf", "ursus", "stag", "elk", "leveret", "owl", "falcon", "osprey", "kite",
    "lioness", "panther", "cougar", "lynx", "leopard", "jaguar", "cheetah", "otter", "mink", "seal",
    "sparrow", "thrush", "warbler", "swift", "crow", "raven", "jay", "hawk", "falcon", "kite",
    "celestial", "lunar", "solstice", "radiance", "cosmos", "nebula", "drift", "breeze", "tempest", "ember",
    "granite", "shoreline", "willow", "fern", "tendril", "trunk", "husk", "seed", "creeper", "twig",
    "quartz", "silt", "powder", "prism", "jewel", "opal", "shell", "coral", "reef", "current",
    "lagoon", "islet", "delta", "rivulet", "spring", "cascade", "gulf", "bay", "bluff", "strand",
    "tortoise", "frog", "toad", "newt", "salamander", "gecko", "iguana", "python", "viper", "cobra",
    "boa", "adder", "rattlesnake", "mamba", "cottonmouth", "alligator", "crocodile", "rex", "raptor", "trike",
    "drake", "hydra", "wyrm", "serpent", "dragon", "griffin", "pegasus", "unicorn", "centaur", "siren",
    "nymph", "sprite", "pixie", "fairy", "elf", "gnome", "dwarf", "orc", "troll", "ogre",
    "giant", "titan", "golem", "djinn", "genie", "sphinx", "chimera", "manticore", "basilisk", "kraken",
    "medusa", "harpy", "cyclops", "minotaur", "satyr", "dryad", "siren", "naga", "yeti",
    "summit", "pinnacle", "knoll", "gorge", "ridge", "precipice", "plateau", "savanna", "heath", "glade",
    "orca", "narwhal", "squid", "cuttlefish", "octopus", "jellyfish", "starfish", "sea urchin", "clam", "oyster",
    "wendigo", "sasquatch", "chupacabra", "bigfoot", "loch", "ness", "leviathan", "behemoth", "banshee", "phantom",
    "spirit", "shade", "wraith", "ghoul", "zombie", "vampire", "werewolf", "lich", "wight", "shade"
];




// Function to generate a random file name with up to 7 characters
function generateFileName() {
    let fileName = '';
    while (fileName.length < 5 || fileName.length > 9) {
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
