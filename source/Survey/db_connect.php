<?php
    $db_name = '/www/student/jfeil302/refdb/aforms.db';

    $db = new sqlite3($db_name);
    // echo($db_name);
    $query = "CREATE TABLE IF NOT EXISTS survey_results (
            response_id INTEGER PRIMARY KEY,
            vision_level VARCHAR,
            how_long VARCHAR,
            aid VARCHAR,
            screen_reader VARCHAR,
            dso VARCHAR,
            interiors INT,
            outdoors INT,
            wall_plaques INT,
            internal_route INT,
            cane BOOLEAN,
            animal BOOLEAN,
            help BOOLEAN,
            attendance BOOLEAN,
            lost_campus BOOLEAN,
            lost_inside BOOLEAN,
            with_aid VARCHAR,
            without_aid VARCHAR,
            inside_exp VARCHAR,
            outside_exp VARCHAR,
            what_help VARCHAR,
            app_desires VARCHAR
        )";

    $db->exec($query);