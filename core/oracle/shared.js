/**
 * ════════════════════════════════════════════════════════════════
 *  🌾🌌 QUANTUMPIFORGE SHARED CONSTANTS — Eternal Pattern Library
 *  Extracted from OINIO Soul System for unified platform integration
 * ════════════════════════════════════════════════════════════════
 */

const crypto = require('crypto');

// Eternal Pattern Library - The 16 fundamental archetypes
const PATTERNS = [
  'The Wheel',
  'The Mirror',
  'The Threshold',
  'The Void',
  'The Bloom',
  'The Mountain',
  'The Storm',
  'The Seed',
  'The River',
  'The Summit',
  'The Web',
  'The Flame',
  'The Echo',
  'The Gate',
  'The Root',
  'The Sky'
];

// Oracle Messages - Deterministic wisdom for each pattern
const MESSAGES = [
  'The wheel turns, bringing wisdom from the past into the present. What cycles are you completing?',
  'See yourself reflected in this situation. What truths are you avoiding?',
  'You stand at the threshold of transformation. Are you ready to step through?',
  'Emptiness contains infinite potential. What are you ready to create?',
  'Hidden growth emerges into light. What has been developing beneath the surface?',
  'Stability provides the foundation for growth. What structures support your journey?',
  'Chaos clears the old to make way for the new. What needs to be released?',
  'Potential waits to be awakened. What seeds are you planting today?',
  'Flow with the natural current. Where is life trying to take you?',
  'From the summit, new perspectives emerge. What clarity are you gaining?',
  'All things are interconnected. What relationships need your attention?',
  'Transformation through passion and intensity. What fire burns within you?',
  'Lessons return until learned. What patterns are repeating in your life?',
  'Opportunity knocks at the crossroads. Which path calls to you?',
  'Deep truth lies in the foundations. What ancestral wisdom guides you?',
  'Infinite possibility expands before you. What dreams are you ready to pursue?'
];

/**
 * Generate a deterministic oracle reading using cryptographic hashing
 * @param {string} question - The question being asked
 * @param {string} seed - Cryptographic seed (hex string, 64 characters)
 * @param {number} epochNumber - Epoch number for deterministic variation
 * @returns {Object} Reading object with resonance, clarity, flux, emergence, pattern, message
 */
function generateDeterministicReading(question, seed, epochNumber) {
  // Validate inputs
  if (!question || typeof question !== 'string') {
    throw new Error('Question must be a non-empty string');
  }
  if (!seed || typeof seed !== 'string' || !/^[0-9a-f]{64}$/i.test(seed)) {
    throw new Error('Seed must be a valid 64-character hex string');
  }
  if (!Number.isInteger(epochNumber) || epochNumber < 1) {
    throw new Error('Epoch number must be a positive integer');
  }

  // Create deterministic input string
  const input = `${seed}:${question}:${epochNumber}`;

  // Generate hash for deterministic randomness
  const hash = crypto.createHash('sha256').update(input).digest('hex');

  // Extract deterministic values from hash
  const resonance = parseInt(hash.substring(0, 2), 16) % 100 + 1;  // 1-100
  const clarity = parseInt(hash.substring(2, 4), 16) % 100 + 1;    // 1-100
  const flux = parseInt(hash.substring(4, 6), 16) % 100 + 1;       // 1-100
  const emergence = parseInt(hash.substring(6, 8), 16) % 100 + 1;  // 1-100

  // Select pattern deterministically
  const patternIndex = parseInt(hash.substring(8, 10), 16) % PATTERNS.length;
  const pattern = PATTERNS[patternIndex];
  const message = MESSAGES[patternIndex];

  return {
    resonance,
    clarity,
    flux,
    emergence,
    pattern,
    message,
    hash: hash.substring(0, 16) // Include hash fragment for verification
  };
}

/**
 * Generate personality traits based on reading values
 * @param {Object} reading - Oracle reading object
 * @returns {Array} Array of personality traits
 */
function generatePersonalityTraits(reading) {
  const traits = [];

  // Resonance-based traits (spiritual/intuitive)
  if (reading.resonance > 80) traits.push('Highly Intuitive');
  else if (reading.resonance > 60) traits.push('Spiritually Aware');
  else if (reading.resonance > 40) traits.push('Grounded');
  else traits.push('Practical');

  // Clarity-based traits (mental/cognitive)
  if (reading.clarity > 80) traits.push('Crystal Clear Thinker');
  else if (reading.clarity > 60) traits.push('Analytical');
  else if (reading.clarity > 40) traits.push('Thoughtful');
  else traits.push('Instinctive');

  // Flux-based traits (emotional/adaptive)
  if (reading.flux > 80) traits.push('Highly Adaptable');
  else if (reading.flux > 60) traits.push('Emotionally Flexible');
  else if (reading.flux > 40) traits.push('Steady');
  else traits.push('Resilient');

  // Emergence-based traits (creative/expressive)
  if (reading.emergence > 80) traits.push('Creative Visionary');
  else if (reading.emergence > 60) traits.push('Innovative');
  else if (reading.emergence > 40) traits.push('Expressive');
  else traits.push('Reflective');

  return traits;
}

/**
 * Calculate reading intensity based on values
 * @param {Object} reading - Oracle reading object
 * @returns {string} Intensity level ('gentle', 'moderate', 'intense', 'overwhelming')
 */
function calculateReadingIntensity(reading) {
  const average = (reading.resonance + reading.clarity + reading.flux + reading.emergence) / 4;

  if (average > 80) return 'overwhelming';
  if (average > 60) return 'intense';
  if (average > 40) return 'moderate';
  return 'gentle';
}

module.exports = {
  PATTERNS,
  MESSAGES,
  generateDeterministicReading,
  generatePersonalityTraits,
  calculateReadingIntensity
};