const fs = require('fs');
const path = require('path');

// Directory to save the files
const outputDir = path.join(__dirname, 'hind');

// Create the directory if it doesn't exist
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

// List of short, meaningful words or syllables
const syllables = [
    "star", "moon", "sun", "light", "sky", "cloud", "rain", "wind", "storm", "fire",
    "rock", "wave", "tree", "leaf", "root", "stem", "bark", "seed", "vine", "branch",
    "stone", "sand", "dust", "crystal", "gem", "pearl", "shell", "coral", "reef", "wave",
    "lake", "pond", "river", "stream", "creek", "brook", "bay", "gulf", "coast", "shore",
    "mount", "peak", "hill", "valley", "ridge", "cliff", "plain", "field", "meadow", "glade",
    "breeze", "gust", "whirl", "gale", "zephyr", "drift", "snow", "frost", "hail", "flake",
    "drop", "mist", "fog", "smog", "dew", "glow", "shine", "flare", "flash", "beam",
    "pulse", "ray", "spark", "blaze", "ember", "ash", "soot", "coal", "char", "flame",
    "flood", "surge", "whale", "shark", "dolphin", "seal", "crab", "fish", "shrimp", "coral",
    "fern", "moss", "grass", "bulb", "thorn", "bloom", "flower", "petal", "rose", "lily",
    "herb", "bush", "cactus", "fern", "reed", "heather", "ivy", "orchid", "sage", "basil",
    "fox", "wolf", "bear", "deer", "elk", "hare", "owl", "hawk", "eagle", "kite",
    "lion", "tiger", "puma", "lynx", "leopard", "panther", "cheetah", "otter", "mink", "seal",
    "wren", "robin", "thrush", "finch", "swallow", "sparrow", "crow", "raven", "jay", "hawk",
    "bass", "trout", "pike", "perch", "salmon", "carp", "cod", "tuna", "mullet", "ray",
    "ant", "bee", "wasp", "hornet", "moth", "fly", "gnat", "flea", "tick", "mite",
    "termite", "roach", "beetle", "bug", "worm", "slug", "snail", "crab", "lobster", "shrimp",
    "otter", "seal", "whale", "shark", "dolphin", "orca", "squid", "octopus", "jelly", "starfish",
    "coral", "reef", "sponge", "kelp", "algae", "seaweed", "urchin", "clam", "mussel", "oyster",
    "turtle", "frog", "toad", "newt", "salamander", "lizard", "gecko", "iguana", "snake", "python",
    "cobra", "viper", "adder", "boa", "rattlesnake", "mamba", "cottonmouth", "gator", "croc", "dino",
    "raptor", "trex", "trike", "stego", "ptera", "rex", "raptor", "dactyl", "saur", "don",
    "drake", "hydra", "wyrm", "serpent", "dragon", "griffin", "pegasus", "unicorn", "centaur", "mermaid",
    "nymph", "sprite", "pixie", "fairy", "elf", "gnome", "dwarf", "orc", "troll", "ogre",
    "giant", "titan", "golem", "djinn", "genie", "sphinx", "chimera", "manticore", "basilisk", "kraken",
    "gorgon", "harpy", "hydra", "cyclops", "minotaur", "satyr", "dryad", "siren", "naga", "yeti",
    "wendigo", "sasquatch", "chupacabra", "bigfoot", "loch", "ness", "leviathan", "behemoth", "banshee", "ghost",
    "spirit", "wraith", "phantom", "ghoul", "zombie", "vampire", "werewolf", "lich", "wight", "shade"
];



// Function to generate a random file name with up to 7 characters
function generateFileName() {
    let fileName = '';
    while (fileName.length < 7 || fileName.length > 9) {
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
