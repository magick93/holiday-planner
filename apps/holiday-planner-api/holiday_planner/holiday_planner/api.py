from .models import Attraction, AttractionModelService, Category, CategorySchema, CountrySchema, TouristCountry, TouristPlace, PlaceModelService
from .pg_models import Country
from django.core.exceptions import ObjectDoesNotExist
from ninja import Schema, constants
from icecream import ic
# from pydantic import BaseModel as ModelConfig
from ninja_extra import (
    ControllerBase,
    ModelConfig,
    ModelControllerBase,
    ModelEndpointFactory,
    ModelSchemaConfig,
    api_controller,
    NinjaExtraAPI,
    http_get,
    http_patch
)

from .geocodingview import GeoCodingAPIView
from .holidayplanner_admin import HolidayPlannerAdmin

api = NinjaExtraAPI(
   title="Holiday Planner API",
   description="This is a demo API with dynamic OpenAPI info section"
)


@api_controller('/', tags=['GeoCoding'], permissions=[])
class GeoCodingAPI:

    @http_get('/geocoding',)
    def geocoding(self, name: str):
        """Geocoding API"""
        return {"result": GeoCodingAPIView.get(self, name).data}
    
@api_controller('/', tags=['HolidayPlannerAdminAPI'], permissions=[])
class HolidayPlannerAdminAPI(ControllerBase):

    # country_model = get

    def toggle_is_public(iso: str):
        # Define the function here
        country = Country.objects.get(iso=iso)
        old_value = country.is_public
        country.is_public = not old_value
        country.save()
        new_value = country.is_public
        return old_value, new_value
    
    @http_patch('/toggle-country-public-status/{iso}',  response=CountrySchema)
    def toggle_country_public_status(self, iso: str):
        # self.toggle_is_public(iso)
        try:
            old_value, new_value = HolidayPlannerAdmin.toggle_is_public(self, iso)
            return CountrySchema(id=iso, name=Country.objects.get(iso=iso).name, iso=iso, is_public=new_value)
        except ObjectDoesNotExist as e:
            return self.create_response(f'{e}', status_code=404 )
        except ValueError as e:
            return self.create_response(f'{e}', status_code=400 )
        except Exception as e:
            return self.create_response(f'{e}', status_code=500 )
           

@api_controller("/attractions")
class AttractionModelController(ModelControllerBase):
    service = AttractionModelService(model=Attraction)
    model_config = ModelConfig(
        model=Attraction,        
        schema_config=ModelSchemaConfig(read_only_fields=["id", "category"]),
    )

    get_attraction_category = ModelEndpointFactory.find_one(
        path="/{int:attraction_id}/category",
        schema_out=CategorySchema,
        lookup_param='attraction_id',
        object_getter=lambda self, pk, **kw: self.service.get_one(pk=pk).category
    )

    get_events_by_category = ModelEndpointFactory.list(
        path="/category/{int:category_id}/",
        schema_out=model_config.retrieve_schema,
        # lookup_param='category_id',
        queryset_getter=lambda self, **kw: Category.objects.filter(pk=kw['category_id']).first().events.all()
    )


@api_controller("/places")
class PlaceModelController(ModelControllerBase):
    service = PlaceModelService(model=TouristPlace)
    model_config = ModelConfig(
        model=TouristPlace,        
        schema_config=ModelSchemaConfig(read_only_fields=["id"]),
    )

    get_places_by_country = ModelEndpointFactory.list(
        path="/places/{int:country_id}/",
        schema_out=model_config.retrieve_schema,
        # lookup_param='country_id',
        queryset_getter=lambda self, **kw: TouristCountry.objects.filter(pk=kw['country_id']).first().places.all()
    )



api.register_controllers(
    HolidayPlannerAdminAPI,
    GeoCodingAPI,
    AttractionModelController,
    PlaceModelController
)
