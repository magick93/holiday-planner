import os
from supabase import create_client, Client
from typing import Optional

class SupabaseClientSingleton:
    _instance: Optional[Client] = None

    @classmethod
    def get_instance(cls) -> Client:
        if cls._instance is None:
            url: str = os.environ.get("SUPABASE_URL")
            key: str = os.environ.get("SUPABASE_KEY")
            cls._instance = create_client(url, key)
        return cls._instance


