const searchWrapper = document.querySelector(".searchbar-container");
const inputBox = searchWrapper.querySelector(".searchbar");
const autoCompleteBox = searchWrapper.querySelector(".autocomplete-box");

// Handler user input
inputBox.onkeyup = (e)=>{
    let userData = e.target.value;
    let emptyArray = [];

    if(userData) {
        emptyArray = completions.filter((data)=>{
            return data.toLocaleLowerCase().startsWith(userData.toLocaleLowerCase());
        })

        emptyArray = emptyArray.map((data)=>{
            return data = '<li>' + data + '</li>';
        })

        console.log(emptyArray);
        searchWrapper.classList.add("active");

        showCompletions(emptyArray);

        let allList = autoCompleteBox.querySelectorAll("li");

        for(let i = 0; i < allList.length; i++) {
            allList[i].setAttribute("onclick", "select(this)");
        }
    } else {
        searchWrapper.classList.remove("active");
    }
}

function select(element) {
    inputBox.value = element.textContent;

    searchWrapper.classList.remove("active");
}

function showCompletions(list) {
    let listData;

    if(list.length >= 5) {
        let maxLength = 5;
        let newArray = [];

        for(var i = 0; i < maxLength; i++) {
            newArray.push(list[i]);
        }

        listData = newArray.join('');
    } else {
        listData = list.join('');
    }

    autoCompleteBox.innerHTML = listData;
}