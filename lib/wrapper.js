/**
 * Singularity Shuttle — shared responsive scaler.
 *
 * Each page calls fitStage(stageW, stageH) once after CreateJS init.
 * The stage is wrapped in #stageInner; we proportionally shrink to fit
 * the viewport width without ever upscaling above 1×.
 */
function fitStage(stageW, stageH) {
  var inner = document.getElementById("stageInner");
  if (!inner) return;
  function resize() {
    var vw = window.innerWidth;
    var scale = Math.min(1, vw / stageW);
    inner.style.transform = "scale(" + scale + ")";
    inner.style.height = (stageH * scale) + "px";
  }
  window.addEventListener("resize", resize);
  resize();
}

/**
 * Mobile autoplay gate. Browsers block audio until a user gesture.
 * Show a fullscreen "tap to begin" overlay; on tap, resume the audio
 * context and call the supplied start callback (Animate's init/play).
 */
function mountAudioGate(onStart) {
  var gate = document.createElement("div");
  gate.id = "audioGate";
  gate.innerHTML =
    '<div class="audioGateInner">' +
      '<div class="audioGateTitle">Singularity Shuttle</div>' +
      '<div class="audioGateHint">Tap to begin</div>' +
    '</div>';
  document.body.appendChild(gate);

  function start() {
    gate.removeEventListener("click", start);
    gate.removeEventListener("touchend", start);
    if (window.createjs && createjs.Sound && createjs.Sound.context && createjs.Sound.context.resume) {
      try { createjs.Sound.context.resume(); } catch (e) { /* ignore */ }
    }
    gate.style.opacity = "0";
    setTimeout(function () { gate.parentNode && gate.parentNode.removeChild(gate); }, 250);
    if (typeof onStart === "function") onStart();
  }
  gate.addEventListener("click", start);
  gate.addEventListener("touchend", start);
}
