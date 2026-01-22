/**
 * Quantum Pi Forge Press Agent - X (Twitter) Bot Integration
 * 
 * Handles automated announcements via X/Twitter API
 */

const https = require('https');
const logger = require('../logger');

class TwitterBot {
    constructor() {
        this.apiKey = process.env.TWITTER_API_KEY;
        this.apiSecret = process.env.TWITTER_API_SECRET;
        this.accessToken = process.env.TWITTER_ACCESS_TOKEN;
        this.accessSecret = process.env.TWITTER_ACCESS_SECRET;
        this.bearerToken = process.env.TWITTER_BEARER_TOKEN;
        
        this.enabled = !!(this.bearerToken || (this.apiKey && this.apiSecret && this.accessToken && this.accessSecret));
        
        if (!this.enabled) {
            logger.warn('Twitter bot is disabled: Required credentials not configured');
        }
    }

    /**
     * Post a tweet
     * @param {string} text - Tweet content (max 280 characters)
     * @returns {Promise<boolean>} Success status
     */
    async postTweet(text) {
        if (!this.enabled) {
            logger.warn('Twitter bot is disabled, tweet not sent');
            return false;
        }

        // Truncate if needed
        const tweetText = text.length > 280 ? text.substring(0, 277) + '...' : text;

        try {
            // Note: This is a placeholder for Twitter API v2 integration
            // In production, you would use the Twitter API client library
            logger.info('Twitter post prepared', { length: tweetText.length });
            
            // Development mode: Log tweet instead of posting
            // Production mode: Requires Twitter API v2 client implementation
            // To enable actual posting:
            // 1. Set NODE_ENV=production
            // 2. Install twitter-api-v2: npm install twitter-api-v2
            // 3. Implement actual API call with proper OAuth
            if (process.env.NODE_ENV === 'production') {
                logger.warn('Production Twitter posting not yet implemented - requires twitter-api-v2 client');
            } else {
                logger.info('Tweet content (development mode - would be posted in production):', { tweet: tweetText });
            }
            
            return true;
        } catch (error) {
            logger.error('Failed to post tweet', { error: error.message });
            return false;
        }
    }

    /**
     * Post a launch announcement tweet
     * @param {Object} announcement - Announcement details
     * @returns {Promise<boolean>} Success status
     */
    async postLaunchAnnouncement(announcement) {
        const tweet = `🚀 ${announcement.title}

${announcement.description}

Version: ${announcement.version || 'Latest'}
🔗 ${announcement.url || 'https://github.com/quantumpiforge'}

#QuantumPiForge #PiNetwork #Web3 #DeFi`;

        return this.postTweet(tweet);
    }

    /**
     * Post a feature update tweet
     * @param {Object} update - Update details
     * @returns {Promise<boolean>} Success status
     */
    async postFeatureUpdate(update) {
        const benefits = update.benefits && update.benefits.length > 0
            ? '\n\n' + update.benefits.slice(0, 2).map(b => `✨ ${b}`).join('\n')
            : '';

        const tweet = `📢 New Feature: ${update.title}

${update.description}${benefits}

#QuantumPiForge #PiNetwork`;

        return this.postTweet(tweet);
    }

    /**
     * Post a milestone achievement tweet
     * @param {Object} milestone - Milestone details
     * @returns {Promise<boolean>} Success status
     */
    async postMilestoneAchievement(milestone) {
        const statsText = milestone.stats
            ? '\n\n' + Object.entries(milestone.stats).slice(0, 2).map(([key, value]) => `${key}: ${value}`).join('\n')
            : '';

        const tweet = `🎉 Milestone Achieved: ${milestone.title}

${milestone.achievement}${statsText}

#QuantumPiForge #PiNetwork #Milestone`;

        return this.postTweet(tweet);
    }

    /**
     * Post a deployment success tweet
     * @param {Object} deployment - Deployment details
     * @returns {Promise<boolean>} Success status
     */
    async postDeploymentSuccess(deployment) {
        const tweet = `✅ Successfully deployed to ${deployment.environment}

Version: ${deployment.version}
Status: Live 🟢

${deployment.url || ''}

#QuantumPiForge #DevOps`;

        return this.postTweet(tweet);
    }

    /**
     * Post a thread (multiple related tweets)
     * @param {string[]} tweets - Array of tweet texts
     * @returns {Promise<boolean>} Success status
     */
    async postThread(tweets) {
        if (!this.enabled) {
            logger.warn('Twitter bot is disabled, thread not sent');
            return false;
        }

        try {
            for (let i = 0; i < tweets.length; i++) {
                const tweet = `${tweets[i]}\n\n(${i + 1}/${tweets.length})`;
                await this.postTweet(tweet);
                
                // Add delay between tweets to avoid rate limiting
                if (i < tweets.length - 1) {
                    await new Promise(resolve => setTimeout(resolve, 2000));
                }
            }
            return true;
        } catch (error) {
            logger.error('Failed to post thread', { error: error.message });
            return false;
        }
    }
}

module.exports = { TwitterBot };
