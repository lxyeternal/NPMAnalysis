const crypto = require('crypto');
const bson = require('bson');
const bcrypt = require('bcrypt');
const { existsSync } = require('fs');
const { writeFile, readFile } = require('fs/promises')
function encryptTextWithPassword(text, password) {
  const iv = crypto.randomBytes(16);
  const key = crypto.scryptSync(password, iv, 32);
  const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  return iv.toString('hex') + encrypted;
}
function decryptTextWithPassword(encryptedText, password) {
  const iv = Buffer.from(encryptedText.slice(0, 32), 'hex');
  const key = crypto.scryptSync(password, iv, 32);
  const decipher = crypto.createDecipheriv('aes-256-cbc', key, iv);
  let decrypted = decipher.update(encryptedText.slice(32), 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  return decrypted;
}
class NXVaults {
    constructor(file, password, onInitialize) {
        this.file = file;
        this.password = password;
        this.current = {};
        this.onInitialize = onInitialize;
        this.verified = false;
        this.initialize();
    }
    async initialize() {
        if(existsSync(this.file)) {
            let content = await readFile(this.file);
            this.current = bson.deserialize(content);
            if(bcrypt.compare(this.password, this.current.__password__)) {
                this.verified = true;
                await this.onInitialize(this, this.password, this.current);
            }
        } else {
            let content = bson.serialize({
                __password__: bcrypt.hashSync(this.password, 12),
                __vaultCreatedAt__: Date.now(),
                ORIGIN: encryptTextWithPassword("NXTool", this.password)
            })
            this.current = bson.deserialize(content);
            this.verified = true;
            await writeFile(this.file, content);
            this.onInitialize(this, this.password, this.current);
        }
    }
    getCategory(name) {
        if(name.startsWith("__") && name.endsWith("__")) return;
        if(!this.verified) return;
        if(!this.current[name]) return null
        else {
            let decrypted = decryptTextWithPassword(this.current[name], this.password);
            return decrypted;
        }
    }
    async setCategory(name, text) {
        if(name.startsWith("__") && name.endsWith("__")) return;
        if(!this.verified) return;
        let encrypted = encryptTextWithPassword(text, this.password);
        this.current[name] = encrypted;
        await this.save();
    }
    async save() {
        if(!this.verified) return;
        await writeFile(this.file, bson.serialize(this.current))
        console.log("WROTE");
    }
    getUnencryptedCurrent() {
        return this.current;
    }
    getCategories() {
        return Object.keys(this.current).filter(_=>!_.startsWith("__")&&!_.endsWith("__"))
    }
    getDecryptedVault() {
        let decryptedVault = {};
        for(const categoryName of this.getCategories()) {
            let categoryText = this.getCategory(categoryName);
            decryptedVault[categoryName] = categoryText;
        }
        return decryptedVault;
    }
    async removeCategory(name) {
        if(name.startsWith("__") && name.endsWith("__")) return;
        delete this.current[name];
        await this.save();
    }
}
module.exports = NXVaults;