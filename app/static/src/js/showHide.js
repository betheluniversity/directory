// Advance search show/hide
const advancedSearchLink = document.querySelector('#advancedSearch--link')
const advancedSearchOptions = document.querySelector('#advancedSearch--options')
advancedSearchLink.addEventListener('click', function(){
    advancedSearchOptions.classList.toggle('show')
})

// Profile menu show/hide
const profileDropdownLink = document.querySelector('#profileDropdown--link')
const profileDropdownMenu = document.querySelector('#profileDropdown--menu')

if (profileDropdownLink){
    profileDropdownLink.addEventListener('click', function(){
        profileDropdownMenu.classList.toggle('show')
    })
}