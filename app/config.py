from functools import lru_cache
from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file='.env',extra='ignore')
    aws_region:str='eu-north-1'
    aws_access_key_id:str=''
    aws_secret_access_key:str=''
    s3_bucket: str = Field(
        default='',
        validation_alias=AliasChoices('S3_BUCKET', 'S3_BUCKET_NAME'),
    )
    database_url:str=''  # Render PostgreSQL External Database URL
    bedrock_embed_model:str='amazon.titan-embed-text-v2:0'
    bedrock_chat_model:str='amazon.nova-lite-v1:0'
    embed_dim:int=1024
    max_upload_bytes:int=10485760
    pinecone_api_key:str=''
    pinecone_index_name:str='rag-sentinel-index'
    pinecone_cloud:str='aws'
    pinecone_region:str='eu-north-1'
    pinecone_ready_timeout:int=180
    min_relevance:float=0.25
    hitl_enabled:bool=True
    memory_turns:int=6


@lru_cache
def settings() -> Settings:
    return Settings()