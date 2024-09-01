const videoElement = document.getElementById('videoElement');
const canvasElement = document.getElementById('canvasElement');
const photoElement = document.getElementById('photoElement');
const startButton = document.getElementById('startButton');
const captureButton = document.getElementById('captureButton');

const ShowBase64 = document.getElementById('data_img');

let stream;

async function startWebcam() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        videoElement.srcObject = stream;
        startButton.disabled = true;
        captureButton.disabled = false;
    } catch (error) {
        console.error('Error accessing webcam:', error);
    }
}
startButton.addEventListener('click', startWebcam);

function capturePhoto() {
    canvasElement.width = videoElement.videoWidth;
    canvasElement.height = videoElement.videoHeight;
    canvasElement.getContext('2d').drawImage(videoElement, 0, 0);
    const photoDataUrl = canvasElement.toDataURL('image/jpeg');
    photoElement.src = photoDataUrl;
    photoElement.style.display = 'block'; 
    ShowBase64.value = photoDataUrl;
    const video = document.querySelector('video');
 
    const mediaStream = video.srcObject; 
    const tracks = mediaStream.getTracks(); 
    tracks[0].stop(); 
    tracks.forEach(track => track.stop())
}

captureButton.addEventListener('click', capturePhoto);