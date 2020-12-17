const FormBox = document.getElementById('textile-formid')
const CollectionBox = document.getElementById('collection-data-box')
const ModelBox = document.getElementById('model-data-box')

const endpointCollection = document.getElementById('endpoint-collection')
const endpointModel = document.getElementById('endpoint-model')





$.ajax({
    type: 'GET',
    url: endpointCollection.textContent,
    success: function(response){
        console.log(response.data)
        const CollectionData = response.data
        CollectionData.map(item=>{
            const option = document.createElement('option')
            option.textContent = item.name
            option.setAttribute('value', item.id)
            CollectionBox.appendChild(option)
            const currentCollection = document.getElementById('current-collection').textContent
            $("#collection-data-box").val(currentCollection).change();
        })

        const testVal = $("#collection-data-box option:selected").val();
        console.log(testVal)
        GetModel(testVal)

    },
    error: function(error){
        console.log(error)
    },

})




CollectionBox.addEventListener('change', e=>{
    console.log(e.target.value)
    ModelBox.innerHTML = ""
    const ModelText = document.createElement('option')
    ModelText.textContent = "Показать все"
    ModelText.setAttribute('value', 'all')
    ModelBox.appendChild(ModelText)

    const SelectedCollection = e.target.value
//    var link = endpointModel.textContent
//    link = link.replace('ID', SelectedCollection)


    $.ajax({
        type: 'GET',
        url: endpointModel.textContent,
        data: {
            'collection': SelectedCollection,
        },
        success: function(response){
            console.log(response.data)
            const ModelData = response.data
            ModelData.map(item=>{
                const option = document.createElement('option')
                option.textContent = item.model
                option.setAttribute('value', item.model)
                ModelBox.appendChild(option)
            })

        },
        error: function(error){
            console.log(error)
        },

    })

})


function GetModel(id) {
    ModelBox.innerHTML = ""
    const ModelText = document.createElement('option')
    ModelText.textContent = "Показать все"
    ModelText.setAttribute('value', 'all')
    ModelBox.appendChild(ModelText)

    const SelectedCollection = id
//    var link = endpointModel.textContent
//    link = link.replace('ID', SelectedCollection)


    $.ajax({
        type: 'GET',
        url: endpointModel.textContent,
        data: {
            'collection': SelectedCollection,
        },
        success: function(response){
            console.log(response.data)
            const ModelData = response.data
            ModelData.map(item=>{
                const option = document.createElement('option')
                option.textContent = item.model
                option.setAttribute('value', item.model)
                ModelBox.appendChild(option)
            })
            const currentCollection = document.getElementById('current-model').textContent
            $("#model-data-box").val(currentCollection).change();

        },
        error: function(error){
            console.log(error)
        },

    })
}
