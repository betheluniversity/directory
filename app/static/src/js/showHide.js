const accordionItems = document.querySelectorAll('.accordionItem')
const accordionContentPanes = document.querySelectorAll('.accordionContent')
const form = document.querySelector('.directory-form')

// First open by default, setting closed to have an explicit height for animation to work
const firstItem = accordionItems[0].querySelector('.accordionContent')
accordionItems[0].classList.add('active')
firstItem.style.height = firstItem.scrollHeight + 'px'
accordionItems[1].querySelector('.accordionContent').style.height = '0px'
accordionItems[2].querySelector('.accordionContent').style.height = '0px'

// add listener to each title
accordionItems.forEach(function (accordion) {
    let accordionTitle = accordion.firstElementChild
    accordionTitle.addEventListener('click', toggleAccordion)
})

function toggleAccordion (e) {
    form.reset()
    accordionItems.forEach(a => {
        if (this.parentElement === a) {
            a.classList.add('active')
        } else {
            a.classList.remove('active')
        }
    })

    accordionContentPanes.forEach(a => {
        if (a.previousElementSibling === this) {
            // For the department search, require the department to be selected
            if( a.classList.contains('departmentRequired') )
                document.getElementById('department').required = true;
            else
                document.getElementById('department').required = false;

            a.classList.remove('hide-accordion')
            a.style.height = a.scrollHeight + 'px'
        } else {
            a.classList.add('hide-accordion')
            a.style.height = '0px'
        }
    })
}

// Profile menu show/hide
const profileDropdownLink = document.querySelector('#profileDropdown--link')
const profileDropdownMenu = document.querySelector('#profileDropdown--menu')

if (profileDropdownLink) {
    profileDropdownLink.addEventListener('click', function () {
        profileDropdownMenu.classList.toggle('show')
    })
}
