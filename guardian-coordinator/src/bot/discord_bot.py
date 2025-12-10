"""
Hephaestus Guardian Coordinator - Discord Bot
Main Discord bot for guardian governance coordination.
"""

import os
import sys
import logging
import discord
from discord.ext import commands

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.bot.guardian_commands import GuardianCommands

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GuardianBot(commands.Bot):
    """Guardian Coordinator Discord Bot."""
    
    def __init__(self):
        # Configure intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        
        super().__init__(
            command_prefix="!",  # Fallback prefix, mainly using slash commands
            intents=intents,
            description="Hephaestus Guardian Coordinator Bot"
        )
        
        self.guardian_channel_id = os.getenv('DISCORD_GUARDIAN_CHANNEL_ID')
        self.guild_id = os.getenv('DISCORD_GUILD_ID')
    
    async def setup_hook(self):
        """Initialize bot and register commands."""
        logger.info("Setting up Guardian Bot...")
        
        # Add guardian commands
        self.tree.add_group(GuardianCommands())
        
        # Sync commands to guild if specified, otherwise global
        if self.guild_id:
            guild = discord.Object(id=int(self.guild_id))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            logger.info(f"Synced commands to guild {self.guild_id}")
        else:
            await self.tree.sync()
            logger.info("Synced commands globally")
        
        logger.info("Guardian Bot setup complete")
    
    async def on_ready(self):
        """Called when bot is ready."""
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        logger.info(f"Connected to {len(self.guilds)} guild(s)")
        
        # Set bot status
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="guardian proposals"
        )
        await self.change_presence(activity=activity, status=discord.Status.online)
        
        logger.info("Guardian Bot is ready!")
    
    async def on_guild_join(self, guild):
        """Called when bot joins a guild."""
        logger.info(f"Joined guild: {guild.name} (ID: {guild.id})")
    
    async def on_command_error(self, ctx, error):
        """Handle command errors."""
        if isinstance(error, commands.CommandNotFound):
            return  # Ignore unknown commands
        
        logger.error(f"Command error: {str(error)}", exc_info=error)
        
        if ctx.interaction:
            await ctx.interaction.response.send_message(
                f"❌ An error occurred: {str(error)}",
                ephemeral=True
            )
    
    async def on_message(self, message):
        """Process messages."""
        # Ignore messages from the bot itself
        if message.author == self.user:
            return
        
        # Process commands
        await self.process_commands(message)


def main():
    """Main entry point for the Discord bot."""
    # Validate required environment variables
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        logger.error(
            "DISCORD_BOT_TOKEN environment variable not set. "
            "Please set it in your .env file or environment."
        )
        sys.exit(1)
    
    guardian_channel_id = os.getenv('DISCORD_GUARDIAN_CHANNEL_ID')
    if not guardian_channel_id:
        logger.warning(
            "DISCORD_GUARDIAN_CHANNEL_ID not set. "
            "Commands will work in all channels (not recommended for production)."
        )
    
    # Create and run bot
    logger.info("Starting Hephaestus Guardian Coordinator Bot...")
    bot = GuardianBot()
    
    try:
        bot.run(token, log_handler=None)  # We're using our own logging
    except discord.LoginFailure:
        logger.error("Failed to login. Check your DISCORD_BOT_TOKEN.")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Bot shutdown requested")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
