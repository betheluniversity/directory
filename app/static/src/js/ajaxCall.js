const form = document.querySelector('.directory-form')
const results = document.querySelector('#results')
const introText = results.querySelector('.introText')
const loader = document.querySelector('.loader')

form.addEventListener('submit', e => {
    e.preventDefault()
    introText.classList.toggle('hide')
    // show load animation
    loader.classList.remove('hide-loader')

    let obj = serialize(form)

    postAjax('/search', obj, function (xhr) {
        results.innerHTML = xhr.responseText

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


                if (pageNumber === parseInt(iDC.getAttribute('max-page'))) {
                    loader.classList.add('hide-loader')
                }

                // get data and add on page number
                obj = iDC.getAttribute('data') + '&page=' + newPageNumber
                postAjax('/search', obj, function (xhr) {
                    // append results
                    infiniteScroll.innerHTML += xhr.responseText
                    iDC.setAttribute('busy', 'false')
                })
            }
        }
    })
})

function postAjax (url, data, callback) {
    const params = typeof data === 'string' ? data : Object.keys(data).map(
        function (k) { return encodeURIComponent(k) + '=' + encodeURIComponent(data[k]) }
    ).join('&')
    // console.log(params)
    const xhr = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP')
    xhr.open('POST', url)
    xhr.onreadystatechange = function () {
        console.log(xhr.readyState + ' ' + xhr.status)
        if( xhr.status === 0) {
            location.href = '/'
        } else if (xhr.readyState === 3 && xhr.status === 200) {
            console.log('Loading...')
        } else if (xhr.readyState > 3 && xhr.status === 200) {
            callback(xhr)
            form.reset()
            detailsLink()
        }
    }
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest')
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')
    xhr.send(params)
    return xhr
}

function detailsLink () {
    // Set listener after results have ajaxed in
    const showDetails = document.querySelectorAll('.person__details__link')
    for (let index = 0; index < showDetails.length; index++) {
        showDetails[index].addEventListener('click', function () {
            let next = this.parentElement.parentElement.nextElementSibling
            next.classList.toggle('hide')
            this.innerHTML === '- Hide details' ? this.innerHTML = '+ Show details' : this.innerHTML = '- Hide details'
            let homeLink = next.querySelector('.person__home__link')
            if (homeLink) {
                homeLink.addEventListener('click', function () {
                    this.nextElementSibling.classList.toggle('hide')
                })
            }
        })
    }
}

/*!
 * Serialize all form data into a query string
 * (c) 2018 Chris Ferdinandi, MIT License, https://gomakethings.com
 * @param  {Node}   form The form to serialize
 * @return {String}      The serialized form data
 * url:  https://vanillajstoolkit.com/helpers/serialize/
 */
function serialize (form) {
    // Setup our serialized data
    const serialized = []

    // Loop through each field in the form
    for (let i = 0; i < form.elements.length; i++) {
        const field = form.elements[i]

        // Don't serialize fields without a name, submits, buttons, file and reset inputs, and disabled fields
        if (!field.name || field.disabled || field.type === 'file' || field.type === 'reset' || field.type === 'submit' || field.type === 'button') continue

        // If a multi-select, get all selections
        if (field.type === 'select-multiple') {
            for (let n = 0; n < field.options.length; n++) {
                if (!field.options[n].selected) continue
                serialized.push(encodeURIComponent(field.name) + '=' + encodeURIComponent(field.options[n].value))
            }
        }

        // Convert field data to a query string
        else if ((field.type !== 'checkbox' && field.type !== 'radio') || field.checked) {
            serialized.push(encodeURIComponent(field.name) + '=' + encodeURIComponent(field.value))
        }
    }

    return serialized.join('&')
}
