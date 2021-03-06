<head>
	<title>Apartment Hunting</title>
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css"rel="stylesheet">
</head>
<body>
<div class="container h-100">
    <div class="row h-100 justify-content-center align-items-center">
        <div class="col-10 col-md-8 col-lg-6" style="padding:40px;">
        <h1> Apartment Hunting </h1>
        <p> A website for spreadsheet lovers! </p>

        <form action='main.py' method='POST'>
        <h5>Required Fields</h5>
        <label>City: </label> <input type='text' name='city'>
        <label> State: </label>
        <select name='state'>
          	<option value='AL'>AL</option>
            <option value='AK'>AK</option>
            <option value='AR'>AR</option>
            <option value='AZ'>AZ</option>
            <option value='CA'>CA</option>
            <option value='CO'>CO</option>
            <option value='CT'>CT</option>
            <option value='DC'>DC</option>
            <option value='DE'>DE</option>
            <option value='FL'>FL</option>
            <option value='GA'>GA</option>
            <option value='HI'>HI</option>
            <option value='IA'>IA</option>
            <option value='ID'>ID</option>
            <option value='IL'>IL</option>
            <option value='IN'>IN</option>
            <option value='KS'>KS</option>
            <option value='KY'>KY</option>
            <option value='LA'>LA</option>
            <option value='MA'>MA</option>
            <option value='MD'>MD</option>
            <option value='ME'>ME</option>
            <option value='MI'>MI</option>
            <option value='MN'>MN</option>
            <option value='MO'>MO</option>
            <option value='MS'>MS</option>
            <option value='MT'>MT</option>
            <option value='NC'>NC</option>
            <option value='NE'>NE</option>
            <option value='NH'>NH</option>
            <option value='NJ'>NJ</option>
            <option value='NM'>NM</option>
            <option value='NV'>NV</option>
            <option value='NY'>NY</option>
            <option value='ND'>ND</option>
            <option value='OH'>OH</option>
            <option value='OK'>OK</option>
            <option value='OR'>OR</option>
            <option value='PA'>PA</option>
            <option value='RI'>RI</option>
            <option value='SC'>SC</option>
            <option value='SD'>SD</option>
            <option value='TN'>TN</option>
            <option value='TX'>TX</option>
            <option value='UT'>UT</option>
            <option value='VT'>VT</option>
            <option value='VA'>VA</option>
            <option value='WA'>WA</option>
            <option value='WI'>WI</option>
            <option value='WV'>WV</option>
            <option value='WY'>WY</option>
        </select><br><br>

        <h5>Additional Filters (optional)</h5>
        <label>Max Price: $</label><input type='text' name='price'><br><br>

        <label for='beds'>Beds </label>
        <select name='beds'>
            <option value='1-bedrooms'>1</option><option value='2-bedrooms'>2</option><option value='3-bedrooms'>3</option><option value='4-bedrooms'>4+</option>
        </select><br><br>

        <label for='bathrooms'>Bathrooms </label>
        <select name='bathrooms'>
            <option value='1-bathrooms'>1+</option><option value='2-bathrooms'>2+</option><option value='3-bathrooms'>3+</option>
        </select><br>

        <br><label for='features'>Other Features:</label><br>
        <input type='checkbox' class='features' name='checkbox[]' value='washer-dryer'> In Unit Washer & Dryer<br>
        <input type='checkbox' class='features' name='checkbox[]' value='parking'> Parking<br>
        <input type='checkbox' class='features' name='checkbox[]' value='fitness-center'> Fitness Center<br>
        <input type='checkbox' class='features' name='checkbox[]' value='pet-friendly'> Pet Friendly<br><br>

        <label>Work Address (ie. 10900 Euclid Ave, Cleveland, OH 44106): </label> <input type='text' name='work'><br><br>

        <input type='submit' class='btn btn-primary' name='submit' value='Submit'>
        </form>

        <?php
                $pythonCmd = "python main.py";
                if (!empty($_POST["city"]) && !empty($_POST["state"])) {
                    $city = str_replace(" ","-", $_POST['city']);
                    $state = $_POST['state'];
                    if(!empty($_POST['price'])){
                       $price = $_POST['price'];
                       $pythonCmd .= " -price under-$price";
                    }
                    $beds = $_POST['beds'];
                    $bathrooms = $_POST['bathrooms'];
                    $features = "";
                    if(!empty($_POST['checkbox'])){
                        foreach($_POST['checkbox'] as $amenities){
                            $features .= "-$amenities";
                        }
                        $features = substr($features, 1);
                        $pythonCmd .= " -features $features";
                    }
                    if(!empty($_POST['work'])){
                       $work = $_POST['work'];
                       $pythonCmd .= " -work '$work'";
                    }
                    $pythonCmd .= " -city $city -state $state -beds $beds -bathrooms $bathrooms";
                    $output = shell_exec($pythonCmd);
                    echo "Your spreadsheet is ready to view at: $output";
                }

        ?>
        </div>
        </div>
    </div>
</body>