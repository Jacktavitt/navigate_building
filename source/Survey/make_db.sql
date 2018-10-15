
-- create initial table
CREATE TABLE survey_results (
    response_id INTEGER PRIMARY KEY,
    vision_level VARCHAR,
    how_long VARCHAR,
    aid VARCHAR,
    screen_reader VARCHAR,
    dso VARCHAR,
    interiors VARCHAR,
    outdoors VARCHAR,
    wall_plaques VARCHAR,
    internal_route VARCHAR,
    cane VARCHAR,
    animal VARCHAR,
    help VARCHAR,
    attendance VARCHAR,
    lost_campus VARCHAR,
    lost_inside VARCHAR,
    with_aid VARCHAR,
    without_aid VARCHAR,
    inside_exp VARCHAR,
    outside_exp VARCHAR,
    what_help VARCHAR,
    app_desires VARCHAR
)

-- insert results into db
INSERT INTO survey_results(
    vision_level ,
    how_long ,
    aid ,
    screen_reader ,
    dso ,
    interiors ,
    outdoors ,
    wall_plaques ,
    internal_route ,
    cane ,
    animal ,
    help ,
    attendance ,
    lost_campus ,
    lost_inside ,
    with_aid ,
    without_aid ,
    inside_exp ,
    outside_exp ,
    what_help ,
    app_desires 
)
VALUES (
    -- vision_level VARCHAR,
    'partially blind',
    -- how_long VARCHAR,
    '9 years',
    -- aid VARCHAR,
    'service cat',
    -- screen_reader VARCHAR,
    'NVDA',
    -- dso VARCHAR,
    'just this survey and free pizza',
    -- interiors INT,
    2,
    -- outdoors INT,
    4,
    -- wall_plaques INT,
    1,
    -- internal_route INT,
    2,
    -- cane BOOLEAN,
    0,
    -- animal BOOLEAN,
    1,
    -- help BOOLEAN,
    0,
    -- attendance BOOLEAN,
    0,
    -- lost_campus BOOLEAN,
    1,
    -- lost_inside BOOLEAN,
    0,
    -- with_aid VARCHAR,
    'its crazy',
    -- without_aid VARCHAR,
    'yeah',
    -- inside_exp VARCHAR,
    'nope',
    -- outside_exp VARCHAR,
    'teaeaf',
    -- what_help VARCHAR,
    'none',
    -- app_desires VARCHAR
    'big screen'
)
