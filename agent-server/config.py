import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration management class for the AI agent server"""
    
    # AI Agent Configuration
    AGENT_MODEL: str = os.getenv("AGENT_MODEL", "anthropic:claude-3-5-sonnet-20241022")
    
    # Database Configuration
    DATABASE_FILE: str = os.getenv("DATABASE_FILE", "ai_tools.db")
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
    DEEPSEEK_API_KEY: Optional[str] = os.getenv("DEEPSEEK_API_KEY")
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that required configuration is present"""
        # Check if at least one API key is available
        if not any([cls.OPENAI_API_KEY, cls.ANTHROPIC_API_KEY, cls.DEEPSEEK_API_KEY]):
            print("Warning: No API keys found. Please set OPENAI_API_KEY, ANTHROPIC_API_KEY, or DEEPSEEK_API_KEY in your .env file.")
            return False
        return True
    
    @classmethod
    def get_database_path(cls) -> str:
        """Get the full path to the database file"""
        return os.path.join(os.path.dirname(__file__), cls.DATABASE_FILE)
    
    @classmethod
    def print_config(cls):
        """Print current configuration (without sensitive data)"""
        print("Current Configuration:")
        print(f"  AGENT_MODEL: {cls.AGENT_MODEL}")
        print(f"  DATABASE_FILE: {cls.DATABASE_FILE}")
        print(f"  HOST: {cls.HOST}")
        print(f"  PORT: {cls.PORT}")
        print(f"  DEBUG: {cls.DEBUG}")
        print(f"  OPENAI_API_KEY: {'Set' if cls.OPENAI_API_KEY else 'Not set'}")
        print(f"  ANTHROPIC_API_KEY: {'Set' if cls.ANTHROPIC_API_KEY else 'Not set'}")
        print(f"  GOOGLE_API_KEY: {'Set' if cls.GOOGLE_API_KEY else 'Not set'}")
        print(f"  DEEPSEEK_API_KEY: {'Set' if cls.DEEPSEEK_API_KEY else 'Not set'}")


# Create a global config instance
config = Config()
