/**
 * ════════════════════════════════════════════════════════════════
 *  🌾🌌 QUANTUMPIFORGE ORACLE ENGINE — The Eternal Pattern Recognizer
 *  Extracted from OINIO Soul System for unified platform integration
 * ════════════════════════════════════════════════════════════════
 */

const crypto = require('crypto');

// Import shared constants and functions
const { PATTERNS, MESSAGES, generateDeterministicReading } = require('./shared');

/**
 * Core Oracle Engine Class
 * Provides deterministic cryptographic divination readings
 */
class OracleEngine {
  constructor() {
    this.patterns = PATTERNS;
    this.messages = MESSAGES;
  }

  /**
   * Generate a deterministic oracle reading
   * @param {string} question - The question to ask the oracle
   * @param {string} seed - Cryptographic seed (hex string)
   * @param {number} epochNumber - Epoch number for deterministic variation
   * @returns {Object} Oracle reading with resonance, clarity, flux, emergence, pattern, message
   */
  generateReading(question, seed, epochNumber) {
    if (!question || typeof question !== 'string') {
      throw new Error('Question must be a non-empty string');
    }
    if (!seed || typeof seed !== 'string') {
      throw new Error('Seed must be a non-empty string');
    }
    if (!Number.isInteger(epochNumber) || epochNumber < 1) {
      throw new Error('Epoch number must be a positive integer');
    }

    return generateDeterministicReading(question, seed, epochNumber);
  }

  /**
   * Create a new soul with unique cryptographic seed
   * @param {string} name - Name for the soul
   * @returns {Object} Soul object with name, seed, created timestamp, and empty epochs array
   */
  createSoul(name) {
    if (!name || typeof name !== 'string' || name.trim().length === 0) {
      throw new Error('Soul name must be a non-empty string');
    }

    const seed = crypto.randomBytes(32).toString('hex');
    const created = new Date().toISOString();

    return {
      name: name.trim(),
      seed,
      created,
      lastEpoch: null,
      epochs: []
    };
  }

  /**
   * Verify soul signature integrity
   * @param {Object} soul - Soul object to verify
   * @returns {boolean} True if soul signature is valid
   */
  verifySoulSignature(soul) {
    if (!soul || typeof soul !== 'object') {
      return false;
    }

    // Verify required properties exist
    if (!soul.name || !soul.seed || !soul.created || !Array.isArray(soul.epochs)) {
      return false;
    }

    // Verify seed is valid hex
    if (!/^[0-9a-f]{64}$/i.test(soul.seed)) {
      return false;
    }

    // Verify created timestamp is valid ISO string
    const createdDate = new Date(soul.created);
    if (isNaN(createdDate.getTime())) {
      return false;
    }

    // Verify epochs array contains valid epoch objects
    for (const epoch of soul.epochs) {
      if (!this.verifyEpochSignature(epoch)) {
        return false;
      }
    }

    return true;
  }

  /**
   * Verify epoch signature integrity
   * @param {Object} epoch - Epoch object to verify
   * @returns {boolean} True if epoch signature is valid
   */
  verifyEpochSignature(epoch) {
    if (!epoch || typeof epoch !== 'object') {
      return false;
    }

    // Verify required properties
    if (!epoch.number || !epoch.question || !epoch.timestamp || !epoch.reading) {
      return false;
    }

    // Verify epoch number is positive integer
    if (!Number.isInteger(epoch.number) || epoch.number < 1) {
      return false;
    }

    // Verify timestamp is valid ISO string
    const timestampDate = new Date(epoch.timestamp);
    if (isNaN(timestampDate.getTime())) {
      return false;
    }

    // Verify reading has required properties
    const reading = epoch.reading;
    if (!reading.resonance || !reading.clarity || !reading.flux || !reading.emergence ||
        !reading.pattern || !reading.message) {
      return false;
    }

    // Verify reading values are in valid ranges
    if (reading.resonance < 1 || reading.resonance > 100 ||
        reading.clarity < 1 || reading.clarity > 100 ||
        reading.flux < 1 || reading.flux > 100 ||
        reading.emergence < 1 || reading.emergence > 100) {
      return false;
    }

    return true;
  }

  /**
   * Get available patterns
   * @returns {Array} Array of pattern names
   */
  getAvailablePatterns() {
    return [...this.patterns];
  }

  /**
   * Get pattern description
   * @param {string} patternName - Name of the pattern
   * @returns {string|null} Pattern description or null if not found
   */
  getPatternDescription(patternName) {
    const patternIndex = this.patterns.indexOf(patternName);
    if (patternIndex === -1) return null;

    // Pattern descriptions (extracted from original system)
    const descriptions = [
      'Cyclical growth, returning to center with wisdom',
      'Reflection, seeing yourself in the situation',
      'At the edge of transformation',
      'Emptiness that contains all potential',
      'Emergence, flowering of hidden growth',
      'Stability, grounding, foundation',
      'Chaos, disruption, clearing the old',
      'Beginning, potential waiting to sprout',
      'Flow, movement, natural progression',
      'Challenge, achievement, perspective',
      'Interconnection, complexity, relationships',
      'Transformation through fire, passion',
      'Repetition, lessons returning, resonance',
      'Opportunity, choice, passage between worlds',
      'Foundation, ancestry, deep truth',
      'Freedom, expansion, infinite possibility'
    ];

    return descriptions[patternIndex] || null;
  }

  /**
   * Calculate soul statistics
   * @param {Object} soul - Soul object
   * @returns {Object|null} Statistics object or null if no epochs
   */
  calculateSoulStatistics(soul) {
    if (!soul.epochs || soul.epochs.length === 0) {
      return null;
    }

    const epochs = soul.epochs;
    const stats = {
      totalEpochs: epochs.length,
      avgResonance: epochs.reduce((sum, e) => sum + e.reading.resonance, 0) / epochs.length,
      avgClarity: epochs.reduce((sum, e) => sum + e.reading.clarity, 0) / epochs.length,
      avgFlux: epochs.reduce((sum, e) => sum + e.reading.flux, 0) / epochs.length,
      avgEmergence: epochs.reduce((sum, e) => sum + e.reading.emergence, 0) / epochs.length,
      patternCount: {},
      firstEpoch: epochs[0].timestamp,
      lastEpoch: epochs[epochs.length - 1].timestamp
    };

    // Count pattern occurrences
    epochs.forEach(epoch => {
      const pattern = epoch.reading.pattern;
      stats.patternCount[pattern] = (stats.patternCount[pattern] || 0) + 1;
    });

    // Find most common pattern
    const topPattern = Object.entries(stats.patternCount)
      .sort((a, b) => b[1] - a[1])[0];
    stats.mostCommonPattern = topPattern ? topPattern[0] : null;
    stats.mostCommonPatternCount = topPattern ? topPattern[1] : 0;

    return stats;
  }
}

module.exports = OracleEngine;