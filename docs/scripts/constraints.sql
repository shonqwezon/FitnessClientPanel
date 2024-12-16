-- client_plan
ALTER TABLE client_plan DROP CONSTRAINT IF EXISTS fk_client_id;
ALTER TABLE client_plan DROP CONSTRAINT IF EXISTS fk_plan_id;

ALTER TABLE client_plan ADD CONSTRAINT
    fk_client_id FOREIGN KEY (client_id) REFERENCES client(id)
        ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE client_plan ADD CONSTRAINT
    fk_plan_id FOREIGN KEY (plan_id) REFERENCES plan(id)
        ON UPDATE CASCADE ON DELETE CASCADE;

-- manager
ALTER TABLE manager DROP CONSTRAINT IF EXISTS fk_sportcenter_id;

ALTER TABLE manager ADD CONSTRAINT
    fk_sportcenter_id FOREIGN KEY (sportcenter_id) REFERENCES sportcenter(id)
        ON UPDATE CASCADE ON DELETE CASCADE;

-- plan_service
ALTER TABLE plan_service DROP CONSTRAINT IF EXISTS fk_plan_id;
ALTER TABLE plan_service DROP CONSTRAINT IF EXISTS fk_service_id;

ALTER TABLE plan_service ADD CONSTRAINT
    fk_plan_id FOREIGN KEY (plan_id) REFERENCES plan(id)
        ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE plan_service ADD CONSTRAINT
    fk_service_id FOREIGN KEY (service_id) REFERENCES service(id)
        ON UPDATE CASCADE ON DELETE CASCADE;

-- plan
ALTER TABLE plan DROP CONSTRAINT IF EXISTS fk_sportcenter_id;

ALTER TABLE plan ADD CONSTRAINT
    fk_sportcenter_id FOREIGN KEY (sportcenter_id) REFERENCES sportcenter(id)
        ON UPDATE CASCADE ON DELETE CASCADE;
