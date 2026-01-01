/**
 * Quantum Pi Forge Press Agent - Discord Bot Integration
 * 
 * Handles automated announcements and community updates via Discord webhooks
 */

const https = require('https');
const logger = require('../logger');

class DiscordBot {
    constructor() {
        this.webhookUrl = process.env.DISCORD_WEBHOOK_URL;
        this.enabled = !!this.webhookUrl;
        
        if (!this.enabled) {
            logger.warn('Discord bot is disabled: DISCORD_WEBHOOK_URL not configured');
        }
    }

    /**
     * Send a message to Discord
     * @param {Object} message - Message configuration
     * @param {string} message.content - Plain text content
     * @param {Object[]} message.embeds - Rich embeds (optional)
     * @param {string} message.username - Bot username (optional)
     * @param {string} message.avatar_url - Bot avatar URL (optional)
     * @returns {Promise<boolean>} Success status
     */
    async sendMessage(message) {
        if (!this.enabled) {
            logger.warn('Discord bot is disabled, message not sent');
            return false;
        }

        const payload = {
            content: message.content || '',
            embeds: message.embeds || [],
            username: message.username || 'Quantum Pi Forge Press Agent',
            avatar_url: message.avatar_url || undefined
        };

        try {
            await this._sendWebhook(payload);
            logger.info('Discord message sent successfully', { 
                contentLength: payload.content.length,
                embedCount: payload.embeds.length 
            });
            return true;
        } catch (error) {
            logger.error('Failed to send Discord message', { error: error.message });
            return false;
        }
    }

    /**
     * Send a launch announcement to Discord
     * @param {Object} announcement - Announcement details
     * @returns {Promise<boolean>} Success status
     */
    async sendLaunchAnnouncement(announcement) {
        const embed = {
            title: `🚀 ${announcement.title}`,
            description: announcement.description,
            color: 0x7289DA, // Discord blurple
            fields: [
                {
                    name: '📦 Release Version',
                    value: announcement.version || 'N/A',
                    inline: true
                },
                {
                    name: '📅 Date',
                    value: new Date(announcement.date).toLocaleDateString(),
                    inline: true
                }
            ],
            timestamp: new Date().toISOString(),
            footer: {
                text: 'Pi Forge Quantum Genesis'
            }
        };

        if (announcement.url) {
            embed.url = announcement.url;
        }

        if (announcement.features && announcement.features.length > 0) {
            embed.fields.push({
                name: '✨ Key Features',
                value: announcement.features.map(f => `• ${f}`).join('\n')
            });
        }

        return this.sendMessage({
            content: '🌌 **New Launch Announcement from Quantum Pi Forge!**',
            embeds: [embed]
        });
    }

    /**
     * Send a feature update to Discord
     * @param {Object} update - Update details
     * @returns {Promise<boolean>} Success status
     */
    async sendFeatureUpdate(update) {
        const embed = {
            title: `✨ ${update.title}`,
            description: update.description,
            color: 0x00D166, // Green
            fields: [],
            timestamp: new Date().toISOString(),
            footer: {
                text: 'Pi Forge Quantum Genesis'
            }
        };

        if (update.benefits && update.benefits.length > 0) {
            embed.fields.push({
                name: '💡 Benefits',
                value: update.benefits.map(b => `• ${b}`).join('\n')
            });
        }

        if (update.url) {
            embed.url = update.url;
            embed.fields.push({
                name: '🔗 Learn More',
                value: `[View Documentation](${update.url})`
            });
        }

        return this.sendMessage({
            content: '📢 Feature Update Available',
            embeds: [embed]
        });
    }

    /**
     * Send a milestone achievement to Discord
     * @param {Object} milestone - Milestone details
     * @returns {Promise<boolean>} Success status
     */
    async sendMilestoneAchievement(milestone) {
        const embed = {
            title: `🎉 ${milestone.title}`,
            description: milestone.description,
            color: 0xFFD700, // Gold
            fields: [
                {
                    name: '🎯 Achievement',
                    value: milestone.achievement
                }
            ],
            timestamp: new Date().toISOString(),
            footer: {
                text: 'Pi Forge Quantum Genesis'
            }
        };

        if (milestone.stats) {
            Object.entries(milestone.stats).forEach(([key, value]) => {
                embed.fields.push({
                    name: key,
                    value: String(value),
                    inline: true
                });
            });
        }

        return this.sendMessage({
            content: '🏆 **Milestone Achieved!**',
            embeds: [embed]
        });
    }

    /**
     * Send deployment success notification to Discord
     * @param {Object} deployment - Deployment details
     * @returns {Promise<boolean>} Success status
     */
    async sendDeploymentSuccess(deployment) {
        const embed = {
            title: `✅ Deployment Successful`,
            description: `Deployment to ${deployment.environment} completed successfully`,
            color: 0x43B581, // Success green
            fields: [
                {
                    name: '🌍 Environment',
                    value: deployment.environment,
                    inline: true
                },
                {
                    name: '📦 Version',
                    value: deployment.version,
                    inline: true
                },
                {
                    name: '⏱️ Duration',
                    value: deployment.duration || 'N/A',
                    inline: true
                }
            ],
            timestamp: new Date().toISOString(),
            footer: {
                text: 'Pi Forge Quantum Genesis - CI/CD'
            }
        };

        if (deployment.url) {
            embed.fields.push({
                name: '🔗 Live URL',
                value: deployment.url
            });
        }

        return this.sendMessage({
            content: '🚀 Deployment Complete',
            embeds: [embed]
        });
    }

    /**
     * Internal method to send webhook request
     * @private
     */
    async _sendWebhook(payload) {
        return new Promise((resolve, reject) => {
            const url = new URL(this.webhookUrl);
            const data = JSON.stringify(payload);

            const options = {
                hostname: url.hostname,
                path: url.pathname + url.search,
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Content-Length': data.length
                }
            };

            const req = https.request(options, (res) => {
                let responseData = '';

                res.on('data', (chunk) => {
                    responseData += chunk;
                });

                res.on('end', () => {
                    if (res.statusCode >= 200 && res.statusCode < 300) {
                        resolve(responseData);
                    } else {
                        reject(new Error(`Discord webhook returned status ${res.statusCode}: ${responseData}`));
                    }
                });
            });

            req.on('error', (error) => {
                reject(error);
            });

            req.write(data);
            req.end();
        });
    }
}

module.exports = { DiscordBot };
