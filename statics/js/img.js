
let camera_button = document.querySelector("#start-camera");
let video = document.querySelector("#video");
let click_button = document.querySelector("#click-photo");
let canvas = document.querySelector("#canvas");

camera_button.addEventListener('click', async function () {
    let stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
    video.srcObject = stream;
    click_button.hidden = false;
    camera_button.hidden = true;
});

click_button.addEventListener('click', async function () {
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    let image_data_url = canvas.toDataURL('image/jpeg');

    document.getElementById("imageData").value = image_data_url;
    document.getElementById('imgFile').style.display = 'none';
});

function previewFile(input) {
    var file = $("input[type=file]").get(0).files[0];
    if (file) {
        var reader = new FileReader();
        reader.onload = function () {
            $("#previewImg").attr("src", reader.result);
        }
        reader.readAsDataURL(file);
    }
    // other side

}



function inputfile() {
    document.getElementById('imgFile').style.display = 'none';
    document.getElementById('previewImg').hidden = false;
    document.getElementById('canvas').hidden = true;
    document.getElementById("imageData").value = "";
}
