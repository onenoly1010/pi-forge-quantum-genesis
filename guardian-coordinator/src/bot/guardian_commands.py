"""
Guardian slash commands for Discord bot.
Implements /guardian_propose and /guardian_vote commands.
"""

import os
import logging
import aiohttp
from typing import Optional
import discord
from discord import app_commands

logger = logging.getLogger(__name__)


class GuardianCommands(app_commands.Group):
    """Guardian governance commands."""
    
    def __init__(self):
        super().__init__(name="guardian", description="Guardian coordination commands")
        self.api_base_url = f"http://{os.getenv('API_HOST', 'localhost')}:{os.getenv('API_PORT', '8001')}"
    
    @app_commands.command(name="propose", description="Create a new guardian proposal")
    @app_commands.describe(
        action="Action type (deploy_contract, transfer_funds, update_guardian, change_quorum, mint_nft, custom)",
        description="Detailed description of the proposal",
        params="JSON parameters for the action (optional)"
    )
    async def guardian_propose(
        self,
        interaction: discord.Interaction,
        action: str,
        description: str,
        params: Optional[str] = "{}"
    ):
        """
        Create a new guardian proposal.
        
        Usage:
            /guardian propose action:deploy_contract description:Deploy Guardian NFT params:{"contract":"GuardianNFT"}
        """
        # Defer response since API call might take time
        await interaction.response.defer(ephemeral=True)
        
        try:
            # Parse params JSON
            import json
            try:
                params_dict = json.loads(params)
            except json.JSONDecodeError:
                await interaction.followup.send(
                    "❌ Invalid JSON in params field. Use valid JSON format.",
                    ephemeral=True
                )
                return
            
            # Get proposer ID (use Discord username)
            proposer = str(interaction.user.name)
            
            # Prepare proposal payload
            payload = {
                "action": action,
                "description": description,
                "params": params_dict,
                "proposer": proposer
            }
            
            # Call API to create proposal
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_base_url}/api/guardian/proposal",
                    json=payload
                ) as response:
                    if response.status == 201:
                        result = await response.json()
                        proposal_id = result['proposal_id']
                        
                        # Create Discord thread for discussion
                        thread = await interaction.channel.create_thread(
                            name=f"🔐 Proposal: {action} - {proposal_id}",
                            auto_archive_duration=10080,  # 7 days
                            type=discord.ChannelType.public_thread
                        )
                        
                        # Post proposal details to thread
                        embed = discord.Embed(
                            title=f"📋 Guardian Proposal: {proposal_id}",
                            description=description,
                            color=discord.Color.blue()
                        )
                        embed.add_field(name="Action", value=action, inline=True)
                        embed.add_field(name="Proposer", value=proposer, inline=True)
                        embed.add_field(name="Quorum Required", value=result['quorum_required'], inline=True)
                        embed.add_field(name="Status", value=result['status'], inline=True)
                        embed.add_field(name="Votes", value=f"✅ 0 | ❌ 0", inline=True)
                        embed.add_field(name="Parameters", value=f"```json\n{json.dumps(params_dict, indent=2)}```", inline=False)
                        embed.set_footer(text=f"Use /guardian vote proposal_id:{proposal_id} vote:approve to vote")
                        
                        message = await thread.send(embed=embed)
                        
                        # Add voting reactions
                        await message.add_reaction("✅")
                        await message.add_reaction("❌")
                        
                        # Update proposal with thread ID
                        # TODO: Add endpoint to update proposal metadata
                        
                        # Send confirmation
                        await interaction.followup.send(
                            f"✅ Proposal created: {proposal_id}\n"
                            f"Discussion thread: {thread.mention}",
                            ephemeral=True
                        )
                        
                        logger.info(f"Proposal {proposal_id} created by {proposer}")
                    
                    else:
                        error_text = await response.text()
                        await interaction.followup.send(
                            f"❌ Failed to create proposal: {error_text}",
                            ephemeral=True
                        )
                        logger.error(f"API error creating proposal: {error_text}")
        
        except Exception as e:
            await interaction.followup.send(
                f"❌ Error creating proposal: {str(e)}",
                ephemeral=True
            )
            logger.error(f"Error in guardian_propose: {str(e)}", exc_info=True)
    
    @app_commands.command(name="vote", description="Vote on a guardian proposal")
    @app_commands.describe(
        proposal_id="Proposal ID to vote on",
        vote="Your vote (approve, reject, or abstain)",
        comment="Optional comment on your vote"
    )
    @app_commands.choices(vote=[
        app_commands.Choice(name="✅ Approve", value="approve"),
        app_commands.Choice(name="❌ Reject", value="reject"),
        app_commands.Choice(name="⏸️ Abstain", value="abstain")
    ])
    async def guardian_vote(
        self,
        interaction: discord.Interaction,
        proposal_id: str,
        vote: app_commands.Choice[str],
        comment: Optional[str] = None
    ):
        """
        Vote on a guardian proposal.
        
        Usage:
            /guardian vote proposal_id:proposal_1 vote:approve comment:"Looks good to me"
        """
        # Defer response
        await interaction.response.defer(ephemeral=True)
        
        try:
            # Get guardian ID (use Discord username)
            guardian_id = str(interaction.user.name)
            
            # Prepare vote payload
            payload = {
                "guardian_id": guardian_id,
                "vote": vote.value,
                "comment": comment
            }
            
            # Call API to submit vote
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_base_url}/api/guardian/vote/{proposal_id}",
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        # Format vote emoji
                        vote_emoji = {
                            "approve": "✅",
                            "reject": "❌",
                            "abstain": "⏸️"
                        }.get(vote.value, "❓")
                        
                        # Build response message
                        message = f"{vote_emoji} Vote recorded on {proposal_id}\n\n"
                        message += f"**Current Status:**\n"
                        message += f"✅ Approve: {result['votes_approve']}\n"
                        message += f"❌ Reject: {result['votes_reject']}\n"
                        message += f"Quorum: {result['votes_approve']}/{result['quorum_required']}\n"
                        
                        if result['quorum_met']:
                            message += f"\n🎉 **Quorum reached!**\n"
                        
                        if result['executed']:
                            message += f"\n⚡ **Proposal executed automatically!**\n"
                        
                        message += f"\nStatus: {result['proposal_status']}"
                        
                        await interaction.followup.send(message, ephemeral=True)
                        
                        # Post vote to thread if possible
                        # TODO: Find and update the proposal thread
                        
                        logger.info(
                            f"Vote recorded: {guardian_id} voted {vote.value} on {proposal_id}"
                        )
                    
                    elif response.status == 400:
                        error = await response.json()
                        await interaction.followup.send(
                            f"❌ Cannot vote: {error.get('detail', 'Unknown error')}",
                            ephemeral=True
                        )
                    
                    elif response.status == 404:
                        await interaction.followup.send(
                            f"❌ Proposal {proposal_id} not found",
                            ephemeral=True
                        )
                    
                    else:
                        error_text = await response.text()
                        await interaction.followup.send(
                            f"❌ Failed to submit vote: {error_text}",
                            ephemeral=True
                        )
                        logger.error(f"API error submitting vote: {error_text}")
        
        except Exception as e:
            await interaction.followup.send(
                f"❌ Error submitting vote: {str(e)}",
                ephemeral=True
            )
            logger.error(f"Error in guardian_vote: {str(e)}", exc_info=True)
    
    @app_commands.command(name="status", description="Check status of a proposal")
    @app_commands.describe(proposal_id="Proposal ID to check")
    async def guardian_status(
        self,
        interaction: discord.Interaction,
        proposal_id: str
    ):
        """
        Check the status of a proposal.
        
        Usage:
            /guardian status proposal_id:proposal_1
        """
        await interaction.response.defer(ephemeral=True)
        
        try:
            # Call API to get proposal
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_base_url}/api/guardian/proposals/{proposal_id}"
                ) as response:
                    if response.status == 200:
                        proposal = await response.json()
                        
                        # Build status embed
                        embed = discord.Embed(
                            title=f"📊 Proposal Status: {proposal_id}",
                            description=proposal['description'],
                            color=discord.Color.green() if proposal['quorum_met'] else discord.Color.orange()
                        )
                        
                        embed.add_field(name="Action", value=proposal['action'], inline=True)
                        embed.add_field(name="Status", value=proposal['status'], inline=True)
                        embed.add_field(name="Proposer", value=proposal['proposer'], inline=True)
                        embed.add_field(
                            name="Votes",
                            value=f"✅ {proposal['votes_approve']} | ❌ {proposal['votes_reject']}",
                            inline=True
                        )
                        embed.add_field(
                            name="Quorum",
                            value=f"{proposal['votes_approve']}/{proposal['quorum_required']}",
                            inline=True
                        )
                        embed.add_field(
                            name="Executed",
                            value="✅ Yes" if proposal['executed'] else "⏳ Pending",
                            inline=True
                        )
                        
                        await interaction.followup.send(embed=embed, ephemeral=True)
                    
                    elif response.status == 404:
                        await interaction.followup.send(
                            f"❌ Proposal {proposal_id} not found",
                            ephemeral=True
                        )
                    
                    else:
                        error_text = await response.text()
                        await interaction.followup.send(
                            f"❌ Error fetching proposal: {error_text}",
                            ephemeral=True
                        )
        
        except Exception as e:
            await interaction.followup.send(
                f"❌ Error checking status: {str(e)}",
                ephemeral=True
            )
            logger.error(f"Error in guardian_status: {str(e)}", exc_info=True)
