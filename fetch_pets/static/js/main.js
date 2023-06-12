const alert = document.getElementById("alert")

if(alert){
    setTimeout(function(){
        alert.style.display = 'none'
    }, 3000)
}