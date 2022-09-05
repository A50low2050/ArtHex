$(document).ready(function () {
  bsCustomFileInput.init()
	
  /*get file from input */
  $("#UploadInp").change(function () {
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imgUpload').attr('src', e.target.result);
            }
            reader.readAsDataURL(this.files[0]);
        }
    });
	
	/*get text from input*/
	$("#UploadInp").on('change', function(){
		var input_text = this.value.split('\\')
		
		var text = input_text[input_text.length - 1]
		$('#name_file').val(text)
	});

});


var selectedLink = location.href.replace(/http:\/\/[^\/]+\//i,'/');
$('a[href="' + selectedLink + '"]').addClass('active');


imgInp.onchange = evt => {
	const [file] = imgInp.files
	
	if(file){
		img_user.src = URL.createObjectURL(file)
	}
}


/*redirects the user to the image upload page*/
$('#download_picture').click(function(){   
    $('.form-download-picture').submit();

});


$('#save').click(function(){   
    $('#form-change-photo').submit();

});


