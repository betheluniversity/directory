const form = document.querySelector(".directory-form");
form.addEventListener("submit", e => {
    e.preventDefault();
    const fd = new FormData();
    fd.append('search_type', 'name_search')
    fd.append('first_name', form.querySelector("#first_name").value)
    fd.append('last_name', form.querySelector("#last_name").value)
    fd.append('username', form.querySelector("#username").value)
    fd.append('email', form.querySelector("#email").value)
    fd.append('department', form.querySelector("#department").value)
    fd.append('bu_id', form.querySelector("#bu_id").value)
    // fd.append('view_ids', form.querySelector(".view_ids").value || "false" )
    // fd.append('home', form.querySelector(".home").value || "false" )
    // fd.append(// 'group', form.querySelector(".group").value || "false" )
    // fd.append('student', form.querySelector(".student").value || "false" )
    // fd.append('faculty_or_staff', form.querySelector(".faculty_or_staff").value || "false")
    
    // Converting form data to an object to pass via xhr
    const obj = {};
    [...fd.entries()].forEach(entry => obj[entry[0]] = entry[1]);

    const results = document.querySelector('#results')

    function postAjax(url, data, success) {
	    const params = typeof data == 'string' ? data : Object.keys(data).map(
	            function(k){ return encodeURIComponent(k) + '=' + encodeURIComponent(data[k]) }
	        ).join('&');
	
	    const xhr = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");
	    xhr.open('POST', url);
	    xhr.onreadystatechange = function() {
            if (xhr.readyState==3 && xhr.status==200){
                console.log('loading');
            }
	        if (xhr.readyState>3 && xhr.status==200) { 
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