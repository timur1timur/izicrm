const FormBox = document.getElementById('textile-formid')
const CollectionBox = document.getElementById('collection-data-box')
const ModelBox = document.getElementById('model-data-box')
const MarkupBox = document.getElementById('markup-data-box')

const endpointCollection = document.getElementById('endpoint-collection')
const endpointModel = document.getElementById('endpoint-model')
const endpointMarkup = document.getElementById('endpoint-markup')
const endpointSetMarkup = document.getElementById('endpoint-set-markup')



$.ajax({
    type: 'GET',
    url: endpointMarkup.textContent,
    success: function(response){
        console.log(response.data)
        const MarkupData = response.data
        MarkupData.map(item=>{
            const option = document.createElement('option')
            option.textContent = item.source_t
            option.setAttribute('value', item.source_t)
            MarkupBox.appendChild(option)
            const currentMarkup = document.getElementById('current-customer').textContent
            $("#markup-data-box").val(currentMarkup).change();
        })
    },
    error: function(error){
        console.log(error)
    },

})

MarkupBox.addEventListener('change', e=>{
    console.log(e.target.value)
    const SelectedMarkup = e.target.value

    $.ajax({
        type: 'GET',
        url: endpointSetMarkup.textContent,
        data: {
            'customer': SelectedMarkup,
        },
        success: function(response){
            console.log(response)

        },
        error: function(error){
            console.log(error)
        },

    })
    document.location.reload()
})

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

//FormBox.addEventListener('submit', e=>{
//    e.preventDefault();
//    var employeeTable = $('#foo-filtering tbody');
//    employeeTable.empty();
//    console.log(CollectionBox.value, ModelBox.value)
//        $.ajax({
//        type: 'GET',
//        url: 'get-json/',
//        data: {
//            'collection': CollectionBox.value,
//            'model': ModelBox.value
//        },
//        success: function(response){
//            console.log(response.data)
//
//            $.each(response.data,function(i,item){
//                var icon = '<i data-feather="edit-3" class="wd-16 mr-2"></i>'
//                var lin = "'edit/"+item.id+"/'"
//                var link = "<a href="+lin+">"+icon+"</a>"
//                $("#foo-filtering tbody").append(
//                    "<tr>"
//                        +"<td>"+item.article+"</td>"
//                        +"<td>"+item.manufacturer_id+"</td>"
//                        +"<td>"+item.collection_id+"</td>"
//                        +"<td>"+item.model+"</td>"
//                        +"<td>"+item.color+"</td>"
//                        +"<td>"+item.height+"</td>"
//                        +"<td>"+item.price_opt+"</td>"
//                        +"<td>"+link+"</td>"
//                    +"</tr>" )
//                })
//
//        },
//        error: function(error){
//            console.log(error)
//        },
//
//    })
//
//})

//$("#textile-formid").submit(function(e) {
//    e.preventDefault();
//    console.log('Submitted');
//})