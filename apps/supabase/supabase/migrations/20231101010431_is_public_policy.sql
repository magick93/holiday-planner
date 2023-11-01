ALTER TABLE public.place ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.place FORCE ROW LEVEL SECURITY;


CREATE POLICY "Select only is_public country places" ON "public"."place"
AS PERMISSIVE FOR SELECT
TO anon
USING (EXISTS ( SELECT 1 FROM public.country c WHERE c.id = get_country_id_by_iso2_code(place.place_code) AND c.is_public = true ))


-- Create new user for django api
CREATE USER anon_user WITH PASSWORD 'password123';

-- Assign the new user to the 'anon' role
GRANT anon TO anon_user;





