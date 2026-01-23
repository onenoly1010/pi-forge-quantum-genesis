/**
 * ════════════════════════════════════════════════════════════════
 *  🌾🌌 QUANTUMPIFORGE ORACLE ENGINE TESTS — Validation Suite
 *  Extracted and adapted from OINIO Soul System for unified platform
 * ════════════════════════════════════════════════════════════════
 */

const OracleEngine = require('../engine');
const TraitsEngine = require('../traits');
const VerificationEngine = require('../verification');
const OracleUtils = require('../utils');

describe('Oracle Engine Tests', () => {
  let oracle;
  let traits;
  let verification;
  let utils;

  beforeEach(() => {
    oracle = new OracleEngine();
    traits = new TraitsEngine();
    verification = new VerificationEngine();
    utils = new OracleUtils();
  });

  describe('OracleEngine', () => {
    test('should create a new soul with valid structure', () => {
      const soul = oracle.createSoul('Test Soul');

      expect(soul).toHaveProperty('name', 'Test Soul');
      expect(soul).toHaveProperty('seed');
      expect(soul).toHaveProperty('created');
      expect(soul).toHaveProperty('epochs');
      expect(Array.isArray(soul.epochs)).toBe(true);
      expect(soul.epochs.length).toBe(0);
    });

    test('should generate deterministic readings', () => {
      const question = 'What is my path?';
      const seed = 'a'.repeat(64); // 64 character hex seed
      const epochNumber = 1;

      const reading = oracle.generateReading(question, seed, epochNumber);

      expect(reading).toHaveProperty('resonance');
      expect(reading).toHaveProperty('clarity');
      expect(reading).toHaveProperty('flux');
      expect(reading).toHaveProperty('emergence');
      expect(reading).toHaveProperty('pattern');
      expect(reading).toHaveProperty('message');

      // Values should be within valid ranges
      expect(reading.resonance).toBeGreaterThanOrEqual(1);
      expect(reading.resonance).toBeLessThanOrEqual(100);
      expect(reading.clarity).toBeGreaterThanOrEqual(1);
      expect(reading.clarity).toBeLessThanOrEqual(100);
      expect(reading.flux).toBeGreaterThanOrEqual(1);
      expect(reading.flux).toBeLessThanOrEqual(100);
      expect(reading.emergence).toBeGreaterThanOrEqual(1);
      expect(reading.emergence).toBeLessThanOrEqual(100);
    });

    test('should verify valid soul signature', () => {
      const soul = oracle.createSoul('Valid Soul');
      const isValid = oracle.verifySoulSignature(soul);

      expect(isValid).toBe(true);
    });

    test('should reject invalid soul signature', () => {
      const invalidSoul = { name: 'Invalid' }; // Missing required fields
      const isValid = oracle.verifySoulSignature(invalidSoul);

      expect(isValid).toBe(false);
    });

    test('should return available patterns', () => {
      const patterns = oracle.getAvailablePatterns();

      expect(Array.isArray(patterns)).toBe(true);
      expect(patterns.length).toBe(16); // Should have 16 eternal patterns
      expect(patterns).toContain('The Wheel');
      expect(patterns).toContain('The Mirror');
    });

    test('should calculate soul statistics', () => {
      const soul = oracle.createSoul('Stats Soul');

      // Add some mock epochs
      soul.epochs = [
        {
          number: 1,
          question: 'Test?',
          timestamp: new Date().toISOString(),
          reading: { resonance: 75, clarity: 80, flux: 70, emergence: 85, pattern: 'The Wheel', message: 'Test' }
        },
        {
          number: 2,
          question: 'Test 2?',
          timestamp: new Date().toISOString(),
          reading: { resonance: 80, clarity: 75, flux: 75, emergence: 80, pattern: 'The Mirror', message: 'Test 2' }
        }
      ];

      const stats = oracle.calculateSoulStatistics(soul);

      expect(stats).toHaveProperty('totalEpochs', 2);
      expect(stats).toHaveProperty('avgResonance');
      expect(stats).toHaveProperty('avgClarity');
      expect(stats).toHaveProperty('avgFlux');
      expect(stats).toHaveProperty('avgEmergence');
      expect(stats).toHaveProperty('patternCount');
      expect(stats.patternCount['The Wheel']).toBe(1);
      expect(stats.patternCount['The Mirror']).toBe(1);
    });
  });

  describe('TraitsEngine', () => {
    test('should generate personality profile', () => {
      const reading = {
        resonance: 85,
        clarity: 75,
        flux: 60,
        emergence: 90,
        pattern: 'The Wheel',
        message: 'Test message'
      };

      const profile = traits.generatePersonalityProfile(reading);

      expect(profile).toHaveProperty('traits');
      expect(profile).toHaveProperty('elementalAffinity');
      expect(profile).toHaveProperty('intensity');
      expect(profile).toHaveProperty('dominantTraits');
      expect(profile).toHaveProperty('growthAreas');
      expect(profile).toHaveProperty('profile');

      expect(Array.isArray(profile.traits)).toBe(true);
      expect(profile.traits.length).toBeGreaterThan(0);
    });

    test('should calculate elemental affinity', () => {
      const reading = {
        resonance: 80,
        clarity: 70,
        flux: 60,
        emergence: 85
      };

      const affinity = traits.calculateElementalAffinity(reading);

      expect(affinity).toHaveProperty('element');
      expect(affinity).toHaveProperty('strength');
      expect(affinity).toHaveProperty('description');
      expect(typeof affinity.strength).toBe('number');
      expect(affinity.strength).toBeGreaterThanOrEqual(0);
      expect(affinity.strength).toBeLessThanOrEqual(100);
    });

    test('should identify dominant traits', () => {
      const reading = {
        resonance: 90,
        clarity: 80,
        flux: 70,
        emergence: 85
      };

      const dominantTraits = traits.identifyDominantTraits(reading);

      expect(Array.isArray(dominantTraits)).toBe(true);
      expect(dominantTraits.length).toBeGreaterThan(0);
      expect(dominantTraits.length).toBeLessThanOrEqual(6);
    });
  });

  describe('VerificationEngine', () => {
    test('should derive key from password and salt', () => {
      const password = 'testpassword';
      const salt = 'a'.repeat(32); // 32 character hex salt

      const key = verification.deriveKey(password, salt);

      expect(Buffer.isBuffer(key)).toBe(true);
      expect(key.length).toBe(32); // 256 bits
    });

    test('should encrypt and decrypt data', () => {
      const data = 'Test data to encrypt';
      const password = 'testpassword';
      const salt = verification.generateSalt();
      const key = verification.deriveKey(password, salt);

      const encrypted = verification.encrypt(data, key);
      const decrypted = verification.decrypt(encrypted, key);

      expect(encrypted).toHaveProperty('ciphertext');
      expect(encrypted).toHaveProperty('iv');
      expect(encrypted).toHaveProperty('authTag');
      expect(decrypted).toBe(data);
    });

    test('should generate and verify signatures', () => {
      const data = { test: 'data' };
      const privateKey = 'a'.repeat(64); // 64 character hex key

      const signature = verification.generateSignature(data, privateKey);
      const isValid = verification.verifySignature(data, signature, privateKey);

      expect(typeof signature).toBe('string');
      expect(signature.length).toBe(64); // SHA-256 hex length
      expect(isValid).toBe(true);
    });

    test('should generate secure container', () => {
      const soul = {
        name: 'Test Soul',
        seed: 'a'.repeat(64),
        created: new Date().toISOString(),
        epochs: []
      };
      const password = 'testpassword';

      const container = verification.createSecureContainer(soul, password);

      expect(container).toHaveProperty('version');
      expect(container).toHaveProperty('algorithm');
      expect(container).toHaveProperty('salt');
      expect(container).toHaveProperty('encrypted');
      expect(container).toHaveProperty('signature');
      expect(container).toHaveProperty('hash');
      expect(container).toHaveProperty('created');
      expect(container).toHaveProperty('metadata');
    });

    test('should open secure container', () => {
      const soul = {
        name: 'Test Soul',
        seed: 'a'.repeat(64),
        created: new Date().toISOString(),
        epochs: []
      };
      const password = 'testpassword';

      const container = verification.createSecureContainer(soul, password);
      const openedSoul = verification.openSecureContainer(container, password);

      expect(openedSoul.name).toBe(soul.name);
      expect(openedSoul.seed).toBe(soul.seed);
    });
  });

  describe('OracleUtils', () => {
    test('should format reading for display', () => {
      const reading = {
        resonance: 75,
        clarity: 80,
        flux: 70,
        emergence: 85,
        pattern: 'The Wheel',
        message: 'Test message',
        hash: 'abcd1234'
      };

      const formatted = utils.formatReading(reading);

      expect(typeof formatted).toBe('string');
      expect(formatted).toContain('The Wheel');
      expect(formatted).toContain('75/100');
      expect(formatted).toContain('Test message');
    });

    test('should generate safe filename', () => {
      const filename = utils.generateSoulFilename('Test Soul Name!@#');

      expect(filename).toBe('test_soul_name.soul.json');
    });

    test('should validate soul data', () => {
      const validSoul = {
        name: 'Valid Soul',
        seed: 'a'.repeat(64),
        created: new Date().toISOString(),
        epochs: []
      };

      const invalidSoul = {
        name: ''
      };

      const validResult = utils.validateSoulData(validSoul);
      const invalidResult = utils.validateSoulData(invalidSoul);

      expect(validResult.isValid).toBe(true);
      expect(validResult.errors.length).toBe(0);

      expect(invalidResult.isValid).toBe(false);
      expect(invalidResult.errors.length).toBeGreaterThan(0);
    });

    test('should generate progress bar', () => {
      const bar = utils.generateProgressBar(75);

      expect(typeof bar).toBe('string');
      expect(bar).toContain('75%');
      expect(bar).toContain('[');
      expect(bar).toContain(']');
    });

    test('should create readings summary', () => {
      const readings = [
        { resonance: 80, clarity: 75, flux: 70, emergence: 85, pattern: 'The Wheel' },
        { resonance: 70, clarity: 80, flux: 75, emergence: 80, pattern: 'The Mirror' }
      ];

      const summary = utils.createReadingsSummary(readings);

      expect(summary.count).toBe(2);
      expect(summary.averageResonance).toBe(75);
      expect(summary.averageClarity).toBe(78);
      expect(summary.patternDistribution['The Wheel']).toBe(1);
      expect(summary.patternDistribution['The Mirror']).toBe(1);
    });
  });

  describe('Integration Tests', () => {
    test('should create soul, generate reading, and analyze traits', () => {
      // Create soul
      const soul = oracle.createSoul('Integration Test Soul');
      expect(oracle.verifySoulSignature(soul)).toBe(true);

      // Generate reading
      const reading = oracle.generateReading('What is my purpose?', soul.seed, 1);
      expect(reading.resonance).toBeGreaterThanOrEqual(1);
      expect(reading.resonance).toBeLessThanOrEqual(100);

      // Analyze traits
      const profile = traits.generatePersonalityProfile(reading);
      expect(profile.traits.length).toBeGreaterThan(0);
      expect(profile.elementalAffinity.element).toBeDefined();

      // Verify epoch structure
      const epoch = {
        number: 1,
        question: 'What is my purpose?',
        timestamp: new Date().toISOString(),
        reading
      };

      const report = verification.generateVerificationReport(soul);
      expect(report.soulValid).toBe(true);
    });

    test('should handle edge cases gracefully', () => {
      // Test with invalid inputs
      expect(() => oracle.createSoul('')).toThrow();
      expect(() => oracle.generateReading('', 'invalid', 0)).toThrow();
      expect(() => traits.generatePersonalityProfile(null)).toThrow();
      expect(() => utils.formatReading({})).toThrow();
    });
  });
});