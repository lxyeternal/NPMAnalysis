const fs = require('fs');
const path = require('path');

// Directory to save the files
const outputDir = path.join(__dirname, 'addons');

// Create the directory if it doesn't exist
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

// List of short, meaningful words or syllables
const syllables = [
    "lunar", "solis", "nova", "comet", "nebula", "quasar", "pulsar", "cosmos", "galaxy", "eclipse",
    "granite", "shale", "basalt", "quartzite", "gneiss", "obsidian", "flint", "pebble", "cobble", "boulder",
    "torrent", "rivulet", "delta", "fjord", "strait", "current", "gulf", "estuary", "lagoon", "shoal",
    "ridge", "bluff", "summit", "crag", "butte", "mesa", "plateau", "canyon", "gorge", "gully",
    "zephyr", "sirocco", "mistral", "levanter", "chinook", "squall", "tempest", "cyclone", "whirlwind", "breeze",
    "aurora", "halo", "corona", "radiance", "gleam", "shine", "glint", "luster", "sheen", "glow",
    "ember", "cinder", "spark", "flicker", "glimmer", "blaze", "inferno", "flame", "pyre", "bonfire",
    "rime", "hoarfrost", "sleet", "flurry", "snowdrift", "hailstone", "frostbite", "icicle", "snowflake", "crystal",
    "kelp", "algae", "coral", "plankton", "seagrass", "anemone", "reef", "barnacle", "urchin", "mussel",
    "faun", "sylvan", "nymph", "dryad", "pixie", "sprite", "elf", "gnome", "troll", "ogre",
    "wisp", "shade", "phantom", "poltergeist", "banshee", "wraith", "specter", "revenant", "haunt", "spook",
    "griffon", "pegasus", "sphinx", "wyvern", "hydra", "cerberus", "manticore", "chimera", "basilisk", "kraken",
    "salamander", "wyvern", "serpent", "drake", "wyrm", "leviathan", "roc", "dragon", "phoenix", "griffin",
    "quill", "plume", "talon", "claw", "fang", "horn", "tusk", "antler", "hoof", "mane",
    "glacier", "iceberg", "floe", "crevasse", "serac", "firn", "shelf", "tundra", "permafrost", "snowcap",
    "fern", "briar", "thistle", "bracken", "vine", "tangle", "creeper", "ivy", "shrub", "willow",
    "vortex", "maelstrom", "eddy", "whirlpool", "riptide", "undertow", "surge", "breaker", "swell", "wake",
    "comet", "asteroid", "meteor", "planetoid", "satellite", "orbit", "galaxy", "nebula", "quasar", "void",
    "magma", "lava", "pyroclast", "ashfall", "tephra", "lahar", "volcano", "caldera", "geyser", "hot spring",
    "quartz", "topaz", "ruby", "sapphire", "emerald", "diamond", "amethyst", "opal", "turquoise", "citrine",
    "tiger", "jaguar", "panther", "cheetah", "lynx", "caracal", "leopard", "puma", "bobcat", "serval",
    "cave", "grotto", "cavern", "chasm", "sinkhole", "abyss", "catacomb", "crevice", "fissure", "hollow",
    "harpy", "siren", "naiad", "dryad", "nymph", "sprite", "pixie", "elf", "fairy", "boggart",
    "rune", "glyph", "sigil", "ward", "hex", "charm", "enchantment", "spell", "incantation", "ritual"
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
