-- CS4400: Introduction to Database Systems (Fall 2024)
-- Project Phase III: Stored Procedures SHELL [v3] Thursday, Nov 7, 2024
set global transaction isolation level serializable;
set global SQL_MODE = 'ANSI,TRADITIONAL';
set names utf8mb4;
set SQL_SAFE_UPDATES = 0;

use business_supply;
-- -----------------------------------------------------------------------------
-- stored procedures and views
-- -----------------------------------------------------------------------------
/* Standard Procedure: If one or more of the necessary conditions for a procedure to
be executed is false, then simply have the procedure halt execution without changing
the database state. Do NOT display any error messages, etc. */

-- [1] add_owner()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new owner.  A new owner must have a unique
username. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_owner;
delimiter //
create procedure add_owner (in ip_username varchar(40), in ip_first_name varchar(100),
	in ip_last_name varchar(100), in ip_address varchar(500), in ip_birthdate date)
sp_main: begin
    -- ensure new owner has a unique username
    if ip_username not in (select username from users where username = ip_username) then
		insert into users (username, first_name, last_name, address, birthdate) 
        values (ip_username, ip_first_name, ip_last_name, ip_address, ip_birthdate); 
        insert into business_owners (username) values (ip_username); 
	elseif ip_username in (select username from users where username = ip_username) then leave sp_main;
    end if; 
end //
delimiter ;

-- [2] add_employee()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new employee without any designated driver or
worker roles.  A new employee must have a unique username and a unique tax identifier. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_employee;
delimiter //
create procedure add_employee (in ip_username varchar(40), in ip_first_name varchar(100),
	in ip_last_name varchar(100), in ip_address varchar(500), in ip_birthdate date,
    in ip_taxID varchar(40), in ip_hired date, in ip_employee_experience integer,
    in ip_salary integer)
sp_main: begin
    -- ensure new owner has a unique username
    -- ensure new employee has a unique tax identifier
    if ip_username not in (select username from employees where username = ip_username)
    and
    ip_taxID not in (select taxID from employees where taxid = ip_taxID) then
		
        insert into users(username, first_name, last_name, address, birthdate)
        values (ip_username, ip_first_name, ip_last_name, ip_address, ip_birthdate)
        ;
        insert into employees(username, taxID, hired, experience, salary) 
        values (ip_username, ip_taxID, ip_hired, ip_employee_experience, ip_salary) 
        ;
	elseif ip_username in (select username from employees where username = ip_username)
    and 
    ip_taxID in (select taxID from employees where taxID = ip_taxID) then
    leave sp_main; 
	end if; 
		
end //
delimiter ;

-- [3] add_driver_role()
-- -----------------------------------------------------------------------------
/* This stored procedure adds the driver role to an existing employee.  The
employee/new driver must have a unique license identifier. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_driver_role; #sussy
delimiter //
create procedure add_driver_role (in ip_username varchar(40), in ip_licenseID varchar(40),
	in ip_license_type varchar(40), in ip_driver_experience integer)
sp_main: begin
    -- ensure employee exists and is not a worker
    -- ensure new driver has a unique license identifier
    if ip_username in (select username from employees) 
    and
    ip_username not in (select username from workers) 
    and
    (ip_username, ip_licenseID) not in (select username, licenseID from drivers) 
    then insert into drivers (username, licenseID, license_type, successful_trips) 
    values (ip_username, ip_licenseID, ip_license_type, ip_driver_experience); 
    insert into workers (username) values (ip_username) 
    ;
    end if; 
--     if ip_username is null 
--     or ip_licenseID is null 
--     or ip_license_type is null 
--     or ip_driver_experience is null then
--         leave sp_main;
--     -- Check if employee exists
--     elseif ip_username not in (select username from employees) then
--         leave sp_main;
--     -- Check if already a worker
--     elseif ip_username in (select username from workers) then
--         leave sp_main;
--     -- Check if license ID is already in use
--     elseif ip_licenseID in (select licenseID from drivers) then
--         leave sp_main;
--     -- If all checks pass, add the driver
--     else
--         insert into drivers (username, licenseID, license_type, successful_trips) 
--         values (ip_username, ip_licenseID, ip_license_type, ip_driver_experience);
--     end if;
    
    
--     declare is_worker integer;
--     declare license_exists integer;
--     
--     select count(*) into employee_exists from employees where username = ip_username;
--     select count(*) into is_worker from workers where username = ip_username;
--     select count(*) into license_exists from drivers where licenseID = ip_licenseID;
--     
--     if ip_username is null 
--         or ip_licenseID is null 
--         or ip_license_type is null 
--         or ip_driver_experience is null 
--         or trim(ip_licenseID) = ''
--         or trim(ip_license_type) = ''
--         or employee_exists = 0
--         or is_worker > 0 
--         or license_exists > 0 then
--         leave sp_main;
--     end if;
--     
--     insert into drivers (username, licenseID, license_type, successful_trips)
--     values (ip_username, ip_licenseID, ip_license_type, ip_driver_experience);

    -- if ip_username in (select username from employees where username = ip_username) 
--     and
--     (select username from drivers where username = ip_username)
--     and
--     ip_licenseID not in (select licenseID from drivers where licenseID = ip_licenseID)
--     then 
--         insert into drivers (username, licenseID, license_type, successful_trips) 
--         values (ip_username, ip_licenseID, ip_license_type, ip_driver_experience)
--         ;
--         insert into workers (username) values (ip_username);
-- 	elseif ip_username not in (select username from employees where username = ip_username)
--     or
--     ip_licenseID in (select licenseID from drivers where licenseID = ip_licenseID)
--     then
-- 		leave sp_main;
-- 	end if; 
end //
delimiter ;

-- [4] add_worker_role()
-- -----------------------------------------------------------------------------
/* This stored procedure adds the worker role to an existing employee. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_worker_role;
delimiter //
create procedure add_worker_role (in ip_username varchar(40))
sp_main: begin
    -- ensure employee exists and is not a driver
    if ip_username in (select username from employees where username = ip_username) 
    and 
    ip_username not in (select username from drivers where username = ip_username) then 
		insert into workers (username) values (ip_username); 
	elseif ip_username not in (select username from employees where username = ip_username) then
		leave sp_main; 
	elseif ip_username in (select username from drivers where username = ip_username) then
		leave sp_main; 
	end if; 
end //
delimiter ;

-- [5] add_product()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new product.  A new product must have a
unique barcode. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_product;
delimiter //
create procedure add_product (in ip_barcode varchar(40), in ip_name varchar(100),
	in ip_weight integer)
sp_main: begin
	-- ensure new product doesn't already exist
    if ip_barcode is null
    or ip_name is null 
    or ip_weight is null then
		leave sp_main; 
	elseif ip_barcode in (select barcode from products) then
		leave sp_main; 
	elseif ip_barcode not in (select barcode from products where barcode = ip_barcode) then
		insert into products (barcode, iname, weight) values (ip_barcode, ip_name, ip_weight); 
	end if; 
end //
delimiter ;

-- [6] add_van()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new van.  A new van must be assigned 
to a valid delivery service and must have a unique tag.  Also, it must be driven
by a valid driver initially (i.e., driver works for the same service). And the van's starting
location will always be the delivery service's home base by default. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_van;
delimiter //
create procedure add_van (in ip_id varchar(40), in ip_tag integer, in ip_fuel integer,
	in ip_capacity integer, in ip_sales integer, in ip_driven_by varchar(40))
sp_main: begin
	-- ensure new van doesn't already exist
    -- ensure that the delivery service exists
    -- ensure that a valid driver will control the van
    if ip_id is null
    or ip_tag is null
    or ip_fuel is null
    or ip_capacity is null
    or ip_sales is null then
    signal sqlstate '45000'
    set message_text = 'required fields cannot be null';
    leave sp_main;
end if;

if (ip_id, ip_tag) in (select id, tag from vans) then
    signal sqlstate '45000'
    set message_text = 'van with this id, tag alr exists';
    leave sp_main;
end if;

if ip_id not in (select id from delivery_services) then
    signal sqlstate '45000'
    set message_text = 'this service dne';
    leave sp_main;
end if;

if ip_driven_by is not null and ip_driven_by not in (select username from drivers) then
    signal sqlstate '45000'
    set message_text = 'driver DNE';
    leave sp_main;
end if;

insert into vans (id, tag, fuel, capacity, sales, driven_by, located_at) 
values (ip_id, ip_tag, ip_fuel, ip_capacity, ip_sales, ip_driven_by,
    (select home_base from delivery_services where id = ip_id)
);

end //
delimiter ;

-- [7] add_business()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new business.  A new business must have a
unique (long) name and must exist at a valid location, and have a valid rating.
And a resturant is initially "independent" (i.e., no owner), but will be assigned
an owner later for funding purposes. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_business;
delimiter //
create procedure add_business (in ip_long_name varchar(40), in ip_rating integer,
	in ip_spent integer, in ip_location varchar(40))
sp_main: begin
	-- ensure new business doesn't already exist
    -- ensure that the location is valid
    -- ensure that the rating is valid (i.e., between 1 and 5 inclusively)
	if ip_long_name is null
    or ip_location is null
    or ip_rating is null
	then 
		signal sqlstate '45000'
		set message_text = 'null values not allowed';
	end if;

	if ip_long_name in (select long_name from businesses)
	then 
		signal sqlstate '45000'
		set message_text = 'business alr exists';
	end if;

	if ip_location not in (select label from locations)
	then 
		signal sqlstate '45000'
		set message_text = 'location dne';
	end if;

	if ip_rating < 1 or ip_rating > 5
	then 
		signal sqlstate '45000'
		set message_text = 'rating not valid';
	end if;

	insert into businesses (long_name, rating, spent, location) 
	values (ip_long_name, ip_rating, ip_spent, ip_location);
			
end //
delimiter ;

-- [8] add_service()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new delivery service.  A new service must have
a unique identifier, along with a valid home base and manager. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_service;
delimiter //
create procedure add_service (in ip_id varchar(40), in ip_long_name varchar(100),
	in ip_home_base varchar(40), in ip_manager varchar(40))
sp_main: begin
	-- ensure new delivery service doesn't already exist
    -- ensure that the home base location is valid
    -- ensure that the manager is valid
    declare id_exists INTEGER; 
    declare location_exists integer;
    declare manager_exists integer; 
    declare manager_other_service integer;
    
    select count(*) into id_exists from delivery_services where id =ip_id;
    select count(*) into location_exists from locations where label = ip_home_base;
    select count(*) into manager_exists from workers where username = ip_manager;
    select count(*) into manager_other_service from delivery_services where manager = ip_manager;
    
    if (id_exists > 0) or (location_exists = 0) or (manager_exists = 0) or (manager_other_service>0) then
		signal sqlstate '45000'
        set message_text = 'smthn wrong';
	end if;
    insert into delivery_services (id, long_name, home_base,manager) 
    values (ip_id, ip_long_name, ip_home_base, ip_manager); 
    
    insert into work_for (username, id) values (ip_manager, ip_id); 

end //
delimiter ;

-- [9] add_location()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new location that becomes a new valid van
destination.  A new location must have a unique combination of coordinates. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_location;
delimiter //
create procedure add_location (in ip_label varchar(40), in ip_x_coord integer,
	in ip_y_coord integer, in ip_space integer)
sp_main: begin
	-- ensure new location doesn't already exist
    -- ensure that the coordinate combination is distinct
    if ip_label is null
        or ip_x_coord is null
        or ip_y_coord is null
        or ip_space is null
        or trim(ip_label) = ''
        or ip_label in (select label from locations)
        or (ip_x_coord, ip_y_coord) in (select x_coord, y_coord from locations) then
        leave sp_main;
    end if;
    
    insert into locations (label, x_coord, y_coord, space)
    values (ip_label, ip_x_coord, ip_y_coord, ip_space);
    
end //
delimiter ;

-- [10] start_funding()
-- -----------------------------------------------------------------------------
/* This stored procedure opens a channel for a business owner to provide funds
to a business. The owner and business must be valid. */
-- -----------------------------------------------------------------------------
drop procedure if exists start_funding;
delimiter //
create procedure start_funding (in ip_owner varchar(40), in ip_amount integer, in ip_long_name varchar(40), in ip_fund_date date)
sp_main: begin
	-- ensure the owner and business are valid

	declare owner_exists integer;
    declare business_exists integer;
    
    if ip_owner is null
        or ip_amount is null
        or ip_long_name is null
        or ip_fund_date is null
        or trim(ip_owner) = ''
        or trim(ip_long_name) = '' then
        leave sp_main;
    end if;
    
    select count(*) into owner_exists 
    from business_owners 
    where username = ip_owner;
    
    select count(*) into business_exists 
    from businesses 
    where long_name = ip_long_name;
    
    if owner_exists > 0 and business_exists > 0 then
        insert into fund (username, invested, invested_date, business) 
        values (ip_owner, ip_amount, ip_fund_date, ip_long_name);
    end if;
end //
delimiter ;

-- [11] hire_employee()
-- -----------------------------------------------------------------------------
/* This stored procedure hires a worker to work for a delivery service.
If a worker is actively serving as manager for a different service, then they are
not eligible to be hired.  Otherwise, the hiring is permitted. */
-- -----------------------------------------------------------------------------
drop procedure if exists hire_employee;
delimiter //
create procedure hire_employee (in ip_username varchar(40), in ip_id varchar(40))
sp_main: begin
	-- ensure that the employee hasn't already been hired by that service
	-- ensure that the employee and delivery service are valid
    -- ensure that the employee isn't a manager for another service
    declare employee_exists integer;
    declare service_exists integer;
    declare already_hired integer;
    declare is_manager integer;
    
    #check if rules are followed
    select count(*) into employee_exists from workers where username = ip_username; 
    select count(*) into service_exists from delivery_services where id = ip_id; 
    select count(*) into already_hired from work_for where username = ip_username and id = ip_id;
    select count(*) into is_manager from delivery_services where manager = ip_username; 
    
    if (employee_exists = 0) or (service_exists = 0) or (already_hired > 0) or (is_manager > 0) then
		signal SQLSTATE '45000'
        set message_text = 'smthn wrong';
	end if;
    
    insert into work_for (username, id) values (ip_username, ip_id);
    end //
    delimiter ;

end //
delimiter ;

-- [12] fire_employee()
-- -----------------------------------------------------------------------------
/* This stored procedure fires a worker who is currently working for a delivery
service.  The only restriction is that the employee must not be serving as a manager 
for the service. Otherwise, the firing is permitted. */
-- -----------------------------------------------------------------------------
drop procedure if exists fire_employee;
delimiter //
create procedure fire_employee (in ip_username varchar(40), in ip_id varchar(40))
sp_main: begin
	-- ensure that the employee is currently working for the service
    -- ensure that the employee isn't an active manager
    if ip_username is null or ip_id is null then
        leave sp_main;
    end if;
    
    -- Check if the employee works for THIS specific service
    if NOT EXISTS (SELECT 1 FROM work_for 
                  WHERE username = ip_username AND id = ip_id) then
        leave sp_main;
    end if;
    
    -- Check if they're the manager of THIS service
    if EXISTS (SELECT 1 FROM delivery_services 
              WHERE id = ip_id AND manager = ip_username) then
        leave sp_main;
    end if;
    
    -- Delete only their employment for THIS service
    delete from work_for 
    where username = ip_username AND id = ip_id; 
end //
delimiter ;

-- [13] manage_service()
-- -----------------------------------------------------------------------------
/* This stored procedure appoints a worker who is currently hired by a delivery
service as the new manager for that service.  The only restrictions is that
the worker must not be working for any other delivery service. Otherwise, the appointment 
to manager is permitted.  The current manager is simply replaced. */
-- -----------------------------------------------------------------------------
drop procedure if exists manage_service;
delimiter //
create procedure manage_service (in ip_username varchar(40), in ip_id varchar(40))
sp_main: begin
	-- ensure that the employee is currently working for the service
	DECLARE v_worker INT;
    DECLARE v_working_for_others INT;
    
    -- ensure that the employee is currently working for the service
    SELECT COUNT(*) INTO v_worker
    FROM work_for
    WHERE username = ip_username AND id = ip_id;
    
    IF v_worker = 0 THEN
		SELECT 'This employee does not work for the specified service.';
	LEAVE sp_main;
    END IF;
    
    -- ensure that the employee isn't working for any other services
    SELECT COUNT(*) INTO v_working_for_others
    FROM work_for
    WHERE username = ip_username;
    
    IF v_working_for_others > 1 THEN
		SELECT 'Cannot promote worker that works for multiple delivery services.';
	LEAVE sp_main;
    END IF;
    
    UPDATE delivery_services
    SET manager = ip_username
    WHERE id = ip_id;

end //
delimiter ;

-- [14] takeover_van()
-- -----------------------------------------------------------------------------
/* This stored procedure allows a valid driver to take control of a van owned by 
the same delivery service. The current controller of the van is simply relieved 
of those duties. */
-- -----------------------------------------------------------------------------
drop procedure if exists takeover_van;
delimiter //
create procedure takeover_van (in ip_username varchar(40), in ip_id varchar(40),
	in ip_tag integer)
sp_main: begin
	if ip_username is NULL then leave sp_main; end if;
	if ip_id is NULL then leave sp_main; end if;
    
	-- The employee is currently operating vans for that service
    if ip_username not in (select driven_by from vans where id = ip_id) then leave sp_main; end if;
	-- ensure that the driver is not driving for another service
    if ip_username in (select driven_by from vans where id != ip_id) then leave sp_main; end if;
	-- ensure that the selected van is owned by the same service
    if (select count(*) from vans where id = ip_id and tag = ip_tag) = 0 then leave sp_main; end if;
    -- ensure that the employee is a valid driver
    if ip_username not in (select username from drivers) then leave sp_main; end if;
    update vans set driven_by = ip_username where (id = ip_id and tag = ip_tag);


end //
delimiter ;

-- [15] load_van()
-- -----------------------------------------------------------------------------
/* This stored procedure allows us to add some quantity of fixed-size packages of
a specific product to a van's payload so that we can sell them for some
specific price to other businesses.  The van can only be loaded if it's located
at its delivery service's home base, and the van must have enough capacity to
carry the increased number of items.

The change/delta quantity value must be positive, and must be added to the quantity
of the product already loaded onto the van as applicable.  And if the product
already exists on the van, then the existing price must not be changed. */
-- -----------------------------------------------------------------------------
drop procedure if exists load_van;
delimiter //
create procedure load_van (in ip_id varchar(40), in ip_tag integer, in ip_barcode varchar(40),
	in ip_more_packages integer, in ip_price integer)
sp_main: begin
    -- add more of the product to the van
    DECLARE v_service_home_base VARCHAR(40);
    DECLARE v_van_location VARCHAR(40);
    DECLARE v_van_capacity INTEGER;
    DECLARE v_payload INT;
    DECLARE v_product_exists INT;
    DECLARE v_contain_exists INT;
    DECLARE v_van_exists INT;

	-- check that the input price is a postive integer
    IF ip_price < 1 THEN
		SELECT 'price must be a positive intger';
        LEAVE sp_main;
	END IF;

    -- ensure that the van being loaded is owned by the service *
    SELECT COUNT(*) INTO v_van_exists
    FROM vans
    WHERE id = ip_id AND tag = ip_tag;

    IF v_van_exists = 0 THEN
        SELECT 'Van does not exist or is not owned by the service.';
        LEAVE sp_main;
    END IF;

    -- ensure that the van being loaded is owned by the service * 
    SELECT COUNT(*) INTO v_product_exists
    FROM products
    WHERE barcode = ip_barcode;

    IF v_product_exists = 0 THEN
        SELECT 'Product does not exist.';
        LEAVE sp_main;
    END IF;

    -- ensure that the van is located at the service home base *

		-- Get the service home base and van location
    SELECT home_base INTO v_service_home_base
    FROM delivery_services
    WHERE id = ip_id;

    SELECT located_at, capacity INTO v_van_location, v_van_capacity
    FROM vans
    WHERE id = ip_id AND tag = ip_tag;

		-- Ensure that the van is located at the service home base
    IF v_van_location != v_service_home_base THEN
        SELECT 'Van is not at the service home base.';
        LEAVE sp_main;
    END IF;

    -- Ensure that the quantity of new packages is greater than zero *
    IF ip_more_packages <= 0 THEN
        SELECT 'Quantity of new packages must be greater than zero.';
        LEAVE sp_main;
    END IF;

    -- Ensure that the price is greater than zero
    IF ip_price <= 0 THEN
        SELECT 'Price must be greater than zero.';
        LEAVE sp_main;
    END IF;

	-- ensure that the van has sufficient capacity to carry the new packages *
	SET v_payload = (SELECT COALESCE(SUM(quantity), 0)
					FROM contain
                    WHERE id = ip_id AND tag = ip_tag) 
                    + ip_more_packages;
    
    -- Ensure that the van has sufficient capacity
    IF v_payload > v_van_capacity THEN
        SELECT 'Van does not have enough capacity for the new packages.';
        LEAVE sp_main;
    END IF;

    -- Check if the product already exists in the van's payload
    SELECT COUNT(*) INTO v_contain_exists
    FROM contain
    WHERE id = ip_id AND tag = ip_tag AND barcode = ip_barcode;

    IF v_contain_exists > 0 THEN
        -- Update the quantity of the existing product
        UPDATE contain
        SET quantity = quantity + ip_more_packages
        WHERE id = ip_id AND tag = ip_tag AND barcode = ip_barcode;
    ELSE
        -- Insert the new product into the van's payload
        INSERT INTO contain (id, tag, barcode, quantity, price)
        VALUES (ip_id, ip_tag, ip_barcode, ip_more_packages, ip_price);
    END IF;

end //
delimiter ;


-- [16] refuel_van()
-- -----------------------------------------------------------------------------
/* This stored procedure allows us to add more fuel to a van. The van can only
be refueled if it's located at the delivery service's home base. */
-- -----------------------------------------------------------------------------
drop procedure if exists refuel_van;
delimiter //
create procedure refuel_van (in ip_id varchar(40), in ip_tag integer, in ip_more_fuel integer)
sp_main: begin
	-- ensure that the van being switched is valid and owned by the service
    -- ensure that the van is located at the service home base
        IF NOT EXISTS (
        SELECT 1 
        FROM vans v
        JOIN delivery_services ds ON v.id = ds.id
        WHERE v.id = ip_id 
        AND v.tag = ip_tag
        AND v.located_at = ds.home_base
    ) THEN 
        LEAVE sp_main;
    END IF;

    -- Update van's fuel
    UPDATE vans 
    SET fuel = fuel + ip_more_fuel
    WHERE id = ip_id AND tag = ip_tag;
end //
delimiter ;

-- [17] drive_van()
-- -----------------------------------------------------------------------------
/* This stored procedure allows us to move a single van to a new
location (i.e., destination). This will also update the respective driver's 
experience and van's fuel. The main constraints on the van(s) being able to 
move to a new  location are fuel and space.  A van can only move to a destination
if it has enough fuel to reach the destination and still move from the destination
back to home base.  And a van can only move to a destination if there's enough
space remaining at the destination. */
-- -----------------------------------------------------------------------------
drop function if exists fuel_required;
delimiter //
create function fuel_required (ip_departure varchar(40), ip_arrival varchar(40))
	returns integer reads sql data
begin
	if (ip_departure = ip_arrival) then return 0;
    else return (select 1 + truncate(sqrt(power(arrival.x_coord - departure.x_coord, 2) + power(arrival.y_coord - departure.y_coord, 2)), 0) as fuel
		from (select x_coord, y_coord from locations where label = ip_departure) as departure,
        (select x_coord, y_coord from locations where label = ip_arrival) as arrival);
	end if;
end //
delimiter ;


drop procedure if exists drive_van;
delimiter //
create procedure drive_van (in ip_id varchar(40), in ip_tag integer, in ip_destination varchar(40))
sp_main: begin
    
    DECLARE v_current_location VARCHAR(40);
    DECLARE v_home_base VARCHAR(40);
    DECLARE v_fuel_needed_to_destination INTEGER;
    DECLARE v_fuel_needed_to_home_base INTEGER;
    DECLARE v_fuel_available INTEGER;
    DECLARE v_remaining_fuel INTEGER;
    DECLARE v_space_available INTEGER;
    DECLARE v_vans_at_destination INTEGER;
    DECLARE v_driver VARCHAR(40);


    -- ensure that the destination is a valid location *
    IF NOT EXISTS (SELECT 1 FROM locations WHERE label = ip_destination) THEN
        SELECT 'Invalid destination location.';
	LEAVE sp_main;
    END IF;


    -- Check if the van exists
    IF NOT EXISTS (SELECT 1 FROM vans WHERE id = ip_id AND tag = ip_tag) THEN
        SELECT 'Van does not exist.';
	LEAVE sp_main;
    END IF;


    -- Get the van's current location, fuel, and driver
    SELECT located_at, fuel, driven_by INTO v_current_location, v_fuel_available, v_driver
    FROM vans
    WHERE id = ip_id AND tag = ip_tag;


    -- ensure that the van isn't already at the location *
    IF v_current_location = ip_destination THEN
        SELECT 'Van is already at the destination.';
	LEAVE sp_main;
    END IF;


    -- Get the home base of the delivery service
    SELECT home_base INTO v_home_base
    FROM delivery_services
    WHERE id = ip_id;


	-- ensure that the van has enough fuel to reach the destination and (then) home base *


		-- Calculate fuel required to reach the destination
    SET v_fuel_needed_to_destination = fuel_required(v_current_location, ip_destination);


		-- Calculate fuel required to return to home base from destination
    SET v_fuel_needed_to_home_base = fuel_required(ip_destination, v_home_base);


		-- Check if the van has enough fuel to reach the destination
    IF v_fuel_available < v_fuel_needed_to_destination THEN
        SELECT 'Not enough fuel to reach destination.';
	LEAVE sp_main;
    END IF;


		-- Calculate remaining fuel after reaching destination
    SET v_remaining_fuel = v_fuel_available - v_fuel_needed_to_destination;


		-- Check if remaining fuel is enough to return to home base
    IF v_remaining_fuel < v_fuel_needed_to_home_base THEN
        SELECT 'Not enough fuel to return to home base after reaching destination.';
	LEAVE sp_main;
    END IF;


	-- ensure that the van has enough space at the destination for the trip *
    
		-- Check if the destination has enough space
    SELECT space INTO v_space_available
    FROM locations
    WHERE label = ip_destination;


    IF v_space_available IS NOT NULL THEN
        -- Count the number of vans currently at the destination
        SELECT COUNT(*) INTO v_vans_at_destination
        FROM vans
        WHERE located_at = ip_destination;


        -- Check if there is enough space
        IF v_vans_at_destination >= v_space_available THEN
            SELECT 'Not enough space at the destination.';
		LEAVE sp_main;
        END IF;
    END IF;


	-- Update the van's location and fuel
    UPDATE vans
    SET located_at = ip_destination,
        fuel = v_remaining_fuel
    WHERE id = ip_id AND tag = ip_tag;


    -- Update the driver's experience
    IF v_driver IS NOT NULL THEN
        UPDATE employees
        SET experience = experience + 1
        WHERE username = v_driver;
    END IF;
    
end //
delimiter ;


-- [18] purchase_product()
-- -----------------------------------------------------------------------------
/* This stored procedure allows a business to purchase products from a van
at its current location.  The van must have the desired quantity of the product
being purchased.  And the business must have enough money to purchase the
products.  If the transaction is otherwise valid, then the van and business
information must be changed appropriately.  Finally, we need to ensure that all
quantities in the payload table (post transaction) are greater than zero. */
-- -----------------------------------------------------------------------------
drop procedure if exists purchase_product;
delimiter //
create procedure purchase_product (in ip_long_name varchar(40), in ip_id varchar(40),
	in ip_tag integer, in ip_barcode varchar(40), in ip_quantity integer)
sp_main: begin
	-- ensure that the business is valid
    -- ensure that the van is valid and exists at the business's location
	-- ensure that the van has enough of the requested product
	-- update the van's payload
    -- update the monies spent and gained for the van and business
    -- ensure all quantities in the contain table are greater than zero
    DECLARE business_location VARCHAR(40);
    DECLARE current_quantity INTEGER;
    DECLARE product_price INTEGER;
    DECLARE total_cost INTEGER;
    
    -- Get business location
    SELECT location INTO business_location
    FROM businesses
    WHERE long_name = ip_long_name;
    
    -- If business doesn't exist, exit
    IF business_location IS NULL THEN
        LEAVE sp_main;
    END IF;
    
    -- Check if van is at business location and get current quantity and price
    SELECT c.quantity, c.price INTO current_quantity, product_price
    FROM contain c
    JOIN vans v ON c.id = v.id AND c.tag = v.tag
    WHERE c.id = ip_id 
    AND c.tag = ip_tag 
    AND c.barcode = ip_barcode
    AND v.located_at = business_location;
    
    -- If van not at location or product not found, exit
    IF current_quantity IS NULL OR current_quantity < ip_quantity THEN
        LEAVE sp_main;
    END IF;
    
    -- Calculate total cost
    SET total_cost = ip_quantity * product_price;
    
    -- Update van's payload
    UPDATE contain 
    SET quantity = quantity - ip_quantity
    WHERE id = ip_id 
    AND tag = ip_tag 
    AND barcode = ip_barcode;
    
    -- Update van's sales
    UPDATE vans 
    SET sales = sales + total_cost
    WHERE id = ip_id AND tag = ip_tag;
    
    -- Update business spent amount
    UPDATE businesses 
    SET spent = spent + total_cost
    WHERE long_name = ip_long_name;
    
    -- Remove products with zero quantity
    DELETE FROM contain 
    WHERE quantity <= 0;
    
end //
delimiter ;

-- [19] remove_product()
-- -----------------------------------------------------------------------------
/* This stored procedure removes a product from the system.  The removal can
occur if, and only if, the product is not being carried by any vans. */
-- -----------------------------------------------------------------------------
drop procedure if exists remove_product;
delimiter //
create procedure remove_product (in ip_barcode varchar(40))
sp_main: begin
	-- ensure that the product exists
    -- ensure that the product is not being carried by any vans
    declare product_exist integer; 
    declare product_in_van integer; 
    
    select count(*) into product_exist from products where barcode = ip_barcode; 
    select count(*) into product_in_van from contain where barcode = ip_barcode; 
    
    if product_exist = 0 then 
		signal sqlstate '45000'
        set message_text = 'product dne'; 
	end if; 
    
    if product_in_van > 0 then 
		signal sqlstate '45000'
        set message_text = 'product carried in van atm'; 
	end if; 
    delete from products where barcode = ip_barcode; 

end //
delimiter ;

-- [20] remove_van()
-- -----------------------------------------------------------------------------
/* This stored procedure removes a van from the system.  The removal can
occur if, and only if, the van is not carrying any products.*/
-- -----------------------------------------------------------------------------
drop procedure if exists remove_van;
delimiter //
create procedure remove_van (in ip_id varchar(40), in ip_tag integer)
sp_main: begin
	-- ensure that the van exists
    -- ensure that the van is not carrying any products
    declare van_exists integer; 
    declare nonempty_van integer; 
    
    select count(*) into van_exists from vans where id = ip_id;
    select count(*) into nonempty_van from contain where id = ip_id and tag = ip_tag; 
    
    if van_exists = 0 then
		signal sqlstate '45000'
        set message_text = 'van dne';
	end if; 
    if nonempty_van > 0 then
		signal sqlstate '45000'
        set message_text = 'van has stuff atm';
	end if; 
    delete from vans where id = ip_id and tag = ip_tag;

end //
delimiter ;

-- [21] remove_driver_role()
-- -----------------------------------------------------------------------------
/* This stored procedure removes a driver from the system.  The removal can
occur if, and only if, the driver is not controlling any vans.  
The driver's information must be completely removed from the system. */
-- -----------------------------------------------------------------------------
drop procedure if exists remove_driver_role;
delimiter //
create procedure remove_driver_role (in ip_username varchar(40))
sp_main: begin
	-- ensure that the driver exists
    -- ensure that the driver is not controlling any vans
    -- remove all remaining information
    IF NOT EXISTS (
        SELECT 1 FROM drivers 
        WHERE username = ip_username
    ) THEN LEAVE sp_main;
    END IF;
    -- Check if driver is controlling any vans
    IF EXISTS (
        SELECT 1 FROM vans 
        WHERE driven_by = ip_username
    ) THEN LEAVE sp_main;
    END IF;
    -- Remove driver information (if all checks pass)
    DELETE FROM drivers 
    WHERE username = ip_username;
    -- Also need to remove from employees if they have no other roles
    IF NOT EXISTS (
        SELECT 1 FROM workers 
        WHERE username = ip_username
    ) THEN 
        DELETE FROM employees 
        WHERE username = ip_username;
        
        DELETE FROM users
        WHERE username = ip_username;
    END IF;

end //
delimiter ;


-- [22] display_owner_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of an owner.
For each owner, it includes the owner's information, along with the number of
businesses for which they provide funds and the number of different places where
those businesses are located.  It also includes the highest and lowest ratings
for each of those businesses, as well as the total amount of debt based on the
monies spent purchasing products by all of those businesses. And if an owner
doesn't fund any businesses then display zeros for the highs, lows and debt. */
-- -----------------------------------------------------------------------------
create or replace view display_owner_view as
select u.username, 
	u.first_name, 
	u.last_name, 
	u.address, 
	count(distinct f.business) as num_businesses, 
	count(distinct b.location) as num_locations, 
	coalesce(max(b.rating),0) as max_rating, 
	coalesce(min(b.rating),0) as min_rating, 
	coalesce(sum(b.spent), 0) as total_debt
from users u
	join business_owners bo on u.username = bo.username
	left join fund f on bo.username = f.username
	left join businesses b on f.business = b.long_name
	group by u.username, u.first_name, u.last_name, u.address
;

-- [23] display_employee_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of an employee.
For each employee, it includes the username, tax identifier, salary, hiring date and
experience level, along with license identifer and driving experience (if applicable,
'n/a' if not), and a 'yes' or 'no' depending on the manager status of the employee. */
-- -----------------------------------------------------------------------------
create or replace view display_employee_view as
select 
    e.username,
    e.taxID,
    e.salary,
    e.hired as hiring_date,
    e.experience as experience_level,
    COALESCE(d.licenseID, 'n/a') as license_identifier,
    COALESCE(CAST(d.successful_trips AS CHAR), 'n/a') as driving_experience,
    CASE 
        WHEN ds.manager IS NOT NULL THEN 'yes'
        ELSE 'no'
    END as manager_status
FROM 
    employees e
    LEFT JOIN drivers d ON e.username = d.username
    LEFT JOIN delivery_services ds ON e.username = ds.manager;



-- [24] display_driver_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of a driver.
For each driver, it includes the username, licenseID and drivering experience, along
with the number of vans that they are controlling. */
-- -----------------------------------------------------------------------------
create or replace view display_driver_view as
select d.username, d.licenseID, d.successful_trips, count(v.driven_by)
from drivers d left join vans v on d.username = v.driven_by group by d.username, d.licenseID, d.successful_trips;

-- [25] display_location_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of a location.
For each location, it includes the label, x- and y- coordinates, along with the
name of the business or service at that location, the number of vans as well as 
the identifiers of the vans at the location (sorted by the tag), and both the 
total and remaining capacity at the location. */
create or replace view display_location_view as
select l.label, l.x_coord, l.y_coord,
case
	when b.long_name is not null then b.long_name
    when ds.long_name is not null then ds.long_name
end as long_name,
count(distinct v.id, v.tag) as num_vans,
GROUP_CONCAT(concat(v.id,'',v.tag) ORDER BY v.tag) AS van_ids,
l.space as capacity,
l.space - count(v.tag) as remaining_capacity
from locations l left join businesses b on b.location = l.label
left join delivery_services ds on l.label = ds.home_base
left join vans v on v.located_at = l.label
where v.id is not null
group by label, x_coord, y_coord, long_name;

-- [26] display_product_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of the products.
For each product that is being carried by at least one van, it includes a list of
the various locations where it can be purchased, along with the total number of packages
that can be purchased and the lowest and highest prices at which the product is being
sold at that location. */
-- -----------------------------------------------------------------------------
create or replace view display_product_view as
select p.iname as product_name, v.located_at, c.quantity as amount_available, min(c.price) as low_price, max(c.price) as high_price
from products p join contain c on c.barcode = p.barcode 
join vans v on v.tag = c.tag and v.id = c.id
group by p.iname, p.barcode, v.located_at, c.quantity;

-- [27] display_service_view()
-- -----------------------------------------------------------------------------
/* This view displays information in the system from the perspective of a delivery
service.  It includes the identifier, name, home base location and manager for the
service, along with the total sales from the vans.  It must also include the number
of unique products along with the total cost and weight of those products being
carried by the vans. */
-- -----------------------------------------------------------------------------
create or replace view display_service_view as
select ds.id, ds.long_name, ds.home_base, ds.manager,
(select sum(sales) from vans v where v.id = ds.id) as revenue, count(c.barcode) as products_carried, sum(c.price*c.quantity) as cost_carried, sum(p.weight*c.quantity) as weight_carried
from delivery_services ds
left join contain c on c.id = ds.id
left join products p on p.barcode = c.barcode
group by ds.id;





