{% load static %}
//  Sequence of Blocks (does not include fear vs surprise as this is always last) [AM]
var sequence1 = [1,2,4,3];
var sequence2 = [2,3,1,4];
var sequence3 = [3,4,2,1];
var sequence4 = [4,1,3,2];

// Sequence of Videos in a specific block
var sequencea = [1,2,20,3,19,4,18,5,17,6,16,7,15,8,14,9,13,10,12,11];
var sequenceb = [2,3,1,4,20,5,19,6,18,7,17,8,16,9,15,10,14,11,13,12];
var sequencec = [3,4,2,5,1,6,20,7,19,8,18,9,17,10,16,11,15,12,14,13];
var sequenced = [4,5,3,6,2,7,1,8,20,9,19,10,18,11,17,12,16,13,15,14];
var sequencee = [5,6,4,7,3,8,2,9,1,10,20,11,19,12,18,13,17,14,16,15];
var sequencef = [6,7,5,8,4,9,3,10,2,11,1,12,20,13,19,14,18,15,17,16];
var sequenceg = [7,8,6,9,5,10,4,11,3,12,2,13,1,14,20,15,19,16,18,17];
var sequenceh = [8,9,7,10,6,11,5,12,4,13,3,14,2,15,1,16,20,17,19,18];
var sequencei = [9,10,8,11,7,12,6,13,5,14,4,15,3,16,2,17,1,18,20,19];
var sequencej = [10,11,9,12,8,13,7,14,6,15,5,16,4,17,3,18,2,19,1,20];
var sequencek = [11,12,10,13,9,14,8,15,7,16,6,17,5,18,4,19,3,20,2,1];
var sequencel = [12,13,11,14,10,15,9,16,8,17,7,18,6,19,5,20,4,1,3,2];
var sequencem = [13,14,12,15,11,16,10,17,9,18,8,19,7,20,6,1,5,2,4,3];
var sequencen = [14,15,13,16,12,17,11,18,10,19,9,20,8,1,7,2,6,3,5,4];
var sequenceo = [15,16,14,17,13,18,12,19,11,20,10,1,9,2,8,3,7,4,6,5];
var sequencep = [16,17,15,18,14,19,13,20,12,1,11,2,10,3,9,4,8,5,7,6];
var sequenceq = [17,18,16,19,15,20,14,1,13,2,12,3,11,4,10,5,9,6,8,7];
var sequencer = [18,19,17,20,16,1,15,2,14,3,13,4,12,5,11,6,10,7,9,8];
var sequences = [19,20,18,1,17,2,16,3,15,4,14,5,13,6,12,7,11,8,10,9];
var sequencet = [20,1,19,2,18,3,17,4,16,5,15,6,14,7,13,8,12,9,11,10];

// Aaron started here

var block_id;
var trial_id;
var block_id_seq;
var trial_id_seq;

// Get the block sequence from file if just starting the experiment, otherwise get from local storage
if (localStorage.getItem("block_id") == undefined) {
  var read_block = new XMLHttpRequest();
  read_block.open('GET', "/block_condition.txt", false);
  read_block.send();
  
  block_id = read_block.responseText;
  block_id = block_id.trim();
  localStorage.setItem("block_id", block_id);
  block_id_seq = eval(block_id);
} else {
  block_id = localStorage.getItem("block_id");
  block_id_seq = eval(block_id);
}

// Get the block sequence from file if just starting the experiment, otherwise get from local storage
if (localStorage.getItem("trial_id") == undefined) {
  var read_trial = new XMLHttpRequest();
  read_trial.open('GET', "/latin_condition.txt", false);
  read_trial.send();
  
  trial_id = read_trial.responseText;
  trial_id = trial_id.trim();
  localStorage.setItem("trial_id", trial_id);
  trial_id_seq = eval(trial_id);
} else {
  trial_id = localStorage.getItem("trial_id");
  trial_id_seq = eval(trial_id);
}

// end Aaron here

// Work out what page needs to be shown next.
// Heavily modified by Aaron tagged with [AM].
function js_direction(block, current_page_index) {
//  20 latin sequences were used
//  If you want to change the testing sequence, simply change the letter in line below
  var seq;
  var next_page_index;
  var next_page;

  // Start Aaron here
  var block_seq = block_id_seq;
  var block_index;

  // Determine which block is in progress
  // Start first block if no block given.
  if (block == null) {
    block = block_seq[0];
    block_index = 0;
  } else if (block == 5) {
    block_index = 4;
  } else {
    for (i = 0; i < 4; i++) {
      if (block == block_seq[i]) {
        block_index = i;
        break;
      }
    }
  }

  // Shift to the correct trial sequence for the current block
  // Handles looping from last to first sequence.
  if (block_index != 0) {
    var char = trial_id.substr(trial_id.length - 1);
    var next_char;
    var last_char = "t"; 

    if (char.charCodeAt(0) + block_index > last_char.charCodeAt(0)) {
      next_char = String.fromCharCode(char.charCodeAt(0) + block_index - 20);
    } else {
      next_char = String.fromCharCode(char.charCodeAt(0) + block_index);
    }

    
    var new_seq = trial_id.substring(0, trial_id.length-1);
    new_seq = new_seq.concat(next_char);
    trial_id_seq = eval(new_seq);
  }

  // end Aaron here

  seq = trial_id_seq; // [AM]

  //first page [Modified by AM to handle blocks]
  if (current_page_index == 4) {
    next_page =  seq[0] + 4 + (20 * (block - 1));
    displayNextPage(block, next_page);
  } else if (current_page_index == 0.5) { //after the break, go to the 10th index [Modified by AM to handle blocks]
    next_page =  seq[10] + 4  + (20 * (block - 1));
    displayNextPage(block, next_page);
  } else {
    //loop over the sequence until find the current page index [Modified by AM to handle blocks]
      for (i = 0; i < 20; i++) {
        if ((current_page_index - seq[i]) == 4 + (20 * (block - 1))) {
          next_page_index = i + 1;
          next_page = seq[next_page_index] + 4  + (20 * (block - 1));
          
          break;
        }
      }


      // Aaron start here
      // If halfway through a block show the block's mid-way break page.
      if (next_page_index == 10) {
        switch (block) {
          case 1:
            window.location = "/BreakA.html"
            break;
          case 2:
            window.location = "/BreakS.html"
            break;
          case 3:
            window.location = "/BreakF.html"
            break;
          case 4:
            window.location = "/BreakH.html"
            break;
          case 5:
            window.location = "/BreakFS.html"
            break;
          default:
            console.error("No valid block for determining break page");
            break;
        }

        // Aaron end here
        
        // Move to experiment part 2 if at the end of the last block in part 1 [Modified by AM to handle blocks]
      } else if (next_page_index == 20 && block_index == 3) {
        window.location = "/Intropart2.html"
        
        // Show the end emotional questionaire if finished with part 2 [Modified by AM to handle blocks]
      } else if (next_page_index == 20 && block_index == 4) {
        window.location = "/ERQ.html"
        // Move to the block end break page and determine next block if not on the last block [Modified by AM to handle blocks]
      } else if (next_page_index == 20 && block_index != 3) {
        
        block_index++;
        block = block_id_seq[block_index];
        switch (block) {
          case 1:
            window.location = "/BlockEndA.html"
            break;
          case 2:
            window.location = "/BlockEndS.html"
            break;
          case 3:
            window.location = "/BlockEndF.html"
            break;
          case 4:
            window.location = "/BlockEndH.html"
            break;
          default:
            console.error("No valid block for determining break page");
            break;
        }
        
        
      } else {//deal with the rest normal pages [Modified by AM to handle blocks]
          displayNextPage(block, next_page);
      }
  }
}

// Display the next page [Modified by AM to handle blocks and pages >= 100]
function displayNextPage(block, next_page) {
  var current_block;
  switch (block) {
    case 1:
      current_block = "anger";
      break;
    case 2:
      current_block = "surprise";
      break;
    case 3:
      current_block = "fear";
      break;
    case 4:
      current_block = "happiness";
      break;
    case 5:
      current_block = "fs_compare";
      break;
    default:
      console.error("Did not find a valid block sequence");
  }
    if (next_page < 10) {
      window.location = "/"+current_block+"/p00"+next_page+".html";
    } else if (next_page < 100){
      window.location = "/"+current_block+"/p0"+next_page+".html";
    } else {
      window.location = "/"+current_block+"/p"+next_page+".html";
    }
}

// Transition between breakpoints (breaks, start of block, end of block, etc)
// [Modified by AM to handle blocks and to log to participant-specific files]
function breakpoint(block, page, indicator) {
  // Use block id and sequence id to make log file
  var id = "&id="+block_id+trial_id;
  var data = 'data='+indicator+",";
  data = data+id;
  console.log(data);
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("POST","/learn/static/learn/writetotxt.php",true);
  //Must add this request header to XMLHttpRequest request for POST
  xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xmlhttp.send(data);

  js_direction(block, page);
}


// Save participant answers to log file [Modified by AM to handle blocks and to log to participant-specific files]
function save(block, page) {
  // get the input
  var response=document.getElementById("response");
  var id = "&id="+block_id+trial_id;

  if (document.querySelector('input[name = "Option"]:checked') == null
  || document.querySelector('input[name = "Unknown/Known"]:checked') == null) {
    alert("Please answer all the questions");
  } else {
    var option = document.querySelector('input[name = "Option"]:checked').value
    var unknownKnown = document.querySelector('input[name = "Unknown/Known"]:checked').value

    var data = 'data='+option+","+unknownKnown+","+",";
    data = data+id;
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST","/learn/static/learn/writetotxt.php",true);
    //Must add this request header to XMLHttpRequest request for POST
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send(data);

    js_direction(block, page);
  }
}

// Save extended participant answers to log file [Modified by AM to handle blocks and to log to participant-specific files]
function extrasave(block, page) {
  // get the input
  var response=document.getElementById("response");
  var id = "&id="+block_id+trial_id;

  if (document.querySelector('input[name = "Option"]:checked') == null
  || document.querySelector('input[name = "Unknown/Known"]:checked') == null
  || document.querySelector('input[name = "Biased"]:checked') == null) {
    alert("Please answer all the questions");
  } else {
    var option = document.querySelector('input[name = "Option"]:checked').value
    var unknownKnown = document.querySelector('input[name = "Unknown/Known"]:checked').value
    var biased = document.querySelector('input[name = "Biased"]:checked').value

    var data = 'data='+option+","+unknownKnown+","+biased+",";
    data = data+id;
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST","/learn/static/learn/writetotxt.php",true);
    //Must add this request header to XMLHttpRequest request for POST
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send(data);

    js_direction(block, page);
  }
}

// Aaron start here

// Update the file with the latin sequence for the next participant
function nextsequence() {
  var char = trial_id.substr(trial_id.length - 1);
  var next_char;
  var last_char = "t"; 
  var jump_char = "p";
  var jump_block_char = "3";
  if (char.charCodeAt(0) == last_char.charCodeAt(0) && block_id.substr(block_id.length - 1).charCodeAt(0) == jump_block_char.charCodeAt(0)) {
    next_char = "a";
  } else if (block_id.substr(block_id.length - 1).charCodeAt(0) == jump_block_char.charCodeAt(0) && char.charCodeAt(0) >= jump_char.charCodeAt(0)) {
    if (char.charCodeAt(0) + 6 > last_char.charCodeAt(0)) {
      next_char = String.fromCharCode(char.charCodeAt(0) +  6 - 20);
    } else {
      next_char = String.fromCharCode(char.charCodeAt(0) + 6);
    }  
  }
   else {
    // Determine which sequence letter is needed (loop from end to start)
    if (char.charCodeAt(0) + 5 > last_char.charCodeAt(0)) {
    next_char = String.fromCharCode(char.charCodeAt(0) + 5 - 20);
    } else {
    next_char = String.fromCharCode(char.charCodeAt(0) + 5);
    }
  }
  
  
  
  var data = "data=" + trial_id.substring(0, trial_id.length-1);
  data = data.concat(next_char);
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("POST","/updatetrialseq.php",true);
  //Must add this request header to XMLHttpRequest request for POST
  xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xmlhttp.send(data);
}

// Update the file with the block sequence for the next participant
function nextblock() {
  var char = block_id.substr(block_id.length - 1);
  var next_char;
  var last_char = "4";
  var jump_char = "p"; 
  if (trial_id.substr(trial_id.length - 1).charCodeAt(0) >= jump_char.charCodeAt(0)) {
    if (char.charCodeAt(0) + 2 > last_char.charCodeAt(0)) {
      next_char = String.fromCharCode(char.charCodeAt(0) + 2 - 4);
    } else {
      next_char = String.fromCharCode(char.charCodeAt(0) + 2);
    }
  } else {
    if (char.charCodeAt(0) + 1 > last_char.charCodeAt(0)) {
      next_char = String.fromCharCode(char.charCodeAt(0) + 1 - 4);
    } else {
      next_char = String.fromCharCode(char.charCodeAt(0) + 1);
    }
  }
  
  
  var data = "data=" + block_id.substring(0, block_id.length-1);
  data = data.concat(next_char);
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("POST","/updateblockseq.php",true);
  //Must add this request header to XMLHttpRequest request for POST
  xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xmlhttp.send(data);
}

// Save participant information to their log file [replaces previous code in the p003.html file]
function saveinfo() {
  nextsequence();
  nextblock();
  // get the input
  var id = "&id="+block_id+trial_id;

  if (document.querySelector('input[name = "Age"]').value == null
  || document.querySelector('input[name = "Gender"]:checked') == null
  || document.querySelector('input[name = "GlassesContacts"]:checked') == null) {
    alert("Please answer all the questions");
  } else {
    var age = document.querySelector('input[name = "Age"]').value;
    var gender = document.querySelector('input[name = "Gender"]:checked').value;
    var glassescontacts = document.querySelector('input[name = "GlassesContacts"]:checked').value;

    var data = 'data='+age+","+gender+","+glassescontacts+",";
    data = data+id;
    console.log(data);
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST","/p003.php",true);
    //Must add this request header to XMLHttpRequest request for POST
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send(data);

    window.location = "/p004.html";
  }
}

// Save participant ERQ information to their log file [replaces previous code in the ERQ.html file]
function saveERQ() {
  // get the input
  var id = "&id="+block_id+trial_id;

  if (document.querySelector('input[name = "Item1"]:checked') == null
  || document.querySelector('input[name = "Item2"]:checked') == null
  || document.querySelector('input[name = "Item3"]:checked') == null
  || document.querySelector('input[name = "Item4"]:checked') == null
  || document.querySelector('input[name = "Item5"]:checked') == null
  || document.querySelector('input[name = "Item6"]:checked') == null
  || document.querySelector('input[name = "Item7"]:checked') == null
  || document.querySelector('input[name = "Item8"]:checked') == null
  || document.querySelector('input[name = "Item9"]:checked') == null
  || document.querySelector('input[name = "Item10"]:checked') == null) {
    alert("Please answer all the questions");
  } else {
    var item1 = document.querySelector('input[name = "Item1"]:checked').value;
    var item2 = document.querySelector('input[name = "Item2"]:checked').value;
    var item3 = document.querySelector('input[name = "Item3"]:checked').value;
    var item4 = document.querySelector('input[name = "Item4"]:checked').value;
    var item5 = document.querySelector('input[name = "Item5"]:checked').value;
    var item6 = document.querySelector('input[name = "Item6"]:checked').value;
    var item7 = document.querySelector('input[name = "Item7"]:checked').value;
    var item8 = document.querySelector('input[name = "Item8"]:checked').value;
    var item9 = document.querySelector('input[name = "Item9"]:checked').value;
    var item10 = document.querySelector('input[name = "Item10"]:checked').value;

    var data = 'data='+item1+","+item2+","+item3+","+item4+","+item5+","+item6+","
                +item7+","+item8+","+item9+","+item10+",";
    data = data+id;
    console.log(data);
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST","/ERQ.php",true);
    //Must add this request header to XMLHttpRequest request for POST
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send(data);

    window.location = "/Feedback.html";
  }
}

// Save participant language/ethnicity information to their log file [replaces previous code in the Feedback.html file]
function savefeedback() {
  // get the input
  var id = "&id="+block_id+trial_id;

  if (document.querySelector('input[name = "Ethnicity"]:checked') == null
  || document.querySelector('input[name = "Language"]:checked') == null
  || (document.querySelector('input[name = "Ethnicity"]:checked').value == "Other" &&
      document.querySelector('input[name = "OtherEthnicity"]').textContent == null)
  || (document.querySelector('input[name = "Language"]:checked').value == "Other" &&
      document.querySelector('input[name = "OtherLanguage"]').textContent == null)) {
    alert("Please answer all the questions");
  } else {
    var ethnicity = document.querySelector('input[name = "Ethnicity"]:checked').value;
    var otherethnicity = document.querySelector('input[name = "OtherEthnicity"]').value;
    var language = document.querySelector('input[name = "Language"]:checked').value;
    var otherlanguage = document.querySelector('input[name = "OtherLanguage"]').value;

    var data = 'data='+ethnicity+","+otherethnicity+","+language+","+otherlanguage+",";
    data = data+id;
    console.log(data);
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST","/Feedback.php",true);
    //Must add this request header to XMLHttpRequest request for POST
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send(data);

    window.location = "/Conclusion.html";
  }
}

// Save participant answers to their log file [replaces previous code in the p0xx.html files]
function savevideo(data) {
  var id = "&id="+block_id+trial_id;
  data = data+id;
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("POST","/learn/static/learn/writetotxt.php",true);
  //Must add this request header to XMLHttpRequest request for POST
  xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xmlhttp.send(data);
}

// Aaron end here
