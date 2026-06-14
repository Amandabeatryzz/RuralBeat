from pydantic_settings import BaseSettings
# A classe Settings é uma subclasse de BaseSettings do Pydantic, que é usada para definir as configurações do aplicativo. Ela inclui campos para a URL do banco de dados
#, a chave secreta usada para assinar os tokens JWT, o algoritmo de assinatura e o tempo de expiração dos tokens. 
# A classe Config dentro de Settings especifica que as configurações podem ser carregadas a partir de um arquivo .env,
#  o que é útil para manter as configurações sensíveis fora do código-fonte. O objeto settings é uma instância da classe Settings, que pode ser importada e usada em outras partes do aplicativo para acessar as configurações definidas.

class Settings(BaseSettings):
    DATABASE_URL: str = "database/ruralbeat.db"
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256" 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24h

    class Config:
        env_file = ".env"


settings = Settings()

