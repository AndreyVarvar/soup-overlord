import discord
from src.bot_core import SoupOverlordCore
from src.music_database import MusicDatabase, Track, get_all_links_in_message


def register(soup_overlord: SoupOverlordCore):
    soup_overlord.log("Registering 'on-message' event.")

    music_database: MusicDatabase = soup_overlord.music_database

    @soup_overlord.bot.event
    async def on_message(message: discord.Message):
        if message.author.bot:
            return  # don't allow bots to trigger the event

        if message.channel == soup_overlord.config["discordServer"]["musicChannelID"]:
            links = get_all_links_in_message(message)

            if len(links) >= 2:
                await message.reply("This track contains more than 1 spotify link, therefore it's not eligible to be registered.")
                return
            
            if len(links) == 1:
                link = links[0]
                entries = music_database.filter(lambda entry: entry.link == link)

                if len(entries) > 1:  # catch when there are more than 1 entry with the same link
                    await soup_overlord.discord_log(f"Link `{link}` has `{len(entries)}` entries!")
                    await soup_overlord.discord_log(f"`{entries}`")

                if len(entries) > 0:
                    example: Track = entries[0]

                    await message.reply(
                        f"`{example.track_name}` by `{example.track_author}` was already sent before by `{soup_overlord.get_cached_name(example.original_sender)}`"
                    )
                    return

