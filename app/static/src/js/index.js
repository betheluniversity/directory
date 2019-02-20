import '../css/main.scss'
import '../css/awesomplete.css'

import {  } from "./ajaxCall";
import {  } from "./showHide";
import {  } from "awesomplete";

const input = document.getElementById("department");
const awesomplete = new Awesomplete(input, {
    minChars: 1
});
awesomplete.list = ["Chemistry","Physics", "Nursing", "Business"];
