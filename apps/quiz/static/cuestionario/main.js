const modalBtns = [...document.getElementsByClassName('modal-button')]
const modalBody = document.getElementById('modal-body-confirm')
const startBtn = document.getElementById('start-button')
const url = window.location.href
modalBtns.forEach(modalBtn => modalBtn.addEventListener('click', ()=>{
    const pk = modalBtn.getAttribute('data-pk')
    const nombre = modalBtn.getAttribute('data-cuestionario')
    const pregunta = modalBtn.getAttribute('data-pregunta')
    const tiempo = modalBtn.getAttribute('data-tiempo')
    
    modalBody.innerHTML = `
        <div class="h5 mb-3">
        ¿Está seguro de iniciar "<b>${nombre}</b>"?
        </div>
        <div class="text-muted">
            <ul>
                <li>Título: <b>${nombre}</b></li>
                <li>Número de preguntas: <b>${pregunta}</b></li>
                <li>Tiempo: <b>${tiempo} minutos</b></li>
                
            </ul>
        </div>
    `
    startBtn.addEventListener('click', ()=>{
      window.location.href=url + pk
    })
    

}))