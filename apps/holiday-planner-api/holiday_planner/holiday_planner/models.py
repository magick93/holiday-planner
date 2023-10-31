from typing import Any
from pydantic import BaseModel, constr
from django.db import models
from ninja_extra import ModelService
from pydantic import BaseModel as PydanticModel, Field
from typing import List, Optional


class CountrySchema(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    iso: constr(max_length=2)
    is_public: Optional[bool] = None

class CategorySchema(BaseModel):
    id: str
    title: str

class Category(models.Model):
    title = models.CharField(max_length=100)


class TouristCountry(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=2)

    def __str__(self):
        return self.name
    
 

class Attraction(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_child_friendly = models.BooleanField()
    category = models.OneToOneField(
        Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='attractions'
    )
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title


class AttractionModelService(ModelService):
    def create(self, schema: PydanticModel, **kwargs: Any) -> Any:
        data = schema.dict(by_alias=True)
        data.update(kwargs)

        instance = self.model._default_manager.create(**data)
        return instance
    

class TouristPlaceSchema(BaseModel):
    id: str
    name: str
    country: str

class TouristPlace(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(TouristCountry, on_delete=models.CASCADE, related_name='tourist_places')
    attractions = models.ManyToManyField('Attraction', related_name='tourist_places')

    def __str__(self):
        return self.name
    
class PlaceModelService(ModelService):
    def create(self, schema: PydanticModel, **kwargs: Any) -> Any:
        data = schema.dict(by_alias=True)
        data.update(kwargs)

        instance = self.model._default_manager.create(**data)
        return instance