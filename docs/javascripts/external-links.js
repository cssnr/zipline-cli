// Open External Links in New Tab

// noinspection JSUnresolvedReference,JSIgnoredPromiseFromCall
document$.subscribe(function () {
    // console.log('processing:', window.location)
    for (const el of document.querySelectorAll('a')) {
        if (el.host !== globalThis.location.host) {
            el.target = '_blank'
            el.rel = 'noopener'
        }
    }
})
