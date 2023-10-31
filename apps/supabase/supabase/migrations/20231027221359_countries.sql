create sequence country_seq;

create table if not exists country (
  id int not null default nextval ('country_seq'),
  iso char(2) not null unique,
  name varchar(80) not null,
  nicename varchar(80) not null,
  iso3 char(3) default null,
  numcode smallint default null,
  phonecode int not null,
  primary key (id)
);

create table place (
  id int not null default nextval ('country_seq'),
  name varchar(80) not null,
  primary key (id)
);

alter table place add column latitude double precision;
alter table place add column longitude double precision;
alter table place add column elevation numeric(10, 5);
alter table place add column feature_code varchar(10);
alter table place add column place_code char(2);
alter table place add column admin1_id int;
alter table place add column admin2_id int;
alter table place add column timezone varchar(50);
alter table place add column population int;
alter table place add column place_id int;
alter table place add column admin1 varchar(80);
alter table place add column admin2 varchar(80);
alter table place add column created_at timestamp with time zone default now();
alter table place add column updated_at timestamp with time zone default now();

create extension postgis with schema extensions;

alter table place 
add column geom geometry(point, 4326) 
generated always as (extensions.st_setsrid(extensions.st_makepoint(longitude, latitude), 4326)) stored unique;

alter table place add country_id int references country(id);

create or replace function get_country_id_by_iso2_code(iso_code char(2))
returns int as $$
declare
  country_id int;
begin
  select id into country_id from country where iso = upper(iso_code) limit 1;

  if country_id is null then
    raise warning 'country with iso code % not found', iso_code;
    return null;
  end if;

  return country_id;
end;
$$ language plpgsql;


create or replace function upsert_places(data json)
returns void language plpgsql as $$
declare
    item json;
begin

  -- check if data is a scalar or an array
  if json_typeof(data) = 'object' then
    data = json_build_array(data);
  end if;

 -- if data is a scalar then log
  if json_typeof(data) <> 'array' then
    raise notice 'invalid data type %', json_typeof(data);
    return;
  end if;

    for item in select * from json_array_elements(data) loop
        insert into public.place(
            "name",
            latitude,
            longitude,
            elevation,
            feature_code,
            place_code,
            admin1_id,
            admin2_id,
            timezone,
            population,
            admin1,
            admin2,
            country_id
        )
        values (
            item->>'name',
            (item->>'latitude')::float8,
            (item->>'longitude')::float8,
            (item->>'elevation')::numeric,
            item->>'feature_code',
            item->>'country_code',
            (item->>'admin1_id')::int4,
            (item->>'admin2_id')::int4,
            item->>'timezone',
            (item->>'population')::int4,
            item->>'admin1',
            item->>'admin2',
            get_country_id_by_iso2_code(item->>'country_code')
        )
        on conflict(geom) do update set
            "name" = excluded."name",
            latitude = excluded.latitude,
            longitude = excluded.longitude,
            elevation = excluded.elevation,
            feature_code = excluded.feature_code,
            place_code = excluded.place_code,
            admin1_id = excluded.admin1_id,
            admin2_id = excluded.admin2_id,
            timezone = excluded.timezone,
            population = excluded.population,
            admin1 = excluded.admin1,
            admin2 = excluded.admin2,
            country_id = excluded.country_id;
    end loop;
end;
$$;

-- create a function to update the 'updated_at' column
create or replace function update_updated_at_column()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

-- create a trigger to call the function when a row in the 'place' table is updated
create trigger update_place_updated_at
before update on place
for each row execute function update_updated_at_column();



-- table for basic tourist attraction info
create table tourist_attraction (
    id serial primary key,
    name varchar(255) not null,
    description text,
    type varchar(255),
    place int4 not null references place(id)
);

-- table for accessibility info
create table accessibility (
    attraction_id int references tourist_attraction(id),
    wheelchair_accessible boolean,
    accommodations text,
    primary key(attraction_id)
);

-- table for admission fee info
create table admission_fee (
    attraction_id int references tourist_attraction(id),
    cost numeric(10, 2),
    discounts text,
    primary key(attraction_id)
);

-- table for amenities
create table amenities (
    attraction_id int references tourist_attraction(id),
    onsite_offerings text,
    primary key(attraction_id)
);

-- table for operation hours
create table operation_hours (
    attraction_id int references tourist_attraction(id),
    open_time time,
    close_time time,
    days_closed text[],
    primary key(attraction_id)
);

-- table for visit details
create table visit_details (
    attraction_id int references tourist_attraction(id),
    best_time_to_visit text,
    child_friendly boolean,
    crowds text,
    educational_value text,
    entertainment text,
    ideal_length_of_visit text,
    photography_allowed boolean,
    restrooms_available boolean,
    weather_issues text,
    primary key(attraction_id)
);

-- table for services
create table services (
    attraction_id int references tourist_attraction(id),
    language_services text,
    safety text,
    transportation text,
    parking text,
    primary key(attraction_id)
);

alter table country add column is_public boolean default false;




