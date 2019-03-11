// Advanced search show/hide
const basicSearchOptions = document.querySelector('.basicSearch--options')
const advancedSearchLink = document.querySelector('.advancedSearch--link')
const advancedSearchOptions = document.querySelector('.advancedSearch--options')

//set default
advancedSearchOptions.style.height = '0'
basicSearchOptions.style.height = basicSearchOptions.scrollHeight + 'px'

advancedSearchLink.addEventListener('click', function(){
    if (advancedSearchOptions.classList.contains('hide')){
        basicSearchOptions.classList.toggle('hide')
        advancedSearchOptions.classList.toggle('hide')
        basicSearchOptions.style.height = 0
        advancedSearchOptions.style.height = advancedSearchOptions.scrollHeight + 'px'
    } else {
        basicSearchOptions.classList.toggle('hide')
        advancedSearchOptions.classList.toggle('hide')
        basicSearchOptions.style.height = basicSearchOptions.scrollHeight + 'px'
        advancedSearchOptions.style.height = '0'
    }
})

// Profile menu show/hide
const profileDropdownLink = document.querySelector('#profileDropdown--link')
const profileDropdownMenu = document.querySelector('#profileDropdown--menu')

if (profileDropdownLink){
    profileDropdownLink.addEventListener('click', function(){
        profileDropdownMenu.classList.toggle('show')
    })
}