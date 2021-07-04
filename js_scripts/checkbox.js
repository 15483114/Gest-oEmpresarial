function displayRadioValue() {
    var ele = document.getElementsByName('inlineRadioOptions');
      
    for(i = 0; i < ele.length; i++) {
        if(ele[i].checked) {
            var str = "Choosen button was: " + ele[i].value;
            document.getElementById("result").innerHTML = str;
            alert(str);
        }
    }
}