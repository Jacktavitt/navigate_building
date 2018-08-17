<?php
$message = "";
if (isset($_POST['submit_survey']) ) {
    // include db connection
    include "db_connect.php";
    // initialize variables
    $vl= $hl= $aid= $sr= $dso= $inter= $outd= $wp= $ir= $cane= $anim= $help= $attd= $lc= $li= $wa= $woa= $iex= $oex= $whlp= $app ='';
    $vlErr= $hlErr= $aidErr= $srErr= $dsoErr= $interErr= $outdErr= $wpErr= $irErr= $caneErr= $animErr= $helpErr= $attdErr= $lcErr= $liErr= $waErr= $woaErr= $iexErr= $oexErr= $whlpErr= $appErr='';

    $formElts = array($vl, $hl, $aid, $sr, $dso, $inter, $outd, $wp, $ir,
                        $cane, $anim, $help, $attd, $lc, $li, $wa, $woa,
                        $iex, $oex, $whlp, $app);
    $formEltErrs = array($vlErr, $hlErr, $aidErr, $srErr, $dsoErr,
                        $interErr, $outdErr, $wpErr, $irErr, $caneErr,
                        $animErr, $helpErr, $attdErr, $lcErr, $liErr, 
                        $waErr, $woaErr, $iexErr, $oexErr, $whlpErr, $appErr);
    $cleanPost = $_POST;
    // remove submit button element
    array_pop($cleanPost);
    
    function error_check(&$var, &$varErr, $postKey, $postVar) {
        if (empty($postVar)){
            $varErr="Missing $postKey element";
        } else {
            $var = htmlspecialchars($postVar);
        }
    }
    $multiArray = array();
    $iterator = new MultipleIterator;
    $iterator->attachIterator(new ArrayIterator($formElts));
    $iterator->attachIterator(new ArrayIterator($formEltErrs));
    $iterator->attachIterator(new ArrayIterator($cleanPost));
    foreach ($iterator as $keys => $values) {
        error_check($values[0],$values[1], $keys[2],$values[2]);
        // var_dump($values[0],$values[1],$keys[2],$values[2]);
        array_push($multiArray, array($keys[2] => array($values[0], $values[1])));
        // echo "<br>";
    }
    // for($ctr=0;$ctr<count($cleanPost);$ctr++){
        // echo $formElts[$ctr].','. $formEltErrs[$ctr].','.$cleanPost[$ctr].','."<br>";
    // } 
    var_dump($multiArray);
    


    // var_dump($_POST);
    
	// // make query with student data
	// $query = "INSERT INTO survey_results (
      // vision_level ,
      // how_long ,
      // aid ,
      // screen_reader ,
      // dso ,
      // interiors ,
      // outdoors ,
      // wall_plaques ,
      // internal_route ,
      // cane ,
      // animal ,
      // help ,
      // attendance ,
      // lost_campus ,
      // lost_inside ,
      // with_aid ,
      // without_aid ,
      // inside_exp ,
      // outside_exp ,
      // what_help ,
      // app_desires) 
      // VALUES ('$vl', '$hl', '$aid', '$sr', '$dso', '$inter', '$outd', '$wp', '$ir', '$cane', '$anim', '$help', '$attd', '$lc', '$li', '$wa', '$woa', '$iex', '$oex', '$whlp', '$app')";

    // // var_dump(array_keys($_POST));
    // // var_dump(array_values($_POST));
    // function rayprint($v1,$v2){
        // return $v1 .','. $v2;
    // }
    
    // $keys = array_keys($_POST);
    // $values = array_values($_POST);
    // array_pop($keys);
    // array_pop($values);
    // $aa = implode(', ',$keys);
    // $vv = implode(', ',$values);

    // $smartquery="INSERT INTO survey_results($aa) VALUES ('$vv')";
    // // echo htmlspecialchars($_SERVER["PHP_SELF"]);
    // echo $smartquery;
    // // $message = "Thanks";
    	// execute query and check if success
	// if( $db->exec($smartquery) ){
		// $message = "data inserted success";
	// }
	// else {
		// $message = "Data insert failed";
	// }
}
?>

<!DOCTYPE html>
<html lang = "en">
<head>
  <link rel="stylesheet" href="style.css">
  <title>Student Survey Form</title>
</head>
<body>
<div><?php echo $message;?></div>
  <h1>Hello!</h1>
    <p>
      Thank you for taking the time to fill out this survey.
      This information is <em>TOTALLY ANONYMOUS</em> so please answer freely and to the best of your ability!
    </p>
  <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>" method = "POST">
    <fieldset>
      <legend>
        <h3>Background Questions</h3>
      </legend>
      <fieldset>
        <div>
          <label for="vision_level">How would you describe your level of vision?</label>
          <input type="text" id="vision_level" name="vision_level"/>
        </div>
      </fieldset>
      <fieldset>  
        <div>
          <label for="how_long">How long have you had a visual impairment?</label>
          <input type="text" name="how_long" id="how_long" />
        </div>
      </fieldset>
      <fieldset>
        <div>
          <label for="aid">What do you use to help you navigate the University?</label>
          <input type="text" id="aid" name="aid"/>
        </div>
      </fieldset>
      <fieldset>
        <div>
          <label for="screen_reader">If you use a screen reader, which do you prefer?</label>
          <input type="text" name="screen_reader" id="screen_reader"/>
        </div>
      </fieldset>
      <fieldset>
        <div>
            <label for="dso">What elements of the Disability Services Office do you use?</label>
          <input type="text" name="dso" id="dso" />
        </div>
      </fieldset>
    </fieldset>
    <fieldset>
      <legend>
        <h3>Scale Questions</h3>
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
        <h3>Yes or No Questions</h3>
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
    <legend><h3>Open-ended Questions</h3></legend>
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
        <textarea id="app_desires" name="app_desires" cols="80" rows="10"></textarea>
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
