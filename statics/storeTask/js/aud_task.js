
let recorder = null;

function startRecord() {
    const onsuccess = (stream) => {
        recorder = new MediaRecorder(stream, {
            type: 'audio/ogg; codecs=opus'
        });

        recorder.start(); // Starting the record

        recorder.ondataavailable = (e) => {
            // Converting audio blob to base64
            let reader = new FileReader()
            reader.onloadend = () => {

                // alert(reader.result);
                document.getElementById('data_aud').value = reader.result;
                document.getElementById('record').src = reader.result;
                // You can upload the base64 to server here.
            }
            reader.readAsDataURL(e.data);
        }

        document.getElementById('stop').hidden = false;
        document.getElementById('start').hidden = true;
    }

    navigator.getUserMedia = (
        navigator.getUserMedia ||
        navigator.webkitGetUserMedia ||
        navigator.mozGetUserMedia ||
        navigator.msGetUserMedia
    );

    navigator.getUserMedia({
        audio: true
    }, onsuccess, (e) => {
        console.log(e);
    });
}
function stopRecord() {
    recorder.stop();
}

