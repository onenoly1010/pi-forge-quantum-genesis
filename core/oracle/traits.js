/**
 * ════════════════════════════════════════════════════════════════
 *  🌾🌌 QUANTUMPIFORGE TRAITS ENGINE — Soul Signature Analysis
 *  Extracted from OINIO Soul System for unified platform integration
 * ════════════════════════════════════════════════════════════════
 */

const { generatePersonalityTraits, calculateReadingIntensity } = require('./shared');

/**
 * Personality Traits Engine
 * Analyzes oracle readings to generate comprehensive personality profiles
 */
class TraitsEngine {
  constructor() {
    // Archetypal trait mappings based on reading values
    this.traitMappings = {
      resonance: {
        high: ['Intuitive', 'Spiritual', 'Empathic', 'Connected'],
        medium: ['Aware', 'Mindful', 'Reflective', 'Harmonious'],
        low: ['Grounded', 'Practical', 'Realistic', 'Stable']
      },
      clarity: {
        high: ['Analytical', 'Precise', 'Logical', 'Clear-thinking'],
        medium: ['Thoughtful', 'Considerate', 'Deliberate', 'Focused'],
        low: ['Instinctive', 'Spontaneous', 'Creative', 'Free-flowing']
      },
      flux: {
        high: ['Adaptable', 'Flexible', 'Change-oriented', 'Dynamic'],
        medium: ['Balanced', 'Steady', 'Reliable', 'Consistent'],
        low: ['Resilient', 'Strong', 'Enduring', 'Persistent']
      },
      emergence: {
        high: ['Visionary', 'Creative', 'Innovative', 'Expansive'],
        medium: ['Expressive', 'Communicative', 'Artistic', 'Imaginative'],
        low: ['Reflective', 'Contemplative', 'Wise', 'Patient']
      }
    };

    // Elemental affinities based on combined readings
    this.elementalAffinities = {
      fire: { resonance: 70, clarity: 60, flux: 80, emergence: 75 },
      water: { resonance: 75, clarity: 50, flux: 70, emergence: 60 },
      earth: { resonance: 60, clarity: 70, flux: 40, emergence: 50 },
      air: { resonance: 65, clarity: 80, flux: 75, emergence: 70 },
      spirit: { resonance: 85, clarity: 65, flux: 60, emergence: 80 }
    };
  }

  /**
   * Generate comprehensive personality profile from oracle reading
   * @param {Object} reading - Oracle reading object
   * @returns {Object} Personality profile with traits, elemental affinity, and analysis
   */
  generatePersonalityProfile(reading) {
    if (!reading || typeof reading !== 'object') {
      throw new Error('Valid reading object required');
    }

    const traits = generatePersonalityTraits(reading);
    const elementalAffinity = this.calculateElementalAffinity(reading);
    const intensity = calculateReadingIntensity(reading);
    const dominantTraits = this.identifyDominantTraits(reading);
    const growthAreas = this.identifyGrowthAreas(reading);

    return {
      traits,
      elementalAffinity,
      intensity,
      dominantTraits,
      growthAreas,
      profile: this.generateProfileSummary(reading, traits, elementalAffinity, intensity)
    };
  }

  /**
   * Calculate elemental affinity based on reading values
   * @param {Object} reading - Oracle reading object
   * @returns {Object} Elemental affinity with element name and strength
   */
  calculateElementalAffinity(reading) {
    let bestMatch = null;
    let bestScore = 0;

    Object.entries(this.elementalAffinities).forEach(([element, ideal]) => {
      const score = this.calculateAffinityScore(reading, ideal);
      if (score > bestScore) {
        bestScore = score;
        bestMatch = element;
      }
    });

    return {
      element: bestMatch,
      strength: Math.round(bestScore * 100),
      description: this.getElementalDescription(bestMatch)
    };
  }

  /**
   * Calculate affinity score between reading and ideal values
   * @param {Object} reading - Actual reading values
   * @param {Object} ideal - Ideal values for element
   * @returns {number} Affinity score (0-1)
   */
  calculateAffinityScore(reading, ideal) {
    const values = ['resonance', 'clarity', 'flux', 'emergence'];
    let totalDifference = 0;

    values.forEach(value => {
      const diff = Math.abs(reading[value] - ideal[value]);
      totalDifference += diff / 100; // Normalize to 0-1 range
    });

    const averageDifference = totalDifference / values.length;
    return Math.max(0, 1 - averageDifference); // Convert to similarity score
  }

  /**
   * Get elemental description
   * @param {string} element - Element name
   * @returns {string} Element description
   */
  getElementalDescription(element) {
    const descriptions = {
      fire: 'Passionate, transformative, driven by intense energy and creative force',
      water: 'Fluid, intuitive, flowing with emotional depth and adaptive wisdom',
      earth: 'Grounded, stable, rooted in practical wisdom and enduring strength',
      air: 'Intellectual, communicative, soaring with ideas and expansive vision',
      spirit: 'Transcendent, mystical, connected to higher consciousness and universal truth'
    };

    return descriptions[element] || 'Balanced elemental harmony';
  }

  /**
   * Identify dominant traits from reading
   * @param {Object} reading - Oracle reading object
   * @returns {Array} Array of dominant trait categories
   */
  identifyDominantTraits(reading) {
    const dominant = [];

    Object.entries(reading).forEach(([aspect, value]) => {
      if (aspect === 'pattern' || aspect === 'message' || aspect === 'hash') return;

      let level;
      if (value > 75) level = 'high';
      else if (value > 50) level = 'medium';
      else level = 'low';

      const traits = this.traitMappings[aspect][level];
      dominant.push(...traits.slice(0, 2)); // Take top 2 traits per aspect
    });

    // Remove duplicates and return top 6
    return [...new Set(dominant)].slice(0, 6);
  }

  /**
   * Identify growth areas based on lower reading values
   * @param {Object} reading - Oracle reading object
   * @returns {Array} Array of growth area suggestions
   */
  identifyGrowthAreas(reading) {
    const growthAreas = [];

    if (reading.resonance < 50) {
      growthAreas.push('Develop greater spiritual awareness and intuition');
    }
    if (reading.clarity < 50) {
      growthAreas.push('Cultivate clearer thinking and mental focus');
    }
    if (reading.flux < 50) {
      growthAreas.push('Embrace change and build emotional flexibility');
    }
    if (reading.emergence < 50) {
      growthAreas.push('Express creativity and explore new possibilities');
    }

    return growthAreas;
  }

  /**
   * Generate comprehensive profile summary
   * @param {Object} reading - Oracle reading object
   * @param {Array} traits - Personality traits
   * @param {Object} elementalAffinity - Elemental affinity object
   * @param {string} intensity - Reading intensity level
   * @returns {string} Profile summary text
   */
  generateProfileSummary(reading, traits, elementalAffinity, intensity) {
    const intensityDescriptions = {
      gentle: 'a gentle, nurturing presence',
      moderate: 'a balanced, harmonious energy',
      intense: 'an intense, transformative force',
      overwhelming: 'an overwhelming, transcendent power'
    };

    return `You embody ${intensityDescriptions[intensity]} with ${elementalAffinity.element} elemental affinity. ` +
           `Your personality reflects ${traits.slice(0, 3).join(', ')} qualities. ` +
           `The ${reading.pattern} pattern suggests ${this.getPatternInsight(reading.pattern)}.`;
  }

  /**
   * Get pattern-specific insight
   * @param {string} pattern - Pattern name
   * @returns {string} Pattern insight
   */
  getPatternInsight(pattern) {
    const insights = {
      'The Wheel': 'cyclical wisdom and the completion of important life lessons',
      'The Mirror': 'self-reflection and seeing yourself clearly in situations',
      'The Threshold': 'standing at the edge of significant transformation',
      'The Void': 'embracing emptiness as the source of infinite potential',
      'The Bloom': 'the emergence of hidden growth into full expression',
      'The Mountain': 'stability and the strength of foundational wisdom',
      'The Storm': 'necessary disruption clearing the way for renewal',
      'The Seed': 'potential waiting to be awakened and nurtured',
      'The River': 'flowing with life\'s natural current and direction',
      'The Summit': 'gaining new perspective from achieved goals',
      'The Web': 'understanding the interconnectedness of all things',
      'The Flame': 'transformation through passion and creative fire',
      'The Echo': 'lessons that return until fully learned and integrated',
      'The Gate': 'opportunity and choice at life\'s crossroads',
      'The Root': 'deep ancestral wisdom and foundational truth',
      'The Sky': 'infinite possibility and expansive vision'
    };

    return insights[pattern] || 'unique archetypal wisdom';
  }

  /**
   * Compare two personality profiles
   * @param {Object} profile1 - First personality profile
   * @param {Object} profile2 - Second personality profile
   * @returns {Object} Comparison results
   */
  compareProfiles(profile1, profile2) {
    const sharedTraits = profile1.traits.filter(trait =>
      profile2.traits.includes(trait)
    );

    const uniqueTo1 = profile1.traits.filter(trait =>
      !profile2.traits.includes(trait)
    );

    const uniqueTo2 = profile2.traits.filter(trait =>
      !profile1.traits.includes(trait)
    );

    return {
      sharedTraits,
      uniqueTo1,
      uniqueTo2,
      elementalCompatibility: this.calculateElementalCompatibility(
        profile1.elementalAffinity.element,
        profile2.elementalAffinity.element
      )
    };
  }

  /**
   * Calculate elemental compatibility between two elements
   * @param {string} element1 - First element
   * @param {string} element2 - Second element
   * @returns {string} Compatibility description
   */
  calculateElementalCompatibility(element1, element2) {
    if (element1 === element2) return 'harmonious resonance';

    const complementary = {
      fire: ['air', 'spirit'],
      water: ['earth', 'spirit'],
      earth: ['water', 'fire'],
      air: ['fire', 'water'],
      spirit: ['all elements']
    };

    if (complementary[element1]?.includes(element2)) {
      return 'complementary energies';
    }

    return 'challenging but growth-oriented dynamic';
  }
}

module.exports = TraitsEngine;