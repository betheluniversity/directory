!function(t){var e={};function i(n){if(e[n])return e[n].exports;var s=e[n]={i:n,l:!1,exports:{}};return t[n].call(s.exports,s,s.exports,i),s.l=!0,s.exports}i.m=t,i.c=e,i.d=function(t,e,n){i.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:n})},i.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},i.t=function(t,e){if(1&e&&(t=i(t)),8&e)return t;if(4&e&&"object"==typeof t&&t&&t.__esModule)return t;var n=Object.create(null);if(i.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var s in t)i.d(n,s,function(e){return t[e]}.bind(null,s));return n},i.n=function(t){var e=t&&t.__esModule?function(){return t.default}:function(){return t};return i.d(e,"a",e),e},i.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},i.p="",i(i.s=0)}([function(t,e,i){"use strict";i.r(e);i(1),i(2),i(3),i(4),i(5)},function(t,e,i){},function(t,e,i){},function(t,e){const i=document.querySelector("#results"),n=i.querySelector(".loader"),s=i.querySelector(".introText"),o=document.querySelector(".directory-form");o.addEventListener("submit",t=>{t.preventDefault(),s.classList.toggle("hide"),n.classList.toggle("hide");const e=new FormData(o);function r(t,e,i){const n="string"==typeof e?e:Object.keys(e).map(function(t){return encodeURIComponent(t)+"="+encodeURIComponent(e[t])}).join("&");console.log(n);const s=window.XMLHttpRequest?new XMLHttpRequest:new ActiveXObject("Microsoft.XMLHTTP");return s.open("POST",t),s.onreadystatechange=function(){3===s.readyState&&200===s.status?console.log("Loading..."):s.status>=500||0===s.status||s.readyState>3&&200===s.status&&i(s)},s.setRequestHeader("X-Requested-With","XMLHttpRequest"),s.setRequestHeader("Content-Type","application/x-www-form-urlencoded"),s.send(n),s}obj={},[...e.entries()].forEach(t=>obj[t[0]]=t[1]),r("/search",obj,function(t){o.reset(),i.innerHTML=t.responseText;const e=document.querySelectorAll(".person");for(let t=0;t<e.length;t++)e[t].addEventListener("click",function(){this.classList.toggle("show-details")});const n=document.querySelector("#infiniteScroll");window.onscroll=function(t){console.log("F "+window.innerHeight+" "+window.scrollY+" "+n.offsetHeight),window.innerHeight+window.scrollY>=n.offsetHeight&&parseInt(document.querySelector("#infiniteDataContainer").getAttribute("page"))<parseInt(document.querySelector("#infiniteDataContainer").getAttribute("max-page"))&&"false"===document.querySelector("#infiniteDataContainer").getAttribute("busy")&&(document.querySelector("#infiniteDataContainer").setAttribute("busy","true"),console.log("T "+window.innerHeight+" "+window.scrollY+" "+n.offsetHeight),page_number=parseInt(document.querySelector("#infiniteDataContainer").getAttribute("page"))+1,document.querySelector("#infiniteDataContainer").setAttribute("page",page_number),new_page_number=document.querySelector("#infiniteDataContainer").getAttribute("page"),obj=document.querySelector("#infiniteDataContainer").getAttribute("data")+"&page="+new_page_number,r("/search",obj,function(t){n.innerHTML=n.innerHTML+t.responseText,document.querySelector("#infiniteDataContainer").setAttribute("busy","false")}))}})})},function(t,e){const i=document.querySelectorAll(".accordionItem"),n=document.querySelectorAll(".accordionContent"),s=i[0].querySelector(".accordionContent");function o(t){i.forEach(t=>{this.parentElement===t?t.classList.add("active"):t.classList.remove("active")}),n.forEach(t=>{t.previousElementSibling===this?(t.classList.remove("hide-accordion"),t.style.height=t.scrollHeight+"px"):(t.classList.add("hide-accordion"),t.style.height="0px")})}i[0].classList.add("active"),s.style.height=s.scrollHeight+"px",i[1].querySelector(".accordionContent").style.height="0px",i[2].querySelector(".accordionContent").style.height="0px",i.forEach(function(t){t.firstElementChild.addEventListener("click",o)});const r=document.querySelector("#profileDropdown--link"),u=document.querySelector("#profileDropdown--menu");r&&r.addEventListener("click",function(){u.classList.toggle("show")})},function(t,e,i){!function(){var e=function(t,i){var n=this;e.count=(e.count||0)+1,this.count=e.count,this.isOpened=!1,this.input=s(t),this.input.setAttribute("autocomplete","off"),this.input.setAttribute("aria-owns","awesomplete_list_"+this.count),this.input.setAttribute("role","combobox"),this.options=i=i||{},function(t,e,i){for(var n in e){var s=e[n],o=t.input.getAttribute("data-"+n.toLowerCase());"number"==typeof s?t[n]=parseInt(o):!1===s?t[n]=null!==o:s instanceof Function?t[n]=null:t[n]=o,t[n]||0===t[n]||(t[n]=n in i?i[n]:s)}}(this,{minChars:2,maxItems:10,autoFirst:!1,data:e.DATA,filter:e.FILTER_CONTAINS,sort:!1!==i.sort&&e.SORT_BYLENGTH,container:e.CONTAINER,item:e.ITEM,replace:e.REPLACE,tabSelect:!1},i),this.index=-1,this.container=this.container(t),this.ul=s.create("ul",{hidden:"hidden",role:"listbox",id:"awesomplete_list_"+this.count,inside:this.container}),this.status=s.create("span",{className:"visually-hidden",role:"status","aria-live":"assertive","aria-atomic":!0,inside:this.container,textContent:0!=this.minChars?"Type "+this.minChars+" or more characters for results.":"Begin typing for results."}),this._events={input:{input:this.evaluate.bind(this),blur:this.close.bind(this,{reason:"blur"}),keydown:function(t){var e=t.keyCode;n.opened&&(13===e&&n.selected?(t.preventDefault(),n.select()):9===e&&n.selected&&n.tabSelect?n.select():27===e?n.close({reason:"esc"}):38!==e&&40!==e||(t.preventDefault(),n[38===e?"previous":"next"]()))}},form:{submit:this.close.bind(this,{reason:"submit"})},ul:{mousedown:function(t){t.preventDefault()},click:function(t){var e=t.target;if(e!==this){for(;e&&!/li/i.test(e.nodeName);)e=e.parentNode;e&&0===t.button&&(t.preventDefault(),n.select(e,t.target))}}}},s.bind(this.input,this._events.input),s.bind(this.input.form,this._events.form),s.bind(this.ul,this._events.ul),this.input.hasAttribute("list")?(this.list="#"+this.input.getAttribute("list"),this.input.removeAttribute("list")):this.list=this.input.getAttribute("data-list")||i.list||[],e.all.push(this)};function i(t){var e=Array.isArray(t)?{label:t[0],value:t[1]}:"object"==typeof t&&"label"in t&&"value"in t?t:{label:t,value:t};this.label=e.label||e.value,this.value=e.value}e.prototype={set list(t){if(Array.isArray(t))this._list=t;else if("string"==typeof t&&t.indexOf(",")>-1)this._list=t.split(/\s*,\s*/);else if((t=s(t))&&t.children){var e=[];n.apply(t.children).forEach(function(t){if(!t.disabled){var i=t.textContent.trim(),n=t.value||i,s=t.label||i;""!==n&&e.push({label:s,value:n})}}),this._list=e}document.activeElement===this.input&&this.evaluate()},get selected(){return this.index>-1},get opened(){return this.isOpened},close:function(t){this.opened&&(this.ul.setAttribute("hidden",""),this.isOpened=!1,this.index=-1,this.status.setAttribute("hidden",""),s.fire(this.input,"awesomplete-close",t||{}))},open:function(){this.ul.removeAttribute("hidden"),this.isOpened=!0,this.status.removeAttribute("hidden"),this.autoFirst&&-1===this.index&&this.goto(0),s.fire(this.input,"awesomplete-open")},destroy:function(){if(s.unbind(this.input,this._events.input),s.unbind(this.input.form,this._events.form),!this.options.container){var t=this.container.parentNode;t.insertBefore(this.input,this.container),t.removeChild(this.container)}this.input.removeAttribute("autocomplete"),this.input.removeAttribute("aria-autocomplete");var i=e.all.indexOf(this);-1!==i&&e.all.splice(i,1)},next:function(){var t=this.ul.children.length;this.goto(this.index<t-1?this.index+1:t?0:-1)},previous:function(){var t=this.ul.children.length,e=this.index-1;this.goto(this.selected&&-1!==e?e:t-1)},goto:function(t){var e=this.ul.children;this.selected&&e[this.index].setAttribute("aria-selected","false"),this.index=t,t>-1&&e.length>0&&(e[t].setAttribute("aria-selected","true"),this.status.textContent=e[t].textContent+", list item "+(t+1)+" of "+e.length,this.input.setAttribute("aria-activedescendant",this.ul.id+"_item_"+this.index),this.ul.scrollTop=e[t].offsetTop-this.ul.clientHeight+e[t].clientHeight,s.fire(this.input,"awesomplete-highlight",{text:this.suggestions[this.index]}))},select:function(t,e){if(t?this.index=s.siblingIndex(t):t=this.ul.children[this.index],t){var i=this.suggestions[this.index];s.fire(this.input,"awesomplete-select",{text:i,origin:e||t})&&(this.replace(i),this.close({reason:"select"}),s.fire(this.input,"awesomplete-selectcomplete",{text:i}))}},evaluate:function(){var t=this,e=this.input.value;e.length>=this.minChars&&this._list&&this._list.length>0?(this.index=-1,this.ul.innerHTML="",this.suggestions=this._list.map(function(n){return new i(t.data(n,e))}).filter(function(i){return t.filter(i,e)}),!1!==this.sort&&(this.suggestions=this.suggestions.sort(this.sort)),this.suggestions=this.suggestions.slice(0,this.maxItems),this.suggestions.forEach(function(i,n){t.ul.appendChild(t.item(i,e,n))}),0===this.ul.children.length?(this.status.textContent="No results found",this.close({reason:"nomatches"})):(this.open(),this.status.textContent=this.ul.children.length+" results found")):(this.close({reason:"nomatches"}),this.status.textContent="No results found")}},e.all=[],e.FILTER_CONTAINS=function(t,e){return RegExp(s.regExpEscape(e.trim()),"i").test(t)},e.FILTER_STARTSWITH=function(t,e){return RegExp("^"+s.regExpEscape(e.trim()),"i").test(t)},e.SORT_BYLENGTH=function(t,e){return t.length!==e.length?t.length-e.length:t<e?-1:1},e.CONTAINER=function(t){return s.create("div",{className:"awesomplete",around:t})},e.ITEM=function(t,e,i){var n=""===e.trim()?t:t.replace(RegExp(s.regExpEscape(e.trim()),"gi"),"<mark>$&</mark>");return s.create("li",{innerHTML:n,"aria-selected":"false",id:"awesomplete_list_"+this.count+"_item_"+i})},e.REPLACE=function(t){this.input.value=t.value},e.DATA=function(t){return t},Object.defineProperty(i.prototype=Object.create(String.prototype),"length",{get:function(){return this.label.length}}),i.prototype.toString=i.prototype.valueOf=function(){return""+this.label};var n=Array.prototype.slice;function s(t,e){return"string"==typeof t?(e||document).querySelector(t):t||null}function o(t,e){return n.call((e||document).querySelectorAll(t))}function r(){o("input.awesomplete").forEach(function(t){new e(t)})}s.create=function(t,e){var i=document.createElement(t);for(var n in e){var o=e[n];if("inside"===n)s(o).appendChild(i);else if("around"===n){var r=s(o);r.parentNode.insertBefore(i,r),i.appendChild(r),null!=r.getAttribute("autofocus")&&r.focus()}else n in i?i[n]=o:i.setAttribute(n,o)}return i},s.bind=function(t,e){if(t)for(var i in e){var n=e[i];i.split(/\s+/).forEach(function(e){t.addEventListener(e,n)})}},s.unbind=function(t,e){if(t)for(var i in e){var n=e[i];i.split(/\s+/).forEach(function(e){t.removeEventListener(e,n)})}},s.fire=function(t,e,i){var n=document.createEvent("HTMLEvents");for(var s in n.initEvent(e,!0,!0),i)n[s]=i[s];return t.dispatchEvent(n)},s.regExpEscape=function(t){return t.replace(/[-\\^$*+?.()|[\]{}]/g,"\\$&")},s.siblingIndex=function(t){for(var e=0;t=t.previousElementSibling;e++);return e},"undefined"!=typeof self&&(self.Awesomplete=e),"undefined"!=typeof Document&&("loading"!==document.readyState?r():document.addEventListener("DOMContentLoaded",r)),e.$=s,e.$$=o,t.exports&&(t.exports=e)}()}]);