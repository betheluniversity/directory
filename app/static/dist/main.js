/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./app/static/src/js/index.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./app/static/src/css/awesomplete.css":
/*!********************************************!*\
  !*** ./app/static/src/css/awesomplete.css ***!
  \********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("// extracted by mini-css-extract-plugin\n\n//# sourceURL=webpack:///./app/static/src/css/awesomplete.css?");

/***/ }),

/***/ "./app/static/src/css/main.scss":
/*!**************************************!*\
  !*** ./app/static/src/css/main.scss ***!
  \**************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("// extracted by mini-css-extract-plugin\n\n//# sourceURL=webpack:///./app/static/src/css/main.scss?");

/***/ }),

/***/ "./app/static/src/js/ajaxCall.js":
/*!***************************************!*\
  !*** ./app/static/src/js/ajaxCall.js ***!
  \***************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("const form = document.querySelector('.directory-form')\nconst results = document.querySelector('#results')\nconst introText = results.querySelector('.introText')\nconst loader = document.querySelector('.loader')\n\nform.addEventListener('submit', e => {\n    e.preventDefault()\n    introText.classList.toggle('hide')\n    // show load animation\n    loader.classList.remove('hide-loader')\n\n    let obj = serialize(form)\n\n    postAjax('/search', obj, function (xhr) {\n        results.innerHTML = xhr.responseText\n\n        const infiniteScroll = document.querySelector('#infiniteScroll')\n        const iDC = document.querySelector('#infiniteDataContainer')\n\n        window.onscroll = function (ev) {\n            // you're at the bottom of the page\n            if ((window.innerHeight + window.scrollY) >= infiniteScroll.offsetHeight &&\n                    parseInt(iDC.getAttribute('page')) < parseInt(iDC.getAttribute('max-page')) &&\n                    iDC.getAttribute('busy') === 'false') {\n                // set to busy\n                iDC.setAttribute('busy', 'true')\n\n                // increase page number\n                let pageNumber = parseInt(iDC.getAttribute('page')) + 1\n                iDC.setAttribute('page', pageNumber)\n\n                // get new page number\n                let newPageNumber = iDC.getAttribute('page')\n\n\n                if (pageNumber === parseInt(iDC.getAttribute('max-page'))) {\n                    loader.classList.add('hide-loader')\n                }\n\n                // get data and add on page number\n                obj = iDC.getAttribute('data') + '&page=' + newPageNumber\n                postAjax('/search', obj, function (xhr) {\n                    // append results\n                    infiniteScroll.innerHTML += xhr.responseText\n                    iDC.setAttribute('busy', 'false')\n                })\n            }\n        }\n    })\n})\n\nfunction postAjax (url, data, callback) {\n    const params = typeof data === 'string' ? data : Object.keys(data).map(\n        function (k) { return encodeURIComponent(k) + '=' + encodeURIComponent(data[k]) }\n    ).join('&')\n    // console.log(params)\n    const xhr = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP')\n    xhr.open('POST', url)\n    xhr.onreadystatechange = function () {\n        if (xhr.readyState === 1) {\n\n        }\n        if (xhr.readyState === 3 && xhr.status === 200) {\n            console.log('Loading...')\n        } else if (xhr.readyState > 3 && xhr.status === 200) {\n            callback(xhr)\n            form.reset()\n            detailsLink()\n        }\n    }\n    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest')\n    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')\n    xhr.send(params)\n    return xhr\n}\n\nfunction detailsLink () {\n    // Set listener after results have ajaxed in\n    const showDetails = document.querySelectorAll('.person__details__link')\n    for (let index = 0; index < showDetails.length; index++) {\n        showDetails[index].addEventListener('click', function () {\n            let next = this.parentElement.parentElement.nextElementSibling\n            next.classList.toggle('hide')\n            this.innerHTML === '- Hide details' ? this.innerHTML = '+ Show details' : this.innerHTML = '- Hide details'\n            let homeLink = next.querySelector('.person__home__link')\n            if (homeLink) {\n                homeLink.addEventListener('click', function () {\n                    this.nextElementSibling.classList.toggle('hide')\n                })\n            }\n        })\n    }\n}\n\n/*!\n * Serialize all form data into a query string\n * (c) 2018 Chris Ferdinandi, MIT License, https://gomakethings.com\n * @param  {Node}   form The form to serialize\n * @return {String}      The serialized form data\n * url:  https://vanillajstoolkit.com/helpers/serialize/\n */\nfunction serialize (form) {\n    // Setup our serialized data\n    const serialized = []\n\n    // Loop through each field in the form\n    for (let i = 0; i < form.elements.length; i++) {\n        const field = form.elements[i]\n\n        // Don't serialize fields without a name, submits, buttons, file and reset inputs, and disabled fields\n        if (!field.name || field.disabled || field.type === 'file' || field.type === 'reset' || field.type === 'submit' || field.type === 'button') continue\n\n        // If a multi-select, get all selections\n        if (field.type === 'select-multiple') {\n            for (let n = 0; n < field.options.length; n++) {\n                if (!field.options[n].selected) continue\n                serialized.push(encodeURIComponent(field.name) + '=' + encodeURIComponent(field.options[n].value))\n            }\n        }\n\n        // Convert field data to a query string\n        else if ((field.type !== 'checkbox' && field.type !== 'radio') || field.checked) {\n            serialized.push(encodeURIComponent(field.name) + '=' + encodeURIComponent(field.value))\n        }\n    }\n\n    return serialized.join('&')\n}\n\n\n//# sourceURL=webpack:///./app/static/src/js/ajaxCall.js?");

/***/ }),

/***/ "./app/static/src/js/index.js":
/*!************************************!*\
  !*** ./app/static/src/js/index.js ***!
  \************************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _css_main_scss__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../css/main.scss */ \"./app/static/src/css/main.scss\");\n/* harmony import */ var _css_main_scss__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_css_main_scss__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var _css_awesomplete_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../css/awesomplete.css */ \"./app/static/src/css/awesomplete.css\");\n/* harmony import */ var _css_awesomplete_css__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_css_awesomplete_css__WEBPACK_IMPORTED_MODULE_1__);\n/* harmony import */ var _microsoftEdgeFixes__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./microsoftEdgeFixes */ \"./app/static/src/js/microsoftEdgeFixes.js\");\n/* harmony import */ var _microsoftEdgeFixes__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_microsoftEdgeFixes__WEBPACK_IMPORTED_MODULE_2__);\n/* harmony import */ var _ajaxCall__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./ajaxCall */ \"./app/static/src/js/ajaxCall.js\");\n/* harmony import */ var _ajaxCall__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_ajaxCall__WEBPACK_IMPORTED_MODULE_3__);\n/* harmony import */ var _showHide__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./showHide */ \"./app/static/src/js/showHide.js\");\n/* harmony import */ var _showHide__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_showHide__WEBPACK_IMPORTED_MODULE_4__);\n/* harmony import */ var awesomplete__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! awesomplete */ \"./node_modules/awesomplete/awesomplete.js\");\n/* harmony import */ var awesomplete__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(awesomplete__WEBPACK_IMPORTED_MODULE_5__);\n/// //////////////////////////////////////////////////////////////////////////\n// This is needed to connect to awesomplete for the department search.\n// The other part of the JS code lives in index.html because it needs to get\n// the jinja variable populated from the python.\n/// //////////////////////////////////////////////////////////////////////////\n\n\n\n\n\n\n\n/// //////////////////////////////////////////////////////////////////////////\n\n\n//# sourceURL=webpack:///./app/static/src/js/index.js?");

/***/ }),

/***/ "./app/static/src/js/microsoftEdgeFixes.js":
/*!*************************************************!*\
  !*** ./app/static/src/js/microsoftEdgeFixes.js ***!
  \*************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("// missing forEach on NodeList for IE11\nif (window.NodeList && !NodeList.prototype.forEach) {\n  NodeList.prototype.forEach = Array.prototype.forEach;\n}\n\n\n//# sourceURL=webpack:///./app/static/src/js/microsoftEdgeFixes.js?");

/***/ }),

/***/ "./app/static/src/js/showHide.js":
/*!***************************************!*\
  !*** ./app/static/src/js/showHide.js ***!
  \***************************************/
/*! no static exports found */
/***/ (function(module, exports) {

eval("const accordionItems = document.querySelectorAll('.accordionItem')\nconst accordionContentPanes = document.querySelectorAll('.accordionContent')\nconst form = document.querySelector('.directory-form')\n\n// First open by default, setting closed to have an explicit height for animation to work\nconst firstItem = accordionItems[0].querySelector('.accordionContent')\naccordionItems[0].classList.add('active')\nfirstItem.style.height = firstItem.scrollHeight + 'px'\naccordionItems[1].querySelector('.accordionContent').style.height = '0px'\naccordionItems[2].querySelector('.accordionContent').style.height = '0px'\n\n// add listener to each title\naccordionItems.forEach(function (accordion) {\n    let accordionTitle = accordion.firstElementChild\n    accordionTitle.addEventListener('click', toggleAccordion)\n})\n\nfunction toggleAccordion (e) {\n    form.reset()\n    accordionItems.forEach(a => {\n        if (this.parentElement === a) {\n            a.classList.add('active')\n        } else {\n            a.classList.remove('active')\n        }\n    })\n\n    accordionContentPanes.forEach(a => {\n        if (a.previousElementSibling === this) {\n            // For the department search, require the department to be selected\n            if( a.classList.contains('departmentRequired') )\n                document.getElementById('department').required = true;\n            else\n                document.getElementById('department').required = false;\n\n            a.classList.remove('hide-accordion')\n            a.style.height = a.scrollHeight + 'px'\n        } else {\n            a.classList.add('hide-accordion')\n            a.style.height = '0px'\n        }\n    })\n}\n\n// Profile menu show/hide\nconst profileDropdownLink = document.querySelector('#profileDropdown--link')\nconst profileDropdownMenu = document.querySelector('#profileDropdown--menu')\n\nif (profileDropdownLink) {\n    profileDropdownLink.addEventListener('click', function () {\n        profileDropdownMenu.classList.toggle('show')\n    })\n}\n\n\n//# sourceURL=webpack:///./app/static/src/js/showHide.js?");

/***/ }),

/***/ "./node_modules/awesomplete/awesomplete.js":
/*!*************************************************!*\
  !*** ./node_modules/awesomplete/awesomplete.js ***!
  \*************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

eval("/**\n * Simple, lightweight, usable local autocomplete library for modern browsers\n * Because there weren’t enough autocomplete scripts in the world? Because I’m completely insane and have NIH syndrome? Probably both. :P\n * @author Lea Verou http://leaverou.github.io/awesomplete\n * MIT license\n */\n\n(function () {\n\nvar _ = function (input, o) {\n\tvar me = this;\n\n    // Keep track of number of instances for unique IDs\n    _.count = (_.count || 0) + 1;\n    this.count = _.count;\n\n\t// Setup\n\n\tthis.isOpened = false;\n\n\tthis.input = $(input);\n\tthis.input.setAttribute(\"autocomplete\", \"off\");\n\tthis.input.setAttribute(\"aria-owns\", \"awesomplete_list_\" + this.count);\n\tthis.input.setAttribute(\"role\", \"combobox\");\n\n\t// store constructor options in case we need to distinguish\n\t// between default and customized behavior later on\n\tthis.options = o = o || {};\n\n\tconfigure(this, {\n\t\tminChars: 2,\n\t\tmaxItems: 10,\n\t\tautoFirst: false,\n\t\tdata: _.DATA,\n\t\tfilter: _.FILTER_CONTAINS,\n\t\tsort: o.sort === false ? false : _.SORT_BYLENGTH,\n\t\tcontainer: _.CONTAINER,\n\t\titem: _.ITEM,\n\t\treplace: _.REPLACE,\n\t\ttabSelect: false\n\t}, o);\n\n\tthis.index = -1;\n\n\t// Create necessary elements\n\n\tthis.container = this.container(input);\n\n\tthis.ul = $.create(\"ul\", {\n\t\thidden: \"hidden\",\n        role: \"listbox\",\n        id: \"awesomplete_list_\" + this.count,\n\t\tinside: this.container\n\t});\n\n\tthis.status = $.create(\"span\", {\n\t\tclassName: \"visually-hidden\",\n\t\trole: \"status\",\n\t\t\"aria-live\": \"assertive\",\n        \"aria-atomic\": true,\n        inside: this.container,\n        textContent: this.minChars != 0 ? (\"Type \" + this.minChars + \" or more characters for results.\") : \"Begin typing for results.\"\n\t});\n\n\t// Bind events\n\n\tthis._events = {\n\t\tinput: {\n\t\t\t\"input\": this.evaluate.bind(this),\n\t\t\t\"blur\": this.close.bind(this, { reason: \"blur\" }),\n\t\t\t\"keydown\": function(evt) {\n\t\t\t\tvar c = evt.keyCode;\n\n\t\t\t\t// If the dropdown `ul` is in view, then act on keydown for the following keys:\n\t\t\t\t// Enter / Esc / Up / Down\n\t\t\t\tif(me.opened) {\n\t\t\t\t\tif (c === 13 && me.selected) { // Enter\n\t\t\t\t\t\tevt.preventDefault();\n\t\t\t\t\t\tme.select();\n\t\t\t\t\t}\n\t\t\t\t\telse if (c === 9 && me.selected && me.tabSelect) {\n\t\t\t\t\t\tme.select();\n\t\t\t\t\t}\n\t\t\t\t\telse if (c === 27) { // Esc\n\t\t\t\t\t\tme.close({ reason: \"esc\" });\n\t\t\t\t\t}\n\t\t\t\t\telse if (c === 38 || c === 40) { // Down/Up arrow\n\t\t\t\t\t\tevt.preventDefault();\n\t\t\t\t\t\tme[c === 38? \"previous\" : \"next\"]();\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n\t\t},\n\t\tform: {\n\t\t\t\"submit\": this.close.bind(this, { reason: \"submit\" })\n\t\t},\n\t\tul: {\n\t\t\t// Prevent the default mousedowm, which ensures the input is not blurred.\n\t\t\t// The actual selection will happen on click. This also ensures dragging the\n\t\t\t// cursor away from the list item will cancel the selection\n\t\t\t\"mousedown\": function(evt) {\n\t\t\t\tevt.preventDefault();\n\t\t\t},\n\t\t\t// The click event is fired even if the corresponding mousedown event has called preventDefault\n\t\t\t\"click\": function(evt) {\n\t\t\t\tvar li = evt.target;\n\n\t\t\t\tif (li !== this) {\n\n\t\t\t\t\twhile (li && !/li/i.test(li.nodeName)) {\n\t\t\t\t\t\tli = li.parentNode;\n\t\t\t\t\t}\n\n\t\t\t\t\tif (li && evt.button === 0) {  // Only select on left click\n\t\t\t\t\t\tevt.preventDefault();\n\t\t\t\t\t\tme.select(li, evt.target);\n\t\t\t\t\t}\n\t\t\t\t}\n\t\t\t}\n\t\t}\n\t};\n\n\t$.bind(this.input, this._events.input);\n\t$.bind(this.input.form, this._events.form);\n\t$.bind(this.ul, this._events.ul);\n\n\tif (this.input.hasAttribute(\"list\")) {\n\t\tthis.list = \"#\" + this.input.getAttribute(\"list\");\n\t\tthis.input.removeAttribute(\"list\");\n\t}\n\telse {\n\t\tthis.list = this.input.getAttribute(\"data-list\") || o.list || [];\n\t}\n\n\t_.all.push(this);\n};\n\n_.prototype = {\n\tset list(list) {\n\t\tif (Array.isArray(list)) {\n\t\t\tthis._list = list;\n\t\t}\n\t\telse if (typeof list === \"string\" && list.indexOf(\",\") > -1) {\n\t\t\t\tthis._list = list.split(/\\s*,\\s*/);\n\t\t}\n\t\telse { // Element or CSS selector\n\t\t\tlist = $(list);\n\n\t\t\tif (list && list.children) {\n\t\t\t\tvar items = [];\n\t\t\t\tslice.apply(list.children).forEach(function (el) {\n\t\t\t\t\tif (!el.disabled) {\n\t\t\t\t\t\tvar text = el.textContent.trim();\n\t\t\t\t\t\tvar value = el.value || text;\n\t\t\t\t\t\tvar label = el.label || text;\n\t\t\t\t\t\tif (value !== \"\") {\n\t\t\t\t\t\t\titems.push({ label: label, value: value });\n\t\t\t\t\t\t}\n\t\t\t\t\t}\n\t\t\t\t});\n\t\t\t\tthis._list = items;\n\t\t\t}\n\t\t}\n\n\t\tif (document.activeElement === this.input) {\n\t\t\tthis.evaluate();\n\t\t}\n\t},\n\n\tget selected() {\n\t\treturn this.index > -1;\n\t},\n\n\tget opened() {\n\t\treturn this.isOpened;\n\t},\n\n\tclose: function (o) {\n\t\tif (!this.opened) {\n\t\t\treturn;\n\t\t}\n\n\t\tthis.ul.setAttribute(\"hidden\", \"\");\n\t\tthis.isOpened = false;\n\t\tthis.index = -1;\n\n\t\tthis.status.setAttribute(\"hidden\", \"\");\n\n\t\t$.fire(this.input, \"awesomplete-close\", o || {});\n\t},\n\n\topen: function () {\n\t\tthis.ul.removeAttribute(\"hidden\");\n\t\tthis.isOpened = true;\n\n\t\tthis.status.removeAttribute(\"hidden\");\n\n\t\tif (this.autoFirst && this.index === -1) {\n\t\t\tthis.goto(0);\n\t\t}\n\n\t\t$.fire(this.input, \"awesomplete-open\");\n\t},\n\n\tdestroy: function() {\n\t\t//remove events from the input and its form\n\t\t$.unbind(this.input, this._events.input);\n\t\t$.unbind(this.input.form, this._events.form);\n\n\t\t// cleanup container if it was created by Awesomplete but leave it alone otherwise\n\t\tif (!this.options.container) {\n\t\t\t//move the input out of the awesomplete container and remove the container and its children\n\t\t\tvar parentNode = this.container.parentNode;\n\n\t\t\tparentNode.insertBefore(this.input, this.container);\n\t\t\tparentNode.removeChild(this.container);\n\t\t}\n\n\t\t//remove autocomplete and aria-autocomplete attributes\n\t\tthis.input.removeAttribute(\"autocomplete\");\n\t\tthis.input.removeAttribute(\"aria-autocomplete\");\n\n\t\t//remove this awesomeplete instance from the global array of instances\n\t\tvar indexOfAwesomplete = _.all.indexOf(this);\n\n\t\tif (indexOfAwesomplete !== -1) {\n\t\t\t_.all.splice(indexOfAwesomplete, 1);\n\t\t}\n\t},\n\n\tnext: function () {\n\t\tvar count = this.ul.children.length;\n\t\tthis.goto(this.index < count - 1 ? this.index + 1 : (count ? 0 : -1) );\n\t},\n\n\tprevious: function () {\n\t\tvar count = this.ul.children.length;\n\t\tvar pos = this.index - 1;\n\n\t\tthis.goto(this.selected && pos !== -1 ? pos : count - 1);\n\t},\n\n\t// Should not be used, highlights specific item without any checks!\n\tgoto: function (i) {\n\t\tvar lis = this.ul.children;\n\n\t\tif (this.selected) {\n\t\t\tlis[this.index].setAttribute(\"aria-selected\", \"false\");\n\t\t}\n\n\t\tthis.index = i;\n\n\t\tif (i > -1 && lis.length > 0) {\n\t\t\tlis[i].setAttribute(\"aria-selected\", \"true\");\n\n\t\t\tthis.status.textContent = lis[i].textContent + \", list item \" + (i + 1) + \" of \" + lis.length;\n\n            this.input.setAttribute(\"aria-activedescendant\", this.ul.id + \"_item_\" + this.index);\n\n\t\t\t// scroll to highlighted element in case parent's height is fixed\n\t\t\tthis.ul.scrollTop = lis[i].offsetTop - this.ul.clientHeight + lis[i].clientHeight;\n\n\t\t\t$.fire(this.input, \"awesomplete-highlight\", {\n\t\t\t\ttext: this.suggestions[this.index]\n\t\t\t});\n\t\t}\n\t},\n\n\tselect: function (selected, origin) {\n\t\tif (selected) {\n\t\t\tthis.index = $.siblingIndex(selected);\n\t\t} else {\n\t\t\tselected = this.ul.children[this.index];\n\t\t}\n\n\t\tif (selected) {\n\t\t\tvar suggestion = this.suggestions[this.index];\n\n\t\t\tvar allowed = $.fire(this.input, \"awesomplete-select\", {\n\t\t\t\ttext: suggestion,\n\t\t\t\torigin: origin || selected\n\t\t\t});\n\n\t\t\tif (allowed) {\n\t\t\t\tthis.replace(suggestion);\n\t\t\t\tthis.close({ reason: \"select\" });\n\t\t\t\t$.fire(this.input, \"awesomplete-selectcomplete\", {\n\t\t\t\t\ttext: suggestion\n\t\t\t\t});\n\t\t\t}\n\t\t}\n\t},\n\n\tevaluate: function() {\n\t\tvar me = this;\n\t\tvar value = this.input.value;\n\n\t\tif (value.length >= this.minChars && this._list && this._list.length > 0) {\n\t\t\tthis.index = -1;\n\t\t\t// Populate list with options that match\n\t\t\tthis.ul.innerHTML = \"\";\n\n\t\t\tthis.suggestions = this._list\n\t\t\t\t.map(function(item) {\n\t\t\t\t\treturn new Suggestion(me.data(item, value));\n\t\t\t\t})\n\t\t\t\t.filter(function(item) {\n\t\t\t\t\treturn me.filter(item, value);\n\t\t\t\t});\n\n\t\t\tif (this.sort !== false) {\n\t\t\t\tthis.suggestions = this.suggestions.sort(this.sort);\n\t\t\t}\n\n\t\t\tthis.suggestions = this.suggestions.slice(0, this.maxItems);\n\n\t\t\tthis.suggestions.forEach(function(text, index) {\n\t\t\t\t\tme.ul.appendChild(me.item(text, value, index));\n\t\t\t\t});\n\n\t\t\tif (this.ul.children.length === 0) {\n\n                this.status.textContent = \"No results found\";\n\n\t\t\t\tthis.close({ reason: \"nomatches\" });\n\n\t\t\t} else {\n\t\t\t\tthis.open();\n\n                this.status.textContent = this.ul.children.length + \" results found\";\n\t\t\t}\n\t\t}\n\t\telse {\n\t\t\tthis.close({ reason: \"nomatches\" });\n\n                this.status.textContent = \"No results found\";\n\t\t}\n\t}\n};\n\n// Static methods/properties\n\n_.all = [];\n\n_.FILTER_CONTAINS = function (text, input) {\n\treturn RegExp($.regExpEscape(input.trim()), \"i\").test(text);\n};\n\n_.FILTER_STARTSWITH = function (text, input) {\n\treturn RegExp(\"^\" + $.regExpEscape(input.trim()), \"i\").test(text);\n};\n\n_.SORT_BYLENGTH = function (a, b) {\n\tif (a.length !== b.length) {\n\t\treturn a.length - b.length;\n\t}\n\n\treturn a < b? -1 : 1;\n};\n\n_.CONTAINER = function (input) {\n\treturn $.create(\"div\", {\n\t\tclassName: \"awesomplete\",\n\t\taround: input\n\t});\n}\n\n_.ITEM = function (text, input, item_id) {\n\tvar html = input.trim() === \"\" ? text : text.replace(RegExp($.regExpEscape(input.trim()), \"gi\"), \"<mark>$&</mark>\");\n\treturn $.create(\"li\", {\n\t\tinnerHTML: html,\n\t\t\"aria-selected\": \"false\",\n        \"id\": \"awesomplete_list_\" + this.count + \"_item_\" + item_id\n\t});\n};\n\n_.REPLACE = function (text) {\n\tthis.input.value = text.value;\n};\n\n_.DATA = function (item/*, input*/) { return item; };\n\n// Private functions\n\nfunction Suggestion(data) {\n\tvar o = Array.isArray(data)\n\t  ? { label: data[0], value: data[1] }\n\t  : typeof data === \"object\" && \"label\" in data && \"value\" in data ? data : { label: data, value: data };\n\n\tthis.label = o.label || o.value;\n\tthis.value = o.value;\n}\nObject.defineProperty(Suggestion.prototype = Object.create(String.prototype), \"length\", {\n\tget: function() { return this.label.length; }\n});\nSuggestion.prototype.toString = Suggestion.prototype.valueOf = function () {\n\treturn \"\" + this.label;\n};\n\nfunction configure(instance, properties, o) {\n\tfor (var i in properties) {\n\t\tvar initial = properties[i],\n\t\t    attrValue = instance.input.getAttribute(\"data-\" + i.toLowerCase());\n\n\t\tif (typeof initial === \"number\") {\n\t\t\tinstance[i] = parseInt(attrValue);\n\t\t}\n\t\telse if (initial === false) { // Boolean options must be false by default anyway\n\t\t\tinstance[i] = attrValue !== null;\n\t\t}\n\t\telse if (initial instanceof Function) {\n\t\t\tinstance[i] = null;\n\t\t}\n\t\telse {\n\t\t\tinstance[i] = attrValue;\n\t\t}\n\n\t\tif (!instance[i] && instance[i] !== 0) {\n\t\t\tinstance[i] = (i in o)? o[i] : initial;\n\t\t}\n\t}\n}\n\n// Helpers\n\nvar slice = Array.prototype.slice;\n\nfunction $(expr, con) {\n\treturn typeof expr === \"string\"? (con || document).querySelector(expr) : expr || null;\n}\n\nfunction $$(expr, con) {\n\treturn slice.call((con || document).querySelectorAll(expr));\n}\n\n$.create = function(tag, o) {\n\tvar element = document.createElement(tag);\n\n\tfor (var i in o) {\n\t\tvar val = o[i];\n\n\t\tif (i === \"inside\") {\n\t\t\t$(val).appendChild(element);\n\t\t}\n\t\telse if (i === \"around\") {\n\t\t\tvar ref = $(val);\n\t\t\tref.parentNode.insertBefore(element, ref);\n\t\t\telement.appendChild(ref);\n\n\t\t\tif (ref.getAttribute(\"autofocus\") != null) {\n\t\t\t\tref.focus();\n\t\t\t}\n\t\t}\n\t\telse if (i in element) {\n\t\t\telement[i] = val;\n\t\t}\n\t\telse {\n\t\t\telement.setAttribute(i, val);\n\t\t}\n\t}\n\n\treturn element;\n};\n\n$.bind = function(element, o) {\n\tif (element) {\n\t\tfor (var event in o) {\n\t\t\tvar callback = o[event];\n\n\t\t\tevent.split(/\\s+/).forEach(function (event) {\n\t\t\t\telement.addEventListener(event, callback);\n\t\t\t});\n\t\t}\n\t}\n};\n\n$.unbind = function(element, o) {\n\tif (element) {\n\t\tfor (var event in o) {\n\t\t\tvar callback = o[event];\n\n\t\t\tevent.split(/\\s+/).forEach(function(event) {\n\t\t\t\telement.removeEventListener(event, callback);\n\t\t\t});\n\t\t}\n\t}\n};\n\n$.fire = function(target, type, properties) {\n\tvar evt = document.createEvent(\"HTMLEvents\");\n\n\tevt.initEvent(type, true, true );\n\n\tfor (var j in properties) {\n\t\tevt[j] = properties[j];\n\t}\n\n\treturn target.dispatchEvent(evt);\n};\n\n$.regExpEscape = function (s) {\n\treturn s.replace(/[-\\\\^$*+?.()|[\\]{}]/g, \"\\\\$&\");\n};\n\n$.siblingIndex = function (el) {\n\t/* eslint-disable no-cond-assign */\n\tfor (var i = 0; el = el.previousElementSibling; i++);\n\treturn i;\n};\n\n// Initialization\n\nfunction init() {\n\t$$(\"input.awesomplete\").forEach(function (input) {\n\t\tnew _(input);\n\t});\n}\n\n// Make sure to export Awesomplete on self when in a browser\nif (typeof self !== \"undefined\") {\n\tself.Awesomplete = _;\n}\n\n// Are we in a browser? Check for Document constructor\nif (typeof Document !== \"undefined\") {\n\t// DOM already loaded?\n\tif (document.readyState !== \"loading\") {\n\t\tinit();\n\t}\n\telse {\n\t\t// Wait for it\n\t\tdocument.addEventListener(\"DOMContentLoaded\", init);\n\t}\n}\n\n_.$ = $;\n_.$$ = $$;\n\n// Expose Awesomplete as a CJS module\nif ( true && module.exports) {\n\tmodule.exports = _;\n}\n\nreturn _;\n\n}());\n\n\n//# sourceURL=webpack:///./node_modules/awesomplete/awesomplete.js?");

/***/ })

/******/ });