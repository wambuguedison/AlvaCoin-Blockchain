"use strict"
const results = document.querySelector("#results");
//mine
const mineurl = "http://localhost:5000/mine";
let mine = document.querySelector("#mine");

mine.addEventListener("click", ()=>{
    fetch(mineurl, {"mode": "no-cors"})
    .then((response) => response.json())
    .then((data) => {
        results.innerText = JSON.stringify(data);
        console.log(data)
    })
    .catch((err) => {
        console.log(err)
    })
})


//chain
const chainurl =  "http://localhost:5000/chain";
let chain = document.querySelector("#chain");

chain.addEventListener("click", () => {
    fetch(chainurl, {mode: "no-cors"})
    .then((response) => response.json())
    .then((data) => {
        results.innerText = JSON.stringify(data['chain'],null,4);
        console.log(data);
    })
    .catch((err)=>{
        console.log("Fetch Error :-S", err);
    })
})

//clear
let clear = document.querySelector("#clear");
clear.addEventListener("click", (event)=>{
    results.innerText = "";
})