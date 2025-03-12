import glob
import importlib
import os


module_files = glob.glob(os.path.dirname(__file__) + "/*.py")
__all__ = [os.path.basename(f)[:-3] for f in module_files if not f.endswith("__init__.py")]
__all__.remove("cogLoldle")


async def setup(bot):
    for cog in __all__:
        module = importlib.import_module(f".{cog}", package=__name__)
        await bot.add_cog(module.setup(bot))
