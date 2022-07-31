const toggleModal = () => {
    document.querySelector('.modal-container').classList.toggle('modal-container-hidden')
};

var my_divs = document.querySelectorAll('.modal-div')

function update_div(fname,lname) {
    console.log(fname,lname)
    container = document.querySelector(".modal-container") 
    document.getElementById('intro').innerHTML = "Hello, this is " + fname + "!"
    container.classList.toggle('modal-container-hidden')
}

// my_divs.forEach(function(my_div) {
//     my_div.addEventListener('click', function() {
//         console.log(this)
//     })
// })

document.querySelector('.close-bar svg').addEventListener('click',toggleModal)

function focusSbox() {
    document.querySelector(".form-input").focus();
}

document.querySelector('.srch-icon').addEventListener('click',focusSbox)
