const results = document.querySelector('#results')
const loader = results.querySelector('.loader')
const introText = results.querySelector('.introText')

const form = document.querySelector('.directory-form')
form.addEventListener('submit', e => {
    e.preventDefault()
    introText.classList.toggle('hide')
    loader.classList.toggle('hide')
    // loader.classList.toggle('show')

    const fd = new FormData(form)
    // Converting form data to an object to pass via xhr
    obj = {};
    [...fd.entries()].forEach(entry => obj[entry[0]] = entry[1])

    function postAjax (url, data, callback) {
        const params = typeof data === 'string' ? data : Object.keys(data).map(
            function (k) { return encodeURIComponent(k) + '=' + encodeURIComponent(data[k]) }
        ).join('&')
        console.log(params)
        const xhr = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP')
        xhr.open('POST', url)
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 3 && xhr.status === 200) {
                console.log('Loading...')
            } else if (xhr.status >= 500 || xhr.status === 0) {
                // status code 0 is returned when you are signed out of CAS.
                // location.href = '/'
            } else if (xhr.readyState > 3 && xhr.status === 200) {
                callback(xhr)
            }
        }
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest')
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')
        xhr.send(params)
        return xhr
    }

    postAjax('/search', obj, function(xhr){
        form.reset()
        results.innerHTML = xhr.responseText

        // Set listener after results have ajaxed in
        const showDetails = document.querySelectorAll('.person')
        // const showDetails = document.querySelectorAll('.person__details__link')
        for (let index = 0; index < showDetails.length; index++) {
            showDetails[index].addEventListener('click', function () {
                // this.parentElement.parentElement.nextElementSibling.classList.toggle('show-details')
                this.classList.toggle('show-details')
                // this.innerHTML === '- Hide details' ? this.innerHTML = '+ Show details' : this.innerHTML = '- Hide details'
            })
        }

        const infiniteScroll = document.querySelector('#infiniteScroll')
        window.onscroll = function(ev) {
            const infiniteDataContainer = document.querySelector('#infiniteDataContainer')

            // you're at the bottom of the page
            if ((window.innerHeight + window.scrollY) >= infiniteScroll.offsetHeight
                    && parseInt(infiniteDataContainer.getAttribute('page')) < parseInt(infiniteDataContainer.getAttribute('max-page'))
                    && infiniteDataContainer.getAttribute('busy') === 'false') {

                // prevent other AJAX while this is running
                infiniteDataContainer.setAttribute('busy', 'true');

                // increase page number
                const new_page_number = parseInt(infiniteDataContainer.getAttribute('page')) + 1
                infiniteDataContainer.setAttribute('page', page_number)

                // get data and append page number to the data
                obj = infiniteDataContainer.getAttribute('data') + '&page=' + new_page_number;
                postAjax('/search', obj, function(xhr){
                    // append results to the other results
                    infiniteScroll.innerHTML = infiniteScroll.innerHTML + xhr.responseText;

                    // allow the
                    infiniteDataContainer.setAttribute('busy', 'false')
                })
            }
        };
    })
})
