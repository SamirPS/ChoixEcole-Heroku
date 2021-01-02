(function() {
  if('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/sw.js')
               .then(function(registration) {
               console.log('Service Worker Registered');
               return registration;
      })
      .catch(function(err) {
        console.error('Unable to register service worker.', err);
      });
      navigator.serviceWorker.ready.then(function(registration) {
        console.log('Service Worker Ready');
      });
    });
  }
})();

let deferredPrompt;
const btnAdd = document.getElementById('installButton');

if (window.matchMedia('(display-mode: fullscreen)').matches) {
  btnAdd.style.visibility = 'hidden';
}

window.addEventListener('beforeinstallprompt', (e) => {
  console.log('beforeinstallprompt event fired');
  e.preventDefault();
  deferredPrompt = e;
  if (window.matchMedia('(display-mode: fullscreen)').matches) {
  if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)){
  btnAdd.style.visibility = 'visible';
}else{
  btnAdd.style.visibility = 'hidden';
}
  }else{
    btnAdd.style.visibility = 'visible';
  }
});

btnAdd.addEventListener('click', (e) => {
  btnAdd.style.visibility = 'hidden';
  if (deferredPrompt) {
  deferredPrompt.prompt();
  deferredPrompt.userChoice
    .then((choiceResult) => {
      if (choiceResult.outcome === 'accepted') {
        console.log('User accepted the A2HS prompt');
      } else {
        console.log('User dismissed the A2HS prompt');
      }
      deferredPrompt = null;
    });
  }
});

window.addEventListener('appinstalled', (evt) => {
  app.logEvent('app', 'installed');
});
