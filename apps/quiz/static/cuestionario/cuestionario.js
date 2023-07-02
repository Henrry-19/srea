//console.log("Hola")
const url = window.location.href

const quizBox=document.getElementById('quiz-box')
let cont=1
//const scoreBox = document.getElementById('score-box')
const resultBox = document.getElementById('score-box')

const timerBox = document.getElementById('timer-box')

const activateTimer = (time) =>{
    if (time.toString().length < 2){
        timerBox.innerHTML = `<b>0${time}:00</b>`
    }else{
        timerBox.innerHTML = `<b>${time}:00</b>`
    }

    let minutes = time - 1
    let seconds = 60
    let displaySeconds 
    let displayMinutes 

    const timer = setInterval(()=>{
        seconds --
        if(seconds < 0) {
            seconds = 59
            minutes -- 
        }

        if(minutes.toString().length < 2) {
            displayMinutes = '0' + minutes
        } else{
            displayMinutes = minutes
        }

        if(seconds.toString().length < 2) {
            displaySeconds = '0' + seconds
        }else{
            displaySeconds = seconds
        }

        if (minutes === 0 && seconds === 0){
            timerBox.innerHTML = `<b>00:00</b>`
            setTimeout(()=>{
                clearInterval(timer)
                alert('Se acabó el tiempo')
                sendData()
            }, 500)
            
        }

        timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`

    }, 1000)

}

$.ajax({
    type:'GET',
    url: `${url}data`,
    success:function(response){
        const data = response.data

        data.forEach((el, id) => {
            for (const [preguntas, respuestas]of Object.entries(el)){
                quizBox.innerHTML += `
                    <hr>
                    <di class="mb-2">
                        <font face="nunito,arial,verdana"><b><b>${id+1 +"."}</b></font>
                        <font face="nunito,arial,verdana"><b>${preguntas}</b></font>      
                    </di>
                `
                respuestas.forEach(respuesta=>{
                    quizBox.innerHTML +=`
                        <div class="mb-2">
                        <br>
                            <input type="radio" class="ans" id="${preguntas}-${respuesta}" name="${preguntas}" value="${respuesta}">
                            <label for="${preguntas}">${respuesta}</label>
                        </div>
                    `
                })         
            }
        });
        activateTimer(response.time)
    },
    error: function(error){
        console.log(error)
    }
})

const quizForm = document.getElementById('quiz-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

const sendData = () =>{ //Función de envío de datos
    const elements = [...document.getElementsByClassName('ans')]
    const data = {} //Constante data, contiene un diccionario vacío
    data['csrfmiddlewaretoken'] = csrf[0].value//En esta constante, voy a poner al token para poder escribir datos
    elements.forEach(el =>{
        if (el.checked) {//Si el elemento marcado está bien  
            data[el.name] = el.value// Como claves tendremos el nombre del elemento (pregunta) y lo estableceremos en el valor del elemento (respuesta)
        } else {
            if(!data[el.name]) {//Si no tenemos ninguna clave que sea el nombre del elemento(pregunta)
                data[el.name] = null //Indicar que la pregunta no ha sido respondida
            }
        }
    })

    $.ajax({
        type: 'POST',
        url:  `${url}save/`, //URL en donde enviaremos nuestros datos
        data: data,
        success: function (response) {
            //console.log(response)
            const resultados=response.resultado
            //console.log(resultados)
            quizForm.classList.add('not-visible')

            scoreBox.innerHTML += `${response.passed ? 'Felicidades ': ' Ups...'} su resultado es: ${response.puntaje} %`

            resultados.forEach(res=>{
                const resDiv = document.createElement("table")
                for(const [pregunta, resp]of Object.entries(res)){
                    resDiv.innerHTML += pregunta
                    const cls =  ['container', 'p-3', 'text-light', 'h6']
                    resDiv.classList.add(...cls)

                    if (resp=='No contestada'){
                        resDiv.innerHTML += '- Sin responder'
                        resDiv.classList.add('bg-danger')
                    }else{
                        const answer = resp['contestada']
                        const correct = resp['respuesta_correcta']

                        if (answer==correct){
                            resDiv.classList.add('bg-success')
                            resDiv.innerHTML += `- Contestada: ${answer}`
                        }else{
                            resDiv.classList.add('bg-danger')
                            resDiv.innerHTML += `| respuesta correcta: ${correct}`
                            resDiv.innerHTML += `| contestada: ${answer}`
                        }
                    }
                }
                resultBox.append(resDiv) //Presentando el resultado
            })
        },
        error:function (error) {
            console.log(error)
        }
    })

}

quizForm.addEventListener('submit', e =>{
    e.preventDefault()
    sendData()
})