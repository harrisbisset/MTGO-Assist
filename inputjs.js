function displayMTGOinput(ID) {
    var linkdiv = document.getElementById("MTGOinputDiv");
    var yes = document.getElementById("Yes");
    var no = document.getElementById("No");
    console.log(ID.id);
    console.log(linkdiv.style.display);

    if (ID.id === "btnYes" && linkdiv.style.display === "none") {
        linkdiv.style.display = "Block";
        yes.required = true;
        no.required = true;
    } else if (ID.id === "btnNo" && linkdiv.style.display === "block") {
        linkdiv.style.display = "None";
        yes.removeAttribute('required');
        no.removeAttribute('required');
    }
}