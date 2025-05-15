const fs = require('fs');
const path = require('path');

// Directory to save the files
const outputDir = path.join(__dirname, 'clipert');

// Create the directory if it doesn't exist
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

// List of short, meaningful words or syllables
const syllables = [
    "solar", "luna", "stellar", "comet", "equinox", "solstice", "meteor", "zenith", "aurora", "nebula",
    "flint", "shard", "marble", "onyx", "opal", "crystal", "granule", "pebble", "boulder", "cairn",
    "tide", "wave", "spray", "current", "cascade", "fountain", "geyser", "lagoon", "harbor", "inlet",
    "summit", "pinnacle", "escarpment", "knoll", "ridge", "valley", "gorge", "plateau", "canyon", "basin",
    "whisper", "gale", "tempest", "cyclone", "typhoon", "breeze", "zephyr", "sirocco", "monsoon", "gust",
    "gleam", "glow", "glint", "luster", "shine", "flare", "radiance", "beam", "glimmer", "twilight",
    "ember", "blaze", "flicker", "inferno", "bonfire", "cinder", "torch", "flame", "pyre", "ignite",
    "frost", "hoar", "rime", "sleet", "flurry", "snowdrift", "icicle", "hail", "glacier", "permafrost",
    "kelp", "plankton", "barnacle", "anemone", "coral", "urchin", "starfish", "mollusk", "oyster", "clam",
    "dryad", "pixie", "elf", "satyr", "faun", "nymph", "sprite", "gnome", "goblin", "troll",
    "shade", "phantasm", "wisp", "specter", "poltergeist", "banshee", "phantom", "haunt", "ghoul", "revenant",
    "griffin", "wyvern", "phoenix", "hydra", "cerberus", "manticore", "basilisk", "chimera", "kraken", "leviathan",
    "salamander", "wyrm", "drake", "serpent", "wyvern", "griffin", "roc", "dragon", "wyrm", "phoenix",
    "claw", "talon", "fang", "antler", "horn", "mane", "plume", "quill", "tusk", "beak",
    "glacier", "snowfield", "icecap", "floe", "serac", "crevasse", "firn", "shelf", "blizzard", "snowstorm",
    "thorn", "bramble", "thicket", "grove", "copse", "orchard", "glade", "clearing", "meadow", "shrub",
    "vortex", "maelstrom", "surge", "swirl", "riptide", "whirlpool", "eddy", "breaker", "wave", "tidal",
    "planet", "meteor", "comet", "asteroid", "satellite", "orbit", "cosmos", "universe", "starfield", "nebula",
    "volcano", "caldera", "magma", "lava", "geode", "obsidian", "pyroclast", "ashfall", "tephra", "lavaflow",
    "amber", "topaz", "garnet", "sapphire", "emerald", "diamond", "ruby", "amethyst", "jasper", "opal",
    "cheetah", "lynx", "panther", "tiger", "lion", "leopard", "jaguar", "puma", "cougar", "caracal",
    "grotto", "cave", "chasm", "cavern", "abyss", "sinkhole", "crevice", "catacomb", "rift", "gully",
    "harpy", "siren", "dryad", "nymph", "sprite", "goblin", "pixie", "fairy", "imp", "djinn",
    "rune", "glyph", "sigil", "charm", "hex", "ward", "spell", "enchant", "ritual", "mantra"
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
