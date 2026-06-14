from pydantic import BaseModel # para criar modelos de dados que serão usados para validar e serializar as requisições e respostas da API. O BaseModel é a classe base do Pydantic, que é uma biblioteca de validação de dados usada pelo FastAPI para garantir que os dados recebidos e enviados pela API estejam no formato correto.
from typing import Optional # para indicar que um campo é opcional, ou seja, pode ser omitido na requisição ou resposta. Isso é útil para campos que não são obrigatórios ou que podem ter valores nulos.


class EventoCreate(BaseModel): # modelo para criar um novo evento, com campos obrigatórios e opcionais. O campo "tipo" tem um valor padrão de "EVENTO", mas pode ser alterado para "HACKATHON" se o evento for um hackathon.
    titulo: str
    descricao: Optional[str] = None
    data_evento: Optional[str] = None   # ISO date: "2025-08-10"
    local: Optional[str] = None
    tipo: str = "EVENTO"                # Evento | Hackathon


class EventoUpdate(BaseModel): # modelo para atualizar um evento existente, onde todos os campos são opcionais, permitindo que apenas os campos que precisam ser atualizados sejam enviados na requisição.
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    data_evento: Optional[str] = None
    local: Optional[str] = None
    tipo: Optional[str] = None


class EventoOut(BaseModel): # modelo para representar um evento na resposta da API, incluindo o ID do evento e os campos obrigatórios e opcionais. O campo "tipo" indica se o evento é um evento comum ou um hackathon.
    id: int
    titulo: str
    descricao: Optional[str]
    data_evento: Optional[str]
    local: Optional[str]
    tipo: str


class InscricaoOut(BaseModel): # modelo para representar uma inscrição em um evento na resposta da API, incluindo o ID da inscrição, o ID do usuário e o ID do evento. Esse modelo é usado para retornar informações sobre as inscrições dos usuários nos eventos.
    id: int
    user_id: int
    evento_id: int