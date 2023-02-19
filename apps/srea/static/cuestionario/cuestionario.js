//console.log("Hola")
const url = window.location.href

const quizBox=document.getElementById('quiz-box')
let cont=1
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
                            <input type="radio" class="ans" id="${preguntas}-${respuesta}" name="${preguntas}" value="${preguntas}">
                            <label for="${preguntas}">${respuesta}</label>
                        </div>
                    `
                })         
            }
        });
    },
    error: function(error){
        console.log(error)
    }
})