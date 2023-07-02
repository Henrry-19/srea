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
        timerBox.innerHTML = `<b>${time}</b>`
        
    }
    
    var convertir = time.toString();
    var ceros = convertir.substring(1, convertir.length - 2)
    var puntos = ceros.split(":").join('');
    let convertir_numero
    if (puntos === "100"){
        nuevos_ceros=(puntos-40)
        convertir_numero=Number(nuevos_ceros)
        
    }else{
        if(puntos === "200"){
            nuevos_ceros=(puntos-80)
            convertir_numero=Number(nuevos_ceros)
        }else{
         convertir_numero=Number(puntos)
        }
    } 

    let minutes = (convertir_numero) - 1
    
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
            displayMinutes ='0' + minutes
           
        } else{
            displayMinutes = minutes
            
        }

        if(seconds.toString().length < 2) {
            displaySeconds = '0' + seconds
        }else{
            displaySeconds = seconds
        }

        if (minutes === 0 && seconds === 0){
            timerBox.innerHTML = `<b> 00:00:00 </b>`
            setTimeout(()=>{
                clearInterval(timer)
                alert('Se acabó el tiempo')
                let formulario = document.getElementById('quiz-form');
                formulario.submit();
            }, 500)
            
        }

        timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds} min</b>`

    }, 1000)

}

$.ajax({
    type:'GET',
    url: `${url}/data`,
    success:function(response){
        activateTimer(response.time)
    },
    error: function(error){
        console.log(error)
    }
})




quizForm.addEventListener('submit', e =>{
    e.preventDefault()
    sendData()
})

