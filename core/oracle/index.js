/**
 * ════════════════════════════════════════════════════════════════
 *  🌾🌌 QUANTUMPIFORGE ORACLE SYSTEM — Unified Entry Point
 *  Extracted from OINIO Soul System for unified platform integration
 * ════════════════════════════════════════════════════════════════
 *
 * The QuantumPiForge Oracle System provides:
 * - Deterministic cryptographic divination readings
 * - Soul signature verification and personality analysis
 * - Eternal pattern recognition and archetypal wisdom
 * - Secure data persistence with encryption
 *
 * Usage:
 * const { OracleEngine, TraitsEngine, VerificationEngine, OracleUtils } = require('./core/oracle');
 */

const OracleEngine = require('./engine');
const TraitsEngine = require('./traits');
const VerificationEngine = require('./verification');
const OracleUtils = require('./utils');

// Import shared constants for convenience
const { PATTERNS, MESSAGES, generateDeterministicReading } = require('./shared');

/**
 * QuantumPiForge Oracle System
 * Main entry point for all oracle functionality
 */
class QuantumPiForgeOracle {
  constructor() {
    this.engine = new OracleEngine();
    this.traits = new TraitsEngine();
    this.verification = new VerificationEngine();
    this.utils = new OracleUtils();

    // Initialize data directories
    this.utils.ensureDataDirectories().catch(console.warn);
  }

  /**
   * Create a new soul with complete oracle setup
   * @param {string} name - Soul name
   * @returns {Object} Complete soul object with oracle capabilities
   */
  createSoul(name) {
    const soul = this.engine.createSoul(name);

    // Extend soul with oracle methods
    soul.consultOracle = (question, epochNumber) => {
      const reading = this.engine.generateReading(question, soul.seed, epochNumber);
      const profile = this.traits.generatePersonalityProfile(reading);

      const epoch = {
        number: epochNumber,
        question,
        timestamp: new Date().toISOString(),
        reading
      };

      soul.epochs.push(epoch);
      soul.lastEpoch = epoch.timestamp;

      return {
        epoch,
        reading,
        profile,
        formatted: this.utils.formatReading(reading)
      };
    };

    soul.getStatistics = () => {
      return this.engine.calculateSoulStatistics(soul);
    };

    soul.exportData = () => {
      return this.utils.exportSoulData(soul);
    };

    soul.verifyIntegrity = () => {
      return this.verification.generateVerificationReport(soul);
    };

    return soul;
  }

  /**
   * Quick consultation - create temporary soul and get reading
   * @param {string} question - Question to ask
   * @param {string} soulName - Optional soul name (defaults to 'Anonymous')
   * @returns {Object} Consultation result
   */
  quickConsultation(question, soulName = 'Anonymous') {
    const tempSoul = this.createSoul(soulName);
    return tempSoul.consultOracle(question, 1);
  }

  /**
   * Get system information
   * @returns {Object} System info
   */
  getSystemInfo() {
    return {
      version: '1.0.0',
      patterns: PATTERNS.length,
      components: ['engine', 'traits', 'verification', 'utils'],
      description: 'QuantumPiForge Oracle System - Deterministic Cryptographic Divination'
    };
  }

  /**
   * Validate system integrity
   * @returns {Object} Validation results
   */
  validateSystem() {
    const results = {
      timestamp: new Date().toISOString(),
      components: {},
      overall: true
    };

    try {
      // Test engine
      const testSoul = this.engine.createSoul('System Test');
      results.components.engine = this.engine.verifySoulSignature(testSoul);

      // Test traits
      const testReading = this.engine.generateReading('System test?', testSoul.seed, 1);
      const testProfile = this.traits.generatePersonalityProfile(testReading);
      results.components.traits = testProfile && testProfile.traits.length > 0;

      // Test verification
      const testKey = this.verification.generateSalt();
      results.components.verification = testKey && testKey.length === 32;

      // Test utils
      const testFilename = this.utils.generateSoulFilename('Test');
      results.components.utils = testFilename === 'test.soul.json';

    } catch (error) {
      results.error = error.message;
      results.overall = false;
    }

    results.overall = Object.values(results.components).every(valid => valid === true);

    return results;
  }
}

// Export individual components for advanced usage
module.exports = {
  OracleEngine,
  TraitsEngine,
  VerificationEngine,
  OracleUtils,
  QuantumPiForgeOracle,

  // Shared constants and functions
  PATTERNS,
  MESSAGES,
  generateDeterministicReading,

  // Convenience function to create full oracle system
  createOracle: () => new QuantumPiForgeOracle()
};