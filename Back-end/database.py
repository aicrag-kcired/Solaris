import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import Client, create_client

# Localiza e lê o arquivo .env
caminho_env = Path(__file__).with_name(".env")
load_dotenv(caminho_env, override=True)

# Pega a URL e a chave do .env
url = os.getenv("SUPABASE_URL")
chave = os.getenv("SUPABASE_KEY")

if not url or not chave:
    raise RuntimeError(
        "Configure SUPABASE_URL e SUPABASE_KEY no arquivo .env."
    )

# Cria a conexão com o Supabase
supabase: Client = create_client(url, chave)