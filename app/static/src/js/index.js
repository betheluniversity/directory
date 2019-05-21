/// //////////////////////////////////////////////////////////////////////////
// This is needed to connect to awesomplete for the department search.
// The other part of the JS code lives in index.html because it needs to get
// the jinja variable populated from the python.
/// //////////////////////////////////////////////////////////////////////////
import '../css/main.scss'
import '../css/awesomplete.css'

import { } from './microsoftEdgeFixes'
import { } from './ajaxCall'
import { } from './showHide'
import { } from 'awesomplete'
/// //////////////////////////////////////////////////////////////////////////

// adding this bit to remove a preload class which prevents css animations
// from running by default
window.addEventListener('load', function () {
    document.body.classList.remove('preload')
})
