from pydantic import ValidationError
from .models import CountrySchema
from .pg_models import Country
from django.core.exceptions import ObjectDoesNotExist
from icecream import ic
ic.configureOutput(includeContext=True)
ic.includeContext = True

class HolidayPlannerAdmin:

    @staticmethod
    def toggle_is_public(self, iso: str):
        try:
            input = CountrySchema(iso=iso)
            # Attempt to retrieve the Country instance with the given iso code
            country = Country.objects.get(iso=input.iso)
            ic(country.name, country.is_public, country.iso, country.id)
        except ValidationError as e:
            # Handle Pydantic validation error
            raise ValueError(f'Invalid input: {e}')
        except Country.DoesNotExist:
            # Raise an exception or return an error message if the instance is not found
            raise ObjectDoesNotExist(f"No Country found with iso code: {iso}")
        
        # Store the old value of is_public
        old_value = country.is_public
        
        # Toggle the is_public field
        country.is_public = not country.is_public
        
        # Save the changes to the database
        country.save()
        
        # Return the old and new values
        return old_value, country.is_public
