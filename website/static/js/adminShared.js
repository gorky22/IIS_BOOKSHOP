function testEmail(value){
    if(value == ""){
        return true
    }
    var res = true
    if(value.length < 7){
        res = false;
    } else if(!value.includes("@")){
        res = false;
    } else if(!value.includes(".")){
        res = false;
    }
    
    if(res == true) {
        return res
    } else {
        Toast.show('Email nie je platný','E')
        return res
    }
}


// Funkcia na vypisanie datumu v krajsie forme
function beautifulDate(input_date) {
    var date = new Date(input_date)
    var year = date.getFullYear()
    var month = date.getMonth()
    var day = date.getDate()
    var birth_date = year + '-' + month + '-' + day

    return birth_date
}



function test_hours(hours){
    if(hours >= 0 && hours <= 24){
        return true;
    } else {
      return false
    }
}


function test_minutes(minutes){
    if(minutes >= 0 && minutes <= 60){
        return true;
    } else {
      return false
    }
}


function test_time(time){
    
    if(time.split("-").length !== 2) {
      return false
    }
    var tmp = time.split("-")
  
    if(tmp[0].split(":").length !== 2) {
      return false
    } else if (tmp[1].split(":").length !== 2){
      return false
    }
  
    var first = tmp[0].split(":")
    var second = tmp[1].split(":")
  
    if(!test_hours(first[0]) || !test_hours(second[0]) || !test_minutes(first[1]) || !test_minutes(second[1])){
      return false
    } else {
      return true
    }
   
}

function checkTime(time, add){
    if(time == "" && add == 0){
        return true
    }
    if(test_time(time) == false){
        Toast.show('Zadaj čas v tvare hh:mm','E')
        return false
    } 

    return true
}

