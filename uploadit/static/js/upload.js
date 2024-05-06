Dropzone.options.dropper = {
    paramName: "file",
    chunking: true,
    forceChunking: true,
    autoProcessQueue: false,
    url: "/upload",
    maxFilesize: 2000, // megabytes
    chunkSize: 1000000, // bytes
    init: function() {
        const uploadButton = document.getElementById('submit-all');
        let myDropzone = this;

        uploadButton.addEventListener("click", function() {
            myDropzone.processQueue();
        });

        myDropzone.on('sending', function(file, xhr, formData){
            let is_public = document.getElementById('is_public')

            if (is_public.checked) {
                formData.append('is_public', true)
            } else {
                formData.append('is_public', false)
            }
        });
    }
}

