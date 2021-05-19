(function(){

    document.querySelector('#fixedInput').addEventListener('keydown', function(e){
        if(e.keyCode != 13){
            return;
        }

        e.preventDefault()

        let categoryName = this.value
        this.value = ''
        addNewCategory(categoryName)
        updateCategoriesString()
    })

    function addNewCategory(name){

        document.querySelector('#fixedContainer').insertAdjacentHTML('beforeend',
            `<li class="fixed">
                    <span class="name">${name}</span>
                    <span onclick="removeCategory(this)" class="btn-outline-dark"><b>X</b></span>
                   </li>`)
    }

})()

function fetchCategoryArray(){
        const categories = []

        document.querySelectorAll('.fixed').forEach(function(e){
            name = e.querySelector('.name').innerHTML
            if (name == '') return;

            categories.push(name)
        })

        return categories;
    }

    function updateCategoriesString(){
        categories = fetchCategoryArray()
        document.querySelector('input[name="fixedString"]').value = categories.join(',')
    }

function removeCategory(e){
    e.parentElement.remove()
    updateCategoriesString()

    }