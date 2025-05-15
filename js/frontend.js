const socket = io()

socket.on('hello', (img) => {
    const image = new Blob([img], { type: 'image/png' });
    const imageUrl = URL.createObjectURL(image);

    /*
    document.querySelector('#imgs')
      .innerHTML += `<img height="300px" width="200px" src="${imageUrl}">`
    */
    document.querySelector('#photoResult').setAttribute("src", imageUrl);
})

document.querySelector('#imgForm').addEventListener('submit', (event) => {
    event.preventDefault()
    var img = document.querySelector('#fileInput').files[0]
    const reader = new FileReader();
    reader.onloadend = function() {
        const image = new Blob([img], { type: 'image/png' });
        const imageUrl = URL.createObjectURL(image);
        document.querySelector('#photoLoad').setAttribute("src", imageUrl);

        socket.emit("image", reader.result);

        document.querySelector('#downloadButton').setAttribute("href", imageUrl);
    }
    reader.readAsArrayBuffer(img);
}) 