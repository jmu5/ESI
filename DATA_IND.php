<?php
    
    date_default_timezone_set("Europe/Helsinki");
    $startTime=date("Y-m-d h:i:sa");
    echo 'Starting... ';

    require 'vendor/autoload.php';
    use \PhpOffice\PhpSpreadsheet\IOFactory;

    $db = new SQLite3('../ESI.db');
    if(!$db){
	    echo $db->lastErrorMsg();
    }else{
	    echo ' Opened database successfully! ';
    }

    $handle = fopen("date.txt", "r");
    if ($handle) {
        while (($line = fgets($handle)) !== false) {
            $data = explode(";", $line);
            $newdate=$data[0];
            $newrow=$data[1];
        }
    }

    fclose($handle);



    $inputFileType='Xlsx';
    $inputFileName='data/industry_subsectors_sa_m_nace2.xlsx';
    $reader=\PhpOffice\PhpSpreadsheet\IOFactory::createReader($inputFileType);
    $spreadsheet=$reader->load($inputFileName);

    $sheetCount=$spreadsheet->getSheetCount();

    $countries=array(
	    1=>'EU',
	    2=>'EA',
	    3=>'BE',
	    4=>'BG',
	    5=>'CZ',
	    6=>'DK',
	    7=>'DE',
	    8=>'EE',
	    9=>'IE',
	    10=>'EL',
	    11=>'ES',
	    12=>'FR',
	    13=>'HR',
	    14=>'IT',
	    15=>'CY',
	    16=>'LV',
	    17=>'LT',
	    18=>'LU',
	    19=>'HU',
	    20=>'MT',
	    21=>'NL',
	    22=>'AT',
	    23=>'PL',
	    24=>'PT',
	    25=>'RO',
	    26=>'SI',
	    27=>'SK',
	    28=>'FI',
	    29=>'SE',
	    30=>'UK',
	    31=>'ME',
	    32=>'MK',
	    33=>'AL',
	    34=>'RS',
	    35=>'TR');

    $subsectors=array(
	    1=>10,
	    2=>11,
	    3=>12,
	    4=>13,
	    5=>14,
	    6=>15,
	    7=>16,
	    8=>17,
	    9=>18,
	    10=>19,
	    11=>20,
	    12=>21,
            13=>22,
            14=>23,
            15=>24,
            16=>25,
            17=>26,
            18=>27,
            19=>28,
            20=>29,
            21=>30,
            22=>31,
	    23=>32,
	    24=>33);

    $monthDay=array(
	    1=>'-01-01',
    	    2=>'-02-01',
	    3=>'-03-01',
	    4=>'-04-01',
	    5=>'-05-01',
	    6=>'-06-01',
	    7=>'-07-01',
	    8=>'-08-01',
	    9=>'-09-01',
	    10=>'-10-01',
	    11=>'-11-01',
	    12=>'-12-01');

    $questions=array(
	    0=>'cof',
	    1=>'Q1',
	    2=>'Q2',
	    3=>'Q3',
	    4=>'Q4',
            5=>'Q5',
            6=>'Q6',
            7=>'Q7');

    $found=false;
    $query="";
    $values=""; 

    for($i=2;$i<=25;$i++){   //2-25
	    
	    $sheet=$spreadsheet->getSheet($i);
            $highestRow=$sheet->getHighestDataRow();
	    $highestColumn=$sheet->getHighestDataColumn();

	    $subsector=$subsectors[($i-1)];
	    echo ' '.$subsector.' ';
	    $year=1985;
	    $month=1;

            for($row=$newrow;$row<=$newrow;$row++){
		    $country=0;
		    $date=$newdate; //$year.$monthDay[$month];
		    //echo ' '.$date.' ';
		    for($col=2;$col<=281;$col++){   //2-281
                           
			    if(($col-2)%8==0){
				    $found=false;
				    $country=$country+1;
				    //$cntr=$countries[$country];
				    $query="INSERT INTO INDUSTRIAL (date, country, subsector";
                                    $values=" ) VALUES ('$date', '$countries[$country]', $subsector";		
		            }
			    if(is_numeric($sheet->getCell([$col, $row])->getValue())){
				    $found=true;
				    $query=$query.", ".$questions[(($col-2)%8)];
				    $values=$values.", ".$sheet->getCell([($col), $row])->getValue();
		            }
			    if(($col-2)%8==7){
			            $query=$query." ";
			            $values=$values.") ";
			            $sql=$query.$values;

				    if($found){
					    //echo $sql;
					    $db->exec($sql);
			            }
			    }	   
		      }
	    $country=0;
	    $month++;
	    if($month==13){
	        $year++;
	        $month=1;
	    }
	    }
    }

    $db->close();
    $endTime=date("Y-m-d h:i:sa");
    echo 'Start time: '.$startTime.', end time: '.$endTime;
?>
