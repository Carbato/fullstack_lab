from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas_spl import SampleCreateModel, SampleUpdateModel
from sqlmodel import select, desc
from app.db.models import Sample


class SampleService:
    async def get_all_samples(self, session: AsyncSession):
        statement = select(Sample).order_by(desc(Sample.created_at))  # order_by(desc(Sample.created_at))
        result = await session.exec(statement)
        return result.all()
    
    async def get_client_samples(self, client_uid, session: AsyncSession):
        statement = select(Sample).where(Sample.client_uid == client_uid).order_by(desc(Sample.created_at))
        result = await session.exec(statement)
        return result.all() 
    
    async def get_a_sample(self, sample_uid: str, session: AsyncSession):
        setatement = select(Sample).where(Sample.uid == sample_uid)
        result = await session.exec(setatement)
        the_sample = result.first()
        return the_sample if the_sample is not None else None
    
    async def create_sample(self, user_uid:str ,sample_data: SampleCreateModel, session: AsyncSession):
        sample_data_dict = sample_data.model_dump()
        new_sample = Sample(**sample_data_dict)
        new_sample.user_uid = user_uid
        session.add(new_sample)
        await session.commit()
        return new_sample
    
    async def update_sample(self, sample_uid: str, update_data: SampleUpdateModel, session: AsyncSession):
        sample_to_update = await self.get_a_sample(sample_uid, session)
        if sample_to_update is not None:
            update_data_dict = update_data.model_dump()
            for key, value in update_data_dict.items():
                setattr(sample_to_update, key, value)
            await session.commit()
            return sample_to_update
        else:
            return None
        
    async def delete_sample(self, sample_uid: str, session: AsyncSession):
        sample_to_delete = await self.get_a_sample(sample_uid, session)

        if sample_to_delete is not None:
            await session.delete(sample_to_delete)
            await session.commit()
            return True
        else:
            return None