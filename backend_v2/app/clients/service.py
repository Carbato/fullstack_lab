from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import ClientCreateModel, ClientUpdateModel
from sqlmodel import select, desc
from .models import Client

class ClientService:
    async def get_all_clients(self, session: AsyncSession):
        statement = select(Client).order_by(desc(Client.name)) # order_by(desc(Client.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_a_client(self, client_uid:str, session: AsyncSession):
        statement = select(Client).where(Client.uid == client_uid)
        result = await session.exec(statement)
        the_client =  result.first()
        return the_client if the_client is not None else None

    
    async def create_client(self, client_data:ClientCreateModel, session: AsyncSession):
        client_data_dict = client_data.model_dump() # Convert the Pydantic model to a dictionary
        new_client = Client(**client_data_dict) # Create a new Client instance
        session.add(new_client)
        await session.commit()
        return new_client

    async def update_client(self, client_uid:str, update_data:ClientUpdateModel, session: AsyncSession):
        client_to_update = await self.get_a_client(client_uid, session) # Get the client to update
        if client_to_update is not None:
            update_data_dict = update_data.model_dump()
            for key, value in update_data_dict.items():
                setattr(client_to_update, key, value) # Update the client's attributes
            await session.commit()
            return client_to_update
        else:
            return None
    

    async def delete_client(self, client_uid:str, session: AsyncSession):
        client_to_delete = await self.get_a_client(client_uid, session)

        if client_to_delete is not None:
            session.delete(client_to_delete)
            await session.delete(client_to_delete)
            await session.commit()
            return {"message": "Client deleted successfully"}
        else:
            return None
