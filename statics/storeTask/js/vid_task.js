const constraints = { "video": { width: { max: 320 } }, "audio": true };

var theStream;
var theRecorder;
var recordedChunks = [];

function startFunction() {
    navigator.mediaDevices.getUserMedia(constraints)
        .then(gotMedia)
        .catch(e => { console.error('getUserMedia() failed: ' + e); });
}

function gotMedia(stream) {
    theStream = stream;
    var video = document.querySelector('video');
    video.srcObject = stream;
    try {
        recorder = new MediaRecorder(stream, { mimeType: "video/webm" });


    } catch (e) {
        console.error('Exception while creating MediaRecorder: ' + e);
        return;
    }

    theRecorder = recorder;
    recorder.ondataavailable =
        (event) => { recordedChunks.push(event.data); };
    recorder.start(100);
}

// From @samdutton's "Record Audio and Video with MediaRecorder"
// https://developers.google.com/web/updates/2016/01/mediarecorder
function download() {
    theRecorder.stop();
    theStream.getTracks().forEach(track => { track.stop(); });
    var blob = new Blob(recordedChunks, { type: "video/webm" });
    var url = URL.createObjectURL(blob);
    var reader = new window.FileReader();
    reader.readAsDataURL(blob);
    reader.onloadend = function () {
        document.getElementById('data_vid').value = reader.result;
    }
    setTimeout(function () { URL.revokeObjectURL(url); }, 100);
}

