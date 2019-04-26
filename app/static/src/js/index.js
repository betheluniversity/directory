/// //////////////////////////////////////////////////////////////////////////
// This is needed to connect to awesomplete for the department search.
// The other part of the JS code lives in index.html because it needs to get
// the jinja variable populated from the python.
/// //////////////////////////////////////////////////////////////////////////
import '../css/main.scss'
import '../css/awesomplete.css'

if (!Object.entries) {
  Object.entries = function( obj ){
    var ownProps = Object.keys( obj ),
        i = ownProps.length,
        resArray = new Array(i); // preallocate the Array
    while (i--)
      resArray[i] = [ownProps[i], obj[ownProps[i]]];

    return resArray;
  };
}

import { } from './ajaxCall'
import { } from './showHide'
import { } from 'awesomplete'
/// //////////////////////////////////////////////////////////////////////////
