const results = document.querySelector('#results')
const loader = results.querySelector('.loader')
const introText = results.querySelector('.introText')

const form = document.querySelector(".directory-form");
form.addEventListener("submit", e => {
    e.preventDefault();
    introText.classList.toggle('hide')
    loader.classList.toggle('hide')
    loader.classList.toggle('show')

    const fd = new FormData(form);
    // Converting form data to an object to pass via xhr
    const obj = {};
    [...fd.entries()].forEach(entry => obj[entry[0]] = entry[1]);

    function postAjax(url, data, success) {
	    const params = typeof data == 'string' ? data : Object.keys(data).map(
	            function(k){ return encodeURIComponent(k) + '=' + encodeURIComponent(data[k]) }
	        ).join('&');
	
	    const xhr = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");
	    xhr.open('POST', url);
	    xhr.onreadystatechange = function() {
            if (xhr.readyState==3 && xhr.status==200){
                console.log('loading');
            } else if (xhr.status >= 500 || xhr.status == 0) {
                location.href = "/";
            } else if (xhr.readyState>3 && xhr.status==200) {
                results.innerHTML = xhr.responseText
                form.reset()

                // Set listener after results have ajaxed in
                const showDetails = document.querySelectorAll('.showDetails--link')
                for (let index = 0; index < showDetails.length; index++) {
                    showDetails[index].addEventListener('click', function(){
                        this.parentElement.parentElement.nextElementSibling.classList.toggle('show')
                        this.innerHTML === 'Hide details' ? this.innerHTML = 'Show details' : this.innerHTML = 'Hide details'
                    })
                }
            }
	    };
	    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
	    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.send(params);
	    return xhr;
	}

    postAjax('/search', obj);
})