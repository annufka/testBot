from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
PORT = env.int("PORT")
ADMINS = env.list("ADMINS")