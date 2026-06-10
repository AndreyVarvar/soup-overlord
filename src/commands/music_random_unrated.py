from discord.ext import commands as cmds

def register(bot: cmds.Bot)
    @bot.hybrid_command(
        name="music-rate-random",
        description="Get a random track to rate"
    )
    async def music_random_unrated(ctx: cmds.Context):
        if ctx.interaction is None:  # to appease type-hintind
            return

        await ctx.interaction.response.defer(ephemeral=True)
        data = music_utils.database_fetch_all_not_sent_by_user(ctx.interaction.user.id)

        if len(data) == 0:
            await ctx.interaction.followup.send("Sadly, there are no tracks for you to vote on.")

        # clean up the data a little
        new_data = []
        for i in range(len(data)):
            item = data[i]
            if item[6] is None or ctx.interaction.user.name not in item[6]:
                new_data.append(item)
        
        data = new_data
        
        if len(data) == 0:
            await ctx.interaction.followup.send("WOW, there isn\'t a single track that doesn\'t have your vote!")
        else:
            link = None
            k = len(data)
            for i in range(k):  # list through all possible items and find the one that works
                random_item = random.choice(data)
                link = music_utils.spotify_get_track_link(random_item, spotify_client)

                if link is None:  # no such track exists on spotify end. Perhaps it got deleted or temporarily not available
                    del data[data.index(random_item)]

                    if len(data) == 0:
                        break
                    else:
                        continue
                else:
                    break

            if link is None:
                await ctx.interaction.followup.send('WOW, there isn\'t a single track that doesn\'t have your vote!')
            else:
                name = other_utils.get_name(bot, random_item[2])
                await ctx.interaction.followup.send(f'What would you rate `{random_item[0]}` by `{random_item[1]}` sent by `{name}`?\n{link}', view=RateMusicView(random_item[0], random_item[1], ctx.interaction.user.name))
