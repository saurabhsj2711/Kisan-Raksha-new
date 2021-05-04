$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#symptoms').text('');
        $('#solution').text('');
        $('#result').hide();
        $('#symptoms').hide();
        $('#solution').hide();
        readURL(this);
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#symptoms').fadeIn(600);
                $('#solution').fadeIn(600);
//                $('#result').innerHTML('  <div id="result" class="textBox"> ' + data);
                var al_sym = "Alternaria Leaf Spot forms lesions on senescing leaves that are brown  purple margins. As lesions expand they typically exhibit concentric zonation and the necrotic tissue will overlap other lesions. As the disease progresses the lesions will become gray and dry with some of the necrotic tissue falling out giving it a “shot-holed” appearance.";
                var al_sol = "Plow crop residue into the soil to reduce inoculum levels; provide plants with adequate irrigation and nutrients, particularly potassium; applications of appropriate foliar fungicides may be required on susceptible cultivars.";

                var bac_sym = "Symptoms of Bacte-rial Blight start as tiny water-soaked spots, and progress into characteristi-cally angular shapes due to leaf veins limiting bacterial movement. Lesions appear on the upper side of the leaf, turn black as they expand, and defoli-ation may occur. Systemic infections follow the main veins as black streaks; symptoms on the bolls are characteristically sunken, water-soaked lesions.";
                var bac_sol = "The use of resistant cotton varieties is the most effective method of controlling the disease; cultural practices such as plowing crop residue into soil after harvest can also limit disease emergence.";

                var gr_sym = "Leaves become yellow, turn to brown colour. Severe intensity of grey mildew disease leads to leaf curling and eventually the defoliation of green leaves and both surfaces of the leaves get uniformly covered by white powdery growth of the fungus.";
                var gr_sol = "Dusting of 8-10 kg of Sulphur powder effectively controls the disease.Also about one gram of Carbendazim or Benomyl per litre of water is effective.If the disease intensity is more, new fungicides like one litre Hexaconazole or 300 gm Nativo-75 WG per hectare is required to control the grey mildew disease.";

                var ch_sym = "Discoloration of leaf for plant due to deficiendy of ingredients ";
                var ch_sol = "Improve the soil quality so that plant can get required ingredients from soil";

                symptoms={"Bacterial blight":bac_sym,"Alternaria":al_sym,"Grey Mildew":gr_sym,"Chlorosis":ch_sym};
                $('#symptoms').text('symptoms:' +symptoms['Bacterial blight']);
                solution={"Bacterial blight":bac_sol,"Alternaria":al_sol,"Grey Mildew":gr_sol,"Chlorosis":ch_sol};
                $('#solution').text('solution:' +solution['Bacterial blight']);
                causes={"Bacterial blight":"Xanthomonas citri pv. malvacearum","Alternaria":"A. macrospora, A. alternata","Grey Mildew":"Mycospaerella areola","Chlorosis":"ALkaline soil causes deficeincy"};
                $('#solution').text('solution:' +solution['Bacterial blight']);


                document.getElementById('demo').innerHTML= '<p><strong>Name :</strong>'+data+'</p>'+
                '<p><strong>Foliar Symptoms : </strong>'+symptoms[data]+'</p>'+
                '<p><strong>Caused by : </strong>'+causes[data]+'</p>'+
                '<p><strong>Diagnostic Note :</strong>'+solution[data]+'</p>'
                ;

                console.log('Success!');
            },
        });
    });

});
