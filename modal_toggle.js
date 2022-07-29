const toggleModal = () => {
    document.querySelector('.modal-container').classList.toggle('modal-container-hidden')
};

document.querySelector('#show-modal').addEventListener('click',toggleModal)

document.querySelector('.close-bar svg').addEventListener('click',toggleModal)


const yeahcool = document.querySelector('#show-modal')
yeahcool.addEventListener('click', (event) => {
    console.log(event.originalTarget);
    // img src (to upload)= event.originalTarget.src
    // post src = (obtained from DB)
    // 
});