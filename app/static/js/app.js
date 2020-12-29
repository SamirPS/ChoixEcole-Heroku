if ('serviceWorker' in navigator) {
  navigator.serviceWorker
  .register('/sw.js')
  .then(function(registration) {
      console.log('Service Worker Registered!');
      return registration;
  })
  .catch(function(err) {
      console.error('Unable to register service worker.', err);
  });
}

const CACHE_NAME = 'static-cache';

const FILES_TO_CACHE = [];

self.addEventListener('install', (evt) => {
  console.log('[ServiceWorker] Install');
  evt.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[ServiceWorker] Pre-caching offline page');
      return cache.addAll(FILES_TO_CACHE);
    })
  );

  self.skipWaiting();
});

self.addEventListener('activate', (evt) => {
  console.log('[ServiceWorker] Activate');
  evt.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(keyList.map((key) => {
        if (key !== CACHE_NAME) {
          console.log('[ServiceWorker] Removing old cache', key);
          return caches.delete(key);
        }
      }));
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', function(event) {
  event.respondWith(fetch(event.request));
});


self.addEventListener('fetch', function(event) {
  event.respondWith(
    fetch(event.request).catch(function() {
      return caches.match(event.request);
    })
  );
});

let deferredInstallPrompt = null;
const installButton = document.getElementById('installButton');
installButton.addEventListener('click', installPWA);

window.addEventListener('beforeinstallprompt', saveBeforeInstallPromptEvent);

function saveBeforeInstallPromptEvent(evt) {
  deferredInstallPrompt = evt;
  installButton.removeAttribute('hidden');
}

function installPWA(evt) {
  deferredInstallPrompt.prompt();
  evt.srcElement.setAttribute('hidden', true);
  deferredInstallPrompt.userChoice
  .then((choice) => {
    if (choice.outcome === 'accepted') {
      console.log('User accepted the A2HS prompt', choice);
    } else {
      console.log('User dismissed the A2HS prompt', choice);
    }
    deferredInstallPrompt = null;
  });
}

window.addEventListener('appinstalled', logAppInstalled);

function logAppInstalled(evt) {
  console.log('App was installed.', evt);
}

function resizeToMinimum(){
  var minimum    = [640, 480];
  var current    = [window.outerWidth, window.outerHeight];
  var restricted = [];
  var i          = 2;

  while(i-- > 0){
    restricted[i] = minimum[i] > current[i] ? minimum[i] : current[i];
  }

  window.resizeTo(current[0], current[1]);
}

window.addEventListener('resize', resizeToMinimum, false);
