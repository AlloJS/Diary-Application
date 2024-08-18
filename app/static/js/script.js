var typeEvent = document.getElementById('type-event')
var nameEvent = document.getElementById('name')
var description = document.getElementById('description')
var date_start = document.getElementById('date_start')
var date_and = document.getElementById('date_and')
var hour_start = document.getElementById('hour_start')
var minute_start = document.getElementById('minute_start')
var hour_and = document.getElementById('hour_and')
var minute_and = document.getElementById('minute_and')
var btnAddEvent = document.getElementById('btn-addEvent')
var montToMonth = document.getElementById('choose-month')
var yearToMonth = document.getElementById('year')
var divPeriod = document.getElementById('div-period')
var divMonth = document.getElementById('div-month')
setInputDisabled();

function setInputDisabled(){
    if(typeEvent.value == 1 || typeEvent.value == 2){
        date_and.readonly = true;
        if(typeEvent.value == 2){
            divMonth.style.display = '';
            divPeriod.style.display = 'none';
        } else if(typeEvent.value == 1 || typeEvent.value == 3) {
            divMonth.style.display = 'none';
            divPeriod.style.display = '';
        }
    } else {
        date_and.readonly = false;
    }
}

function setTipe(type){
    setInputDisabled()
    if(date_start.value != '') setData(date_start);
}

function setData(dataStart){
    if(typeEvent.value == 1){
        date_and.value = dataStart.value;
    }
    if (typeEvent.value == 2) {

        if (dataStart) {
            let date = new Date(dataStart.value);

            if (!isNaN(date.getTime())) {

                date.setMonth(date.getMonth() + 1);

                if (!isNaN(date.getTime())) {
                    let updatedDate = date.toISOString().split('T')[0];
                    date_and.value = updatedDate;
                } else {
                    console.error("Errore nel calcolo della nuova data.");
                }
            } else {
                console.error("Data non valida:", dataStart);
            }
        } else {
            console.error("dataStart è indefinito o vuoto.");
        }
    }

}

btnAddEvent.addEventListener('click',(e)=>{

    if(nameEvent.value == ''){ nameEvent.style.border = "thick solid red";return;} else {nameEvent.style.border = "1px solid black"; }

    if(description.value == '') {description.style.border = "thick solid red";return;} else {description.style.border = "1px solid black"; }

    if(typeEvent.value != 2){

        if(date_start.value == '') {date_start.style.border = "thick solid red";return;} else {date_start.style.border = "1px solid black"; }

        if(date_and.value == '') {date_and.style.border = "thick solid red";return;} else {date_and.style.border = "1px solid black"; }

        if(hour_start.value == '') {hour_start.style.border = "thick solid red";return;} else {hour_start.style.border = "1px solid black"; }

        if(minute_start.value == '') {minute_start.style.border = "thick solid red";return;} else {minute_start.style.border = "1px solid black"; }

        if(hour_and.value == '') {hour_and.style.border = "thick solid red";return;} else {hour_and.style.border = "1px solid black"; }

        if(minute_and.value == '') {minute_and.style.border = "thick solid red";return;} else {minute_and.style.border = "1px solid black"; }

        if((hour_and.value == hour_start.value) && (parseInt(minute_and.value) <  parseInt(minute_start.value))) {minute_and.style.border = "thick solid red";return;} else {minute_and.style.border = "1px solid black"; }
     } else {
         if(montToMonth.value == '') {montToMonth.style.border = "thick solid red";return;} else {montToMonth.style.border = "1px solid black"; }

         if(yearToMonth.value == '') {yearToMonth.style.border = "thick solid red";return;} else {yearToMonth.style.border = "1px solid black"; }
     }



    document.formAdd.submit();
})