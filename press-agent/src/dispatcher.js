/**
 * Quantum Pi Forge Press Agent - Communication Dispatcher
 * 
 * Coordinates announcements across multiple platforms (Discord, Twitter, Telegram)
 */

const { DiscordBot } = require('./bots/discord');
const { TwitterBot } = require('./bots/twitter');
const { TelegramBot } = require('./bots/telegram');
const logger = require('./logger');

class CommunicationDispatcher {
    constructor() {
        this.discord = new DiscordBot();
        this.twitter = new TwitterBot();
        this.telegram = new TelegramBot();
        
        logger.info('Communication Dispatcher initialized', {
            discord: this.discord.enabled,
            twitter: this.twitter.enabled,
            telegram: this.telegram.enabled
        });
    }

    /**
     * Broadcast a message to all enabled platforms
     * @param {string} type - Message type (launch, update, milestone, deployment)
     * @param {Object} data - Message data
     * @returns {Promise<Object>} Results from each platform
     */
    async broadcast(type, data) {
        logger.info('Broadcasting message', { type, platforms: this._getEnabledPlatforms() });

        const results = {
            discord: false,
            twitter: false,
            telegram: false,
            timestamp: new Date().toISOString()
        };

        // Dispatch to all platforms in parallel
        const promises = [];

        if (this.discord.enabled) {
            promises.push(
                this._dispatchToDiscord(type, data)
                    .then(success => { results.discord = success; })
                    .catch(error => {
                        logger.error('Discord broadcast failed', { error: error.message });
                        results.discord = false;
                    })
            );
        }

        if (this.twitter.enabled) {
            promises.push(
                this._dispatchToTwitter(type, data)
                    .then(success => { results.twitter = success; })
                    .catch(error => {
                        logger.error('Twitter broadcast failed', { error: error.message });
                        results.twitter = false;
                    })
            );
        }

        if (this.telegram.enabled) {
            promises.push(
                this._dispatchToTelegram(type, data)
                    .then(success => { results.telegram = success; })
                    .catch(error => {
                        logger.error('Telegram broadcast failed', { error: error.message });
                        results.telegram = false;
                    })
            );
        }

        await Promise.all(promises);

        logger.info('Broadcast complete', results);
        return results;
    }

    /**
     * Send a launch announcement to all platforms
     * @param {Object} announcement - Announcement details
     * @returns {Promise<Object>} Broadcast results
     */
    async sendLaunchAnnouncement(announcement) {
        return this.broadcast('launch', announcement);
    }

    /**
     * Send a feature update to all platforms
     * @param {Object} update - Update details
     * @returns {Promise<Object>} Broadcast results
     */
    async sendFeatureUpdate(update) {
        return this.broadcast('update', update);
    }

    /**
     * Send a milestone achievement to all platforms
     * @param {Object} milestone - Milestone details
     * @returns {Promise<Object>} Broadcast results
     */
    async sendMilestoneAchievement(milestone) {
        return this.broadcast('milestone', milestone);
    }

    /**
     * Send a deployment success notification to all platforms
     * @param {Object} deployment - Deployment details
     * @returns {Promise<Object>} Broadcast results
     */
    async sendDeploymentSuccess(deployment) {
        return this.broadcast('deployment', deployment);
    }

    /**
     * Internal method to dispatch to Discord
     * @private
     */
    async _dispatchToDiscord(type, data) {
        switch (type) {
            case 'launch':
                return this.discord.sendLaunchAnnouncement(data);
            case 'update':
                return this.discord.sendFeatureUpdate(data);
            case 'milestone':
                return this.discord.sendMilestoneAchievement(data);
            case 'deployment':
                return this.discord.sendDeploymentSuccess(data);
            default:
                logger.warn('Unknown message type for Discord', { type });
                return false;
        }
    }

    /**
     * Internal method to dispatch to Twitter
     * @private
     */
    async _dispatchToTwitter(type, data) {
        switch (type) {
            case 'launch':
                return this.twitter.postLaunchAnnouncement(data);
            case 'update':
                return this.twitter.postFeatureUpdate(data);
            case 'milestone':
                return this.twitter.postMilestoneAchievement(data);
            case 'deployment':
                return this.twitter.postDeploymentSuccess(data);
            default:
                logger.warn('Unknown message type for Twitter', { type });
                return false;
        }
    }

    /**
     * Internal method to dispatch to Telegram
     * @private
     */
    async _dispatchToTelegram(type, data) {
        switch (type) {
            case 'launch':
                return this.telegram.sendLaunchAnnouncement(data);
            case 'update':
                return this.telegram.sendFeatureUpdate(data);
            case 'milestone':
                return this.telegram.sendMilestoneAchievement(data);
            case 'deployment':
                return this.telegram.sendDeploymentSuccess(data);
            default:
                logger.warn('Unknown message type for Telegram', { type });
                return false;
        }
    }

    /**
     * Get list of enabled platforms
     * @private
     */
    _getEnabledPlatforms() {
        const platforms = [];
        if (this.discord.enabled) platforms.push('discord');
        if (this.twitter.enabled) platforms.push('twitter');
        if (this.telegram.enabled) platforms.push('telegram');
        return platforms;
    }

    /**
     * Get status of all communication channels
     * @returns {Object} Status object
     */
    getStatus() {
        return {
            discord: {
                enabled: this.discord.enabled,
                configured: !!process.env.DISCORD_WEBHOOK_URL
            },
            twitter: {
                enabled: this.twitter.enabled,
                configured: !!(process.env.TWITTER_BEARER_TOKEN || 
                              (process.env.TWITTER_API_KEY && process.env.TWITTER_API_SECRET))
            },
            telegram: {
                enabled: this.telegram.enabled,
                configured: !!(process.env.TELEGRAM_BOT_TOKEN && process.env.TELEGRAM_CHAT_ID)
            }
        };
    }
}

module.exports = { CommunicationDispatcher };
