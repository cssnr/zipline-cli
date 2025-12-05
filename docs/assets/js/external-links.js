// Open External Links in New Tab

// noinspection JSUnresolvedReference,JSIgnoredPromiseFromCall
document$.subscribe(documentLoaded)

function documentLoaded() {
    // console.log('documentLoaded:', globalThis.location)
    for (const el of document.querySelectorAll('a')) {
        // console.log('el.host:', el.host)
        if (el.host && el.host !== globalThis.location.host) {
            el.target = '_blank'
            el.rel = 'noopener'
        }
    }
}
