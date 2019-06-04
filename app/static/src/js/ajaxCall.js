import { Collapse } from 'bootstrap.native'

const form = document.querySelector('.directory-form')
const results = document.querySelector('#results')
const introText = results.querySelector('.introText')
const loader = document.querySelector('.loader')

form.addEventListener('submit', e => {
    e.preventDefault()
    introText.classList.toggle('hide')
    loader.classList.remove('hide-loader')
    results.innerHTML = ''

    let obj = serialize(form)

    postAjax('/search', obj, function (xhr) {
        results.innerHTML = xhr.responseText

        const infiniteScroll = document.querySelector('#infiniteScroll')
        const iDC = document.querySelector('#infiniteDataContainer')
        const maxPage = parseInt(iDC.getAttribute('max-page'))

        // hide loader if only 1 page
        if (maxPage === 0 || maxPage === 1 || isNaN(maxPage)) {
            loader.classList.add('hide-loader')
        }

        window.onscroll = function (ev) {
            // you're at the bottom of the page
            if ((window.innerHeight + window.pageYOffset) >= infiniteScroll.offsetHeight &&
                    parseInt(iDC.getAttribute('page')) < maxPage &&
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
                    infiniteScroll.innerHTML += xhr.responseText
                    iDC.setAttribute('busy', 'false')

                    // hide loader at end of search results
                    if (parseInt(newPageNumber) === maxPage) {
                        loader.classList.add('hide-loader')
                    }
                })
            }
        }
    })
})

function postAjax (url, data, callback) {
    const params = typeof data === 'string' ? data : Object.keys(data).map(
        function (k) { return encodeURIComponent(k) + '=' + encodeURIComponent(data[k]) }
    ).join('&')
    const xhr = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject('Microsoft.XMLHTTP')
    xhr.open('POST', url)
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 3 && xhr.status === 200) {
            console.log('Loading...')
        } else if (xhr.readyState > 3 && xhr.status === 200) {
            callback(xhr)
            detailsLink()
        } else if (xhr.readyState > 3 && xhr.status === 0) {
            // if the user is logged out, we send them back to the homepage
            location.href = '/'
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
        let collapseLink = showDetails[index]
        let collapseDiv = showDetails[index].parentElement.parentElement.nextElementSibling
        // Generate random 6 digit number to make the collapse HREF and ID unique
        let randomNum = 'id' + Math.floor(100000 + Math.random() * 900000)
        collapseLink.setAttribute('data-target', '#' + randomNum)
        collapseDiv.setAttribute('id', randomNum)

        // Initialize new collapse elements due to ajaxing
        let collapse = new Collapse(collapseLink)
        let collapseInit = collapse.Collapse

        showDetails[index].addEventListener('click', function () {
            this.classList.toggle('active')

            let homeDetailsLink = collapseDiv.querySelector('.person__home__link')
            if (homeDetailsLink) {
                let homeDetailsDiv = homeDetailsLink.nextElementSibling
                // Generate random 6 digit number to make the collapse HREF and ID unique
                let randomNum2 = 'id' + Math.floor(100000 + Math.random() * 900000)
                homeDetailsLink.setAttribute('data-target', '#' + randomNum2)
                homeDetailsDiv.setAttribute('id', randomNum2)

                // Initialize new collapse elements due to ajaxing
                let collapseHome = new Collapse(homeDetailsLink)
                let collapseHomeInit = collapseHome.Collapse

                homeDetailsLink.addEventListener('click', function () {
                    this.classList.toggle('active')
                })
            }
            let idLink = collapseDiv.querySelector('.person__id__link')
            if (idLink) {
                let idDiv = idLink.nextElementSibling
                // Generate random 6 digit number to make the collapse HREF and ID unique
                let randomNum3 = 'id' + Math.floor(100000 + Math.random() * 900000)
                idLink.setAttribute('data-target', '#' + randomNum3)
                idDiv.setAttribute('id', randomNum3)

                // Initialize new collapse elements due to ajaxing
                let collapseID = new Collapse(idLink)
                let collapseIDInit = collapseID.Collapse

                idLink.addEventListener('click', function () {
                    this.classList.toggle('active')
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
