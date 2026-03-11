function searchCourier(){

let input=document.getElementById("searchInput").value.toUpperCase();
let table=document.querySelector("table");
let rows=table.getElementsByTagName("tr");

for(let i=1;i<rows.length;i++){

let td=rows[i].getElementsByTagName("td")[0];

if(td){

let txt=td.textContent||td.innerText;

if(txt.toUpperCase().indexOf(input)>-1){
rows[i].style.display="";
}else{
rows[i].style.display="none";
}

}

}
}