function matchPass() {

    document.getElementById("msg").style.marginBottom = "5px";
    document.getElementById("msg").style.fontSize = "12px";
    let pas = document.getElementById("pass").value;
    let repas = document.getElementById("conf_pass").value;
    // console.log(pas);
    // console.log(repas);
    let pt = "Please enter same password";
    if (pas === repas) {
        pt = "password matched";
        pt = pt.fontcolor("green");

    }
    else {
        pt = pt.fontcolor("red");
        document.getElementById("conf_pass").value = "";
        document.getElementById("conf_pass").focus();
    }
    document.getElementById("msg").innerHTML = pt;

}

function checkMobileNum() {
    document.getElementById("cel_validator").style.marginBottom = "5px";
    document.getElementById("cel_validator").style.fontSize = "12px";
    document.getElementById("cel_validator").style.color = "red";
    var val = document.getElementById("mobNum").value;

    // if (!(/^[6-9]\d{9}$/.test(val)))
    if (/^[6-9]/.test(val)) {
        if (!(/^\d{10}$/.test(val))) {
            document.getElementById("cel_validator").innerHTML = "Invalid number, must be ten digits";
            document.getElementById("mobNum").value = "";
            document.getElementById("mobNum").focus();
        }
        else {
            document.getElementById("cel_validator").innerHTML = "";
        }

    }
    else {
        document.getElementById("cel_validator").innerHTML = "Invalid number, number must start from 6,7,8 or 9";
        document.getElementById("mobNum").value = "";
        document.getElementById("mobNum").focus();
    }


}