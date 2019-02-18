const showHide = require('./showHide')
const ajaxCall = require('./ajaxCall')

import {  } from "awesomplete";

const input = document.getElementById("department");
const awesomplete = new Awesomplete(input, {
    minChars: 1
});
awesomplete.list = ["Chemistry","Physics", "Nursing", "Business"];
