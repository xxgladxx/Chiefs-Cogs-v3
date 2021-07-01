from .eval_utils import EvalUtility
def setup(bot):
  cog = EvalUtility(bot=bot)
  bot.add_cog(cog)
