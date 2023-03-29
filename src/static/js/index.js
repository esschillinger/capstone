var native = document.getElementById('native_language');
var target = document.getElementById('target_language');

$("#languages :input").change(function() {
    if (native.value != "" && target.value != "") {
        document.getElementById('submit').disabled = false;
    }
});