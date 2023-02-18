//console.log("Hola")
const url = window.location.href

const quizBox=document.getElementById('quiz-box')

$.ajax({
    type:'GET',
    url: `${url}data`,
    success:function(response){
        const data = response.data
        data.forEach(el => {
            for (const [preguntas, respuestas]of Object.entries(el)){
                quizBox.innerHTML += `
                    <hr>
                    <di class="mb-2">
                        <b>${preguntas}</b>
                    </di>
                `
                respuestas.forEach(respuesta=>{
                    quizBox.innerHTML +=`
                        <di class="mb-2">
                        <br>
                            <input type="radio" class="ans" id="${preguntas}-${respuesta}" name="${preguntas}" value="${preguntas}">
                            <label for="${preguntas}">${respuesta}</label>
                        </di>
                    `
                })         
            }
        });
    },
    error: function(error){
        console.log(error)
    }
})