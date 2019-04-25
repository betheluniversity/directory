const results = document.querySelector('#results')
const loader = results.querySelector('.loader')
const introText = results.querySelector('.introText')

const form = document.querySelector('.directory-form')
form.addEventListener('submit', e => {
    e.preventDefault()
    introText.classList.toggle('hide')
    loader.classList.toggle('hide-loader')

    const fd = new FormData(form)
    // Converting form data to an object to pass via xhr
    let obj = {};
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
                form.reset()
            }
        }
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest')
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')
        xhr.send(params)
        return xhr
    }

    postAjax('/search', obj, function (xhr) {
        results.innerHTML = xhr.responseText

        // Set listener after results have ajaxed in
        const showDetails = document.querySelectorAll('.person__details__link')
        for (let index = 0; index < showDetails.length; index++) {
            showDetails[index].addEventListener('click', function () {
                this.parentElement.parentElement.nextElementSibling.classList.toggle('hide')
                this.innerHTML === '- Hide details' ? this.innerHTML = '+ Show details' : this.innerHTML = '- Hide details'
            })
        }

        const infiniteScroll = document.querySelector('#infiniteScroll')
        const iDC = document.querySelector('#infiniteDataContainer')

        window.onscroll = function (ev) {
            // you're at the bottom of the page
            if ((window.innerHeight + window.scrollY) >= infiniteScroll.offsetHeight &&
                    parseInt(iDC.getAttribute('page')) < parseInt(iDC.getAttribute('max-page')) &&
                    iDC.getAttribute('busy') === 'false') {
                // set to busy
                iDC.setAttribute('busy', 'true')

                // increase page number
                let pageNumber = parseInt(iDC.getAttribute('page')) + 1
                iDC.setAttribute('page', pageNumber)

                // get new page number
                let newPageNumber = iDC.getAttribute('page')

                // get data and add on page number
                obj = iDC.getAttribute('data') + '&page=' + newPageNumber
                postAjax('/search', obj, function (xhr) {
                    // append results
                    infiniteScroll.innerHTML = infiniteScroll.innerHTML + xhr.responseText
                    iDC.setAttribute('busy', 'false')
                })
            }
        }
    })
})
