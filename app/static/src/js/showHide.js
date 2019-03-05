// Advanced search show/hide
const advancedSearchLink = document.querySelector('.advancedSearch--link')
const advancedSearchOptions = document.querySelector('.advancedSearch--options')

advancedSearchLink.addEventListener('click', function(){
    if (advancedSearchOptions.classList.contains('hide')){
        advancedSearchOptions.classList.toggle('hide')
        advancedSearchOptions.style.height = advancedSearchOptions.scrollHeight + 'px'

    } else {
        advancedSearchOptions.style.height = '0'
        advancedSearchOptions.classList.toggle('hide')
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