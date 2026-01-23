/**
 * ════════════════════════════════════════════════════════════════
 *  🌾🌌 QUANTUMPIFORGE UTILITIES — Helper Functions & Tools
 *  Extracted from OINIO Soul System for unified platform integration
 * ════════════════════════════════════════════════════════════════
 */

const fs = require('fs').promises;
const path = require('path');

/**
 * Oracle Utilities
 * Helper functions for file operations, data formatting, and common operations
 */
class OracleUtils {
  constructor() {
    this.dataDir = path.join(process.cwd(), 'data');
    this.soulsDir = path.join(this.dataDir, 'souls');
    this.backupsDir = path.join(this.dataDir, 'backups');
  }

  /**
   * Ensure data directories exist
   * @returns {Promise<void>}
   */
  async ensureDataDirectories() {
    const dirs = [this.dataDir, this.soulsDir, this.backupsDir];

    for (const dir of dirs) {
      try {
        await fs.access(dir);
      } catch {
        await fs.mkdir(dir, { recursive: true });
      }
    }
  }

  /**
   * Format oracle reading for display
   * @param {Object} reading - Oracle reading object
   * @returns {string} Formatted reading string
   */
  formatReading(reading) {
    if (!reading || typeof reading !== 'object') {
      throw new Error('Valid reading object required');
    }

    return `
🌾 Oracle Reading 🌾

Pattern: ${reading.pattern}
Resonance: ${reading.resonance}/100
Clarity: ${reading.clarity}/100
Flux: ${reading.flux}/100
Emergence: ${reading.emergence}/100

Message: ${reading.message}

Hash: ${reading.hash || 'N/A'}
    `.trim();
  }

  /**
   * Format personality profile for display
   * @param {Object} profile - Personality profile object
   * @returns {string} Formatted profile string
   */
  formatPersonalityProfile(profile) {
    if (!profile || typeof profile !== 'object') {
      throw new Error('Valid profile object required');
    }

    const traitsList = profile.traits.map(trait => `• ${trait}`).join('\n');
    const growthList = profile.growthAreas.map(area => `• ${area}`).join('\n');

    return `
🌟 Personality Profile 🌟

Elemental Affinity: ${profile.elementalAffinity.element} (${profile.elementalAffinity.strength}% affinity)
${profile.elementalAffinity.description}

Intensity: ${profile.intensity}

Traits:
${traitsList}

${profile.growthAreas.length > 0 ? `Growth Areas:
${growthList}

` : ''}Profile Summary:
${profile.profile}
    `.trim();
  }

  /**
   * Format soul statistics for display
   * @param {Object} stats - Soul statistics object
   * @returns {string} Formatted statistics string
   */
  formatSoulStatistics(stats) {
    if (!stats || typeof stats !== 'object') {
      return 'No statistics available';
    }

    const firstEpoch = new Date(stats.firstEpoch).toLocaleDateString();
    const lastEpoch = new Date(stats.lastEpoch).toLocaleDateString();

    return `
📊 Soul Statistics 📊

Total Epochs: ${stats.totalEpochs}
Average Resonance: ${stats.avgResonance.toFixed(1)}/100
Average Clarity: ${stats.avgClarity.toFixed(1)}/100
Average Flux: ${stats.avgFlux.toFixed(1)}/100
Average Emergence: ${stats.avgEmergence.toFixed(1)}/100

Most Common Pattern: ${stats.mostCommonPattern || 'None'} (${stats.mostCommonPatternCount || 0} times)

Journey: ${firstEpoch} → ${lastEpoch}
    `.trim();
  }

  /**
   * Generate filename for soul data
   * @param {string} soulName - Name of the soul
   * @returns {string} Safe filename
   */
  generateSoulFilename(soulName) {
    if (!soulName || typeof soulName !== 'string') {
      throw new Error('Valid soul name required');
    }

    // Sanitize filename: remove special characters, replace spaces with underscores
    const sanitized = soulName
      .toLowerCase()
      .replace(/[^a-z0-9\s-]/g, '') // Remove special characters except spaces and hyphens
      .replace(/\s+/g, '_') // Replace spaces with underscores
      .replace(/-+/g, '-') // Replace multiple hyphens with single hyphen
      .trim();

    return `${sanitized}.soul.json`;
  }

  /**
   * Generate backup filename with timestamp
   * @param {string} originalFilename - Original filename
   * @returns {string} Backup filename with timestamp
   */
  generateBackupFilename(originalFilename) {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const ext = path.extname(originalFilename);
    const name = path.basename(originalFilename, ext);
    return `${name}_backup_${timestamp}${ext}`;
  }

  /**
   * Validate soul data structure
   * @param {Object} soul - Soul object to validate
   * @returns {Object} Validation result with isValid and errors array
   */
  validateSoulData(soul) {
    const result = {
      isValid: true,
      errors: []
    };

    if (!soul || typeof soul !== 'object') {
      result.isValid = false;
      result.errors.push('Soul must be an object');
      return result;
    }

    // Required fields
    const requiredFields = ['name', 'seed', 'created'];
    for (const field of requiredFields) {
      if (!soul[field]) {
        result.isValid = false;
        result.errors.push(`Missing required field: ${field}`);
      }
    }

    // Validate name
    if (soul.name && (typeof soul.name !== 'string' || soul.name.trim().length === 0)) {
      result.isValid = false;
      result.errors.push('Name must be a non-empty string');
    }

    // Validate seed
    if (soul.seed && !/^[0-9a-f]{64}$/i.test(soul.seed)) {
      result.isValid = false;
      result.errors.push('Seed must be a valid 64-character hex string');
    }

    // Validate created timestamp
    if (soul.created) {
      const createdDate = new Date(soul.created);
      if (isNaN(createdDate.getTime())) {
        result.isValid = false;
        result.errors.push('Created must be a valid ISO timestamp');
      }
    }

    // Validate epochs array
    if (soul.epochs && !Array.isArray(soul.epochs)) {
      result.isValid = false;
      result.errors.push('Epochs must be an array');
    }

    return result;
  }

  /**
   * Calculate time since epoch
   * @param {string} epochTimestamp - ISO timestamp string
   * @returns {string} Human-readable time difference
   */
  calculateTimeSince(epochTimestamp) {
    try {
      const epochDate = new Date(epochTimestamp);
      const now = new Date();
      const diffMs = now - epochDate;

      const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
      const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
      const diffMinutes = Math.floor(diffMs / (1000 * 60));

      if (diffDays > 0) {
        return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
      } else if (diffHours > 0) {
        return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
      } else if (diffMinutes > 0) {
        return `${diffMinutes} minute${diffMinutes > 1 ? 's' : ''} ago`;
      } else {
        return 'Just now';
      }
    } catch (error) {
      return 'Unknown';
    }
  }

  /**
   * Generate progress visualization for reading values
   * @param {number} value - Value to visualize (1-100)
   * @param {number} width - Width of progress bar (default: 20)
   * @returns {string} Progress bar string
   */
  generateProgressBar(value, width = 20) {
    if (typeof value !== 'number' || value < 0 || value > 100) {
      return '[██████████] Invalid';
    }

    const filled = Math.round((value / 100) * width);
    const empty = width - filled;

    const bar = '█'.repeat(filled) + '░'.repeat(empty);
    return `[${bar}] ${value}%`;
  }

  /**
   * Create summary of multiple readings
   * @param {Array} readings - Array of reading objects
   * @returns {Object} Summary statistics
   */
  createReadingsSummary(readings) {
    if (!Array.isArray(readings) || readings.length === 0) {
      return {
        count: 0,
        averageResonance: 0,
        averageClarity: 0,
        averageFlux: 0,
        averageEmergence: 0,
        patternDistribution: {}
      };
    }

    const summary = {
      count: readings.length,
      averageResonance: 0,
      averageClarity: 0,
      averageFlux: 0,
      averageEmergence: 0,
      patternDistribution: {}
    };

    let totalResonance = 0;
    let totalClarity = 0;
    let totalFlux = 0;
    let totalEmergence = 0;

    readings.forEach(reading => {
      totalResonance += reading.resonance || 0;
      totalClarity += reading.clarity || 0;
      totalFlux += reading.flux || 0;
      totalEmergence += reading.emergence || 0;

      const pattern = reading.pattern || 'Unknown';
      summary.patternDistribution[pattern] = (summary.patternDistribution[pattern] || 0) + 1;
    });

    summary.averageResonance = Math.round(totalResonance / readings.length);
    summary.averageClarity = Math.round(totalClarity / readings.length);
    summary.averageFlux = Math.round(totalFlux / readings.length);
    summary.averageEmergence = Math.round(totalEmergence / readings.length);

    return summary;
  }

  /**
   * Export soul data to human-readable format
   * @param {Object} soul - Soul object
   * @returns {string} Formatted export string
   */
  exportSoulData(soul) {
    if (!soul || typeof soul !== 'object') {
      throw new Error('Valid soul object required');
    }

    let exportString = `
🌾 SOUL EXPORT: ${soul.name.toUpperCase()} 🌾

Created: ${new Date(soul.created).toLocaleString()}
Seed: ${soul.seed}
Last Epoch: ${soul.lastEpoch || 'None'}

`;

    if (soul.epochs && soul.epochs.length > 0) {
      exportString += `EPOCHS (${soul.epochs.length}):\n\n`;

      soul.epochs.forEach((epoch, index) => {
        exportString += `Epoch ${epoch.number} - ${new Date(epoch.timestamp).toLocaleString()}
Question: ${epoch.question}

${this.formatReading(epoch.reading)}

${'-'.repeat(50)}\n\n`;
      });
    } else {
      exportString += 'No epochs recorded yet.\n';
    }

    return exportString.trim();
  }

  /**
   * Parse command line arguments for CLI usage
   * @param {Array} args - Command line arguments
   * @returns {Object} Parsed arguments object
   */
  parseCliArgs(args) {
    const parsed = {
      command: null,
      options: {},
      values: []
    };

    for (let i = 0; i < args.length; i++) {
      const arg = args[i];

      if (arg.startsWith('--')) {
        // Long option
        const [key, value] = arg.substring(2).split('=');
        parsed.options[key] = value !== undefined ? value : true;
      } else if (arg.startsWith('-')) {
        // Short option
        const key = arg.substring(1);
        const nextArg = args[i + 1];
        if (nextArg && !nextArg.startsWith('-')) {
          parsed.options[key] = nextArg;
          i++; // Skip next arg as it's the value
        } else {
          parsed.options[key] = true;
        }
      } else if (!parsed.command) {
        // First non-option argument is the command
        parsed.command = arg;
      } else {
        // Additional values
        parsed.values.push(arg);
      }
    }

    return parsed;
  }
}

module.exports = OracleUtils;