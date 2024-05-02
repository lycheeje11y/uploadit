function submitForm() {
    let frm = document.getElementsByName('download_form')[0];
    frm.submit();
    frm.reset();  
    return false;
}
function copy(element) {
    var text = document.getElementById(element);
    var copyText = document.getElementById(element).outerHTML;
    var textbox = document.getElementById('html');
    textbox.value = copyText;
    var button = document.getElementById("Button");
    textbox.select();
    document.execCommand("Copy");
    alert("Copied the text: " + text.value + " HTML code!");
    button.innerHTML = "Copied!";
}