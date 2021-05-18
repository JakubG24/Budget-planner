(function(){

    document.querySelector('#categoryInput').addEventListener('keydown', function(e){
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

        document.querySelector('#categoriesContainer').insertAdjacentHTML('beforeend',
            `<li class="category">
                    <span class="name">${name}</span>
                    <a href="#" class="btn-outline-dark"><b>X</b></a>
                   </li>`)
    }
})()