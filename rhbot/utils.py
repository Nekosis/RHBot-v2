import discord
import asyncio
import json
import os
from typing import Optional

import aiohttp
import pystray
from PIL import Image
from discord import app_commands

from .config import logger, ANTHROPIC_API_KEY, DATA_DIR, LOG_DIR
from .constants import ENCODING_GPT4O, TOKENIZER_WIZARDLM

async def num_tokens_from_messages(messages, model):
    if model == 'openai/gpt-4o':
        def _gpt4o_count():
            num_tokens = 0
            for message in messages:
                num_tokens += 3  # role + content
                for key, value in message.items():
                    if key == "content":
                        num_tokens += len(ENCODING_GPT4O.encode(value))
                    elif key == "name":
                        num_tokens += len(ENCODING_GPT4O.encode(value))
            num_tokens += 3  # assistant priming
            return num_tokens
        return await asyncio.to_thread(_gpt4o_count)
    
    elif model == 'anthropic/claude-3.7-sonnet':
        system_parts = []
        chat_messages = []
        for msg in messages:
            if msg['role'] == 'system':
                system_parts.append(msg['content'])
            elif msg['role'] in ['user', 'assistant']:
                chat_messages.append({
                    'role': msg['role'],
                    'content': msg['content']
                })
        
        async with aiohttp.ClientSession() as session:
            try:
                response = await session.post(
                    "https://api.anthropic.com/v1/messages/count_tokens",
                    headers={
                        "x-api-key": ANTHROPIC_API_KEY,
                        "anthropic-version": "2023-06-01",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "claude-3-7-sonnet-20250219",
                        "system": "\n".join(system_parts),
                        "messages": chat_messages
                    }
                )
                if response.status == 200:
                    data = await response.json()
                    return data['input_tokens']
                else:
                    error = await response.text()
                    logger.error(f"Anthropic token count failed:", exc_info=True)
                    return 0
            except Exception as e:
                logger.error("Anthropic API error:", exc_info=True)
                return 0
    
    elif model == 'microsoft/wizardlm-2-8x22b':
        def _wizardlm_count():
            try:
                formatted_chat = TOKENIZER_WIZARDLM.apply_chat_template(messages, tokenize=False)
                tokens = TOKENIZER_WIZARDLM.encode(formatted_chat, add_special_tokens=False)
                return len(tokens)
            except Exception as e:
                total = 0
                for msg in messages:
                    total += len(TOKENIZER_WIZARDLM.encode(msg['content'], add_special_tokens=False))
                return total
        return await asyncio.to_thread(_wizardlm_count)
    
    else:
        raise ValueError(f"Unsupported model: {model}")

def get_guild_dir(guild_id):
    return os.path.join(DATA_DIR, str(guild_id))

def get_channel_path(guild_id, channel_id):
    return os.path.join(get_guild_dir(guild_id), f"{channel_id}.json")
    
def get_game_path(guild_id: int, user_id: int) -> str:
    return os.path.join(DATA_DIR, str(guild_id), 'games', 'monkeyspaw', f'{user_id}.json')

def get_player_cards_dir(user_id: int) -> str:
    return os.path.join(DATA_DIR, 'player_cards', str(user_id))

def get_player_card_path(user_id: int, card_id: str) -> str:
    return os.path.join(get_player_cards_dir(user_id), f'{card_id}.json')

def get_text_game_path(guild_id: int, channel_id: int) -> str:
    return os.path.join(
        DATA_DIR, str(guild_id), 'games', 'textadventure', f'{channel_id}.json'
    )

def build_game_system_prompt(players: dict) -> str:
    """Return a narrator prompt including all active players."""
    def render(desc: str, name: str) -> str:
        return (desc
                .replace('{player}', name)
                .replace('{Player}', name))

    roster = '\n'.join(
        f"- {p['name']}: {render(p['description'], p['name'])}"
        for p in players.values()
    )
    
    return (f"You are an imaginative, immersive narrator for a co-operative multiplayer text adventure. Respond **only** as narrative prose, never mentioning game mechanics.\n\n**Active player roster:**\n{roster}\n\nAfter each user input, describe how the world reacts and ask what the players do next.")

def setup_tray_icon(bot):
    icon_path = os.path.join(os.path.dirname(__file__), 'resources', 'icon.ico')
    
    def view_log():
        try:
            log_files = sorted(
                [f for f in os.listdir(LOG_DIR) if f.endswith('.log')],
                reverse=True
            )
            if log_files:
                latest_log = os.path.join(LOG_DIR, log_files[0])
                os.startfile(latest_log)
        except Exception as e:
            logger.error(f"Failed to open log:", exc_info=True)

    def exit_app():
        logger.info("Shutting down via tray icon...")
        icon.stop()
        # Schedule bot shutdown
        loop = bot.loop
        loop.call_soon_threadsafe(
            lambda: loop.create_task(bot.close())
        )

    menu = pystray.Menu(
        pystray.MenuItem('View Latest Log', lambda: view_log()),
        pystray.MenuItem('Exit', lambda: exit_app())
    )
    
    try:
        image = Image.open(icon_path)
        icon = pystray.Icon("RHBot", image, "RHBot is running", menu)
        icon.run()
    except Exception as e:
        logger.error(f"Failed to create tray icon:", exc_info=True)

def is_admin_or_ai_manager(interaction: discord.Interaction) -> bool:
    if interaction.user.guild_permissions.administrator:
        return True
    
    ai_manager_role = get_ai_manager_role(interaction.guild.id)
    if ai_manager_role and any(role.id == ai_manager_role for role in interaction.user.roles):
        return True
    
    # Raise CheckFailure with error message
    raise app_commands.CheckFailure(
        "You do not have permission to run this command."
    )

def get_ai_manager_role(guild_id: int) -> Optional[int]:
    role_file = os.path.join(get_guild_dir(guild_id), 'ai_manager_role.json')
    if not os.path.exists(role_file):
        return None
    
    try:
        with open(role_file, 'r') as f:
            data = json.load(f)
        return data.get('role_id')
    except:
        return None
