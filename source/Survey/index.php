<?php

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // open a database connection
    $db = new PDO("sqlite:survey.db") or die ('Cannot open database');

    // the database should be set up but what the heck
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

    // set blank form fields to NULL
    $vision_level   = isset($_POST["vision_level"]) ? $_POST["vision_level"] : NULL;
    $how_long       = isset($_POST["how_long"]) ? $_POST["how_long"] : NULL;
    $aid            = isset($_POST["aid"]) ? $_POST["aid"] : NULL;
    $screen_reader  = isset($_POST["screen_reader"]) ? $_POST["screen_reader"] : NULL;
    $dso            = isset($_POST["dso"]) ? $_POST["dso"] : NULL;
    $interiors      = isset($_POST["interiors"]) ? $_POST["interiors"] : NULL;
    $outdoors       = isset($_POST["outdoors"]) ? $_POST["outdoors"] : NULL;
    $wall_plaques   = isset($_POST["wall_plaques"]) ? $_POST["wall_plaques"] : NULL;
    $internal_route = isset($_POST["internal_route"]) ? $_POST["internal_route"] : NULL;
    $cane           = isset($_POST["cane"]) ? $_POST["cane"] : NULL;
    $animal         = isset($_POST["animal"]) ? $_POST["animal"] : NULL;
    $help           = isset($_POST["help"]) ? $_POST["help"] : NULL;
    $attendance     = isset($_POST["attendance"]) ? $_POST["attendance"] : NULL;
    $lost_campus    = isset($_POST["lost_campus"]) ? $_POST["lost_campus"] : NULL;
    $lost_inside    = isset($_POST["lost_inside"]) ? $_POST["lost_inside"] : NULL;
    $without_aid    = isset($_POST["without_aid"]) ? $_POST["without_aid"] : NULL;
    $with_aid       = isset($_POST["with_aid"]) ? $_POST["with_aid"] : NULL;
    $inside_exp     = isset($_POST["inside_exp"]) ? $_POST["inside_exp"] : NULL;
    $outside_exp    = isset($_POST["outside_exp"]) ? $_POST["outside_exp"] : NULL;
    $what_help      = isset($_POST["what_help"]) ? $_POST["what_help"] : NULL;
    $app_desires    = isset($_POST["app_desires"]) ? $_POST["app_desires"] : NULL;
    $submit_survey  = isset($_POST["submit_survey"]) ? $_POST["submit_survey"] : NULL;

    // Create a prepared statement; we don't want any SQL injection
    $prepared_stmt =
        "INSERT INTO survey_results (vision_level, how_long, aid, screen_reader, dso, interiors, outdoors, wall_plaques, internal_route, cane, animal, help, attendance, lost_campus, lost_inside, with_aid, without_aid, inside_exp, outside_exp, what_help, app_desires)
         VALUES ( :vision_level, :how_long, :aid, :screen_reader, :dso, :interiors, :outdoors, :wall_plaques, :internal_route, :cane, :animal, :help, :attendance, :lost_campus, :lost_inside, :with_aid, :without_aid, :inside_exp, :outside_exp, :what_help, :app_desires)";

    // bind the parameters
    $stmt = $db->prepare($prepared_stmt);
    $stmt->bindParam(':vision_level', $vision_level);
    $stmt->bindParam(':how_long', $how_long);
    $stmt->bindParam(':aid', $aid);
    $stmt->bindParam(':screen_reader', $screen_reader);
    $stmt->bindParam(':dso', $dso);
    $stmt->bindParam(':interiors', $interiors);
    $stmt->bindParam(':outdoors', $outdoors);
    $stmt->bindParam(':wall_plaques', $wall_plaques);
    $stmt->bindParam(':internal_route', $internal_route);
    $stmt->bindParam(':cane', $cane);
    $stmt->bindParam(':animal', $animal);
    $stmt->bindParam(':help', $help);
    $stmt->bindParam(':attendance', $attendance);
    $stmt->bindParam(':lost_campus', $lost_campus);
    $stmt->bindParam(':lost_inside', $lost_inside);
    $stmt->bindParam(':with_aid', $with_aid);
    $stmt->bindParam(':without_aid', $without_aid);
    $stmt->bindParam(':inside_exp', $inside_exp);
    $stmt->bindParam(':outside_exp', $outside_exp);
    $stmt->bindParam(':what_help', $what_help);
    $stmt->bindParam(':app_desires', $app_desires);

    // execute the prepared statement
    if( $stmt->execute() ){
        print "<h1>Thank you for submitting your survey!</h1>";
        
    }
    else {
        print "Data insert failed";
    }
}
else {
    $action = htmlspecialchars($_SERVER["PHP_SELF"]);
    // print the form
print <<< _HTML
<!DOCTYPE html>
<html lang = "en">
  <head>
    <link rel="stylesheet" href="style.css">
    <title>Student Survey Form</title>
  </head>
  <body>
    <h1>Hello!</h1>
    <p>
    Thank you for taking the time to fill out this survey.
    This information is <em>TOTALLY ANONYMOUS</em> so please answer freely and to the best of your ability!
    </p>
    <form name="form" onsubmit="validate()" method = "POST">
      <fieldset>
        <legend>
          <h2>Background Questions</h2>
        </legend>
        <fieldset>
          <div>
            <label for="vision_level">How would you describe your level of vision?</label>
            <input value="" type="text" id="vision_level" name="vision_level" />
          </div>
        </fieldset>
        <fieldset>
          <div>
            <label for="how_long">How long have you had a visual impairment?</label>
            <input value="" type="text" name="how_long" id="how_long" />
          </div>
        </fieldset>
        <fieldset>
          <div>
            <label for="aid">What do you use to help you navigate the University?</label>
            <input value="" type="text" id="aid" name="aid"/>
          </div>
        </fieldset>
        <fieldset>
          <div>
            <label for="screen_reader">If you use a screen reader, which do you prefer?</label>
            <input value="" type="text" name="screen_reader" id="screen_reader"/>
          </div>
        </fieldset>
        <fieldset>
          <div>
            <label for="dso">What elements of the Disability Services Office do you use?</label>
            <input value="" type="text" name="dso" id="dso" />
          </div>
        </fieldset>
      </fieldset>
      <fieldset>
        <legend>
          <h2>Scale Questions</h2>
        </legend>
        <fieldset>
          <legend>What is your experience navigating the University building interiors?</legend>
          <div>
            <input type="radio" name="interiors" value="VeryEasy" id="interiors_ve">
            <label for="interiors_ve">Very Easy</label>
          </div>
          <div>
            <input type="radio" name="interiors" value="Easy" id="interiors_e">
            <label for="interiors_e">Easy</label>
          </div>
          <div>
            <input type="radio" name="interiors" value="Neutral" id="interiors_n">
            <label for="interiors_n">Neutral</label>
          </div>
          <div>
            <input type="radio" name="interiors" value="Difficult" id="interiors_d">
            <label for="interiors_d">Difficult</label>
          </div>
          <div>
            <input type="radio" name="interiors" value="VeryDifficult" id="interiors_vd">
            <label for="interiors_vd">Very Difficult</label>
          </div>
        </fieldset>
        <fieldset>
          <legend>What is your experience navigating the campus outdoors?</legend>
          <div>
            <input type="radio" name="outdoors" value="VeryEasy" id="outdoors_ve">
            <label for="outdoors_ve">Very Easy</label>
          </div>
          <div>
            <input type="radio" name="outdoors" value="Easy" id="outdoors_e">
            <label for="outdoors_e">Easy</label>
          </div>
          <div>
            <input type="radio" name="outdoors" value="Neutral" id="outdoors_n">
            <label for="outdoors_n">Neutral</label>
          </div>
          <div>
            <input type="radio" name="outdoors" value="Difficult" id="outdoors_d">
            <label for="outdoors_d">Difficult</label>
          </div>
          <div>
            <input type="radio" name="outdoors" value="VeryDifficult" id="outdoors_vd">
            <label for="outdoors_vd">Very Difficult</label>
          </div>
        </fieldset>
        <fieldset>
          <legend>How helpful are the wall plaques next to classrooms and other facilities?</legend>
          <div>
            <input type="radio" name="wall_plaques" value="VeryHelpful" id="wall_plaques_vh">
            <label for="wall_plaques_vh">Very Helpful</label>
          </div>
          <div>
            <input type="radio" name="wall_plaques" value="Helpful" id="wall_plaques_h">
            <label for="wall_plaques_h">Helpful</label>
          </div>
          <div>
            <input type="radio" name="wall_plaques" value="Neutral" id="wall_plaques_n">
            <label for="wall_plaques_n">Neutral</label>
          </div>
          <div>
            <input type="radio" name="wall_plaques" value="Unhelpful" id="wall_plaques_u">
            <label for="wall_plaques_u">Unhelpful</label>
          </div>
          <div>
            <input type="radio" name="wall_plaques" value="VeryUnhelpful" id="wall_plaques_vu">
            <label for="wall_plaques_vu">Very Unhelpful</label>
          </div>
        </fieldset>
        <fieldset>
          <legend>How long until you have internalized a route (for instance, between your dorm and the dining hall)?</legend>
          <div>
            <input type="radio" name="internal_route" value="1to7Days" id="internal_route_1">
            <label for="internal_route_1">1 to 7 Days</label>
          </div>
          <div>
            <input type="radio" name="internal_route" value="8to24Days" id="internal_route_2">
            <label for="internal_route_2">8 to 24 Days</label>
          </div>
          <div>
            <input type="radio" name="internal_route" value="25to40Days" id="internal_route_3">
            <label for="internal_route_3">25 to 40 Days</label>
          </div>
          <div>
            <input type="radio" name="internal_route" value="41to65Days" id="internal_route_4">
            <label for="internal_route_4">41 to 65 Days</label>
          </div>
          <div>
            <input type="radio" name="internal_route" value="Morethan66Days" id="internal_route_5">
            <label for="internal_route_5">More than 66 Days</label>
          </div>
        </fieldset>
      </fieldset>
      <fieldset>
        <legend>
          <h2>Yes or No Questions</h2>
        </legend>
        <fieldset>
          <legend>Do you use a cane?</legend>
          <div>
            <input type="radio" name="cane" value="Yes" id="cane_yes">
            <label for="cane_yes">Yes</label>
          </div>
          <div>
            <input type="radio" name="cane" value="No" id="cane_no">
            <label for="cane_no">No</label>
          </div>
        </fieldset>
        <fieldset>
          <legend>Do you have a service animal?</legend>
          <div>
            <input type="radio" name="animal" value="Yes" id="animal_yes">
            <label for="animal_yes">Yes</label>
          </div>
          <div>
            <input type="radio" name="animal" value="No" id="animal_no">
            <label for="animal_no">No</label>
          </div>
        </fieldset>
        <fieldset>
          <legend>Does someone help guide you between classes?</legend>
          <div>
            <input type="radio" name="help" value="Yes" id="help_yes">
            <label for="help_yes">Yes</label>
          </div>
          <div>
            <input type="radio" name="help" value="No" id="help_no">
            <label for="help_no">No</label>
          </div>
        </fieldset>
        <fieldset>
          <legend>Does navigating classes get in the way of schoolwork or attendance?</legend>
          <div>
            <input type="radio" name="attendance" value="Yes" id="attendance_yes">
            <label for="attendance_yes">Yes</label>
          </div>
          <div>
            <input type="radio" name="attendance" value="No" id="attendance_no">
            <label for="attendance_no">No</label>
          </div>
        </fieldset>
        <fieldset>
          <legend>Have you become lost on campus?</legend>
          <div>
            <input type="radio" name="lost_campus" value="Yes" id="lost_campus_yes">
            <label for="lost_campus_yes">Yes</label>
          </div>
          <div>
            <input type="radio" name="lost_campus" value="No" id="lost_campus_no">
            <label for="lost_campus_no">No</label>
          </div>
        </fieldset>
        <fieldset>
          <legend>Have you become lost inside a university building?</legend>
          <div>
            <input type="radio" name="lost_inside" value="Yes" id="lost_inside_yes">
            <label for="lost_inside_yes">Yes</label>
          </div>
          <div>
            <input type="radio" name="lost_inside" value="No" id="lost_inside_no">
            <label for="lost_inside_no">No</label>
          </div>
        </fieldset>
      </fieldset>
      <fieldset>
        <legend><h2>Open-ended Questions</h2></legend>
        <fieldset>
          <legend>If you are travelling without an aid or a seeing-eye dog, how do you map the trip in your mind?</legend>
          <label for="without_aid"></label>
          <textarea id="without_aid" name="without_aid" cols="80" rows="10"></textarea>
        </fieldset>
        <fieldset>
          <legend>If you travel with an aid or seeing-eye dog, how do you map the trip in your mind?</legend>
          <label for="with_aid"></label>
          <textarea id="with_aid" name="with_aid" cols="80" rows="10"></textarea>
        </fieldset>
        <fieldset>
          <legend>What is your experience of the University buildings inside? How do you understand the layout? What stands out to you?</legend>
          <label for="inside_experience"></label>
          <textarea id="inside_experience" name="inside_exp" cols="80" rows="10"></textarea>
        </fieldset>
        <fieldset>
          <legend>What is your experience of the campus outside? How do you understand the layout? What stands out to you?</legend>
          <label for="outside_experience"></label>
          <textarea id="outside_experience" name="outside_exp" cols="80" rows="10"></textarea>
        </fieldset>
        <fieldset>
          <legend>What would you find helpful for navigating the inside of campus buildings?</legend>
          <label for="what_helpful"></label>
          <textarea id="what_helpful" name="what_help" cols="80" rows="10"></textarea>
        </fieldset>
        <fieldset>
          <legend>If you had an app that would give you directions from your current room to another room in the building, what would you want the directions to sound like? For example, would you like the turning directions to be in terms of Left and Right and Straight, or East and West? Or some other format? What measure of distance would be most helpful? Metric ("Go ahead 5 feet"), Relative ("Take 3 paces forward"), Constant ("Six doors ahead and arrive at an exit"), or some other method? If you feel strongly, please elaborate!</legend>
          <label for="app_desires"></label>
          <textarea  id="app_desires" name="app_desires" cols="80" rows="10"></textarea>
        </fieldset>
      </fieldset>
      <table>
        <tr>
          <td><input type="reset"></td>
          <td><input type="submit" value="Submit Survey" name="submit_survey"></td>
        </tr>
      </table>
    </form>
  </body>
</html>
_HTML;
}
?>
