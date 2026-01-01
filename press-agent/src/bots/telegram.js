/**
 * Quantum Pi Forge Press Agent - Telegram Bot Integration
 * 
 * Handles automated announcements via Telegram Bot API
 */

const https = require('https');
const logger = require('../logger');

class TelegramBot {
    constructor() {
        this.botToken = process.env.TELEGRAM_BOT_TOKEN;
        this.chatId = process.env.TELEGRAM_CHAT_ID;
        this.enabled = !!(this.botToken && this.chatId);
        
        if (!this.enabled) {
            logger.warn('Telegram bot is disabled: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not configured');
        }
    }

    /**
     * Send a message to Telegram
     * @param {string} text - Message text (supports Markdown)
     * @param {Object} options - Additional options
     * @returns {Promise<boolean>} Success status
     */
    async sendMessage(text, options = {}) {
        if (!this.enabled) {
            logger.warn('Telegram bot is disabled, message not sent');
            return false;
        }

        const payload = {
            chat_id: this.chatId,
            text: text,
            parse_mode: options.parseMode || 'Markdown',
            disable_web_page_preview: options.disablePreview || false
        };

        try {
            await this._sendApiRequest('sendMessage', payload);
            logger.info('Telegram message sent successfully', { length: text.length });
            return true;
        } catch (error) {
            logger.error('Failed to send Telegram message', { error: error.message });
            return false;
        }
    }

    /**
     * Send a launch announcement to Telegram
     * @param {Object} announcement - Announcement details
     * @returns {Promise<boolean>} Success status
     */
    async sendLaunchAnnouncement(announcement) {
        const features = announcement.features && announcement.features.length > 0
            ? '\n\n*Key Features:*\n' + announcement.features.map(f => `• ${f}`).join('\n')
            : '';

        const message = `🚀 *${announcement.title}*

${announcement.description}

📦 *Version:* ${announcement.version || 'N/A'}
📅 *Date:* ${new Date(announcement.date).toLocaleDateString()}${features}

🔗 ${announcement.url || 'Learn more at our GitHub'}

#QuantumPiForge #Launch`;

        return this.sendMessage(message);
    }

    /**
     * Send a feature update to Telegram
     * @param {Object} update - Update details
     * @returns {Promise<boolean>} Success status
     */
    async sendFeatureUpdate(update) {
        const benefits = update.benefits && update.benefits.length > 0
            ? '\n\n*Benefits:*\n' + update.benefits.map(b => `💡 ${b}`).join('\n')
            : '';

        const message = `✨ *Feature Update: ${update.title}*

${update.description}${benefits}

${update.url ? `\n🔗 [Learn More](${update.url})` : ''}

#QuantumPiForge #Update`;

        return this.sendMessage(message);
    }

    /**
     * Send a milestone achievement to Telegram
     * @param {Object} milestone - Milestone details
     * @returns {Promise<boolean>} Success status
     */
    async sendMilestoneAchievement(milestone) {
        const stats = milestone.stats
            ? '\n\n*Stats:*\n' + Object.entries(milestone.stats).map(([key, value]) => `${key}: ${value}`).join('\n')
            : '';

        const message = `🎉 *Milestone Achieved!*

*${milestone.title}*

${milestone.achievement}${stats}

#QuantumPiForge #Milestone`;

        return this.sendMessage(message);
    }

    /**
     * Send deployment success notification to Telegram
     * @param {Object} deployment - Deployment details
     * @returns {Promise<boolean>} Success status
     */
    async sendDeploymentSuccess(deployment) {
        const message = `✅ *Deployment Successful*

Deployment to *${deployment.environment}* completed successfully

🌍 *Environment:* ${deployment.environment}
📦 *Version:* ${deployment.version}
⏱️ *Duration:* ${deployment.duration || 'N/A'}

${deployment.url ? `🔗 Live URL: ${deployment.url}` : ''}

#QuantumPiForge #DevOps`;

        return this.sendMessage(message);
    }

    /**
     * Send a photo with caption to Telegram
     * @param {string} photoUrl - URL of the photo
     * @param {string} caption - Photo caption
     * @returns {Promise<boolean>} Success status
     */
    async sendPhoto(photoUrl, caption) {
        if (!this.enabled) {
            logger.warn('Telegram bot is disabled, photo not sent');
            return false;
        }

        const payload = {
            chat_id: this.chatId,
            photo: photoUrl,
            caption: caption,
            parse_mode: 'Markdown'
        };

        try {
            await this._sendApiRequest('sendPhoto', payload);
            logger.info('Telegram photo sent successfully');
            return true;
        } catch (error) {
            logger.error('Failed to send Telegram photo', { error: error.message });
            return false;
        }
    }

    /**
     * Internal method to send Telegram API request
     * @private
     */
    async _sendApiRequest(method, payload) {
        return new Promise((resolve, reject) => {
            const data = JSON.stringify(payload);
            const path = `/bot${this.botToken}/${method}`;

            const options = {
                hostname: 'api.telegram.org',
                path: path,
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
                        try {
                            const jsonResponse = JSON.parse(responseData);
                            if (jsonResponse.ok) {
                                resolve(jsonResponse);
                            } else {
                                reject(new Error(`Telegram API error: ${jsonResponse.description}`));
                            }
                        } catch (e) {
                            reject(new Error(`Failed to parse Telegram response: ${responseData}`));
                        }
                    } else {
                        reject(new Error(`Telegram API returned status ${res.statusCode}: ${responseData}`));
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

module.exports = { TelegramBot };
