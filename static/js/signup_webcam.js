$(document).ready(function(){
  var canvas = $('#webcam-canvas').first()[0];
  var profile_image = $('#webcam-photo').first()[0];
  var ctx = canvas.getContext('2d');
  var video = document.querySelector('video');

  navigator.getUserMedia  = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;


  if (navigator.getUserMedia){
    // set up the video -> canvas
    navigator.getUserMedia({video: true, audio: false},
      // success
      function(stream) {
        video.srcObject = stream;
      },
      // failure
      function(){
        console.log("Media failed. Probably denied webcam")
        $("#webcam-canvas").hide();
        $("#webcam-vid-error").html("Could not access your webcam")
      }
    );
    // set up canvas by drawing font on it
    ctx.font = "15px Calibri"
    ctx.fillText("Click on preview ", canvas.width/2, canvas.height/2 - 8)
    ctx.fillText("to take snapshot", canvas.width/2, canvas.height/2  + 8)
    // listener on the video element
    video.addEventListener("click", function(){
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    });
  }
  else{
    $("#webcam-vid-error").html("Your brower does not support webcam for profile pics :(");
  }
});
