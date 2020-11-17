var socket = io();

var canvas = document.getElementById("preview");
var context = canvas.getContext('2d');
var label1 = document.getElementById('prediction');
var video = document.getElementById("testvideo");

socket.on('connect', function () {
    socket.emit('my event', { data: 'I\'m connected!' });
});

socket.on('predresult', (msg) => {
    label1.innerHTML = msg;
    console.log(msg)
});

function startrec() {
    var handleSuccess = function (stream) {
        video.srcObject = stream;
        // video.src = URL.createObjectURL(stream);
        setInterval(() => {
            capturepic();
        }, 1500);
    };

    navigator.mediaDevices.getUserMedia({ audio: false, video: true })
        .then(handleSuccess)
}

function capturepic() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.width = canvas.width;
    context.height = canvas.height;
    context.drawImage(video, 0, 0, context.width, context.height);
    var dataURL = canvas.toDataURL('image/jpeg', 1);
    socket.emit('imgdata', dataURL);
}
