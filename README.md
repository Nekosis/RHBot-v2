# RHBot-v2
 [![License: WTFPL](https://img.shields.io/badge/License-WTFPL-brightgreen.svg)](http://www.wtfpl.net/about/) [![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/Nekosis/RHBot-v2)

RHBot-v2 ("**R**ipper's **H**angout **Bot**, **V**ersion **2**") is an AI-focused Discord bot powered by GPT-4o, intended to be a replacement for Shapes, Inc. roleplay bots after their [removal from Discord on account of TOS violations](https://x.com/panley01/status/1918139269652107525). It is intended primarily for private use on one or a small network of servers and aims to be a fully TOS-compliant alternative to Shapes, Inc. services. However, RHBot-v2 has many capabilities beyond roleplay, which include acting as a regular assistant, playing games, and more!

RHBot-v2's main instance runs in [Artificial Hangout](https://discord.gg/TWpw5ZFGjW), a sister server to [Ripper’s Hangout](https://discord.gg/463CsXBDaC).

## Setup

> [!IMPORTANT]
> RHBot-v2 is intended only for use on Microsoft Windows.

First, ensure all necessary dependencies are installed:

```bash
pip install -r requirements.txt
```

Make sure `RHBot-v2.pyw` is in a dedicated folder along with this README file, the LICENSE file, the `requirements.txt` file, and the `resources/` directory. Create a new file in the same directory called `config.yaml` and set it up as follows:

```yaml
discord_token: "YOUR_DISCORD_TOKEN"
openrouter_api_key: "YOUR_OPENROUTER_API_KEY"
anthropic_api_key: "YOUR_ANTHROPIC_API_KEY"
developer_id: "YOUR_DEVELOPER_ID"
developer_username: "YOUR_DEVELOPER_USERNAME"
```

Now, replace:

- `YOUR_DISCORD_TOKEN` with a Discord bot token from the [Discord Developer Portal](https://discord.com/developers/applications). Enable Server Members Intent and Message Content Intent.

- `YOUR_OPENROUTER_API_KEY` with an API key from [OpenRouter](https://openrouter.ai/). An account is required to use the OpenRouter API. Note that payment is necessary to make requests to GPT-4o (pricing info is available [here](https://openrouter.ai/openai/gpt-4o)). The script is currently hardcoded to use OpenRouter, but changing it to use any other OpenAI-compatible API shouldn't be much work.

- `YOUR_ANTHROPIC_API_KEY` with an API key from the [Anthropic Console](https://console.anthropic.com/settings/keys). This is used to count tokens for Claude models. You will need to add some credit in order to use the token counter, but you will only need to do so once. Even if you run out of credit, the token counter will remain available.

- `YOUR_DEVELOPER_ID` with your Discord User ID (enable Developer Mode in User Settings > App Settings > Advanced, then click on your nameplate in the bottom-left corner of the app and select Copy User ID). This prevents users from using your username as their alias.

- `YOUR_DEVELOPER_USERNAME` with your exact Discord username (case-sensitive). This ensures the bot recognizes you for developer privileges in AI interactions.

Create an invite link for the bot by navigating to the OAuth2 URL Generator, found under Settings > OAuth2 in the Discord Developer Portal. Within the generator, enable the `bot` and `applications.commands` scopes. Then, under Bot Permissions, select the following permissions: View Channels, Send Messages, Manage Messages, Embed Links, Read Message History, and Use Slash Commands. Once you've configured these settings, copy the Generated URL and store it in a secure location. **Do not invite the bot to your server yet.**

Run `RHBot-v2.pyw` (note the `.pyw` extension for headless operation). The bot will begin to run in the background, appearing as a system tray icon and writing logs to a `logs/` directory. You can right-click on the system tray to either view the most recent log file or shut down the bot. Once you see the "RHBot-v2 Online" desktop notification, invite the bot to your server using your pre-generated OAuth URL.

## Commands

- `/set-ai-manager-role` - Designate a role that can manage the AI without being granted full administrator permissions. Requires administrator permissions or existing AI Manager role.

- `/activate` - Activate the regular assistant mode in the current channel. The bot will respond to every message in the channel as a general-purpose assistant. Requires administrator permissions or the AI Manager role.

- `/deactivate` - Deactivate the assistant or a character in the current channel. This will delete the channel's conversation history. Requires administrator permissions or the AI Manager role.

- `/wack` - Delete the current channel's conversation history. The bot will continue to respond to messages in the channel, but any previous conversation will be forgotten. Requires administrator permissions or the AI Manager role.

- `/set-alias` - Set an alias for the bot to refer to you as instead of your Discord username. Note that aliases are global across all servers the bot is a member of.

- `/remove-alias` - Remove any custom alias you have set.

- `/create-character` - Create a new roleplay character that the bot can act as. You can use the placeholders `{user}` and `{char}` in the Character Description field, which, when sent to the AI, will be replaced with the username of the person interacting with the character and the character's name, respectively.

- `/activate-character` - Activate a character in the current channel using its Character ID. The bot will respond to every message in the channel as the character. Requires administrator permissions or the AI Manager role.

- `/list-characters` - List all available characters that have been created. Requires administrator permissions or the AI Manager role.

- `/get-character-info` - Get information about a character using its ID.

- `/edit-character` - Edit a character. Requires administrator permissions or the AI Manager role.

- `/delete-character` - Delete a character. Requires administrator permissions or the AI Manager role.

- `/monkeys-paw` - Begin a game of Monkey's Paw. You will have 5 wishes, and the mysterious Monkey's Paw will grant them—with a twist.

- `/monkeys-paw-abort` - End your current Monkey's Paw game.

- `/create-player-card` – Create a player card for adventures. You can use the `{player}` placeholder in the Player Description field, which, when sent to the AI, will be replaced with the player's name.

- `/list-player-cards` – List your player cards.

- `/get-player-card-info` – View one of your cards.

- `/edit-player-card` - Edit a player card.

- `/delete-player-card` – Delete one of your cards.

- `/create-lorebook` - Create a new lorebook.

- `/list-lorebooks` - Show all lorebooks you own.

- `/get-lorebook-info` - View a lorebook’s full text.

- `/edit-lorebook` - Edit a lorebook.

- `/delete-lorebook` - Delete a lorebook.

- `/attach-lorebook` - Attach the lorebook to one of your player cards so it’s sent to the narrator whenever that card is active.

- `/detach-lorebook` - Remove a lorebook from a player card.

- `/start-game` – Begin an adventure in the current channel. Requires administrator permissions or the AI Manager role.

- `/reset-game` – Clear the adventure’s history. Requires administrator permissions or the AI Manager role.

- `/stop-game` – End the adventure and wipe its history. Requires administrator permissions or the AI Manager role.

- `/drop-in` – Join an active adventure with one of your player cards.

- `/ping` - You know this one.

## Images

RHBot-v2 supports image interpretation. If an image is attached to a message, the bot will automatically generate a detailed text description of the image and treat this description as if it were part of the original message.

## Text Adventure System

RHBot-v2 now ships with a multiplayer, AI-narrated text adventure game.  
Players create personal player cards, an admin starts a session, and everybody’s actions are woven together by the narrator.

### How it works

1. **Create a player card** – `/create-player-card` (each user can keep multiple cards).

2. **Start the game** – An admin/AI Manager runs `/start-game <card_id>` in a channel. This channel becomes the adventure venue.

3. **Drop in** – Other users join with `/drop-in <card_id> [entrance text]`; the narrator introduces them diegetically.

4. **Play** – Simply type; the narrator replies with the evolving story.

5. **Manage** – Admins can `/reset-game` (wipe history but keep players) or `/stop-game` (end and delete everything).

> **Lorebooks**  
> Any time the narrator seems confused about world-specific terms, write a lorebook explaining them, then `/attach-lorebook` it to the relevant player card(s). Every attached lorebook is injected into the narrator’s system-prompt under a “# Lorebooks” section, ensuring consistent knowledge for future scenes.

## Models

You can optionally pass a model to `/activate` or `/activate-character` to have the bot use a different AI model in this channel. To ensure correct tokenization, you can currently choose from three models:

- **GPT-4o** (`openai/gpt-4o`) - Default model

- **Claude 3.7 Sonnet** (`anthropic/claude-3.7-sonnet`)

- **WizardLM-2 8x22b** (`microsoft/wizardlm-2-8x22b`) - Can engage with and create NSFW/explicit content

## License

RHBot-v2 is licensed under the [WTFPL](https://www.wtfpl.net/about/), version 2. See the LICENSE file for more details.
