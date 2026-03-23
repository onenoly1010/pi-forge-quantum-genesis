/**
 * ════════════════════════════════════════════════════════════════
 *  🌾🌌 QUANTUMPIFORGE VERIFICATION ENGINE — Cryptographic Integrity
 *  Extracted from OINIO Soul System for unified platform integration
 * ════════════════════════════════════════════════════════════════
 */

const crypto = require('crypto');

/**
 * Cryptographic Verification Engine
 * Ensures integrity and authenticity of souls and epochs
 */
class VerificationEngine {
  constructor() {
    this.algorithm = 'aes-256-gcm';
    this.keyLength = 32; // 256 bits
    this.saltRounds = 100000;
    this.digest = 'sha256';
  }

  /**
   * Derive encryption key from password using PBKDF2
   * @param {string} password - Password to derive key from
   * @param {string} salt - Salt for key derivation (hex string)
   * @returns {Buffer} Derived key
   */
  deriveKey(password, salt) {
    if (!password || typeof password !== 'string') {
      throw new Error('Password must be a non-empty string');
    }
    if (!salt || typeof salt !== 'string' || !/^[0-9a-f]{32}$/i.test(salt)) {
      throw new Error('Salt must be a valid 32-character hex string');
    }

    return crypto.pbkdf2Sync(password, Buffer.from(salt, 'hex'), this.saltRounds, this.keyLength, this.digest);
  }

  /**
   * Encrypt data using AES-256-GCM
   * @param {string|Buffer} data - Data to encrypt
   * @param {Buffer} key - Encryption key
   * @returns {Object} Encrypted data with ciphertext, iv, and authTag
   */
  encrypt(data, key) {
    if (!data) {
      throw new Error('Data to encrypt cannot be empty');
    }
    if (!key || key.length !== this.keyLength) {
      throw new Error('Valid encryption key required');
    }

    const iv = crypto.randomBytes(16); // GCM recommended IV length
    const cipher = crypto.createCipher(this.algorithm, key);
    cipher.setAAD(Buffer.from('oracle-data')); // Additional authenticated data

    let encrypted = cipher.update(data, 'utf8', 'hex');
    encrypted += cipher.final('hex');

    const authTag = cipher.getAuthTag();

    return {
      ciphertext: encrypted,
      iv: iv.toString('hex'),
      authTag: authTag.toString('hex')
    };
  }

  /**
   * Decrypt data using AES-256-GCM
   * @param {Object} encryptedData - Encrypted data object with ciphertext, iv, authTag
   * @param {Buffer} key - Decryption key
   * @returns {string} Decrypted data
   */
  decrypt(encryptedData, key) {
    if (!encryptedData || typeof encryptedData !== 'object') {
      throw new Error('Valid encrypted data object required');
    }
    if (!encryptedData.ciphertext || !encryptedData.iv || !encryptedData.authTag) {
      throw new Error('Encrypted data missing required fields');
    }
    if (!key || key.length !== this.keyLength) {
      throw new Error('Valid decryption key required');
    }

    const decipher = crypto.createDecipher(this.algorithm, key);
    decipher.setAAD(Buffer.from('oracle-data'));
    decipher.setAuthTag(Buffer.from(encryptedData.authTag, 'hex'));

    let decrypted = decipher.update(encryptedData.ciphertext, 'hex', 'utf8');
    decrypted += decipher.final('utf8');

    return decrypted;
  }

  /**
   * Generate cryptographic signature for data integrity
   * @param {Object|string} data - Data to sign
   * @param {string} privateKey - Private key for signing (hex string)
   * @returns {string} Signature (hex string)
   */
  generateSignature(data, privateKey) {
    if (!data) {
      throw new Error('Data to sign cannot be empty');
    }
    if (!privateKey || typeof privateKey !== 'string' || !/^[0-9a-f]{64}$/i.test(privateKey)) {
      throw new Error('Valid 64-character hex private key required');
    }

    const dataString = typeof data === 'string' ? data : JSON.stringify(data);
    const sign = crypto.createSign('SHA256');
    sign.update(dataString);
    sign.end();

    // Use private key as HMAC key for simplicity (in production, use proper ECDSA)
    const hmac = crypto.createHmac('sha256', Buffer.from(privateKey, 'hex'));
    hmac.update(dataString);
    return hmac.digest('hex');
  }

  /**
   * Verify cryptographic signature
   * @param {Object|string} data - Original data
   * @param {string} signature - Signature to verify (hex string)
   * @param {string} privateKey - Private key used for signing (hex string)
   * @returns {boolean} True if signature is valid
   */
  verifySignature(data, signature, privateKey) {
    if (!data || !signature || !privateKey) {
      return false;
    }

    try {
      const dataString = typeof data === 'string' ? data : JSON.stringify(data);
      const hmac = crypto.createHmac('sha256', Buffer.from(privateKey, 'hex'));
      hmac.update(dataString);
      const expectedSignature = hmac.digest('hex');
      return crypto.timingSafeEqual(
        Buffer.from(signature, 'hex'),
        Buffer.from(expectedSignature, 'hex')
      );
    } catch (error) {
      return false;
    }
  }

  /**
   * Generate salt for key derivation
   * @returns {string} Random salt (hex string)
   */
  generateSalt() {
    return crypto.randomBytes(16).toString('hex');
  }

  /**
   * Generate random seed for oracle readings
   * @returns {string} Random seed (hex string, 64 characters)
   */
  generateSeed() {
    return crypto.randomBytes(32).toString('hex');
  }

  /**
   * Hash data for integrity checking
   * @param {Object|string} data - Data to hash
   * @returns {string} SHA-256 hash (hex string)
   */
  hashData(data) {
    const dataString = typeof data === 'string' ? data : JSON.stringify(data);
    return crypto.createHash('sha256').update(dataString).digest('hex');
  }

  /**
   * Verify data integrity using hash
   * @param {Object|string} data - Data to verify
   * @param {string} expectedHash - Expected hash (hex string)
   * @returns {boolean} True if data matches hash
   */
  verifyDataIntegrity(data, expectedHash) {
    if (!expectedHash || typeof expectedHash !== 'string') {
      return false;
    }

    try {
      const actualHash = this.hashData(data);
      return crypto.timingSafeEqual(
        Buffer.from(actualHash, 'hex'),
        Buffer.from(expectedHash, 'hex')
      );
    } catch (error) {
      return false;
    }
  }

  /**
   * Create secure container for soul data
   * @param {Object} soul - Soul object to secure
   * @param {string} password - Password for encryption
   * @returns {Object} Secure container with encrypted data and verification info
   */
  createSecureContainer(soul, password) {
    if (!soul || typeof soul !== 'object') {
      throw new Error('Valid soul object required');
    }
    if (!password || typeof password !== 'string') {
      throw new Error('Password required for encryption');
    }

    const salt = this.generateSalt();
    const key = this.deriveKey(password, salt);
    const dataString = JSON.stringify(soul);
    const encrypted = this.encrypt(dataString, key);
    const signature = this.generateSignature(dataString, soul.seed);
    const hash = this.hashData(soul);

    return {
      version: '1.0',
      algorithm: this.algorithm,
      salt,
      encrypted,
      signature,
      hash,
      created: new Date().toISOString(),
      metadata: {
        soulName: soul.name,
        epochCount: soul.epochs ? soul.epochs.length : 0,
        lastEpoch: soul.lastEpoch
      }
    };
  }

  /**
   * Open secure container and verify integrity
   * @param {Object} container - Secure container object
   * @param {string} password - Password for decryption
   * @returns {Object} Decrypted soul object
   */
  openSecureContainer(container, password) {
    if (!container || typeof container !== 'object') {
      throw new Error('Valid container object required');
    }
    if (!password || typeof password !== 'string') {
      throw new Error('Password required for decryption');
    }

    // Verify container structure
    if (!container.salt || !container.encrypted || !container.signature || !container.hash) {
      throw new Error('Invalid container structure');
    }

    // Derive key and decrypt
    const key = this.deriveKey(password, container.salt);
    const decryptedData = this.decrypt(container.encrypted, key);
    const soul = JSON.parse(decryptedData);

    // Verify signature
    if (!this.verifySignature(decryptedData, container.signature, soul.seed)) {
      throw new Error('Container signature verification failed');
    }

    // Verify data integrity
    if (!this.verifyDataIntegrity(soul, container.hash)) {
      throw new Error('Container data integrity check failed');
    }

    return soul;
  }

  /**
   * Generate verification report for soul
   * @param {Object} soul - Soul object to verify
   * @returns {Object} Verification report
   */
  generateVerificationReport(soul) {
    const report = {
      timestamp: new Date().toISOString(),
      soulValid: false,
      epochsValid: 0,
      totalEpochs: 0,
      issues: []
    };

    try {
      // Verify soul structure
      if (!soul.name || !soul.seed || !soul.created) {
        report.issues.push('Invalid soul structure');
        return report;
      }

      // Verify seed format
      if (!/^[0-9a-f]{64}$/i.test(soul.seed)) {
        report.issues.push('Invalid seed format');
        return report;
      }

      report.soulValid = true;
      report.totalEpochs = soul.epochs ? soul.epochs.length : 0;

      // Verify epochs
      if (soul.epochs && Array.isArray(soul.epochs)) {
        soul.epochs.forEach((epoch, index) => {
          try {
            if (this.verifyEpochStructure(epoch)) {
              report.epochsValid++;
            } else {
              report.issues.push(`Invalid epoch structure at index ${index}`);
            }
          } catch (error) {
            report.issues.push(`Epoch verification error at index ${index}: ${error.message}`);
          }
        });
      }

    } catch (error) {
      report.issues.push(`Verification error: ${error.message}`);
    }

    return report;
  }

  /**
   * Verify epoch structure and data integrity
   * @param {Object} epoch - Epoch object to verify
   * @returns {boolean} True if epoch is valid
   */
  verifyEpochStructure(epoch) {
    if (!epoch || typeof epoch !== 'object') {
      return false;
    }

    // Required fields
    if (!epoch.number || !epoch.question || !epoch.timestamp || !epoch.reading) {
      return false;
    }

    // Validate epoch number
    if (!Number.isInteger(epoch.number) || epoch.number < 1) {
      return false;
    }

    // Validate timestamp
    const timestamp = new Date(epoch.timestamp);
    if (isNaN(timestamp.getTime())) {
      return false;
    }

    // Validate reading
    const reading = epoch.reading;
    if (!reading.resonance || !reading.clarity || !reading.flux || !reading.emergence ||
        !reading.pattern || !reading.message) {
      return false;
    }

    // Validate reading values
    const values = [reading.resonance, reading.clarity, reading.flux, reading.emergence];
    for (const value of values) {
      if (!Number.isInteger(value) || value < 1 || value > 100) {
        return false;
      }
    }

    return true;
  }
}

module.exports = VerificationEngine;