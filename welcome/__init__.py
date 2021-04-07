from .welcome import Welcome

def setup(bot):
    check_folders()
    check_files()
    n = Welcome(bot)
    bot.add_listener(n.member_join, "on_member_join")
    bot.add_cog(n)
